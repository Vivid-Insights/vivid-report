"""Figure 1 and Figure 2 of the specimen: the toy normative model, as a still and as a video figure.

The normative model is the function `words()` below: it maps a z-score to a phrase using four
thresholds. The thresholds are choices, stated in the specimen's Method section, not estimates.

    cd Code && uv run python ../papers/0000-specimen/Code/fig_thresholds.py
"""

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Code"))   # the workspace's shared Code/
import viz_style as vs  # noqa: E402

vs.for_paper(__file__)

THRESHOLDS = [-2.0, -1.0, -0.5, 0.5, 1.0, 2.0]
PHRASES = ["far below average", "below average", "slightly below average", "average",
           "slightly above average", "above average", "far above average"]


def words(z: float) -> str:
    return PHRASES[int(np.searchsorted(THRESHOLDS, z, side="right"))]


def axes_for(ax, t):
    z = np.linspace(-3, 3, 601)
    dens = np.exp(-z ** 2 / 2) / np.sqrt(2 * np.pi)
    ax.plot(z, dens, color=vs.colour("primary"), lw=1.5)
    for c in THRESHOLDS:
        ax.axvline(c, color=t.neutral, lw=0.8, zorder=0)
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 0.46)
    ax.set_xlabel("z-score")
    ax.set_ylabel("Density")
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.xaxis.set_minor_locator(vs.plt.MultipleLocator(0.5))
    return z, dens


def still():
    for t in vs.themes():
        fig, ax = vs.figure()
        z, dens = axes_for(ax, t)
        mids = [-2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5]
        cdf = [0.0] + [0.5 * (1 + math.erf(c / math.sqrt(2))) for c in THRESHOLDS] + [1.0]
        shares = np.diff(cdf)  # share of a standard normal population in each band
        for m, s in zip(mids, shares):
            ax.text(m, 0.43, f"{100 * s:.0f}%", ha="center", va="top", fontsize=9, color=t.muted)
        vs.save(fig, "thresholds")


def frame(i, t, n=96):
    zpos = -2.8 + 5.6 * i / (n - 1)
    fig, ax = vs.figure(12, 8)
    z, dens = axes_for(ax, t)
    y = np.exp(-zpos ** 2 / 2) / np.sqrt(2 * np.pi)
    ax.plot([zpos], [y], "o", color=vs.colour("violet"), ms=7, zorder=5)
    ax.text(0, 0.445, f"z = {zpos:+.2f}:  “{words(zpos)}”", ha="center", va="top", fontsize=11, color=t.ink)
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    still()
    vs.save_video(frame, 96, "threshold-sweep", fps=16, poster_frame=60)
