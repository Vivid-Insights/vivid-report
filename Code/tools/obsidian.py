"""Make a report's figures and quoted text visible inline in Obsidian.

    cd Code && uv run python tools/obsidian.py                 # the open paper, Report.md
    cd Code && uv run python tools/obsidian.py ../papers/0000-specimen/Report.md

Obsidian shows a `::: figure` block as its caption alone. This writes an embed,
`![[papers/NNNN-slug/<path>]]`, on the first line of every figure, video, interactive and panel
block, so the image (the video, or an interactive's still) appears where the reader meets it. The
path is from the top of the vault, so it stays right when the paper moves between `Report.md` and
its folder. The build drops these lines and warns when one no longer matches its block.

An `output`, `prompt` or `conversation` block is shown as its bare text, so it runs together with
the prose around it. This puts a `> ` on each of its lines, which Obsidian renders as a blockquote.
The build takes the prefix off again before it checks the text against its source file and before it
publishes, so the quote stays word for word.

Only the embed lines and the blockquote prefixes are touched: an existing one is replaced, a missing
one added. Run it again after changing a block's `src=`, `poster=` or `fallback=`, or its text.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import BLOCK_RE, MEDIA_KINDS, PREVIEW_RE, QUOTE_KINDS, parse_attrs, unquote_md  # noqa: E402
from common import FRONT_RE, ROOT, load_report, paper_dir, rel, resolve_report  # noqa: E402


def target(kind: str, attrs: dict) -> str | None:
    return attrs.get("fallback") if kind == "interactive" else attrs.get("src")


def with_previews(text: str, base: Path, counts: dict) -> str:
    def sub(m: re.Match) -> str:
        kind, attrs, body = m.group("kind"), parse_attrs(m.group("attrs")), m.group("body")
        if kind in QUOTE_KINDS:
            plain = unquote_md(body)
            quoted = "\n".join(f"> {ln}" if ln.strip() else ">" for ln in plain.split("\n"))
            counts["set"] += 0 if quoted == body else 1
            head = m.group(0)[: m.start("body") - m.start()]
            tail = m.group(0)[m.end("body") - m.start():]
            return head + quoted + tail
        if kind not in MEDIA_KINDS and kind != "panel":
            return m.group(0)
        if kind == "figure":
            body = with_previews(body, base, counts)  # its panels
        t = target(kind, attrs)
        old = PREVIEW_RE.match(body)
        rest = body[old.end():] if old else body
        if t and not t.startswith(("http://", "https://")) and (base / t).exists():
            line = f"![[{(base / t).resolve().relative_to(ROOT).as_posix()}]]"
            counts["set"] += 0 if old and old.group(0).strip() == line else 1
            body = f"{line}\n{rest}"
        elif old:
            counts["removed"] += 1
            body = rest
        head = m.group(0)[: m.start("body") - m.start()]
        tail = m.group(0)[m.end("body") - m.start():]
        return head + body + tail

    return BLOCK_RE.sub(sub, text)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("report", nargs="?")
    a = ap.parse_args(argv)
    report = resolve_report(a.report)
    meta, _ = load_report(report)
    base = paper_dir(meta, report)
    raw = report.read_text(encoding="utf-8")
    fm = FRONT_RE.match(raw)
    head, body = (raw[: fm.end()], raw[fm.end():]) if fm else ("", raw)
    counts = {"set": 0, "removed": 0}
    new = head + with_previews(body, base, counts)
    if new != raw:
        report.write_text(new, encoding="utf-8")
    print(f"{rel(report)}: {counts['set']} Obsidian previews written, {counts['removed']} removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
