"""Output checks applied to EVERY reply (offline and LLM).

* Placeholder blocker (CONSTRAINT-2, flows[*] 'Output check'): no '[TBD' text ever
  reaches the user. Unconfirmed details become an inline '(not confirmed yet)'
  marker, sentences that would be empty without the placeholder are dropped, and the
  fallback sentence naming the owning office is appended once.
* Voice rewrites: designer notes inside facet answers.
* Volunteered-name redaction (CONSTRAINT-5).
* Capability / approval-prediction detectors (CONSTRAINT-3, CONSTRAINT-4).
"""
from __future__ import annotations

import re

from .content import load

TBD_RE = re.compile(r"\[TBD[^\]]*\]?", re.IGNORECASE)
MARKER = "(not confirmed yet)"

_SENT_END = re.compile(r"([.!?])(\s+)")
_STEP_RE = re.compile(r"^\s*\d+\.\s")


def split_sentences(text: str) -> list[str]:
    """Split on sentence ends, but never right after a bare step number ('1.')."""
    out, start = [], 0
    for m in _SENT_END.finditer(text):
        end = m.end(1)
        chunk = text[start:end]
        last_word = chunk.split()[-1] if chunk.split() else ""
        if re.fullmatch(r"\d+\.", last_word):
            continue  # '1.' starts a numbered step: not a sentence end
        out.append(chunk.strip())
        start = m.end()
    tail = text[start:].strip()
    if tail:
        out.append(tail)
    return [s for s in out if s]


def fallback_sentence(office: str | None) -> str:
    bot = load().bot
    office = office or "Reception"
    or_rec = "" if office.lower() in ("reception", "reception/admissions") else " (or Reception)"
    return bot["unconfirmedFallback"].format(office=office, orReception=or_rec)


def _clean_sentence(sentence: str) -> str | None:
    if not TBD_RE.search(sentence):
        return sentence
    replaced = TBD_RE.sub(MARKER, sentence)
    remaining = TBD_RE.sub(" ", sentence)
    words = re.findall(r"[A-Za-z0-9']+", _STEP_RE.sub("", remaining))
    if len(words) < 4:
        return None  # nothing meaningful left once the placeholder is removed
    # tidy '( not confirmed yet)' spacing and doubled markers
    replaced = re.sub(r"\s+([,.;:])", r"\1", replaced)
    replaced = replaced.replace(f"{MARKER} or {MARKER}", MARKER)
    return replaced


def clean_placeholders(text: str, office: str | None) -> tuple[str, bool]:
    """Return (clean text, had_placeholder)."""
    if not TBD_RE.search(text):
        return text, False
    lines_out = []
    for line in text.split("\n"):
        kept = [c for c in (_clean_sentence(s) for s in split_sentences(line)) if c]
        if kept:
            lines_out.append(" ".join(kept))
    body = "\n".join(lines_out).strip()
    fb = fallback_sentence(office)
    body = f"{body}\n{fb}" if body else fb
    # belt and braces: nothing resembling a placeholder may survive
    body = re.sub(r"\[\s*TBD", "", body, flags=re.IGNORECASE)
    return body, True


def apply_voice(text: str) -> str:
    for pattern, repl in load().bot.get("voiceRewrites", []):
        text = re.sub(pattern, repl, text)
    return text


_NAME_PREFIX = re.compile(
    r"(?i:\b(?:i'?m|i am|im|my name is|my name's|this is|it's|its)\s+)"
    r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
)
_NOT_NAMES = {"In", "Year", "Ill", "Sick", "Off", "Not", "Late", "At", "From", "On", "Going",
              "A", "The", "Sixth", "Worried", "Sorry", "Here", "Just", "Still", "Really", "So"}


def volunteered_names(message: str) -> list[str]:
    names = []
    for m in _NAME_PREFIX.finditer(message):
        parts = [p for p in m.group(1).split() if p not in _NOT_NAMES]
        if parts and parts[0] == m.group(1).split()[0]:
            names.extend(parts)
    return names


def redact_names(text: str, names) -> str:
    for n in names:
        text = re.sub(rf"\b{re.escape(n)}\b,?\s?", "", text)
    return text


CAPABILITY_CLAIM = re.compile(
    r"\bI(?:'ve| have|'ll| will| just)?\s+(?:sent|emailed|e-mailed|booked|recorded|submitted|"
    r"contacted|told|informed|notified|passed (?:this|that|it) on|let (?:them|him|her|(?:the|your) [\w ]{1,30}?) know|"
    r"logged|reported|registered|changed)\b",
    re.IGNORECASE,
)
APPROVAL_PREDICTION = re.compile(
    r"should be (?:fine|ok|okay|approved)|(?:likely|probably|usually|normally) (?:be )?(?:approved|granted|allowed|fine)|"
    r"I'?m sure (?:it|they|you)|don'?t worry,? (?:it|they)|will (?:definitely|certainly) (?:be )?(?:approved|allowed|granted)",
    re.IGNORECASE,
)


def violates_constraints(text: str) -> str | None:
    if CAPABILITY_CLAIM.search(text):
        return "CONSTRAINT-3 capability claim"
    if APPROVAL_PREDICTION.search(text):
        return "CONSTRAINT-4 approval prediction"
    return None
