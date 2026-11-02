"""Four screens of one conversation, as it moves between analysts.

Reads the four screenshots saved in Attachments/ and lays them out two by two, each
with the question that produced it and the analyst that answered. Nothing is drawn
by hand: re-run this after replacing a screenshot.

    cd Code && uv run python ../papers/0003-twelve-earpiece/Code/fig_conversation_walk.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Code"))

import matplotlib.pyplot as plt  # noqa: E402
import viz_style as vs  # noqa: E402
from PIL import Image  # noqa: E402

PAPER = vs.for_paper(__file__)

# The question asked, and the analyst that answered it. Taken from the screenshots.
PANELS = [
    ("1.png", "“Tell me about Vilma Koivisto in\nSwedish Damallsvenskan 2026.”", "Scout"),
    ("2.png", "“Could she play in WSL?”", "Transfer"),
    ("3.png", "“How would she fit in at Arsenal?”", "Transfer"),
    ("4.png", "“How has Arsenal’s season progressed?”", "Season"),
]


def main() -> int:
    for theme in vs.themes():
        fig, axes = plt.subplots(2, 2, figsize=(19/2.54, 12.4/2.54))
        for ax, (name, question, analyst) in zip(axes.flat, PANELS):
            img = Image.open(PAPER / "Attachments" / name).convert("RGB")
            ax.imshow(img)
            ax.set_xticks([])
            ax.set_yticks([])
            for side in ax.spines.values():
                side.set_visible(True)
                side.set_color(theme.grid)
                side.set_linewidth(0.6)
            ax.set_title(f"{question}\n{analyst}", fontsize=8, color=theme.ink,
                         linespacing=1.5, pad=6)
        vs.save(fig, "fig_conversation_walk")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
