"""Figure conventions shared by every figure and video figure in the report.

The Vivid Insights figure design: striking but serious. It takes its colours and type from the
Vivid Insights profile and report site (`site/assets/vivid-report.css`), and David's publication
rules for everything else.

Colour. One accent, Vivid violet (#8B5CF6), for the thing a figure is about; everything else in ink,
greys and a pale violet wash. Data series take the categorical palette below, violet first, then
amber, teal, rose, slate and sky, each held by a variable rather than a rank. Never plain black: ink
is a violet-tinted near-black. Never more than one saturated colour where one will do.

Type. Inter for all text (11 pt, legend 10 pt), Space Grotesk for display text (titles in diagrams,
big numerals), IBM Plex Mono in capitals for small labels ("eyebrows": AUTHOR, STEP 3). The fonts
are in `Code/fonts/` under the SIL Open Font License, so every machine draws the same figure.

Form. 10 cm x 8 cm for a chart, wider for a diagram (`width=wide` in the figure block); no top or
right spine, no frame on the legend, no gridlines unless they carry reading; 300 dpi. A diagram is
drawn in centimetres with `vs.diagram()`, from cards (`vs.card`), eyebrow labels (`vs.eyebrow`) and
arrows (`vs.arrow`): flat fills, rounded corners, hairline rules, no shadows, gradients or 3-D.

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
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

CODE_DIR = Path(__file__).resolve().parent
FIGURES = CODE_DIR / "outputs" / "figures"
VIDEOS = CODE_DIR / "outputs" / "videos"
CM = 1 / 2.54
DPI = 300
SIZE = (10 * CM, 8 * CM)

for _f in sorted((CODE_DIR / "fonts").glob("*.ttf")):
    font_manager.fontManager.addfont(str(_f))
BODY = "Inter"
DISPLAY = "Space Grotesk"
MONO = "IBM Plex Mono"

# Colours are assigned to a variable, not to a rank: once a variable has a colour it keeps it in
# every figure of the report. Neutral grey is for "other" and residual terms.
PALETTE = {
    "primary": "#8B5CF6",    # Vivid violet: the thing the figure is about
    "secondary": "#D9821E",  # amber, the complement of violet
    "tertiary": "#138F80",   # teal
    "quaternary": "#D23F6A", # rose
    "fifth": "#5B6478",      # slate
    "sixth": "#3B82C4",      # sky
    "violet": "#8B5CF6",     # kept as a name: the brand accent
}
DARK_PALETTE = {  # the same hues, lifted so they hold contrast on the dark surface
    "primary": "#A78BFA", "secondary": "#F2A54A", "tertiary": "#3CC4AE", "quaternary": "#F07A98",
    "fifth": "#9AA3B5", "sixth": "#7DB4E8", "violet": "#A78BFA",
}


@dataclass(frozen=True)
class Theme:
    name: str
    surface: str      # the page
    ink: str          # text and axes; never plain black
    muted: str        # secondary text
    grid: str         # hairline rules
    neutral: str      # "other"
    palette: dict
    panel: str        # a quiet card on the page
    wash: str         # the accent's pale fill
    accent: str       # Vivid violet, as fill or line
    accent_text: str  # violet dark (light theme) or light (dark theme) enough to read as text
    on_accent: str    # text set on a violet fill


LIGHT = Theme("light", "#FDFDFB", "#1E1B2E", "#5E5F73", "#DDDBE6", "#A3A6B0", PALETTE,
              "#F3F2F7", "#EEE8FE", "#8B5CF6", "#6D28D9", "#FFFFFF")
DARK = Theme("dark", "#15151A", "#ECECF1", "#A3A4B3", "#34343F", "#6C6F7D", DARK_PALETTE,
             "#1F1F27", "#272040", "#8B5CF6", "#C4B5FD", "#FFFFFF")
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
    if name in ("panel", "wash", "accent", "accent_text", "on_accent", "ink", "muted", "grid", "surface"):
        return getattr(_active, name)
    return _active.palette[name]


def use(name: str) -> Theme:
    global _active
    t = {"light": LIGHT, "dark": DARK}[name]
    _active = t
    mpl.rcParams.update({
        "figure.dpi": 100, "savefig.dpi": DPI,
        "figure.facecolor": t.surface, "axes.facecolor": t.surface,
        "savefig.facecolor": t.surface, "savefig.transparent": False,
        "font.family": "sans-serif", "font.sans-serif": [BODY, "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 11, "axes.titlesize": 11, "axes.labelsize": 11,
        "axes.titleweight": "semibold", "axes.titlelocation": "left",
        "xtick.labelsize": 11, "ytick.labelsize": 11, "legend.fontsize": 10,
        "legend.frameon": False, "legend.loc": "lower left",
        "text.color": t.ink, "axes.labelcolor": t.ink, "axes.edgecolor": t.muted,
        "xtick.color": t.muted, "ytick.color": t.muted, "xtick.labelcolor": t.ink, "ytick.labelcolor": t.ink,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.8, "lines.linewidth": 1.8, "lines.solid_capstyle": "round",
        "axes.prop_cycle": mpl.cycler(color=[t.palette[k] for k in ("primary", "secondary", "tertiary", "quaternary", "fifth", "sixth")]),
        "axes.grid": False, "grid.color": t.grid, "grid.linewidth": 0.6,
    })
    return t


# ---- diagrams: drawn in centimetres, from cards, eyebrows and arrows ----------------------------

def diagram(width_cm: float, height_cm: float):
    """A blank canvas measured in centimetres from the bottom left, for a method or process diagram."""
    fig = plt.figure(figsize=(width_cm * CM, height_cm * CM))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, width_cm)
    ax.set_ylim(0, height_cm)
    ax.axis("off")
    fig._vivid_diagram = True  # save() leaves its layout alone
    return fig, ax


def card(ax, x: float, y: float, w: float, h: float, fill: str = "panel", edge: str | None = None,
         radius: float = 0.18, lw: float = 0.8, zorder: float = 1):
    """A flat rounded rectangle. `fill` and `edge` are colour names (`panel`, `wash`, `accent`, …) or hex."""
    def c(v):
        return "none" if v is None else (v if v.startswith("#") or v == "none" else colour(v))
    patch = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
                           fc=c(fill), ec=c(edge), lw=lw if edge else 0, zorder=zorder)
    ax.add_patch(patch)
    return patch


def eyebrow(ax, x: float, y: float, text: str, colour_name: str = "accent_text", size: float = 7.5, **kw):
    """A small label in IBM Plex Mono capitals, spaced out: AUTHOR, STEP 3."""
    spaced = "\u2009".join(text.upper())
    kw.setdefault("va", "baseline")
    return ax.text(x, y, spaced, fontfamily=MONO, fontsize=size, fontweight="medium",
                   color=colour(colour_name), **kw)


def display(ax, x: float, y: float, text: str, size: float = 12, colour_name: str = "ink", **kw):
    """Display text in Space Grotesk: diagram titles and large numerals."""
    kw.setdefault("fontweight", "bold")
    return ax.text(x, y, text, fontfamily=DISPLAY, fontsize=size, color=colour(colour_name), **kw)


def arrow(ax, start, end, colour_name: str = "accent", rad: float = 0.0, lw: float = 1.2, head: float = 8,
          zorder: float = 3, **kw):
    """A thin arrow with a small solid head; `rad` bends it (negative bends it upward, left to right)."""
    a = FancyArrowPatch(start, end, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                        mutation_scale=head, color=colour(colour_name), lw=lw, zorder=zorder,
                        shrinkA=0, shrinkB=0, **kw)
    ax.add_patch(a)
    return a


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
    if not getattr(fig, "_vivid_diagram", False):
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
