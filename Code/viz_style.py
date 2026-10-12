"""Figure conventions shared by every figure and video figure in the report.

David's publication style: 10 cm x 8 cm, all text 11 pt (legend 10 pt), legend without a frame,
top and right spines removed, the steel-blue-first palette below, never plain black, 300 dpi.

Every figure is saved twice, opaque, in `outputs/figures/` (light, the paper) and
`outputs/figures/dark/` (the Vivid Insights dark theme). The report page shows whichever matches the
reader's theme, so a figure never shows dark ink on a dark page. The build reads the PNG's size and
resolution and shows it so that its 11 pt text comes out the same size as the body text.

    import viz_style as vs
    for theme in vs.themes():
        fig, ax = vs.figure()
        ax.plot(x, y, color=vs.colour("primary"))
        vs.save(fig, "my_figure")

Video figures: `vs.save_video(frames_fn, n_frames, "name", fps=24)` renders an mp4 for each theme
with the ffmpeg bundled by imageio-ffmpeg, plus a poster PNG.

A figure script lives in its paper's `Code/` folder and starts with `vs.for_paper(__file__)`, so its
figures and videos go to that paper's `Code/outputs/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CODE_DIR = Path(__file__).resolve().parent
FIGURES = CODE_DIR / "outputs" / "figures"
VIDEOS = CODE_DIR / "outputs" / "videos"
CM = 1 / 2.54
DPI = 300
SIZE = (10 * CM, 8 * CM)

# Colours are assigned to a variable, not to a rank: once a variable has a colour it keeps it in
# every figure of the report. Neutral grey is for "other" and residual terms.
PALETTE = {
    "primary": "#4E79A7",    # steel blue — replaces black
    "secondary": "#E15759",  # muted coral
    "tertiary": "#59A14F",   # sage green
    "quaternary": "#9B6BB5", # soft purple
    "fifth": "#F28E2B",      # warm amber
    "sixth": "#76B7B2",      # soft teal
    "violet": "#8B5CF6",     # Vivid Insights brand accent, for the one thing a figure is about
}
DARK_PALETTE = {  # the same hues, lifted so they hold contrast on the dark surface
    "primary": "#7FA6D3", "secondary": "#F07F81", "tertiary": "#7FC476", "quaternary": "#BE93D6",
    "fifth": "#F7A95C", "sixth": "#93D0CB", "violet": "#A78BFA",
}


@dataclass(frozen=True)
class Theme:
    name: str
    surface: str
    ink: str
    muted: str
    grid: str
    neutral: str
    palette: dict


LIGHT = Theme("light", "#FDFDFB", "#2F3E50", "#5C6270", "#E4E4EA", "#A3A6B0", PALETTE)
DARK = Theme("dark", "#15151A", "#E6E8EF", "#A3A6B5", "#2A2A33", "#6C6F7D", DARK_PALETTE)
_active = LIGHT


def for_paper(script: str) -> Path:
    """Send this script's figures and videos to its own paper's Code/outputs/. Returns the paper folder."""
    global FIGURES, VIDEOS
    code = Path(script).resolve().parent
    FIGURES, VIDEOS = code / "outputs" / "figures", code / "outputs" / "videos"
    return code.parent


def theme() -> Theme:
    return _active


def colour(name: str) -> str:
    if name in ("neutral", "grey", "other"):
        return _active.neutral
    return _active.palette[name]


def use(name: str) -> Theme:
    global _active
    t = {"light": LIGHT, "dark": DARK}[name]
    _active = t
    mpl.rcParams.update({
        "figure.dpi": 100, "savefig.dpi": DPI,
        "figure.facecolor": t.surface, "axes.facecolor": t.surface,
        "savefig.facecolor": t.surface, "savefig.transparent": False,
        "font.family": "sans-serif", "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 11, "axes.titlesize": 11, "axes.labelsize": 11,
        "xtick.labelsize": 11, "ytick.labelsize": 11, "legend.fontsize": 10,
        "legend.frameon": False, "legend.loc": "lower left",
        "text.color": t.ink, "axes.labelcolor": t.ink, "axes.edgecolor": t.ink,
        "xtick.color": t.ink, "ytick.color": t.ink,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.8, "lines.linewidth": 1.5,
        "axes.prop_cycle": mpl.cycler(color=[t.palette[k] for k in ("primary", "secondary", "tertiary", "quaternary", "fifth", "sixth")]),
        "axes.grid": False,
    })
    return t


def themes() -> Iterator[Theme]:
    """Loop over both themes: the figure code runs once per theme."""
    for name in ("light", "dark"):
        yield use(name)
    use("light")


def figure(width_cm: float = 10, height_cm: float | None = None, **kw):
    h = height_cm if height_cm is not None else width_cm * 0.8
    return plt.subplots(figsize=(width_cm * CM, h * CM), **kw)


def _show(path: Path) -> str:
    try:
        return str(path.relative_to(CODE_DIR.parent))
    except ValueError:
        return str(path)


def save(fig, name: str) -> Path:
    out = FIGURES if _active.name == "light" else FIGURES / "dark"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=DPI, facecolor=_active.surface)  # no bbox_inches="tight": the size stays what was asked for
    plt.close(fig)
    print(f"  figure: {_show(path)}")
    return path


def save_video(draw: Callable[[int, Theme], "plt.Figure"], n_frames: int, name: str, fps: int = 24,
               poster_frame: int | None = None, dpi: int = 160) -> list[Path]:
    """Render a video figure in both themes.

    `draw(i, theme)` returns a matplotlib figure for frame i. Each theme gives `outputs/videos/<name>.mp4`
    (light) or `outputs/videos/dark/<name>.mp4`, and a poster PNG beside it, shown before the video plays
    and when the report is printed.
    """
    import imageio.v2 as imageio
    import numpy as np

    written = []
    for t in themes():
        out = VIDEOS if t.name == "light" else VIDEOS / "dark"
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"{name}.mp4"
        writer = imageio.get_writer(path, fps=fps, codec="libx264", quality=8, pixelformat="yuv420p", macro_block_size=16)
        poster_at = n_frames - 1 if poster_frame is None else poster_frame
        for i in range(n_frames):
            fig = draw(i, t)
            fig.set_dpi(dpi)
            fig.canvas.draw()
            frame = np.asarray(fig.canvas.buffer_rgba())[..., :3]
            h, w = frame.shape[0] // 16 * 16, frame.shape[1] // 16 * 16
            writer.append_data(frame[:h, :w])
            if i == poster_at:
                fig.savefig(out / f"{name}-poster.png", dpi=dpi, facecolor=t.surface)
            plt.close(fig)
        writer.close()
        print(f"  video:  {_show(path)}")
        written.append(path)
    return written
