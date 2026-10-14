"""The architecture diagrams of paper 0002, drawn in the report's style.

    cd Code && uv run python ../papers/0002-twelve-earpiece/Code/diagrams.py

Draws the paper's diagrams as SVG in the colours of `Code/viz_style.py`. They began as redrawings
of the course diagrams (section 6 of context-engineering) and the stateless-chat diagram of the
authors' earlier draft, and were then corrected against the Earpiece code (see the architecture
report): function names, context fields and the analysts are as the code has them, and the
identifiers are the examples the code's own schemas give. a light version in
`outputs/figures/` and a dark one in `outputs/figures/dark/`, which the page swaps with the
reader's theme. Figure 5, a screenshot of the product, is used as it is.
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "Code"))
import viz_style as vs  # noqa: E402

OUT = Path(__file__).resolve().parent / "outputs" / "figures"
SANS = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'IBM Plex Mono', Menlo, Consolas, monospace"


class Canvas:
    def __init__(self, w: int, h: int, theme: vs.Theme):
        self.w, self.h, self.t = w, h, theme
        dark = theme.name == "dark"
        self.ink = theme.ink
        self.muted = theme.muted
        self.line = "#6C6F7D" if dark else "#9A9DAA"
        self.box_fill = "#1D1D24" if dark else "#FFFFFF"
        self.panel = "#22222B" if dark else "#F4F3F8"
        self.accent = theme.palette["violet"]
        self.parts: list[str] = []

    def rect(self, x, y, w, h, fill, stroke=None, r=10, width=1.4):
        s = f' stroke="{stroke}" stroke-width="{width}"' if stroke else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{s}/>')

    def text_block(self, cx, cy, lines, size=17, weight=500, family=SANS, fill=None, anchor="middle", lh=1.3):
        fill = fill or self.ink
        total = (len(lines) - 1) * size * lh
        y0 = cy - total / 2
        for i, line in enumerate(lines):
            self.parts.append(
                f'<text x="{cx}" y="{y0 + i * size * lh:.1f}" font-family="{family}" font-size="{size}" '
                f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" dominant-baseline="central">{escape(line)}</text>')

    def box(self, x, y, w, h, lines, size=17, accent=False):
        self.rect(x, y, w, h, self.box_fill, self.accent if accent else self.line, width=2 if accent else 1.4)
        self.text_block(x + w / 2, y + h / 2, lines, size=size)

    def code(self, x, y, w, h, title, lines, size=12.5):
        """A code panel. Each line is (text, highlighted)."""
        self.rect(x, y, w, h, self.panel, self.line, r=8, width=1)
        ty = y + 22
        if title:
            self.parts.append(f'<text x="{x + 14}" y="{ty}" font-family="{SANS}" font-size="11" letter-spacing="0.08em" '
                              f'font-weight="600" fill="{self.muted}">{escape(title.upper())}</text>')
            ty += 22
        for i, (line, hi) in enumerate(lines):
            self.parts.append(
                f'<text x="{x + 14}" y="{ty + i * size * 1.42:.1f}" font-family="{MONO}" font-size="{size}" '
                f'fill="{self.accent if hi else self.ink}" xml:space="preserve">{escape(line)}</text>')

    def arrow(self, x1, y1, x2, y2, both=False):
        start = ' marker-start="url(#head)"' if both else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{self.accent}" stroke-width="2"'
                          f'{start} marker-end="url(#head)"/>')

    def svg(self) -> str:
        defs = (f'<defs><marker id="head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{self.accent}"/></marker></defs>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}">'
                f'{defs}<rect width="100%" height="100%" fill="{self.t.surface}"/>' + "".join(self.parts) + "</svg>\n")


def stateless(t):
    """The application keeps the state: every turn, the whole chat goes to the LLM again."""
    c = Canvas(960, 330, t)
    c.box(20, 40, 150, 260, ["Client"], size=19)
    c.box(370, 40, 170, 130, ["Earpiece API"], size=18, accent=True)
    c.box(370, 220, 170, 80, ["Database of", "chats"], size=16)
    c.box(790, 40, 150, 260, ["LLM API"], size=19)
    c.arrow(178, 70, 362, 70)
    c.text_block(270, 56, ["chat id, new message"], size=12.5, weight=500, family=MONO, fill=c.muted)
    c.arrow(362, 150, 178, 150)
    c.text_block(270, 136, ["the reply"], size=12.5, weight=500, family=MONO, fill=c.muted)
    c.arrow(440, 178, 440, 212)
    c.arrow(470, 212, 470, 178)
    c.arrow(548, 70, 782, 70)
    c.text_block(665, 56, ["the whole chat, every turn"], size=12.5, weight=500, family=MONO, fill=c.muted)
    c.arrow(782, 150, 548, 150)
    c.text_block(665, 136, ["the next message"], size=12.5, weight=500, family=MONO, fill=c.muted)
    c.code(560, 190, 220, 112, "", [
        ("[ system: instructions,", False), ("  user: ...,", False), ("  assistant: ...,", False),
        ("  tool: ...,", False), ("  user: the new message ]", True)], size=12)
    return c.svg()


def context_switch(t):
    c = Canvas(960, 440, t)
    steps = [["The user names", "a player"],
             ["The model calls a", "redirect function"],
             ["A new chat with the", "Scout, in a resolved", "player context"]]
    for i, lines in enumerate(steps):
        c.box(35 + i * 320, 20, 250, 110, lines, accent=(i == 1))
    for i in range(2):
        c.arrow(295 + i * 320, 75, 345 + i * 320, 75)
    c.code(15, 160, 290, 260, "Messages", [
        ("{", False), ('  "role": "system",', False), ('  "content": "... If the user', True),
        ("    names a player, call", True), ('    redirect_to_scout ..."', True), ("}", False),
        ("{", False), ('  "role": "user",', False), ('  "content": "Tell me about', False),
        ('    Jude Bellingham"', False), ("}", False)])
    c.code(335, 160, 290, 260, "Tool call", [
        ("{", False), ('  "role": "assistant",', False), ('  "tool_calls": [{', False),
        ('    "type": "function",', False), ('    "function": {', False),
        ('      "name": "redirect_to_scout",', False), ('      "arguments": {', False),
        ('        "player": {', True), ('          "name":', True), ('          "Jude Bellingham",', True),
        ("          ... }, ... }}}]", False), ("}", False)], size=12)
    c.code(655, 160, 290, 260, "PlayerEvaluationContext", [
        ("{", False), ('  "player": {', False), ('    "id": 379209,', False), ('    "position":', False),
        ('      "MIDFIELDER"', False), ("  },", False), ('  "competition": {', False), ('    "id": 364,', False),
        ('    "year": 2023', False), ("  }", False), ("}", False)])
    return c.svg()


def receptionist(t):
    c = Canvas(960, 470, t)
    c.box(380, 185, 200, 100, ["Receptionist"], size=19, accent=True)
    c.box(20, 20, 300, 110, ["A player", "Scout · Comparison", "Transfer · Team Fit"], size=16)
    c.box(640, 20, 300, 110, ["A match", "Match Analyst · Match Scout"], size=16)
    c.box(20, 340, 300, 110, ["A search for players", "Talent Discovery or Search"], size=16)
    c.box(390, 360, 180, 90, ["A season", "Season Analyst"], size=16)
    c.box(640, 340, 300, 110, ["An opponent", "Opposition Analyst"], size=16)
    c.arrow(325, 110, 372, 190, both=True)
    c.arrow(635, 110, 588, 190, both=True)
    c.arrow(325, 360, 372, 280, both=True)
    c.arrow(480, 293, 480, 352, both=True)
    c.arrow(635, 360, 588, 280, both=True)
    c.parts.append(f'<line x1="170" y1="140" x2="170" y2="330" stroke="{c.muted}" stroke-width="1.6" '
                   f'stroke-dasharray="5 5" marker-start="url(#head)" marker-end="url(#head)"/>')
    c.text_block(182, 235, ["direct"], size=12.5, weight=500, fill=c.muted, anchor="start")
    return c.svg()


def resolve_names(t):
    c = Canvas(960, 140, t)
    steps = [["The model gives", "the name as text"], ["Full-text search:", "up to 20", "candidates"],
             ["The model picks one,", "or none if unsure"], ["Context set, or", "the user is asked"]]
    for i, lines in enumerate(steps):
        c.box(10 + i * 250, 15, 190, 110, lines, size=16, accent=(i == 2))
    for i in range(3):
        c.arrow(206 + i * 250, 70, 254 + i * 250, 70)
    return c.svg()


def contexts(t):
    c = Canvas(960, 450, t)
    rows = [("Player", "PlayerEvaluationContext", ['  "player": {"id": 379209},', '  "competition": {"id": 364,', '                  "year": 2023}']),
            ("Match", "MatchEvaluationContext", ['  "match": {"id": 5465139,', '    "focal_team": {"id": 1611}},', '  "competition": {...}']),
            ("Team", "SeasonEvaluationContext", ['  "team": {"id": 1611},', '  "competition": {"id": 364,', '                  "year": 2023}'])]
    for i, (what, name, fields) in enumerate(rows):
        y = 15 + i * 145
        c.text_block(30, y + 66, [f"We're talking about a {what}"], size=22, weight=500, anchor="start")
        c.arrow(410, y + 66, 540, y + 66)
        lines = [("{", False)] + [(f, False) for f in fields] + [("}", False)]
        c.code(560, y, 380, 132, name, lines)
    return c.svg()



def prompt_structure(t):
    """The four steps of Caut and colleagues, as the transfer function's prompt builds them.

    Counts and wording are read from the saved call in outputs/function-examples/transfer-1.json.
    """
    import json
    call = json.loads((Path(__file__).resolve().parent / "outputs" / "function-examples"
                       / "transfer-1.json").read_text())["model_calls"][1]
    msgs = call["messages"]
    qa = sum(1 for m in msgs[1:59] if m["role"] == "user")
    shots = sum(1 for m in msgs[60:92] if m["role"] == "user")

    c = Canvas(960, 560, t)
    rows = [
        ("Tell it who it is", f"system message", "You are the Twelve Earpiece Scout\nanalyst. Your job is going to be\nto give a concise, 4 sentence\nsummary of a midfielder's\ntransfer potential.", False),
        ("Tell it what it knows", f"{qa} question-answer pairs", "user: What are the metric which\n  measure if a midfielder has\n  box threat?\nassistant: The key to a midfielder\n  having high box threat is ...", False),
        ("Tell it how to answer", f"system message, then {shots} pairs", "user: <synthetic text for\n  another player>\nassistant: Moving to the\n  Premiership from the 1. HNL,\n  21-year-old Baturina ...", False),
        ("Tell it what data to use", "the final user message", "Vilma Koivisto is a unknown footed\n23-year-old midfielder ... playing\nfor Hammarby in the Damallsvenskan.\nLet's consider a move from the\nSwedish Damallsvenskan to the ...", True),
    ]
    for i, (step, what, body, accent) in enumerate(rows):
        y = 12 + i * 136
        c.rect(14, y, 300, 118, c.box_fill, c.accent if accent else c.line, width=2 if accent else 1.4)
        c.text_block(32, y + 40, [step], size=18, weight=600, anchor="start")
        c.text_block(32, y + 72, [what], size=13, weight=500, family=MONO, fill=c.muted, anchor="start")
        c.arrow(322, y + 59, 368, y + 59)
        c.code(384, y, 562, 118, "", [(ln, accent) for ln in body.split("\n")], size=12)
    return c.svg()

FIGURES = {"diagram_stateless": stateless, "diagram_context_switch": context_switch, "diagram_receptionist": receptionist,
           "diagram_resolve_names": resolve_names, "diagram_contexts": contexts,
           "diagram_prompt_structure": prompt_structure}

if __name__ == "__main__":
    for theme_name in ("light", "dark"):
        theme = vs.use(theme_name)
        out = OUT if theme_name == "light" else OUT / "dark"
        out.mkdir(parents=True, exist_ok=True)
        for name, draw in FIGURES.items():
            (out / f"{name}.svg").write_text(draw(theme), encoding="utf-8")
            print(f"  figure: {(out / f'{name}.svg').relative_to(OUT.parents[3])}")
    vs.use("light")
