"""OFFLINE writer: composes replies only from data files (facets, fixed texts,
reference lists, few-shot rows). No text is generated beyond joining these pieces.
"""
from __future__ import annotations

import re

from .content import load
from .safeguarding import normalise

STOPWORDS = set("""a an the i im i'm me my we our you your he she him her his they them it its is are was be
do does did can could will would should what when where who how why which if and or but so to of in on at
for with about from this that there here have has had get got any some not no yes ok okay just really
please want need tell know school ashbourne may might""".split())

# BUILD GUESS: tiny synonym map so paraphrases reach the right facet.
SYNONYMS = {
    "swap": "change", "switch": "change", "swapping": "change", "changing": "change",
    "dropping": "drop", "quit": "drop", "pick": "choose", "picking": "choose", "choosing": "choose",
    "ill": "illness", "sick": "illness", "unwell": "illness", "temperature": "illness",
    "off": "absence", "absent": "absence", "remark": "re-marked", "re-mark": "re-marked",
    "holiday": "leave", "trip": "leave", "days": "several", "results": "results",
    "dentist": "appointment", "doctor": "appointment", "late": "late", "login": "login",
    "password": "login", "extra": "extra", "mock": "mocks", "deadline": "cut-off", "cutoff": "cut-off",
}


def tokens(text: str) -> set[str]:
    out = set()
    for w in re.findall(r"[a-z0-9][a-z0-9'\-]*", normalise(text)):
        w = SYNONYMS.get(w, w)
        if w in STOPWORDS or len(w) < 3:
            continue
        out.add(w.rstrip("s") if len(w) > 4 else w)
    return out


def few_shot_match(message: str, flow: str | None = None):
    """Near-exact match against a few-shot row (Jaccard >= 0.75)."""
    m = tokens(message)
    if not m:
        return None
    best, best_j = None, 0.0
    for row in load().few_shot:
        if flow and row["flow"] != flow:
            continue
        t = tokens(row["user_message"])
        j = len(m & t) / len(m | t) if (m | t) else 0
        if j > best_j:
            best, best_j = row, j
    return best if best_j >= 0.75 else None


def select_facets(area: dict, stage: str, message: str, covered: list[str], forced: str | None = None,
                  limit: int = 2) -> list[dict]:
    in_stage = [f for f in area["facets"] if stage in f["stageRefs"]]
    if forced:
        f = next((f for f in area["facets"] if f["id"] == forced), None)
        return [f] if f else []
    m = tokens(message)
    scored = []
    for i, f in enumerate(in_stage):
        q = tokens(f["question"])
        a = tokens(f["answer"])
        score = 3 * len(m & q) + len(m & a)
        if f["id"] in covered:
            score -= 1  # prefer new material when resuming an area
        scored.append((score, -i, f))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    if scored and scored[0][0] > 0:
        top_score, _, top = scored[0]
        picked = [top]
        # a second facet only if it is new to this conversation and nearly as relevant
        for s2, _, f2 in scored[1:limit]:
            if f2["id"] not in covered and s2 >= max(3, 0.6 * top_score):
                picked.append(f2)
        return picked
    uncovered = [f for f in in_stage if f["id"] not in covered]
    return (uncovered or in_stage)[:1]


def chips_for(area: dict, stage: str, covered: list[str], shown: list[str], max_chips: int = 3) -> list[dict]:
    exclude = set(load().routing.get("chipExcludeFacets", []))
    seen = set(covered) | set(shown) | exclude
    in_stage = [f for f in area["facets"] if stage in f["stageRefs"] and f["id"] not in seen]
    return [{"label": f["question"], "facet_id": f["id"]} for f in in_stage[:max_chips]]


def compose_area(area: dict, facets: list[dict]) -> str:
    return "\n".join(f["answer"] for f in facets)


def compose_function(kind: str, target: dict | None) -> tuple[str, str]:
    """Return (text, owning office) for WORDALISE functions."""
    if kind == "opening_hours":
        if not target:
            return "Which place do you mean, for example the library or Reception? [TBD: opening hours]", "Reception"
        return f"Opening hours for {target['name']}: {target['hours']}.", target.get("owningOffice", "Reception")
    if kind == "who_to_contact":
        if not target:
            return ("Your tutor is the best first person to ask, then your Head of Year. "
                    "Reception can point you to anyone else."), "Reception"
        name = target.get("publishedName")
        who = target["role"]
        lead = f"{who[0].upper()}{who[1:]}"
        text = f"{lead} {target['what']} You can reach them through {target['contact']}."
        if name:
            text += f" Their name is {name}."
        return text, "Reception"
    if kind == "school_rule":
        if not target:
            return "[TBD: the school's published policies]. If you're not sure about a specific situation, ask your tutor.", "your tutor"
        return f"{target['summary'].rstrip('.')}. If you're not sure about a specific situation, ask your tutor.", target.get("owningOffice", "your tutor")
    if kind == "find_support":
        if not target:
            return "Your tutor or Head of Year can point you to the right support. Reception can also help.", "Reception"
        return target["howToAccess"], target.get("owningOffice", "Reception")
    raise ValueError(kind)
