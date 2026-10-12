"""Convert the cited entries of the paper's BibTeX file into references.yaml.

    cd Code && uv run python ../papers/0001-representing-data-in-words/Code/bib_to_yaml.py          # writes the paper's references.yaml
    cd Code && uv run python ../papers/0001-representing-data-in-words/Code/bib_to_yaml.py --list   # show the parsed entries, write nothing

Reads `Attachments/wordalisation-paper/neurips_2026.tex` for the keys actually cited (commented-out
LaTeX ignored) and `reference_nature.bib` for their details. Authors, titles, venues and years are
taken from the BibTeX unchanged, except that LaTeX markup is turned into plain characters.

The report format needs a link for every reference. Where the BibTeX entry has no `doi` or `url`,
the link comes from LINKS below: each was found by looking the work up and checked to resolve, and
the note says how (see the Log in Appendix.md).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]          # this paper's folder
SRC = ROOT / "Attachments" / "wordalisation-paper"
TEX = SRC / "neurips_2026.tex"
BIB = SRC / "reference_nature.bib"
OUT = ROOT / "references.yaml"

# Links for entries whose BibTeX has neither doi nor url. Filled in after looking each one up;
# a work that could not be found stays out of this table and the build reports it.
#
# Looked up on 9 October 2026. A DOI was accepted only when the title Crossref registers for it matches
# the BibTeX title; a URL only when the page it returns carries the work's title.
LINKS: dict[str, dict] = {
    "davenport2020beyond": {"doi": "10.1162/99608f92.55546b4a"},          # Crossref title match
    "greener2022guide": {"doi": "10.1038/s41580-021-00407-0"},            # Crossref title match
    "latif2020leveraging": {"doi": "10.1109/tai.2020.3020521"},           # Crossref title match
    "zhang2020data": {"doi": "10.1145/3392826"},                          # Crossref title match
    "kennedy2016work": {"doi": "10.1080/1369118x.2016.1153126"},          # Crossref title match
    "liu2023pre": {"doi": "10.1145/3560815"},                             # Crossref title match
    "liu2022few": {"doi": "10.52202/068431-0142"},                        # Crossref title match (NeurIPS 35 proceedings)
    "matthews2003personality": {"doi": "10.1017/cbo9780511812743"},       # Crossref title match (Cambridge)
    "mitchell2019model": {"doi": "10.1145/3287560.3287596"},              # Crossref title match
    "crisan2022interactive": {"doi": "10.1145/3531146.3533108"},          # Crossref title match
    "gebru2021datasheets": {"doi": "10.1145/3458723"},                    # Crossref title match
    "tang2024ai": {"doi": "10.1145/3630106.3658935"},                     # Crossref title match
    "tong2021inapplicability": {"doi": "10.1080/17512786.2019.1698974"},  # Crossref title match
    "jia2022visual": {"doi": "10.1007/978-3-031-19827-4_41"},             # Crossref title "Visual Prompt Tuning"
    "crawford2021atlas": {"doi": "10.12987/9780300252392"},               # Crossref title "Atlas of AI" (Yale, the same book)
    "brown2020language": {"url": "https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html"},
    "lewis2020retrieval": {"url": "https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html"},
    "radford2019language": {"url": "https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf"},
    "cairo2016truthful": {"url": "https://www.peachpit.com/store/truthful-art-data-charts-and-maps-for-communication-9780321934079"},
    "richards2023streamlit": {"url": "https://openlibrary.org/isbn/9781803248226"},  # Packt and O'Reilly block scripts; Open Library record checked
    "vendrow2024large": {"url": "https://openreview.net/forum?id=XSeN6xZtZ9"},       # OpenReview API: exact title, SafeGenAI workshop
}

# Where BibTeX's own reading of an entry would misstate it on the page.
OVERRIDES: dict[str, dict] = {
    # `author = {Langchain Blog}` is a publication, not a person called Blog; it has no year.
    "context_engineering": {"author": ["LangChain Blog"], "year": "n.d."},
    # Typos in the BibTeX, corrected at the authors' request (10 October 2026): lost capitals in
    # acronyms and names, and addresses run into the publisher.
    "greener2022guide": {"container": "Nature Reviews Molecular Cell Biology", "publisher": "Nature Publishing Group UK"},
    "zhang2020data": {"title": "How do data science workers collaborate? Roles, workflows, and tools", "publisher": "ACM"},
    "liu2023pre": {"publisher": "ACM"},
    "gebru2021datasheets": {"publisher": "ACM"},
    "brown2020language": {"container": "Advances in Neural Information Processing Systems"},
    "liu2022few": {"container": "Advances in Neural Information Processing Systems"},
    "lewis2020retrieval": {"title": "Retrieval-augmented generation for knowledge-intensive NLP tasks",
                           "container": "Advances in Neural Information Processing Systems"},
    "gu2024survey": {"title": "A survey on LLM-as-a-judge"},
    "li2024generation": {"title": "From generation to judgment: Opportunities and challenges of LLM-as-a-judge"},
    "vendrow2024large": {"container": "NeurIPS Safe Generative AI Workshop 2024"},
    "mitchell2019model": {"container": "Proceedings of the Conference on Fairness, Accountability, and Transparency"},
    "radford2019language": {"container": "OpenAI Blog"},
}

# Names BibTeX split or cased wrongly, corrected wherever they occur.
NAME_FIXES = {"Iii, Hal Daumé": "Daumé III, Hal", "XU, Zhanchao": "Xu, Zhanchao", "Haften, Nanette van": "van Haften, Nanette"}

ACCENTS = {"'": "\u0301", "`": "\u0300", "^": "\u0302", '"': "\u0308", "~": "\u0303", "c": "\u0327", "v": "\u030C", "=": "\u0304"}


def strip_comments(tex: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in tex.splitlines())


def cited_keys(tex: str) -> list[str]:
    keys: list[str] = []
    for m in re.finditer(r"\\cite[pt]?\*?\{([^}]*)\}", strip_comments(tex)):
        for k in m.group(1).split(","):
            k = k.strip()
            if k and k not in keys:
                keys.append(k)
    return keys


def read_braced(s: str, i: int) -> tuple[str, int]:
    """s[i] is '{' or '"'; return the contents and the index after the closing delimiter."""
    if s[i] == '"':
        j = i + 1
        depth = 0
        while j < len(s):
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
            elif s[j] == '"' and depth == 0:
                return s[i + 1:j], j + 1
            j += 1
        raise ValueError("unterminated string")
    depth, j = 0, i
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError("unbalanced braces")


def parse_bib(text: str) -> dict[str, dict]:
    entries = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        typ, key = m.group(1).lower(), m.group(2)
        if typ in ("comment", "preamble", "string"):
            continue
        i, fields = m.end(), {"_type": typ}
        while i < len(text):
            fm = re.compile(r"\s*,?\s*(\w[\w-]*)\s*=\s*").match(text, i)
            if not fm:
                break
            name = fm.group(1).lower()
            i = fm.end()
            if text[i] in "{\"":
                val, i = read_braced(text, i)
            else:
                vm = re.compile(r"[^,}\s]+").match(text, i)
                val, i = vm.group(0), vm.end()
            fields[name] = val
            nxt = re.compile(r"\s*,?\s*").match(text, i)
            i = nxt.end()
            if i < len(text) and text[i] == "}":
                break
        entries[key] = fields
    return entries


def plain(s: str) -> str:
    """LaTeX markup to plain characters. Words are not changed."""
    s = re.sub(r"\\([`'^\"~=])\s*\{?\\?([A-Za-z])\}?", lambda m: m.group(2) + ACCENTS[m.group(1)], s)
    s = re.sub(r"\\([cv])\{([A-Za-z])\}", lambda m: m.group(2) + ACCENTS[m.group(1)], s)
    s = s.replace("\\&", "&").replace("\\_", "_").replace("\\%", "%").replace("\\$", "$").replace("~", " ")
    s = s.replace("--", "–").replace("\\textendash", "–")
    s = re.sub(r"\\(textit|emph|textbf|texttt|textrm|mathrm|url)\{([^{}]*)\}", r"\2", s)
    s = re.sub(r"\\[a-zA-Z]+\s*", "", s)
    s = s.replace("{", "").replace("}", "")
    import unicodedata
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", s)).strip()


def authors(field: str) -> list[str]:
    out = []
    for a in re.split(r"\s+and\s+", field.strip()):
        a = a.strip()
        if a.startswith("{") and a.endswith("}"):
            out.append(plain(a))            # a corporate author: {OpenAI}
            continue
        a = plain(a)
        if "," in a:
            out.append(a)
        elif " " in a:
            parts = a.split()
            out.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
        else:
            out.append(a)
    return out


TYPES = {"article": "article", "inproceedings": "chapter", "incollection": "chapter", "book": "book",
         "misc": "web", "techreport": "report", "online": "web", "phdthesis": "report"}


def convert(key: str, e: dict) -> dict:
    r: dict = {"id": key}
    t = e["_type"]
    arxiv = e.get("eprint") if "arxiv" in (e.get("archiveprefix", "") + e.get("journal", "") + e.get("url", "")).lower() else None
    r["type"] = "preprint" if arxiv or "arxiv" in e.get("journal", "").lower() else TYPES.get(t, "article")
    if e.get("author"):
        r["author"] = authors(e["author"])
    elif e.get("editor"):
        r["editor"] = authors(e["editor"])
    r["title"] = plain(e.get("title", ""))
    r["year"] = plain(e.get("year", ""))
    cont = e.get("journal") or e.get("booktitle") or e.get("howpublished") or ""
    if cont and not cont.strip().startswith("\\url"):
        r["container"] = plain(cont)
    if arxiv and "container" not in r:
        r["container"] = "arXiv"
    for f in ("volume", "pages", "publisher"):
        if e.get(f):
            r[f] = plain(e[f])
    if e.get("number"):
        r["issue" if t == "article" else "number"] = plain(e["number"])
    if arxiv:
        r["number"] = plain(arxiv)
    if e.get("doi"):
        r["doi"] = plain(e["doi"]).replace("https://doi.org/", "")
    url = e.get("url") or (re.search(r"\\url\{([^}]*)\}", e.get("howpublished", "")) or [None, None])[1]
    if url:
        r["url"] = url.replace("\\_", "_").replace("\\%", "%").strip()
    ax = re.search(r"arXiv:(\d{4}\.\d{4,5})", r.get("container", ""))
    if ax and not (r.get("doi") or r.get("url")):
        r["url"] = f"https://arxiv.org/abs/{ax.group(1)}"   # the arXiv number is in the BibTeX venue itself
    if not (r.get("doi") or r.get("url")) and key in LINKS:
        r.update(LINKS[key])
    r.update(OVERRIDES.get(key, {}))
    for f in ("author", "editor"):
        if f in r:
            r[f] = [NAME_FIXES.get(a, a) for a in r[f]]
    if e.get("note") and "accessed" not in e["note"].lower():
        r.setdefault("note", plain(e["note"]))
    return r


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv)
    keys = cited_keys(TEX.read_text(encoding="utf-8"))
    bib = parse_bib(BIB.read_text(encoding="utf-8"))
    missing = [k for k in keys if k not in bib]
    refs = [convert(k, bib[k]) for k in keys if k in bib]
    if args.list:
        for r in refs:
            print(r)
        print(f"\n{len(keys)} cited, {len(missing)} not in the bib: {missing}")
        print("no link:", [r["id"] for r in refs if not (r.get("doi") or r.get("url"))])
        return 0
    header = ("# Works cited in Report.md: the cited entries of Attachments/wordalisation-paper/reference_nature.bib,\n"
              "# converted by Code/bib_to_yaml.py. Do not edit by hand; change the script and re-run it.\n")
    OUT.write_text(header + yaml.safe_dump(refs, sort_keys=False, allow_unicode=True, width=200), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(refs)} references; {len(missing)} cited keys missing from the bib")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
