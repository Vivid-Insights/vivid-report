"""Check that the built page says exactly what the paper's LaTeX source says.

    cd Code && uv run python tools/build.py && uv run python ../papers/0002-representing-data-in-words/Code/check_against_source.py

Extracts the words of `Attachments/wordalisation-paper/neurips_2026.tex` (abstract to bibliography;
comments, the NeurIPS checklist and LaTeX markup removed) and the words of the built page (title
block and body; the Disclaimer, Notes heading and reference list removed), and compares them in order.

What is allowed to differ, and is removed from both sides before comparing: citations (numbered in
the PDF, author–date here), the numbers of cross-references, and the labels the format adds
("Figure 1.", "(a)", section numbers). Quotation marks and dashes are compared by kind, not glyph,
since LaTeX and the web page draw them differently. Everything else must match word for word; any
difference is printed and the exit code is 1.

Since 10 October 2026 the page carries the typo corrections the authors asked for. They are listed in
CORRECTIONS below and applied to the LaTeX before comparing, so the check still proves that nothing
else changed.
"""

from __future__ import annotations

import difflib
import html
import re
import sys
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]          # this paper's folder
WORKSPACE = PAPER.parents[1]
TEX = PAPER / "Attachments" / "wordalisation-paper" / "neurips_2026.tex"
PAGE = WORKSPACE / "build" / "representing-data-in-words" / "index.html"


def unify(s: str) -> str:
    s = s.replace("$", "").replace("{", " ").replace("}", " ").replace("\\%", "%")   # maths: TeX is kept raw on the page
    s = s.replace("``", '"').replace("`", "'").replace("''", '"').replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    s = s.replace("---", "—").replace(" -- ", " – ")
    s = s.replace("\u00a0", " ")
    s = re.sub(r"\s+([.,;:)])", r"\1", s)                         # punctuation left behind by a removed citation
    s = re.sub(r"\(\s+", "(", s)
    return s


notes: list[str] = []

# Corrections made at the authors' request on 10 October 2026 ("correct all typos"), as they read in the
# words this script compares. Each is applied to the LaTeX words and must match exactly once, so the
# check confirms that these, and nothing else, are the differences between the page and the source.
CORRECTIONS = [
    ("absence of standardized benchmarks", "absence of standardised benchmarks"),
    ("prompt, the model generate a wordalisation", "prompt, the model generates a wordalisation"),
    ("He was average in [smart passes]", "He was [average] in [smart passes]"),
    ("Unlike traditional data-to-text generation which aims", "Unlike traditional data-to-text generation, which aims"),
    ("tables, and rely on heavy training, our method are based on in-context learning using already pre-trained LLM to",
     "tables, and relies on heavy training, our method is based on in-context learning using already pre-trained LLMs to"),
    ("from other llm-based", "from other LLM-based"),
    ("the semantic failing for such strategies", "the semantic failings of such strategies"),
    ("methods, wordalisation aim to", "methods, wordalisation aims to"),
    ("and in come cases better than fine tuned models", "and in some cases better than fine-tuned models"),
    ("and corresponding wordalisation for each application", "and corresponding wordalisations for each application"),
    ("Case study of the person 69.", "Case study of person 69."),
    ("heading and other skills an overview", "heading and other skills, an overview"),
    ("generates bland formulaic, but accurate", "generates bland, formulaic but accurate"),
    ("Wikipedia of the big five personality", "Wikipedia of the Big Five personality"),
    ("application, the threshold for z-scores", "application, the thresholds for z-scores"),
    ('described as "outstanding", between 1.0', 'described as "outstanding"; between 1.0'),
    ("a control text, the LLM receives", "a control text, for which the LLM receives"),
    ("A statistical text we send only", "A statistical text, for which we send only"),
    ("cases, while using the full Wordalisation texts and 18 %.", "cases, while the full wordalisation texts gave inaccuracies in 18% of cases."),
    ("generated json file", "generated JSON file"),
    ("over all wordalistations.", "over all wordalisations."),
    ("synthetic text, generate according to", "synthetic text, generated according to"),
    ("distribution and lie at an accuracy", "distribution and lies at an accuracy"),
    ("indicate that the wordalisation were very faithful", "indicate that the wordalisations were very faithful"),
    ("football scout example, the LLM", "football scout examples, the LLM"),
    ("no fall back data", "no fallback data"),
    ("we regenerate description for 30 entities - 10 from each example- resulting in total of 90 texts.",
     "we regenerated descriptions for 30 entities (10 from each example), resulting in a total of 90 texts."),
    ("never evaluates multiple descriptions", "never evaluated multiple descriptions"),
    ("40 texts form the wordalisation prompt", "40 texts from the wordalisation prompt"),
    ("the wordalisation and statistical vastly texts outperformed the statistical text",
     "the wordalisation and statistical texts vastly outperformed the control text"),
    ("adapted from and can be found here", "adapted from, and these can be found here"),
    ("are examples, are a powerful way", "are examples, is a powerful way"),
    ("different objective than captured by", "different objective from those captured by"),
    ("other kind of data (such that categorical variables, time series)", "other kinds of data (such as categorical variables and time series)"),
    ("The examples presented is intended", "The examples presented are intended"),
    ("potential to be adopted to a professional", "potential to be adapted to a professional"),
    # Confirmed by David, 10 October 2026.
    ("chi^2=40.50 for engagement", "chi^2=40.50 for usefulness"),
    ("We had 121 responses", "We had 122 responses"),
]
# The anonymised review links, replaced by the public repository at the authors' request.
LINK_CORRECTIONS = {
    "https://anonymous.4open.science/r/wordalisation-95BF/Prompt%20Cards/README.md": "https://github.com/BeimnetGirma/wordalisations/blob/main/prompt%20cards/prompt-cards.md",
    "https://anonymous.4open.science/r/wordalisation-95BF/README.md": "https://github.com/BeimnetGirma/wordalisations",
}


