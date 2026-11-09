"""Figure: the writing process — six phases, the steps in each, and what author and agent each do.

Drawn from `instructions.md` (`The Six Phases and the Ten Steps`). Review (step 9) and
publication (step 10) are left out: the report describes them separately.

    cd Code && uv run python ../papers/0001-what-is-a-vivid-report/Code/fig_writing_process.py
"""

import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Code"))
import viz_style as vs  # noqa: E402

vs.for_paper(__file__)

# (phase, steps, what the author does, what the agent does) — each from instructions.md
PHASES = [
    ("Sketch", "1",
     "Names the sources\nand who may\npublish them",
     "Searches folders,\nreads and records\nthe material"),
    ("Sketch the\nabstract", "2",
     "Chooses the three\npoints A, B and C;\nwrites the abstract",
     "Suggests points\nfrom the author's\nown text"),
    ("Revise", "3–5",
     "Names the papers;\nsays what each\nparagraph is for",
     "Drafts in\nReport.md; writes\nMethods from code"),
    ("Start and end\ntogether", "6",
     "Answers each\npoint in a\nsentence",
     "Drafts the\nDiscussion against\nthe Introduction"),
    ("Revise the\nabstract", "7",
     "Revises the\nabstract; chooses\nthe title",
     "Reads the abstract\nagainst the report;\nsuggests titles"),
    ("Simplify\nand revise", "8",
     "Decides what\nto cut and\nwhat to fix",
     "Reads it through;\nlists problems;\nruns the checks"),
]

W, H = 18, 9.8
GUTTER, RIGHT, GAP = 1.95, 0.25, 0.14
COL = (W - GUTTER - RIGHT - GAP * (len(PHASES) - 1)) / len(PHASES)
PAD = 0.17
WRAP = 16   # characters per line in a card
LANES = {"author": (3.05, 2.05), "agent": (0.75, 2.05)}   # bottom, height
RULE_Y = 5.5

for t in vs.themes():
    fig, ax = vs.diagram(W, H)
    xs = [GUTTER + i * (COL + GAP) for i in range(len(PHASES))]

    # lane labels in the gutter
    for lane, (word, verb) in {"author": ("Author", "decides\nand edits"),
                               "agent": ("Agent", "drafts\nand checks")}.items():
        y0, h = LANES[lane]
        vs.eyebrow(ax, 0.25, y0 + h - 0.45, word, colour_name="accent_text" if lane == "author" else "muted")
        ax.text(0.25, y0 + h - 0.7, verb, fontsize=7.5, color=t.muted, va="top", linespacing=1.3)

    # the timeline: a violet rule with a node at each phase
    ax.plot([xs[0] + PAD, xs[-1] + COL], [RULE_Y, RULE_Y], color=t.accent, lw=1.4, solid_capstyle="butt", zorder=2)
    for i, (phase, steps, author, agent) in enumerate(PHASES):
        x = xs[i]
        ax.scatter([x + PAD], [RULE_Y], s=22, color=t.accent, zorder=3, edgecolors=t.surface, linewidths=1.2)
        vs.display(ax, x + PAD - 0.04, 7.35, f"{i + 1:02d}", size=17, colour_name="accent_text", va="baseline")
        ax.text(x + PAD, 7.05, phase, fontsize=8.5, fontweight="semibold", color=t.ink, va="top", linespacing=1.15)
        vs.eyebrow(ax, x + PAD, 5.85, f"Step{'s' if '–' in steps else ''} {steps}", colour_name="muted", size=6.5)

        for lane, text, fill in (("author", author, "wash"), ("agent", agent, "panel")):
            y0, h = LANES[lane]
            vs.card(ax, x, y0, COL, h, fill=fill, radius=0.16)
            if lane == "author":   # a violet tick on the author's cards: the decisions are theirs
                vs.card(ax, x, y0 + h - 0.06, COL, 0.06, fill="accent", radius=0.0, zorder=2)
            ax.text(x + PAD, y0 + h - 0.3, textwrap.fill(text.replace("\n", " "), WRAP), fontsize=7, color=t.ink, va="top", linespacing=1.38, zorder=3)

    # the abstract, drafted in phase 2, is the template that phase 5 revises it against
    c2, c5 = xs[1] + COL / 2, xs[4] + COL / 2
    vs.arrow(ax, (c2, 7.95), (c5, 7.95), rad=-0.28, lw=1.1)
    ax.text((c2 + c5) / 2, 9.15, "the abstract is the template", ha="center", va="bottom",
            fontsize=7.5, style="italic", color=t.accent_text)

    vs.save(fig, "writing_process")
