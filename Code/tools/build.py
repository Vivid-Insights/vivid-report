"""Build a report's Markdown into a Vivid Insights web paper.

    cd Code && uv run python tools/build.py                       # Report.md -> build/<slug>/
    cd Code && uv run python tools/build.py "../Sample Report/Specimen.md"
    cd Code && uv run python tools/build.py --open                # build, then open in the browser

The output folder is self-contained (`index.html`, `assets/`, `media/`) so it can be copied
anywhere, embedded in an iframe (`index.html?embed`), or published to the Vivid Insights site by
`tools/publish.py`. The Markdown is the source of truth: never edit the built page.

The syntax beyond ordinary Markdown is documented in `FORMAT.md`. In short:

    ::: figure {#fig-id src="Code/outputs/figures/x.png" alt="..." width=wide}   caption   :::
    ::: video {#fig-id src="Code/outputs/videos/x.mp4" poster="..." loop}         caption   :::
    ::: interactive {#fig-id src="Code/interactives/x/index.html" height=520 fallback="..."}  :::
    ::: table {#tab-id}   caption line, then a Markdown table                                 :::
    ::: output {source="Code/outputs/cache.json" key="0.text" model="..."}  exact text       :::
    ::: prompt {source="Code/prompts/system.md"}                            exact text       :::
    ::: conversation {source="hand-written" assistant="Ask Afya"}   Speaker: text lines       :::
    ::: definition {#def-id title="Wordalisation"}   text                                     :::
    $$ ... $$ {#eq-id}          numbered display equation
    @fig-id  @tab-id  @eq-id  @sec-id  @def-id      cross-references
    [@key]  [@a; @b, p. 4]  @key                    citations from references.yaml
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from urllib.parse import quote

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.footnote import footnote_plugin

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, SITE, ReportError, load_report, load_yaml, paper_dir, rel, resolve_report, site_config, slug_of  # noqa: E402

XREF_KINDS = {"fig": "Figure", "tab": "Table", "eq": "Equation", "sec": "Section", "def": "Definition"}
UNNUMBERED = {"abstract", "disclaimer", "references", "acknowledgements", "acknowledgments", "appendix",
              "notes", "data and code availability", "author contributions", "funding", "what we have built"}
MEDIA_KINDS = {"figure", "video", "interactive"}
PREVIEW_RE = re.compile(r"[ \t]*!\[\[([^\]\n]+)\]\][ \t]*(?:\n|$)")
QUOTE_KINDS = {"output", "prompt", "conversation"}
ALL_KINDS = MEDIA_KINDS | QUOTE_KINDS | {"table", "definition", "box", "panel"}

FENCE_RE = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1\s*$", re.S | re.M)
# A block opens with three or more colons and closes with the same number, so blocks nest the way they
# do in Pandoc and Quarto: the outer block uses more colons than the blocks inside it.
BLOCK_RE = re.compile(r"^(?P<fence>:{3,})[ \t]*(?P<kind>\w+)[ \t]*(?P<attrs>\{[^\n]*\})?[ \t]*\n(?P<body>.*?)\n(?P=fence)[ \t]*$", re.S | re.M)
EQ_RE = re.compile(r"^\$\$[ \t]*\n?(?P<tex>.+?)\n?[ \t]*\$\$[ \t]*(?P<attrs>\{\s*(?:#(?P<id>eq-[\w-]+))?\s*(?P<unnum>-)?\s*\})?[ \t]*$", re.S | re.M)
BARE_XREF_RE = re.compile(r"(?<![\w@])-@((?:fig|tab|eq|sec|def)-[\w-]*\w)")
ATTR_RE = re.compile(r'#([\w-]+)|\.([\w-]+)|([\w-]+)=("([^"]*)"|\'([^\']*)\'|[^\s}]+)|([\w-]+)')
SECTION_SPLIT_RE = re.compile(r"^## (.+)$", re.M)
HEADING_RE = re.compile(r"<h([23])>(.*?)</h\1>", re.S)
TAG_SPLIT_RE = re.compile(r"(<[^>]+>)")
BRACKET_CITE_RE = re.compile(r"\[((?:-?@[\w:.-]+[^\];]*)(?:;\s*-?@[\w:.-]+[^\];]*)*)\]")
NARRATIVE_RE = re.compile(r"(?<![\w@/.:&=-])@([A-Za-z][\w:-]*[\w])")
PENDING_RE = re.compile(r"\[(TO WRITE|CHECK|PLACEHOLDER)(:[^\]]*)?\]")
TEMPLATE_NOTE_RE = re.compile(r"^\*Steps? \d", re.M)


@dataclass
class Issue:
    level: str          # "error" stops a release build; "warning" is listed; "style" is a writing-rule hint
    message: str
    where: str = ""

    def __str__(self):
        w = f" ({self.where})" if self.where else ""
        return f"[{self.level}] {self.message}{w}"


@dataclass
class Result:
    html: str
    out_dir: Path
    issues: list[Issue]
    assets: list[Path]
    meta: dict
    cited: list[str] = field(default_factory=list)

    @property
    def errors(self):
        return [i for i in self.issues if i.level == "error"]


def parse_attrs(s: str | None) -> dict:
    out: dict = {"classes": []}
    if not s:
        return out
    for m in ATTR_RE.finditer(s.strip("{} ")):
        if m.group(1):
            out["id"] = m.group(1)
        elif m.group(2):
            out["classes"].append(m.group(2))
        elif m.group(3):
            v = m.group(5) if m.group(5) is not None else m.group(6) if m.group(6) is not None else m.group(4)
            out[m.group(3)] = v
        elif m.group(7):
            out[m.group(7)] = True
    return out


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", re.sub(r"<[^>]+>", "", s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def png_display_px(p: Path) -> int | None:
    """Width to show a PNG at so that its 11 pt text matches the 19.5 px body text.

    Uses the image's own pixel width and the resolution matplotlib records in it. A 10 cm figure comes
    out about 500 px wide, a 16 cm one fills the column. Returns None if the file says nothing.
    """
    try:
        b = p.read_bytes()[:4096]
        if b[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        width = int.from_bytes(b[16:20], "big")
        i = b.find(b"pHYs")
        if i < 0 or b[i + 12] != 1:
            return None
        dpi = int.from_bytes(b[i + 4:i + 8], "big") * 0.0254
        return round(width / dpi * 72 * 19.5 / 11) if dpi else None
    except (OSError, IndexError):
        return None


def latex_plain(tex: str) -> str:
    """The words of a LaTeX source, for checking a quotation against it: comments, line breaks,
    ties and font commands removed; the characters of the text left as they are."""
    tex = "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in tex.splitlines())
    tex = tex.replace("\\\\", " ").replace("~", " ")
    tex = re.sub(r"\{\\(it|bf|em|tt|sc)\s+([^{}]*)\}", r"\2", tex)
    tex = re.sub(r"\\(textit|textbf|emph|texttt|textsc|textrm)\{([^{}]*)\}", r"\2", tex)
    for a, b in (("\\%", "%"), ("\\&", "&"), ("\\_", "_"), ("\\$", "$"), ("\\#", "#")):
        tex = tex.replace(a, b)
    return tex


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()


def esc(s) -> str:
    return html.escape(str(s), quote=True)


# --------------------------------------------------------------------------- references

def initials(given: str) -> str:
    parts = re.split(r"(\s+|-)", given.strip())
    out = ""
    for p in parts:
        if not p or p.isspace():
            out += " " if out and not out.endswith(" ") else ""
        elif p == "-":
            out = out.rstrip() + "-"
        else:
            out += p if p.endswith(".") and len(p) <= 3 else p[0] + "."
    return out.strip()


def split_name(a) -> tuple[str, str]:
    if isinstance(a, dict):
        return a.get("family") or a.get("literal", ""), a.get("given", "")
    a = str(a)
    if "," in a:
        fam, giv = a.split(",", 1)
        return fam.strip(), giv.strip()
    return a.strip(), ""  # a corporate author, e.g. "World Health Organization"


class Bibliography:
    REQUIRED = ("id", "title", "year")

    def __init__(self, entries: list[dict], issues: list[Issue], src: str):
        self.entries = {}
        self.issues = issues
        for e in entries or []:
            key = e.get("id")
            missing = [f for f in self.REQUIRED if not e.get(f)]
            if not (e.get("author") or e.get("editor")):
                missing.append("author")
            if missing:
                issues.append(Issue("error", f"reference '{key}' is missing {', '.join(missing)}", src))
            if not (e.get("doi") or e.get("url")):
                issues.append(Issue("error", f"reference '{key}' has neither a doi nor a url: every reference is a link", src))
            if key in self.entries:
                issues.append(Issue("error", f"reference id '{key}' is used twice", src))
            self.entries[key] = e
        self.order: list[str] = []      # keys in order of first citation
        self.suffix: dict[str, str] = {}

    def authors(self, e):
        return [split_name(a) for a in (e.get("author") or e.get("editor") or [])]

    def short(self, key) -> str:
        fams = [f for f, _ in self.authors(self.entries[key])]
        if len(fams) > 1 and fams[-1].lower() == "others":
            return f"{fams[0]} et al."
        if len(fams) == 1:
            return fams[0]
        if len(fams) == 2:
            return f"{fams[0]} and {fams[1]}"
        return f"{fams[0]} et al."

    def year(self, key) -> str:
        return f"{self.entries[key]['year']}{self.suffix.get(key, '')}"

    def assign_suffixes(self, cited: list[str]):
        groups: dict[tuple, list[str]] = {}
        for k in cited:
            if k in self.entries:
                groups.setdefault((self.short(k), str(self.entries[k]["year"])), []).append(k)
        for keys in groups.values():
            if len(keys) > 1:
                for i, k in enumerate(keys):
                    self.suffix[k] = "abcdefghijklmnopqrstuvwxyz"[i]

    def link(self, e) -> str:
        if e.get("doi"):
            d = str(e["doi"])
            return d if d.startswith("http") else f"https://doi.org/{d}"
        return e.get("url", "")

    def format_entry(self, key) -> str:
        e = self.entries[key]
        names, etal = [], False
        for fam, giv in self.authors(e):
            if fam.lower() == "others" and not giv:
                etal = True
                continue
            names.append(f"{fam}, {initials(giv)}" if giv else fam)
        if etal:
            auth = ", ".join(names) + ", et al."
        elif len(names) > 1:
            auth = ", ".join(names[:-1]) + ", &amp; " + names[-1] if len(names) > 2 else f"{names[0]} &amp; {names[1]}"
        else:
            auth = names[0] if names else ""
        if e.get("editor") and not e.get("author"):
            auth += " (Ed.)" if len(names) == 1 else " (Eds.)"
        title = esc(str(e["title"]).rstrip("."))
        url = self.link(e)
        t = e.get("type", "article")
        parts = [f'{esc(auth) if "&amp;" not in auth else auth} ({esc(self.year(key))}).',
                 f'<a href="{esc(url)}">{title}</a>.']
        cont = e.get("container") or e.get("journal") or ""
        if t in ("book", "report", "software", "dataset", "web"):
            bits = []
            if e.get("version"):
                bits.append(f"Version {esc(e['version'])}")
            if e.get("number"):
                bits.append(esc(e["number"]))
            if e.get("publisher") or cont:
                bits.append(esc(e.get("publisher") or cont))
            if bits:
                parts.append(", ".join(bits) + ".")
        else:
            c = f"<i>{esc(cont)}</i>" if cont else ""
            if e.get("volume"):
                c += f", <i>{esc(e['volume'])}</i>"
                if e.get("issue"):
                    c += f"({esc(e['issue'])})"
            if e.get("pages"):
                c += f", {esc(e['pages'])}"
            if e.get("number") and t == "preprint":
                c += f":{esc(e['number'])}"
            if c:
                parts.append(c + ".")
        if e.get("doi"):
            parts.append(f'<a class="vr-doi" href="{esc(url)}">{esc(url)}</a>')
        if e.get("note"):
            parts.append(f'<span class="vr-refnote">{esc(e["note"])}</span>')
        return " ".join(parts)

    def sort_key(self, key):
        a = self.authors(self.entries[key])
        return (unicodedata.normalize("NFKD", a[0][0] if a else "").lower(), str(self.year(key)))

    def html(self, cited: list[str]) -> str:
        keys = sorted({k for k in cited if k in self.entries}, key=self.sort_key)
        items = "\n".join(f'<li id="ref-{esc(k)}">{self.format_entry(k)}</li>' for k in keys)
        return f'<ol class="vr-references">\n{items}\n</ol>'


# --------------------------------------------------------------------------- builder

class Builder:
    def __init__(self, report: Path, out_dir: Path | None = None, release: bool = False, status: dict | None = None):
        self.report = report
        self.release = release
        self.status = status or {"state": "draft"}
        self.issues: list[Issue] = []
        self.assets: dict[Path, str] = {}       # source file -> published path
        self.asset_dirs: dict[Path, str] = {}   # interactive folders -> published path
        self.labels: dict[str, tuple[str, str]] = {}   # id -> (kind word, number)
        self.counters = {"fig": 0, "tab": 0, "eq": 0, "def": 0}
        self.placeholders: dict[str, str] = {}
        self.cited: list[str] = []
        self.referenced_ids: set[str] = set()
        self.meta, self.body = load_report(report)
        self.base = paper_dir(self.meta, report)
        self.slug = slug_of(self.meta, report)
        self.out_dir = out_dir or (ROOT / "build" / self.slug)
        self.md = (MarkdownIt("commonmark", {"html": True, "typographer": True})
                   .enable(["table", "strikethrough", "replacements", "smartquotes"])
                   .use(footnote_plugin)
                   .use(dollarmath_plugin, allow_space=False, allow_digits=False, double_inline=False))
        ref_file = self.base / self.meta.get("references", "references.yaml")
        self.bib = Bibliography(load_yaml(ref_file, []) or [], self.issues, rel(ref_file))
        self.has_math = False

    # ---- helpers
    def issue(self, level, msg, where=""):
        self.issues.append(Issue(level, msg, where))

    def placeholder(self, html_: str) -> str:
        key = f"VRBLOCK{len(self.placeholders):04d}X"
        self.placeholders[key] = html_
        return f"\n\n{key}\n\n"

    def asset(self, src: str, where: str) -> str | None:
        p = (self.base / src).resolve()
        if not p.exists():
            self.issue("error", f"file not found: {src}", where)
            return None
        if p not in self.assets:
            r = p.relative_to(self.base) if p.is_relative_to(self.base) else Path(p.name)
            self.assets[p] = "media/" + "/".join(slugify(part.rsplit(".", 1)[0]) + ("." + part.rsplit(".", 1)[1].lower() if "." in part else "")
                                                for part in r.parts)
        return quote(self.assets[p])

    def asset_dir(self, d: Path) -> str:
        if d not in self.asset_dirs:
            self.asset_dirs[d] = "media/interactives/" + slugify(d.name)
        return self.asset_dirs[d]

    def register(self, ident: str | None, prefix: str, where: str) -> str | None:
        """Number a labelled element. Figures count in order of appearance whatever their medium."""
        self.counters[prefix] += 1
        n = str(self.counters[prefix])
        if ident:
            if not ident.startswith(prefix + "-"):
                self.issue("error", f"id '{ident}' should start with '{prefix}-'", where)
            if ident in self.labels:
                self.issue("error", f"id '{ident}' is used twice", where)
            self.labels[ident] = (XREF_KINDS[prefix], n)
        return n

    def render_md(self, text: str) -> str:
        """Render Markdown that may contain blocks of its own (a panel's body, a box)."""
        h = self.md.render(self.preprocess(text))
        for k, v in self.placeholders.items():
            h = h.replace(f"<p>{k}</p>", v)
        return h

    def register_sub(self, ident: str | None, label: str, where: str) -> None:
        if ident:
            if ident in self.labels:
                self.issue("error", f"id '{ident}' is used twice", where)
            self.labels[ident] = ("Figure", label)

    def caption_html(self, text: str) -> str:
        text = text.strip()
        if not text:
            return ""
        return self.md.renderInline(text) if "\n\n" not in text else self.md.render(text)

    # ---- blocks
    def strip_preview(self, kind: str, attrs: dict, content: str, where: str) -> str:
        """An Obsidian embed, `![[papers/NNNN-slug/path]]`, on the first line of a figure, video,
        interactive or panel block shows the image in Obsidian. The page draws the block itself, so
        the line is dropped here, after checking it still points at the block's file."""
        m = PREVIEW_RE.match(content)
        if not m:
            return content
        target = attrs.get("fallback") if kind == "interactive" else attrs.get("src")
        if target:
            want = (self.base / target).resolve()
            got = (ROOT / m.group(1).split("|")[0]).resolve()
            if got != want:
                self.issue("warning", f"the Obsidian preview {m.group(0).strip()} does not show this block's file "
                                      f"({target}); run tools/obsidian.py to refresh it", where)
        return content[m.end():]

    def render_block(self, kind: str, attrs: dict, content: str, where: str) -> str:
        ident = attrs.get("id")
        cls = " ".join(attrs["classes"])
        width = attrs.get("width", "text")
        if kind not in ALL_KINDS:
            self.issue("error", f"unknown block '::: {kind}'. Known: {', '.join(sorted(ALL_KINDS))}", where)
            return f"<pre>{esc(content)}</pre>"

        if kind == "panel":
            self.issue("error", "a panel block belongs inside a figure block, whose fence has more colons", where)
            return ""

        if kind in MEDIA_KINDS:
            content = self.strip_preview(kind, attrs, content, where)

        if kind == "figure" and re.search(r"^:{3,}[ \t]*panel\b", content, re.M):
            return self.render_panels(attrs, content, where)

        if kind == "box":
            return self.render_box(attrs, content, where)

        if kind in MEDIA_KINDS:
            n = self.register(ident, "fig", where)
            cap = self.caption_html(content)
            if not cap:
                self.issue("warning", f"{kind} {ident or n} has no caption", where)
            media = getattr(self, f"media_{kind}")(attrs, where)
            idattr = f' id="{esc(ident)}"' if ident else ""
            return (f'<figure class="vr-figure vr-{kind} vr-w-{esc(width)} {cls}"{idattr}>{media}'
                    f'<figcaption><span class="vr-label">Figure {n}.</span> {cap}</figcaption></figure>')

        if kind == "table":
            n = self.register(ident, "tab", where)
            lines = content.strip().splitlines()
            cap = " ".join(line for line in lines if not line.lstrip().startswith("|")).strip()
            table = "\n".join(line for line in lines if line.lstrip().startswith("|"))
            if not table:
                self.issue("error", "table block holds no Markdown table", where)
            idattr = f' id="{esc(ident)}"' if ident else ""
            return (f'<figure class="vr-table vr-w-{esc(width)} {cls}"{idattr}><figcaption><span class="vr-label">Table {n}.</span> '
                    f'{self.md.renderInline(cap)}</figcaption><div class="vr-table-scroll">{self.md.render(table)}</div></figure>')

        if kind == "definition":
            n = self.register(ident, "def", where)
            title = f" ({self.md.renderInline(attrs['title'])})" if attrs.get("title") else ""
            idattr = f' id="{esc(ident)}"' if ident else ""
            return (f'<div class="vr-definition {cls}"{idattr}><span class="vr-def-label">Definition {n}{title}.</span> '
                    f'{self.md.render(content.strip())}</div>')

        return self.render_quote(kind, attrs, content, where)

    def render_panels(self, attrs, content, where):
        """A figure made of panels (a), (b), …, like LaTeX's subfigure. Text outside the panels is the
        figure's caption. A panel with src= shows that image and its text is its caption; a panel without
        src= is Markdown, and its last paragraph is its caption."""
        ident = attrs.get("id")
        n = self.register(ident, "fig", where)
        panels, caption, last = [], [], 0
        for m in BLOCK_RE.finditer(content):
            caption.append(content[last:m.start()])
            last = m.end()
            if m.group("kind") != "panel":
                caption.append(m.group(0))
                continue
            pa = parse_attrs(m.group("attrs"))
            panels.append((pa, self.strip_preview("panel", pa, m.group("body"), where)))
        caption.append(content[last:])
        cap = self.caption_html("".join(caption))
        cells = []
        for i, (pa, body) in enumerate(panels):
            letter = "abcdefghijklmnopqrstuvwxyz"[i]
            self.register_sub(pa.get("id"), f"{n}{letter}", where)
            if pa.get("src"):
                media, pcap = self.media_figure(pa, where), self.caption_html(body)
            else:
                chunks = [c for c in re.split(r"\n\s*\n", body.strip()) if c.strip()]
                pcap = self.caption_html(chunks[-1]) if chunks else ""
                media = f'<div class="vr-panel-body">{self.render_md(chr(10).join(chr(10) + c + chr(10) for c in chunks[:-1]))}</div>'
            pid = f' id="{esc(pa["id"])}"' if pa.get("id") else ""
            cells.append(f'<div class="vr-panel"{pid}>{media}<div class="vr-subcaption"><span class="vr-sublabel">({letter})</span> {pcap}</div></div>')
        cols = esc(attrs.get("cols", "1"))
        idattr = f' id="{esc(ident)}"' if ident else ""
        width = esc(attrs.get("width", "text"))
        return (f'<figure class="vr-figure vr-w-{width} {" ".join(attrs["classes"])}"{idattr}><div class="vr-panels vr-cols-{cols}">{"".join(cells)}</div>'
                f'<figcaption><span class="vr-label">Figure {n}.</span> {cap}</figcaption></figure>')

    def render_box(self, a, content, where):
        """A framed box of Markdown, like LaTeX's tcolorbox, with an optional bold label at its start.
        With source= the text is checked against that file, as for quoted outputs."""
        text = content.strip("\n")
        if a.get("source") and a["source"] != "hand-written":
            plain = re.sub(r"\\\n", "\n", text)                       # Markdown hard line breaks
            plain = re.sub(r"(\*\*|__|(?<!\w)[*_](?=\S)|(?<=\S)[*_](?!\w))", "", plain)
            if "|" not in plain:
                self.verify_quote(a["source"], a.get("key"), [plain], where)
        body = self.render_md(text)
        if a.get("label"):
            label = f'<strong class="vr-box-label">{self.md.renderInline(a["label"])}</strong> '
            body = re.sub(r"^<p>", "<p>" + label, body, count=1) if body.startswith("<p>") else f"<p>{label}</p>{body}"
        return f'<div class="vr-box {" ".join(a["classes"])}">{body}</div>'

    def media_figure(self, a, where):
        src = a.get("src")
        if not src:
            self.issue("error", "figure needs src=", where)
            return ""
        light = self.asset(src, where)
        dark_src = a.get("dark")
        if not dark_src:
            p = Path(src)
            cand = p.parent / "dark" / p.name
            if (self.base / cand).exists():
                dark_src = str(cand)
        alt = esc(a.get("alt", ""))
        px = png_display_px(self.base / src) if str(src).lower().endswith(".png") and "fill" not in a else None
        size = f' style="max-width:{px}px"' if px else ""
        if not a.get("alt"):
            self.issue("warning", f"figure {src} has no alt text", where)
        if dark_src:
            dark = self.asset(dark_src, where)
            return (f'<div class="vr-media"><img class="vr-only-light" src="{light}" alt="{alt}"{size} loading="lazy">'
                    f'<img class="vr-only-dark" src="{dark}" alt="{alt}"{size} loading="lazy"></div>')
        return f'<div class="vr-media"><img src="{light}" alt="{alt}"{size} loading="lazy"></div>'

    def media_video(self, a, where):
        title = esc(a.get("title", a.get("alt", "Video")))
        if a.get("youtube"):
            return (f'<div class="vr-media vr-embed"><iframe src="https://www.youtube-nocookie.com/embed/{esc(a["youtube"])}" '
                    f'title="{title}" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div>'
                    f'<p class="vr-print-only">Video: https://youtu.be/{esc(a["youtube"])}</p>')
        if a.get("vimeo"):
            return (f'<div class="vr-media vr-embed"><iframe src="https://player.vimeo.com/video/{esc(a["vimeo"])}" '
                    f'title="{title}" loading="lazy" allowfullscreen></iframe></div>')
        src = a.get("src")
        if not src:
            self.issue("error", "video needs src=, youtube= or vimeo=", where)
            return ""
        if not a.get("poster"):
            self.issue("warning", f"video {src} has no poster image (shown before playing and when printed)", where)
        mode = ' autoplay muted loop playsinline' if a.get("loop") else ' controls playsinline'

        def one(vsrc, psrc, cls=""):
            v = self.asset(vsrc, where)
            poster = f' poster="{self.asset(psrc, where)}"' if psrc else ""
            ext = vsrc.rsplit(".", 1)[-1].lower()
            c = f' class="{cls}"' if cls else ""
            return (f'<video{c} preload="metadata"{mode}{poster} aria-label="{title}">'
                    f'<source src="{v}" type="video/{"webm" if ext == "webm" else "mp4"}"></video>')

        dark_v, dark_p = a.get("dark"), None
        if not dark_v and (self.base / Path(src).parent / "dark" / Path(src).name).exists():
            dark_v = str(Path(src).parent / "dark" / Path(src).name)
        if dark_v and a.get("poster"):
            cand = Path(a["poster"]).parent / "dark" / Path(a["poster"]).name
            dark_p = str(cand) if (self.base / cand).exists() else a["poster"]
        if dark_v:
            return (f'<div class="vr-media">{one(src, a.get("poster"), "vr-only-light")}'
                    f'{one(dark_v, dark_p, "vr-only-dark")}</div>')
        return f'<div class="vr-media">{one(src, a.get("poster"))}</div>'

    def media_interactive(self, a, where):
        src = a.get("src")
        if not src:
            self.issue("error", "interactive needs src=", where)
            return ""
        p = (self.base / src).resolve()
        if not p.exists():
            self.issue("error", f"file not found: {src}", where)
            return ""
        d = self.asset_dir(p.parent)
        url = quote(f"{d}/{p.name}")
        h = int(str(a.get("height", 480)))
        title = esc(a.get("title", "Interactive figure"))
        fb = ""
        if a.get("fallback"):
            fb = f'<img class="vr-print-only" src="{self.asset(a["fallback"], where)}" alt="{title}">'
        else:
            self.issue("warning", f"interactive {src} has no fallback= image for print and for readers without JavaScript", where)
        return (f'<div class="vr-media vr-interactive-frame"><iframe src="{url}" title="{title}" loading="lazy" '
                f'style="height:{h}px" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>'
                f'<a class="vr-open-full" href="{url}" target="_blank" rel="noopener">Open full screen ↗</a></div>{fb}')

    def render_quote(self, kind, a, content, where):
        source = a.get("source")
        word = {"output": "LLM output", "prompt": "Prompt", "conversation": "Conversation"}[kind]
        if not source:
            self.issue("error", f"{kind} block needs source= (a file it is quoted from, or source=\"hand-written\")", where)
            source = "unknown"
        hand = source == "hand-written"
        text = content.strip("\n")
        turns = []
        if kind == "conversation":
            for line in text.splitlines():
                m = re.match(r"^([^:\n]{1,40}):\s+(.*)$", line)
                if m:
                    turns.append([m.group(1).strip(), m.group(2)])
                elif turns and line.strip():
                    turns[-1][1] += " " + line.strip()
                elif turns:
                    turns[-1][1] += "\n\n"
            if not turns:
                self.issue("error", "conversation block has no 'Speaker: text' lines", where)
        if not hand and source != "unknown":
            self.verify_quote(source, a.get("key"), [t[1] for t in turns] if turns else [text], where)
        bits = [word if not hand else f"{word} · hand-written example"]
        if a.get("model"):
            bits.append(esc(a["model"]))
        label = f'<div class="vr-quote-head"><span>{bits[0]}</span><span>{" · ".join(bits[1:])}</span></div>'
        if kind == "conversation":
            bot = a.get("assistant", "assistant").lower()
            rows = []
            for who, said in turns:
                side = "bot" if who.lower() in (bot, "assistant") else "user"
                paras = "".join(f"<p>{esc(p.strip())}</p>" for p in said.split("\n\n") if p.strip())
                rows.append(f'<div class="vr-turn vr-{side}"><span class="vr-who">{esc(who)}</span><div class="vr-said">{paras}</div></div>')
            body = f'<div class="vr-quote-body vr-chat">{"".join(rows)}</div>'
        else:
            paras = "".join(f"<p>{esc(p.strip())}</p>" for p in re.split(r"\n\s*\n", text) if p.strip())
            body = f'<div class="vr-quote-body">{paras}</div>'
        src_line = "" if hand else f'<div class="vr-quote-source">Quoted word for word from <code>{esc(source)}</code>{(" · " + esc(a["key"])) if a.get("key") else ""}</div>'
        cap = ""
        ident = a.get("id")
        if ident:
            n = self.register(ident, "fig", where)
            cap = f'<figcaption><span class="vr-label">Figure {n}.</span> {self.md.renderInline(a.get("caption", ""))}</figcaption>'
        idattr = f' id="{esc(ident)}"' if ident else ""
        return f'<figure class="vr-quote vr-{kind}"{idattr}>{label}{body}{src_line}{cap}</figure>'

    def verify_quote(self, source, key, texts, where):
        """The rule is that generated text is quoted, never written. Check it against the file."""
        p = (self.base / source)
        if not p.exists():
            self.issue("error", f"quoted source not found: {source}", where)
            return
        raw = p.read_text(encoding="utf-8", errors="replace")
        if p.suffix == ".tex":
            raw = latex_plain(raw)
        target = None
        if key is not None:
            try:
                obj = json.loads(raw)
                for part in str(key).split("."):
                    obj = obj[int(part)] if isinstance(obj, list) else obj[part]
                target = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
            except Exception as e:  # noqa: BLE001
                self.issue("error", f"could not read key '{key}' from {source}: {e}", where)
                return
        hay = norm_ws(target if target is not None else raw)
        for t in texts:
            t = norm_ws(t)
            ok = (t == hay) if (target is not None and len(texts) == 1) else (t in hay)
            if not ok:
                self.issue("error", f"quoted text is not word for word what {source}{(' at ' + key) if key else ''} says: "
                                    f"'{t[:70]}…'", where)

    # ---- passes
    def preprocess(self, body: str) -> str:
        fences: dict[str, str] = {}

        def keep_fence(m):
            k = f"VRFENCE{len(fences):04d}X"
            fences[k] = m.group(0)
            return k

        body = FENCE_RE.sub(keep_fence, body)

        def line_of(pos):
            return f"line {body.count(chr(10), 0, pos) + 1 + self.front_lines}"

        # Blocks and equations are numbered in one pass in order of position, so numbering follows the page.
        events = [(m.start(), "block", m) for m in BLOCK_RE.finditer(body)] + \
                 [(m.start(), "eq", m) for m in EQ_RE.finditer(body)]
        events.sort(key=lambda e: e[0])
        out, last = [], 0
        for pos, typ, m in events:
            if pos < last:
                continue
            out.append(body[last:pos])
            where = line_of(pos)
            if typ == "block":
                inner = m.group("body")
                for k, v in fences.items():
                    inner = inner.replace(k, v)
                out.append(self.placeholder(self.render_block(m.group("kind"), parse_attrs(m.group("attrs")), inner, where)))
            else:
                self.has_math = True
                ident = m.group("id")
                idattr = f' id="{esc(ident)}"' if ident else ""
                if m.group("unnum"):
                    eqno = ""
                else:
                    eqno = f'<span class="vr-eqno">({self.register(ident, "eq", where)})</span>'
                out.append(self.placeholder(f'<div class="vr-eq"{idattr}><span class="vr-tex">{esc(m.group("tex").strip())}</span>{eqno}</div>'))
            last = m.end()
        out.append(body[last:])
        body = "".join(out)
        for k, v in fences.items():
            body = body.replace(k, v)
        return body

    def number_sections(self, html_: str, toc: list) -> str:
        h2 = h3 = 0
        current_unnumbered = False
        current_h2 = ""

        def sub(m):
            nonlocal h2, h3, current_unnumbered, current_h2
            level, inner = int(m.group(1)), m.group(2)
            ident = None
            mm = re.search(r"\s*\{(#[\w-]+)?\s*(-|\.unnumbered)?\s*\}\s*$", inner)
            unnumbered = False
            if mm:
                ident = mm.group(1)[1:] if mm.group(1) else None
                unnumbered = bool(mm.group(2))
                inner = inner[:mm.start()]
            plain = re.sub(r"<[^>]+>", "", inner).strip()
            if level == 2:
                current_h2 = slugify(plain)
                unnumbered = unnumbered or plain.lower() in UNNUMBERED
                current_unnumbered = unnumbered
                if not unnumbered:
                    h2 += 1
                    h3 = 0
                num = "" if unnumbered else str(h2)
            else:
                unnumbered = unnumbered or current_unnumbered
                if not unnumbered:
                    h3 += 1
                num = "" if unnumbered else f"{h2}.{h3}"
            if not ident:
                # Methods, Results and Discussion share their sub-headings, so a repeated
                # sub-heading takes its section's name rather than clashing.
                ident = f"sec-{slugify(plain)}"
                if level > 2 and ident in self.labels:
                    ident = f"sec-{current_h2}-{slugify(plain)}"
            if ident in self.labels:
                self.issue("error", f"section id '{ident}' is used twice")
            self.labels[ident] = ("Section", num or plain)
            toc.append((level, num, inner.strip(), ident))
            numhtml = f'<span class="vr-secnum">{num}</span>' if num else ""
            return f'<h{level} id="{esc(ident)}">{numhtml}{inner.strip()}</h{level}>'

        return HEADING_RE.sub(sub, html_)

    def wrap_sections(self, html_: str) -> tuple[str, bool]:
        parts = re.split(r"(?=<h2 )", html_)
        out, has_refs = [], False
        for part in parts:
            m = re.match(r'<h2 id="([^"]+)">(?:<span class="vr-secnum">[^<]*</span>)?(.*?)</h2>', part, re.S)
            if not m:
                out.append(part)
                continue
            name = re.sub(r"<[^>]+>", "", m.group(2)).strip().lower()
            cls = {"disclaimer": "vr-disclaimer", "references": "vr-refs-section"}.get(name, "")
            if name == "references":
                has_refs = True
                if re.sub(r"<[^>]+>|\s", "", part[m.end():]) and "vr-pending" not in part[m.end():]:
                    self.issue("error", "text under '## References' would be lost: the list is generated from the "
                                        "references file, so nothing else goes in that section")
                part = part[:m.end()] + "\n<!--VR-REFERENCES-->\n"
            out.append(f'<section class="vr-section {cls}" aria-labelledby="{m.group(1)}">{part}</section>')
        return "".join(out), has_refs

    def resolve_refs(self, html_: str) -> str:
        """Cross-references and citations, applied to text only — never inside tags, code or scripts."""
        segs = TAG_SPLIT_RE.split(html_)
        skip = 0
        for i, s in enumerate(segs):
            if s.startswith("<"):
                t = s.lower()
                if re.match(r"<(code|pre|script|style|a)\b", t):
                    skip += 1
                elif re.match(r"</(code|pre|script|style|a)>", t):
                    skip = max(0, skip - 1)
                continue
            if skip or "@" not in s:
                continue
            s = BRACKET_CITE_RE.sub(self._bracket, s)
            s = BARE_XREF_RE.sub(lambda mm: self._xref(mm.group(1), bare=True), s)
            s = NARRATIVE_RE.sub(self._narrative, s)
            segs[i] = s
        return "".join(segs)

    def _xref(self, ident, bare=False):
        self.referenced_ids.add(ident)
        if ident not in self.labels:
            self.issue("error", f"cross-reference @{ident} points at nothing")
            return f'<span class="vr-broken">&#64;{esc(ident)}</span>'
        word, num = self.labels[ident]
        text = num if bare else f"({num})" if word == "Equation" else f"{word} {num}"
        return f'<a class="vr-xref" href="#{esc(ident)}">{text}</a>'

    def _cite_one(self, key):
        if key not in self.bib.entries:
            self.issue("error", f"citation @{key} is not in the references file")
            return None
        if key not in self.cited:
            self.cited.append(key)
        return key

    def _bracket(self, m):
        items = [x.strip() for x in m.group(1).split(";")]
        if all(re.match(r"-?@(fig|tab|eq|sec|def)-", x) for x in items):
            return ", ".join(self._xref(x.lstrip("-@").split(",")[0].strip(), bare=x.startswith("-")) for x in items)
        rendered = []
        for it in items:
            mm = re.match(r"(-?)@([\w:.-]*[\w])(.*)$", it)
            if not mm:
                return m.group(0)
            key = self._cite_one(mm.group(2))
            if key is None:
                rendered.append(f'<span class="vr-broken">&#64;{esc(mm.group(2))}</span>')
                continue
            loc = mm.group(3).strip().lstrip(",").strip()
            who = "" if mm.group(1) else f"{esc(self.bib.short(key))}, "
            rendered.append(f'<a class="vr-cite" href="#ref-{esc(key)}" data-key="{esc(key)}">{who}{{YEAR:{key}}}{(", " + loc) if loc else ""}</a>')
        return "(" + "; ".join(rendered) + ")"

    def _narrative(self, m):
        ident = m.group(1)
        if re.match(r"(fig|tab|eq|sec|def)-", ident):
            return self._xref(ident)
        if ident not in self.bib.entries:
            self.issue("warning", f"'@{ident}' is neither a cross-reference nor a reference; left as text")
            return m.group(0)
        self._cite_one(ident)
        return f'<a class="vr-cite" href="#ref-{esc(ident)}" data-key="{esc(ident)}">{esc(self.bib.short(ident))} ({{YEAR:{ident}}})</a>'

    # ---- top level
    def build(self) -> Result:
        text = self.report.read_text(encoding="utf-8")
        self.front_lines = text[: len(text) - len(self.body)].count("\n")
        body = self.body

        # Abstract is lifted into the title block; everything else is the body.
        abstract_md = ""
        secs = list(SECTION_SPLIT_RE.finditer(body))
        for i, s in enumerate(secs):
            if s.group(1).strip().lower().startswith("abstract"):
                end = secs[i + 1].start() if i + 1 < len(secs) else len(body)
                abstract_md = body[s.end():end].strip()
                body = body[:s.start()] + body[end:]
                break

        body = self.preprocess(body)
        body_html = self.md.render(body)
        for k, v in self.placeholders.items():
            body_html = body_html.replace(f"<p>{k}</p>", v)
        # Footnotes are lifted out before the sections are wrapped, and come back as Notes before the references.
        fm = re.search(r'<hr class="footnotes-sep" />\s*<section class="footnotes">(.*?)</section>', body_html, re.S)
        footnotes = fm.group(1) if fm else ""
        if fm:
            body_html = body_html.replace(fm.group(0), "")
        toc: list = []
        body_html = self.number_sections(body_html, toc)
        body_html, has_refs = self.wrap_sections(body_html)
        abstract_html = self.md.render(abstract_md) if abstract_md else ""
        abstract_html = self.resolve_refs(abstract_html)
        body_html = self.resolve_refs(body_html)
        self.bib.assign_suffixes(self.cited)
        fill_year = lambda h: re.sub(r"\{YEAR:([^}]+)\}", lambda m: esc(self.bib.year(m.group(1))), h)  # noqa: E731
        body_html, abstract_html = fill_year(body_html), fill_year(abstract_html)
        refs_html = self.bib.html(self.cited) if self.cited else '<p class="vr-pending">No works cited yet.</p>'
        if has_refs:
            body_html = body_html.replace("<!--VR-REFERENCES-->", refs_html)
        elif self.cited:
            self.issue("warning", "citations found but no '## References' section; one was added at the end")
            body_html += f'<section class="vr-section vr-refs-section"><h2 id="sec-references">References</h2>{refs_html}</section>'
            toc.append((2, "", "References", "sec-references"))

        # Footnotes become a Notes block before the references, as in a printed paper.
        if footnotes:
            notes = f'<section class="vr-section vr-notes"><h2 id="sec-notes">Notes</h2>{footnotes}</section>'
            body_html = body_html.replace('<section class="vr-section vr-refs-section"', notes + '<section class="vr-section vr-refs-section"', 1) \
                if "vr-refs-section" in body_html else body_html + notes

        body_html = self.mark_pending(body_html)
        abstract_html = self.mark_pending(abstract_html)
        if re.search(r"\$\$|\\\(|class=\"math", body_html + abstract_html):
            self.has_math = True
        self.final_checks(abstract_md, toc)
        page = self.fill_template(body_html, abstract_html, toc)
        return Result(page, self.out_dir, self.issues, list(self.assets), self.meta, self.cited)

    def mark_pending(self, h: str) -> str:
        h = re.sub(r"<p><em>(Steps? \d.*?)</em></p>", r'<p class="vr-pending">\1</p>', h, flags=re.S)
        return PENDING_RE.sub(lambda m: f'<mark class="vr-todo">{m.group(0)}</mark>', h)

    def final_checks(self, abstract_md, toc):
        raw = self.body
        level = "error" if self.release else "warning"
        for m in PENDING_RE.finditer(raw):
            self.issue(level, f"unfinished marker {m.group(0)[:60]}", f"line {raw.count(chr(10), 0, m.start()) + 1 + self.front_lines}")
        for k, v in self.meta.items():
            if PENDING_RE.search(str(v)):
                self.issue(level, f"unfinished front matter: '{k}' still holds {PENDING_RE.search(str(v)).group(0)[:40]}…")
        for m in TEMPLATE_NOTE_RE.finditer(raw):
            self.issue(level, "template note still in place (a section not yet written)", f"line {raw.count(chr(10), 0, m.start()) + 1 + self.front_lines}")
        names = [re.sub(r"<[^>]+>", "", t[2]).strip().lower() for t in toc if t[0] == 2]
        if "disclaimer" not in names and self.meta.get("disclaimer", True) is not False:
            self.issue("error", "the Disclaimer section is missing; it is part of every Vivid report and is never removed "
                                "(an author who decides otherwise for one report sets `disclaimer: false` in its front matter)")
        if not abstract_md:
            self.issue(level, "no Abstract section")
        for ident, (word, num) in self.labels.items():
            if word in ("Figure", "Table") and ident not in self.referenced_ids:
                self.issue("warning", f"{word} {num} (@{ident}) is never referred to in the text")
        unused = sorted(set(self.bib.entries) - set(self.cited))
        for k in unused:
            self.issue("warning", f"reference '{k}' is in the references file but never cited")
        for k in ("title", "authors", "date"):
            if not self.meta.get(k):
                self.issue(level, f"front matter has no '{k}'")

    # ---- page
    def fill_template(self, body_html, abstract_html, toc) -> str:
        m = self.meta
        cfg = site_config()
        tpl = (SITE / "template.html").read_text(encoding="utf-8")
        authors = m.get("authors") or []
        affs = m.get("affiliations") or {}
        aff_keys = list(affs.keys())

        def aff_refs(a):
            v = a.get("affiliation", [])
            v = v if isinstance(v, list) else [x.strip() for x in str(v).split(",") if x.strip()]
            return [str(x) for x in v]

        auth_html = []
        for a in authors:
            a = a if isinstance(a, dict) else {"name": a}
            sup = ",".join(aff_refs(a))
            orcid = f' <a class="vr-orcid" href="https://orcid.org/{esc(a["orcid"])}" title="ORCID {esc(a["orcid"])}">iD</a>' if a.get("orcid") else ""
            mail = (f' <a class="vr-mail" href="mailto:{esc(a["email"])}" title="{"Corresponding author: " if a.get("corresponding") else ""}{esc(a["email"])}">✉</a>'
                    if a.get("email") else "")
            marks = ",".join(x for x in [sup if sup and len(aff_keys) > 1 else "", "*" if a.get("equal-contribution") else ""] if x)
            auth_html.append(f'<span class="vr-author">{esc(a.get("name", ""))}{f"<sup>{esc(marks)}</sup>" if marks else ""}{orcid}{mail}</span>')
        aff_html = "".join(f'<li>{f"<sup>{esc(k)}</sup>" if len(aff_keys) > 1 else ""}{esc(v)}</li>' for k, v in affs.items())
        if any(isinstance(a, dict) and a.get("equal-contribution") for a in authors):
            aff_html += f'<li class="vr-equal"><sup>*</sup>{esc(m.get("equal-contribution-note", "Equal contribution"))}</li>'

        state = self.status.get("state", "draft")
        badge = {"draft": ("Draft", "draft"), "in-review": ("Under review", "review"), "changes-requested": ("Revising after review", "review"),
                 "approved": ("Reviewed", "ok"), "published": ("Reviewed", "ok")}.get(state, ("Draft", "draft"))
        banner = ""
        if not self.release:
            if self.status.get("review_copy"):
                banner = (f'<div class="vr-banner vr-banner-review">Review copy · round {esc(self.status.get("round", "?"))} · '
                          f'content hash <code>{esc(self.status.get("hash", "")[:12])}</code> · not for circulation</div>')
            else:
                banner = '<div class="vr-banner">Draft · not reviewed by the Vivid Insights team · do not circulate</div>'

        toc_html = "".join(
            f'<li class="vr-toc-l{lvl}"><a href="#{esc(i)}">{f"<span>{esc(n)}</span>" if n else ""}{t}</a></li>' for lvl, n, t, i in toc)

        base_url = (cfg.get("base-url") or "").rstrip("/")
        url = m.get("url") or (f"{base_url}/{cfg.get('reports-path', 'reports').strip('/')}/{self.slug}/" if base_url else "")
        year = str(m.get("date", date.today()))[:4]
        bib_authors = " and ".join(self.bibtex_name(a.get("name", "") if isinstance(a, dict) else str(a)) for a in authors)
        bibtex = (f"@techreport{{{self.slug.replace('-', '_')},\n  title       = {{{m.get('title', '')}}},\n  author      = {{{bib_authors}}},\n"
                  f"  institution = {{Vivid Insights}},\n" + (f"  number      = {{{m.get('report-number')}}},\n" if m.get("report-number") else "")
                  + f"  year        = {{{year}}},\n" + (f"  url         = {{{url}}},\n" if url else "") + "}")
        first_author = authors[0].get("name", "") if authors and isinstance(authors[0], dict) else (authors[0] if authors else "")
        cite_line = f"{self.apa_names(authors)} ({year}). {m.get('title', '')}. Vivid Insights Research Report{(' ' + str(m['report-number'])) if m.get('report-number') else ''}."

        review_html = ""
        rv = self.status.get("record")
        if rv:
            names = ", ".join(esc(x) for x in rv.get("reviewers", []))
            review_html = (f'<div class="vr-review-record"><h3>Review</h3><p>Reviewed by the Vivid Insights team ({names}) over '
                           f'{esc(rv.get("rounds", 1))} round{"s" if rv.get("rounds", 1) != 1 else ""}; approved {esc(rv.get("approved", ""))}. '
                           f'Approved version <code>{esc(self.status.get("hash", "")[:12])}</code>.'
                           + (f' <a href="{esc(rv["link"])}">Review record</a>.' if rv.get("link") else "") + "</p></div>")

        desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", abstract_html)).strip()[:300]
        metas = [f'<meta name="citation_title" content="{esc(m.get("title", ""))}">']
        metas += [f'<meta name="citation_author" content="{esc(a.get("name", "") if isinstance(a, dict) else a)}">' for a in authors]
        metas += [f'<meta name="citation_publication_date" content="{esc(str(m.get("date", "")).replace("-", "/"))}">',
                  '<meta name="citation_technical_report_institution" content="Vivid Insights">']
        if m.get("report-number"):
            metas.append(f'<meta name="citation_technical_report_number" content="{esc(m["report-number"])}">')
        if url:
            metas += [f'<link rel="canonical" href="{esc(url)}">', f'<meta property="og:url" content="{esc(url)}">']
        if not self.release:
            metas.append('<meta name="robots" content="noindex">')

        katex = ""
        if self.has_math:
            kv = cfg.get("katex-version", "0.16.11")
            katex = (f'<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@{kv}/dist/katex.min.css" crossorigin="anonymous">\n'
                     f'<script defer src="https://cdn.jsdelivr.net/npm/katex@{kv}/dist/katex.min.js" crossorigin="anonymous"></script>')

        keywords = m.get("keywords") or []
        vals = {
            "title": esc(m.get("title", "Untitled report")),
            "title_html": self.mark_pending(self.md.renderInline(str(m.get("title", "Untitled report")))),
            "subtitle_html": f'<p class="vr-subtitle">{self.md.renderInline(str(m["subtitle"]))}</p>' if m.get("subtitle") else "",
            "description": esc(desc),
            "citation_meta": "\n".join(metas),
            "katex": katex,
            "report_number": esc(m.get("report-number", "")),
            "kicker": "Research Report" + (f' · {esc(m["report-number"])}' if m.get("report-number") else ""),
            "authors_html": ", ".join(auth_html),
            "affiliations_html": aff_html,
            "date": esc(self.format_date(m.get("date"))),
            "version": esc(m.get("version", "")),
            "badge_text": badge[0], "badge_class": badge[1],
            "abstract_html": abstract_html,
            "keywords_html": (f'<p class="vr-keywords"><span>Keywords</span> {esc(", ".join(map(str, keywords)))}</p>' if keywords else ""),
            "toc_html": toc_html,
            "body_html": body_html,
            "banner": banner,
            "bibtex": esc(bibtex),
            "cite_line": esc(cite_line),
            "review_html": review_html,
            "licence_html": f"Published under {esc(m['licence'])}. " if m.get("licence") else "",
            "provenance_heading": "Licence and provenance" if m.get("licence") else "Provenance",
            "hash": esc(self.status.get("hash", "")[:12]),
            "repository": f' · <a href="{esc(m["repository"])}">Source and working record</a>' if m.get("repository") else "",
            "built": date.today().isoformat(),
            "first_author": esc(first_author),
            "contact": esc(cfg.get("contact", "info@vividinsights.se")),
            "home": esc(cfg.get("home-url", "../../vivid-insights.html")),
            "state": esc(state),
        }
        return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda mm: str(vals.get(mm.group(1), mm.group(0))), tpl)

    @staticmethod
    def bibtex_name(name: str) -> str:
        parts = name.split()
        return f"{parts[-1]}, {' '.join(parts[:-1])}" if len(parts) > 1 else name

    @staticmethod
    def apa_names(authors) -> str:
        names = []
        for a in authors:
            n = (a.get("name", "") if isinstance(a, dict) else str(a)).split()
            names.append(f"{n[-1]}, {initials(' '.join(n[:-1]))}" if len(n) > 1 else " ".join(n))
        if len(names) <= 1:
            return "".join(names)
        return ", ".join(names[:-1]) + ", & " + names[-1]

    @staticmethod
    def format_date(d) -> str:
        if not d:
            return ""
        try:
            dd = d if isinstance(d, date) else date.fromisoformat(str(d))
            return f"{dd.day} {dd.strftime('%B %Y')}"
        except ValueError:
            return str(d)