def apply_corrections(words: list[str]) -> list[str]:
    text = " ".join(words)
    for before, after in CORRECTIONS:
        n = text.count(before)
        if n != 1:
            raise SystemExit(f"Correction expected once in the LaTeX, found {n} times: {before!r}")
        text = text.replace(before, after)
    return text.split()


def tex_words() -> list[str]:
    t = TEX.read_text(encoding="utf-8")
    t = "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in t.splitlines())
    title = re.search(r"\\title\{(.*?)\}", t).group(1)
    t = t[t.index("\\begin{abstract}"):t.index("\\bibliographystyle")]
    # A table's caption is set above the table on the page and below it in LaTeX: move it up.
    t = re.sub(r"(\\begin\{table\}(?:\[[^\]]*\])?)(.*?)(\\caption\{[^{}]*\})(.*?\\end\{table\})",
               lambda m: m.group(1) + m.group(3) + m.group(2) + m.group(4), t, flags=re.S)
    t = re.sub(r"\\begin\{tabularx\}\{\\linewidth\}\{p\{[^}]*\}\s*\|\s*X\}", " ", t)   # column spec
    t = re.sub(r"~?\\cite[pt]?\{[^}]*\}", " ", t)                       # citations: style differs
    t = re.sub(r"(Fig\.|Section|Figure)~?\\ref\{[^}]*\}", r"\1 ", t)     # cross-reference numbers
    t = re.sub(r"\\label\{[^}]*\}", " ", t)
    t = re.sub(r"\\includegraphics(\[[^\]]*\])?\{[^}]*\}", " ", t)
    t = re.sub(r"\\begin\{tcolorbox\}(\[[^\]]*\])?", " ", t)
    t = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^\]]*\])?(\{[^}]*\})?", " ", t)
    t = re.sub(r"\\multicolumn\{\d+\}\{[^}]*\}\{\\textbf\{([^}]*)\}\}", r"\1", t)
    notes.extend(re.findall(r"\\footnote\{\\url\{([^}]*)\}\}", t))
    t = re.sub(r"\\footnote\{\\url\{([^}]*)\}\}", " ", t)              # compared separately: they move to Notes
    t = re.sub(r"\[[^\]]*\]\{[0-9.]*\\(columnwidth|linewidth)\}", " ", t)
    t = re.sub(r"\\url\{\s*([^}]*)\}", r" \1 ", t)
    t = re.sub(r"\\item\[([^\]]*)\]", r" \1 ", t)
    t = re.sub(r"\\(section|subsection|section\*|caption|textbf|textit|emph)\*?\{", "{", t)
    t = re.sub(r"\{\\(it|bf)\s+", "{", t)
    t = re.sub(r"\\(toprule|midrule|bottomrule|hline|centering|footnotesize|hfill|newpage|maketitle|setlength\S*)", " ", t)
    t = t.replace("\\\\", " ").replace("~", " ").replace("&", " ").replace("\\%", "%").replace("\\&", "&")
    t = t.replace("\\[", " $$ ").replace("\\]", " $$ ")
    t = re.sub(r"\{(b|h|t|h!|\\linewidth|\\columnwidth)\}", " ", t)
    t = t.replace("{", " ").replace("}", " ")
    t = t.replace("Q\\ A", "Q&A").replace("Q\\&A", "Q&A")
    words = unify(title + " " + t).split()
    return [w for w in words if w not in ("$$",)]


