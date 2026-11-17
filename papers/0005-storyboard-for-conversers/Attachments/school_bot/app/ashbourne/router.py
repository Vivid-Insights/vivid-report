"""Classifies a message into a flow (and, for process questions, an area + stage).

Order (flows[*].steps 'Safeguarding risk check' runs first in every flow):
  1 safeguarding override          (flows[0])
  2 greeting                       (BUILD GUESS: storyboard has no greeting flow)
  3 out-of-scope: records / schoolwork (RedirectOutOfScope)
  4 acting on someone's behalf     (redirect + the self-service steps for the inner topic)
  5 medical-advice question        (CONSTRAINT-8)
  6 reassurance push inside an area (CONSTRAINT-4)
  7 WhoToContact, GetOpeningHours
  8 process areas (OpenProcessArea) vs ExplainSchoolRule / FindSupport
  9 follow-up inside the remembered area
 10 catch-all
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache

from .content import load
from .safeguarding import is_risk, normalise

# Order in which stages are tested: the first stage whose cue matches wins.
# BUILD GUESS: the storyboard describes stages but not how to tell them apart in text.
STAGE_PRIORITY = {
    "Processes · Subject choices": ["After the cut-off", "Change window", "Choosing"],
    "Processes · Exams": ["After results", "Exam season", "Before entries close"],
    "Processes · Absence & leave": ["Term-time leave request", "Planned appointment", "Unplanned absence"],
    "Processes · Joining the school": ["Just joined", "Applying"],
}

FOLLOW_UP_CUE = re.compile(
    r"^(what if|and|but|what about|how about|ok|okay|so|also|what happens|what do|does|do i|do we|"
    r"can i|can we|is it|is that|how long|how do|when|where|who decides|and if|what else|then|"
    r"what counts|how much|is there|are there|will i|would i)\b"
)


@dataclass
class Route:
    kind: str
    area: str | None = None
    stage: str | None = None
    inner: "Route | None" = None
    target: dict | None = None
    matches: list = field(default_factory=list)


@lru_cache(maxsize=None)
def _rx(pattern: str):
    return re.compile(pattern, re.IGNORECASE)


def _any(patterns, text) -> bool:
    return any(_rx(p).search(text) for p in patterns)


def _count(patterns, text) -> int:
    return sum(1 for p in patterns if _rx(p).search(text))


def _kw(keyword: str) -> str:
    # bare words become whole-word regexes; anything with regex syntax is used as-is
    if re.fullmatch(r"[a-z0-9 '\-]+", keyword):
        return rf"\b{re.escape(keyword)}\b"
    return keyword


def area_scores(text: str) -> dict[str, int]:
    r = load().routing["areas"]
    return {name: _count([_kw(k) for k in spec["keywords"]], text) for name, spec in r.items()}


def classify_stage(area: str, text: str, remembered: str | None = None) -> str:
    stages = load().routing["areas"][area]["stages"]
    for stage in STAGE_PRIORITY[area]:
        if _any([_kw(k) for k in stages[stage]], text):
            return stage
    if remembered:
        return remembered
    return load().area(area)["stages"][0]["name"]


def _match_entry(entries, text):
    best, best_n = None, 0
    for e in entries:
        n = _count([_kw(k) for k in e["keywords"]], text)
        if n > best_n:
            best, best_n = e, n
    return best


def classify(message: str, current_area: str | None = None, current_stage: str | None = None,
             allow_redirects: bool = True) -> Route:
    r = load().routing
    text = normalise(message)

    if is_risk(message):
        return Route("safeguarding")
    if _any(r["greeting"], text):
        return Route("greeting")

    if allow_redirects:
        if _any(r["records"], text):
            return Route("redirect_records")
        if _any(r["schoolwork"], text):
            return Route("redirect_schoolwork")
        if _any(r["actingOnBehalf"], text) and not _rx(r["actingOnBehalfSubjectGuard"]).search(text):
            inner = classify(message, current_area, current_stage, allow_redirects=False)
            if inner.kind in ("catch_all", "greeting"):
                inner = None
            return Route("redirect_acting", inner=inner)

    if _any(r["medical"], text):
        stage = "Unplanned absence"
        return Route("medical", area="Processes · Absence & leave", stage=stage)

    if current_area and _any(r["reassurance"], text):
        return Route("reassurance", area=current_area, stage=current_stage)

    if _any(r["whoToContact"], text):
        return Route("who_to_contact", target=_match_entry(load().role_contacts, text))
    if _any(r["openingHours"], text):
        return Route("opening_hours", target=_match_entry(load().opening_hours, text))

    scores = area_scores(text)
    best_area = max(scores, key=lambda k: scores[k])
    best = scores[best_area]
    # prefer the remembered area on ties (resume where the user left off)
    if current_area and scores.get(current_area, 0) == best and best > 0:
        best_area = current_area

    rule = _any(r["schoolRule"], text)
    support = _any(r["findSupport"], text)

    if best >= 2 or (best >= 1 and not (rule or support)):
        stage = classify_stage(best_area, text, current_stage if best_area == current_area else None)
        return Route("area", area=best_area, stage=stage)
    if support:
        return Route("find_support", target=_match_entry(load().resources, text))
    if rule:
        return Route("school_rule", target=_match_entry(load().policies, text))
    if current_area and FOLLOW_UP_CUE.search(text):
        return Route("area", area=current_area, stage=classify_stage(current_area, text, current_stage))
    return Route("catch_all")


def audience_hint(message: str) -> str | None:
    text = normalise(message)
    r = load().routing
    if _any(r["sixthFormHints"], text):
        return "sixth_form"
    if _any(r["lowerSchoolHints"], text):
        return "years_7_11"
    return None


def speaker_hint(message: str) -> str | None:
    text = normalise(message)
    if re.search(r"\bmy (son|daughter|child|kid|boy|girl)\b|\b(he|she)('?s| is| has| won'?t)\b|\btake (him|her) out\b", text):
        return "parent"
    if re.search(r"\b(i|i'?m|im|me|my)\b", text):
        return "student_or_unknown"
    return None
