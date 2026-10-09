"""Check a report against the writing rules that a machine can check.

    cd Code && uv run python tools/check.py                 # Report.md
    cd Code && uv run python tools/check.py --release       # as tools/publish.py will: unfinished work is an error

Most of WRITING.md needs a reader: no figure of speech, no throat-clearing, the concrete case first.
This catches the part that does not — bold in the body, words that grade the evidence, the
"not X but Y" construction, American spellings, hard-wrapped paragraphs — so a reviewer's time goes
on the argument. Style hints never block a build; they are a list for the author to judge.
The structural checks (broken references, quotes that are not word for word, a missing disclaimer)
come from the build itself and are errors.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import FRONT_RE, resolve_report  # noqa: E402

GRADING = ["striking", "strikingly", "reassuring", "worrying", "encouraging", "damning", "impressive", "remarkable",
           "remarkably", "groundbreaking", "ground-breaking", "game-changing", "revolutionary", "unprecedented",
           "powerful", "novel", "crucial", "seamless", "seamlessly", "cutting-edge", "state-of-the-art"]
FILLER = [r"\bin today'?s\b", r"rapidly evolving", r"\bit is worth noting\b", r"\bit'?s worth noting\b",
          r"\bthe real question\b", r"\bwhat makes this interesting\b", r"\bdelve\b", r"\btapestry\b",
          r"\bplays a (crucial|key|vital|pivotal) role\b", r"\blandscape\b", r"\bunlock(s|ing)?\b"]
NOT_X_BUT_Y = [r"\bnot (just|only|merely|simply)\b[^.]{0,80}\b(but|it'?s|—)", r"\bisn'?t\b[^.]{0,60}(—|–|;|,)\s*it'?s\b",
               r"\bnot\b[^.,;]{1,50},? but (rather )?\b", r"\bless\b[^.]{1,40}\bthan\b[^.]{1,40}\bmore\b",
               r"\bis only half the story\b", r"\band that is the easy part\b"]
OPENERS = [r"^(This|The present) (report|paper|article|study|work) (examines|explores|investigates|presents|describes)\b",
           r"^In this (report|paper|article|section),? we\b"]
US_SPELLINGS = {"wordalization": "wordalisation", "wordalizations": "wordalisations", "visualization": "visualisation",
                "visualizations": "visualisations", "visualize": "visualise", "organization": "organisation",
                "organizations": "organisations", "analyze": "analyse", "analyzed": "analysed", "analyzing": "analysing",
                "behavior": "behaviour", "behaviors": "behaviours", "modeling": "modelling", "modeled": "modelled",
                "color": "colour", "colors": "colours", "center": "centre", "optimize": "optimise", "optimization": "optimisation",
                "recognize": "recognise", "summarize": "summarise", "summarized": "summarised", "characterize": "characterise",
                "generalize": "generalise", "standardize": "standardise", "standardized": "standardised", "favor": "favour",
                "favorable": "favourable", "utilize": "use", "utilization": "use", "prioritize": "prioritise"}

SKIP_BLOCK_RE = re.compile(r"^(```|~~~).*?^\1\s*$|^:::[ \t]*(output|prompt|conversation)\b.*?^:::\s*$", re.S | re.M)


def _strip(text: str) -> tuple[str, int]:
    """Body text with front matter removed and quoted/code blocks blanked (keeping line numbers)."""
    m = FRONT_RE.match(text)
    offset = text[: m.end()].count("\n") if m else 0
    body = text[m.end():] if m else text
    body = SKIP_BLOCK_RE.sub(lambda mm: "\n" * mm.group(0).count("\n"), body)
    return body, offset


def style_issues(report: Path):
    from build import Issue
    text = report.read_text(encoding="utf-8")
    body, offset = _strip(text)
    issues = []
    lines = body.splitlines()
    section = ""
    prev_prose = False
    for i, line in enumerate(lines):
        n = f"line {i + 1 + offset}"
        s = line.strip()
        if s.startswith("#"):
            section = s.lstrip("#").strip().lower()
            prev_prose = False
            continue
        is_prose = bool(s) and not re.match(r"^(\||:::|\$\$|<|!\[|[-*+] |\d+\. |>|\[\^)", s) and not s.startswith("*Step")
        if is_prose and prev_prose:
            issues.append(Issue("style", "paragraph is hard-wrapped: write each paragraph on one line", n))
        prev_prose = is_prose
        if not s or section in ("references",):
            continue
        plain = re.sub(r"`[^`]*`", "", s)
        if re.search(r"\*\*[^*]+\*\*|__[^_]+__|<b>|<strong>", plain) and section not in ("disclaimer",):
            issues.append(Issue("style", "bold in the report body: emphasis should come from sentence order, not typography", n))
        low = plain.lower()
        for w in GRADING:
            if re.search(rf"\b{re.escape(w)}\b", low):
                issues.append(Issue("style", f"'{w}' grades the evidence or sells the work: give the magnitude and let the reader judge", n))
        for p in FILLER:
            if re.search(p, low):
                issues.append(Issue("style", f"stock phrase ({re.search(p, low).group(0)}): say the concrete thing", n))
        for p in NOT_X_BUT_Y:
            if re.search(p, low):
                issues.append(Issue("style", "possible 'not X but Y' construction: say Y", n))
                break
        for p in OPENERS:
            if re.search(p, plain):
                issues.append(Issue("style", "opens on the document rather than the problem", n))
        for us, uk in US_SPELLINGS.items():
            if re.search(rf"\b{us}\b", low):
                issues.append(Issue("style", f"American spelling '{us}': house style is '{uk}' (leave it if it is inside a quotation or a name)", n))
    return issues


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a report against the writing rules a machine can check")
    ap.add_argument("report", nargs="?")
    ap.add_argument("--release", action="store_true", help="treat unfinished work as an error, as publishing does")
    args = ap.parse_args(argv)
    report = resolve_report(args.report)
    from build import Builder, print_issues
    from reviewlib import review_status
    b = Builder(report, release=args.release, status=review_status(report))
    res = b.build()
    issues = res.issues + style_issues(report)
    n = {lvl: sum(1 for i in issues if i.level == lvl) for lvl in ("error", "warning", "style")}
    print(f"{report.name}: {n['error']} errors, {n['warning']} warnings, {n['style']} style hints")
    print_issues(issues)
    return 1 if n["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