page_notes: list[str] = []


def page_words() -> list[str]:
    h = PAGE.read_text(encoding="utf-8")
    title = re.search(r'<h1 class="vr-title">(.*?)</h1>', h, re.S).group(1)
    abstract = re.search(r'<section class="vr-abstract".*?</section>', h, re.S).group(0)
    body = re.search(r'<article class="vr-body">(.*?)</article>', h, re.S).group(1)
    body = re.sub(r'<section class="vr-section vr-disclaimer".*?</section>', " ", body, flags=re.S)
    body = re.sub(r'<section class="vr-section vr-refs-section".*?</section>', " ", body, flags=re.S)
    page_notes.extend(html.unescape(u).replace("\\%", "%") for u in re.findall(r'<section class="vr-section vr-notes">.*?</section>', body, re.S) for u in re.findall(r'href="(https?://[^"]+)"', u))
    body = re.sub(r'<section class="vr-section vr-notes">.*?</section>', " ", body, flags=re.S)
    s = title + " " + abstract + " " + body
    s = re.sub(r"<h2>Abstract</h2>", " ", s)
    s = re.sub(r'\(?<a class="vr-cite"[^>]*>.*?</a>(?:; <a class="vr-cite"[^>]*>.*?</a>)*\)?', " ", s, flags=re.S)
    s = re.sub(r'<a class="vr-xref"[^>]*>.*?</a>', " ", s, flags=re.S)
    s = re.sub(r'<span class="vr-(label|sublabel|secnum)">.*?</span>', " ", s, flags=re.S)
    s = re.sub(r'<a href="#fnref[^"]*" class="footnote-backref">.*?</a>', " ", s)
    s = re.sub(r'<sup class="footnote-ref">.*?</sup>', " ", s)
    s = re.sub(r"<(td|th|li|p|div|h\d|figcaption|tr|br)[^>]*>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return [w for w in unify(s).split()]


def main():
    a, b = apply_corrections(tex_words()), page_words()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]
    for op, i1, i2, j1, j2 in diffs:
        ctx = " ".join(a[max(0, i1 - 6):i1])
        print(f"{op:8} …{ctx}\n   LaTeX: {' '.join(a[i1:i2])!r}\n   page:  {' '.join(b[j1:j2])!r}")
    tn = [LINK_CORRECTIONS.get(u.replace("\\%", "%"), u.replace("\\%", "%")) for u in notes]
    print(f"\nFootnotes: LaTeX {tn}\n           page  {page_notes}\n           {'same' if tn == page_notes else 'DIFFERENT'}")
    print(f"\n{len(a)} words in the LaTeX, {len(b)} on the page, {len(diffs)} differences")
    return 1 if diffs or tn != page_notes else 0


if __name__ == "__main__":
    sys.exit(main())