def write_output(res: Result, builder: Builder) -> None:
    out = res.out_dir
    if out.exists():
        shutil.rmtree(out)
    (out / "assets").mkdir(parents=True)
    shutil.copytree(SITE / "assets", out / "assets", dirs_exist_ok=True)
    for src, dest in builder.assets.items():
        d = out / dest
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, d)
    for src, dest in builder.asset_dirs.items():
        shutil.copytree(src, out / dest, dirs_exist_ok=True)
    (out / "index.html").write_text(res.html, encoding="utf-8")


def build(report: Path, out_dir: Path | None = None, release: bool = False, status: dict | None = None,
          style: bool = True) -> tuple[Result, Builder]:
    if status is None:
        from reviewlib import review_status
        status = review_status(report)
    b = Builder(report, out_dir, release, status)
    res = b.build()
    if style:
        from check import style_issues
        res.issues.extend(style_issues(report))
    write_output(res, b)
    return res, b


def print_issues(issues: list[Issue], show_style: bool = True) -> None:
    order = {"error": 0, "warning": 1, "style": 2}
    for i in sorted(issues, key=lambda x: order[x.level]):
        if i.level == "style" and not show_style:
            continue
        print("  " + str(i))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("report", nargs="?", help="path to the report Markdown (default: Report.md)")
    ap.add_argument("--out", help="output folder (default: build/<slug>/)")
    ap.add_argument("--open", action="store_true", help="open the built page in the browser")
    ap.add_argument("--no-style", action="store_true", help="skip the writing-style hints")
    args = ap.parse_args(argv)
    report = resolve_report(args.report)
    try:
        res, _ = build(report, Path(args.out).resolve() if args.out else None, style=not args.no_style)
    except ReportError as e:
        print(f"Build failed: {e}")
        return 2
    n = {lvl: sum(1 for i in res.issues if i.level == lvl) for lvl in ("error", "warning", "style")}
    print(f"Built {rel(res.out_dir / 'index.html')}  —  {n['error']} errors, {n['warning']} warnings, {n['style']} style hints")
    print_issues(res.issues)
    if args.open:
        subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(res.out_dir / "index.html")])
    return 1 if n["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
