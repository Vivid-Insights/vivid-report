"""Pre-routing safeguarding risk check (CONSTRAINT-1, flows[0]).

Runs on EVERY message before any routing. Deliberately over-triggers. The phrase
list lives in data/safeguarding_phrases.json and is a builder draft: the storyboard
leaves the real list as '[TBD: full phrase list, reviewed by the DSL]'.
"""
from __future__ import annotations

import re
from functools import lru_cache

from .content import load


@lru_cache(maxsize=1)
def _compiled():
    return [re.compile(p, re.IGNORECASE) for p in load().safeguarding_patterns]


_ILL_BE = re.compile(r"\bill (be|go|come|do|call|ask|bring)\b")


def normalise(message: str) -> str:
    m = message.lower().replace("’", "'")
    # texting shorthand: "ill be late" means "i'll be late", not illness (BUILD GUESS)
    m = _ILL_BE.sub(lambda x: "i'll " + x.group(1), m)
    return re.sub(r"\s+", " ", m)


def is_risk(message: str) -> bool:
    text = normalise(message)
    return any(p.search(text) for p in _compiled())
