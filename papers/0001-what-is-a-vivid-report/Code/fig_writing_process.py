"""Figure: the writing process — six phases, the steps in each, and what author and agent each do.

Drawn from `instructions.md` (`The Six Phases and the Eleven Steps`) and David's sketch of the
drafting order (`Writing workflow` keynote). In the revise phase the Methods and Results are written
point by point — A in step 3, B in step 4, C in step 5 — in rounds; the Introduction (step 6) and the
Discussion (step 7) are then written together. Review (step 10) and publication (step 11) are left
out: the report describes them separately.

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
    ("Revise", "3–5", 2.3,
     "Says what each point must show, writes first drafts and edits in place. "
     "Each point goes back and forth until it says what the author means.",
     "Writes the Methods from the code, proposes the examples, quotes outputs from their files "
     "and checks every draft against the code."),
    ("Start and end\ntogether", "6–7", 1.6,
     "Names the papers they know; answers each point in a sentence",
     "Finds and reads the sources; drafts the Discussion against the Introduction"),
    ("Revise the\nabstract", "8", 1,
     "Revises the abstract; chooses the title",
     "Reads the abstract against the report; suggests titles"),
    ("Simplify\nand revise", "9", 1,
     "Decides what to cut and what to fix",
     "Reads it through; lists problems; runs the checks"),
]
# the steps drawn inside a phase: (step, label)
INSET = {
    2: [("Step 3", "A\nMethods and\nResults"), ("Step 4", "B\nMethods and\nResults"), ("Step 5", "C\nMethods and\nResults")],
    3: [("Step 6", "Introduction"), ("Step 7", "Discussion")],
}

W, H = 22, 12.4
GUTTER, RIGHT, GAP = 1.95, 0.25, 0.14
UNIT = (W - GUTTER - RIGHT - GAP * (len(PHASES) - 1)) / sum(p[2] for p in PHASES)
PAD = 0.17
CHARS_PER_CM = 7.8          # Inter at 7 pt
LANES = {"author": (3.2, 2.35), "agent": (0.6, 2.35)}   # bottom, height
RULE_Y = 5.95
NUM_Y, NAME_Y, STEP_Y = 10.2, 9.9, 8.75
CHIP_Y, CHIP_H, CHIP_GAP = 7.05, 1.5, 0.3

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

        # the separate steps inside a phase, in the order they are written
        if i in INSET:
            chips = INSET[i]
            inner = w - 2 * PAD
            cw = (inner - CHIP_GAP * (len(chips) - 1)) / len(chips)
            centres = []
            for k, (step, label) in enumerate(chips):
                cx = x + PAD + k * (cw + CHIP_GAP)
                centres.append(cx + cw / 2)
                vs.card(ax, cx, CHIP_Y, cw, CHIP_H, fill="wash", edge="accent", radius=0.12, lw=0.7, zorder=2)
                vs.eyebrow(ax, cx + 0.12, CHIP_Y + CHIP_H - 0.26, step, colour_name="accent_text", size=5.5, zorder=3)
                head, _, rest = label.partition("\n")
                ax.text(cx + 0.12, CHIP_Y + CHIP_H - 0.38, head, fontsize=8 if rest else 6.8, fontweight="semibold",
                        color=t.ink, va="top", zorder=3)
                if rest:
                    ax.text(cx + 0.12, CHIP_Y + 0.12, rest, fontsize=6, color=t.muted, va="bottom",
                            linespacing=1.2, zorder=3)
                if k:
                    vs.arrow(ax, (cx - CHIP_GAP + 0.05, CHIP_Y + CHIP_H / 2), (cx - 0.05, CHIP_Y + CHIP_H / 2),
                             lw=0.9, head=6, zorder=4)
            if i == 2:   # each point is drafted and redrafted, in rounds
                vs.arrow(ax, (centres[-1], CHIP_Y - 0.02), (centres[0], CHIP_Y - 0.02), rad=-0.22, lw=0.9, head=6)
                ax.text((centres[0] + centres[-1]) / 2, CHIP_Y - 0.72, "in rounds, until each point says what the author means",
                        ha="center", va="center", fontsize=6.5, style="italic", color=t.accent_text, zorder=3)

    # the abstract, drafted in phase 2, is the template that phase 5 revises it against
    c2, c5 = xs[1] + ws[1] / 2, xs[4] + ws[4] / 2
    vs.arrow(ax, (c2, NUM_Y + 0.6), (c5, NUM_Y + 0.6), rad=-0.16, lw=1.1)
    ax.text((c2 + c5) / 2, H - 0.3, "the abstract is the template", ha="center", va="top",
            fontsize=7.5, style="italic", color=t.accent_text)

    vs.save(fig, "writing_process")
