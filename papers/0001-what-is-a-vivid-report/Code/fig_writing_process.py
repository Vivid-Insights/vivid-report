"""Figure: the writing process — six phases, the steps in each, and what author and agent each do.

Drawn from `instructions.md` (`The Six Phases and the Ten Steps`) and David's sketch of the drafting
order (`Writing workflow` keynote). The revise phase is drawn wider: in it the Introduction, Methods
and Results are drafted and redrafted, in rounds, for each of the points A, B and C. Review (step 9)
and publication (step 10) are left out: the report describes them separately.

    cd Code && uv run python ../papers/0001-what-is-a-vivid-report/Code/fig_writing_process.py
"""

import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Code"))
import viz_style as vs  # noqa: E402

vs.for_paper(__file__)

# (phase, steps, relative width, what the author does, what the agent does) — from instructions.md
PHASES = [
    ("Sketch", "1", 1,
     "Names the sources and who may publish them",
     "Searches folders, reads and records the material"),
    ("Sketch the\nabstract", "2", 1,
     "Chooses the three points A, B and C; writes the abstract",
     "Suggests points from the author's own text"),
    ("Revise", "3–5", 2.0,
     "Says what each paragraph is for, writes first drafts and edits in place. "
     "Each section goes back and forth until it says what the author means.",
     "Finds and reads the sources, drafts in Report.md, writes the Methods from the code "
     "and checks every draft against the code and the sources."),
    ("Start and end\ntogether", "6", 1,
     "Answers each point in a sentence",
     "Drafts the Discussion against the Introduction"),
    ("Revise the\nabstract", "7", 1,
     "Revises the abstract; chooses the title",
     "Reads the abstract against the report; suggests titles"),
    ("Simplify\nand revise", "8", 1,
     "Decides what to cut and what to fix",
     "Reads it through; lists problems; runs the checks"),
]
SECTIONS = ["Introduction", "Methods", "Results"]   # drafted in the revise phase, in this order

W, H = 20, 11.6
GUTTER, RIGHT, GAP = 1.95, 0.25, 0.14
UNIT = (W - GUTTER - RIGHT - GAP * (len(PHASES) - 1)) / sum(p[2] for p in PHASES)
PAD = 0.17
CHARS_PER_CM = 7.8          # Inter at 7 pt
LANES = {"author": (3.2, 2.35), "agent": (0.6, 2.35)}   # bottom, height
RULE_Y = 5.95
NUM_Y, NAME_Y, STEP_Y = 9.45, 9.15, 8.0

for t in vs.themes():
    fig, ax = vs.diagram(W, H)
    xs, ws, x = [], [], GUTTER
    for p in PHASES:
        xs.append(x); ws.append(p[2] * UNIT); x += p[2] * UNIT + GAP

    for lane, (word, verb) in {"author": ("Author", "decides\nand edits"),
                               "agent": ("Agent", "drafts\nand checks")}.items():
        y0, h = LANES[lane]
        vs.eyebrow(ax, 0.25, y0 + h - 0.45, word, colour_name="accent_text" if lane == "author" else "muted")
        ax.text(0.25, y0 + h - 0.7, verb, fontsize=7.5, color=t.muted, va="top", linespacing=1.3)

    ax.plot([xs[0] + PAD, xs[-1] + ws[-1]], [RULE_Y, RULE_Y], color=t.accent, lw=1.4, solid_capstyle="butt", zorder=2)
    for i, (phase, steps, _, author, agent) in enumerate(PHASES):
        x, w = xs[i], ws[i]
        ax.scatter([x + PAD], [RULE_Y], s=22, color=t.accent, zorder=3, edgecolors=t.surface, linewidths=1.2)
        vs.display(ax, x + PAD - 0.04, NUM_Y, f"{i + 1:02d}", size=17, colour_name="accent_text", va="baseline")
        ax.text(x + PAD, NAME_Y, phase, fontsize=8.5, fontweight="semibold", color=t.ink, va="top", linespacing=1.15)
        vs.eyebrow(ax, x + PAD, STEP_Y, f"Step{'s' if '–' in steps else ''} {steps}", colour_name="muted", size=6.5)

        wrap = int((w - 2 * PAD) * (CHARS_PER_CM if w < 3 else 8.2))
        for lane, text, fill in (("author", author, "wash"), ("agent", agent, "panel")):
            y0, h = LANES[lane]
            vs.card(ax, x, y0, w, h, fill=fill, radius=0.16)
            if lane == "author":   # a violet edge on the author's cards: the decisions are theirs
                vs.card(ax, x, y0 + h - 0.06, w, 0.06, fill="accent", radius=0.0, zorder=2)
            ax.text(x + PAD, y0 + h - 0.3, textwrap.fill(text, wrap), fontsize=7, color=t.ink,
                    va="top", linespacing=1.38, zorder=3)

    # inside the revise phase: Introduction -> Methods -> Results, and round again, for A, B and C
    i = 2
    x, w = xs[i] + PAD, ws[i] - 2 * PAD
    cgap, cy, ch = 0.32, 7.05, 0.5
    shares = [len(n) + 6 for n in SECTIONS]                     # wider box for a longer name
    cws = [(w - 2 * cgap) * sh / sum(shares) for sh in shares]
    cxs = [x + sum(cws[:k]) + k * cgap for k in range(3)]
    for k, name in enumerate(SECTIONS):
        cx, cw = cxs[k], cws[k]
        vs.card(ax, cx, cy, cw, ch, fill="wash", edge="accent", radius=0.12, lw=0.7, zorder=2)
        ax.text(cx + cw / 2, cy + ch / 2, name, ha="center", va="center", fontsize=7, color=t.ink, zorder=3)
        if k:
            vs.arrow(ax, (cx - cgap + 0.05, cy + ch / 2), (cx - 0.05, cy + ch / 2), lw=0.9, head=6)
    first, last = cxs[0] + cws[0] / 2, cxs[2] + cws[2] / 2
    vs.arrow(ax, (last, cy - 0.02), (first, cy - 0.02), rad=-0.3, lw=0.9, head=6)
    ax.text((first + last) / 2, cy - 0.78, "in rounds, for A, B and C", ha="center", va="center",
            fontsize=6.5, style="italic", color=t.accent_text, zorder=3)

    # the abstract, drafted in phase 2, is the template that phase 5 revises it against
    c2, c5 = xs[1] + ws[1] / 2, xs[4] + ws[4] / 2
    vs.arrow(ax, (c2, NUM_Y + 0.6), (c5, NUM_Y + 0.6), rad=-0.18, lw=1.1)
    ax.text((c2 + c5) / 2, H - 0.3, "the abstract is the template", ha="center", va="top",
            fontsize=7.5, style="italic", color=t.accent_text)

    vs.save(fig, "writing_process")
