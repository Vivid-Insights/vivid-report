"""Misspell the names in the name-test sample, following what is known about name errors.

The error model, agreed with David on 17 October 2026, follows two sources:

- Friedman and Sideli (1992), on errors in patient names in hospital databases, as
  reported by Christen (2006, TR-CS-06-02, section 2): 36% of errors were an added
  or missing name word, initial or title; 39% were single errors (one letter
  deleted, inserted, substituted or two swapped); 14% were several letters
  changed by spelling variation; 12% were punctuation and whitespace. Those four
  shares, scaled to the sample since they sum to 101%, set how many names get
  each kind of error.
- Udupa and Kumar (2010, EMNLP), who give the categories phonetic and cognitive
  errors for the multi-letter changes, and find that misspellings taken from a
  real people-search log lay 2.33 edits (SD 1.60) from the correct name. A quarter
  of the names are therefore made hard: the assigned error plus one or two of
  another kind, at least three edits from the name.

Within single errors, Christen reports substitution as the most common, then
deletion, insertion and transposition; the weights 4:3:2:1 below keep that order,
and the numbers themselves are our choice. Substitutions use neighbouring keys on
a QWERTY keyboard, the source Christen gives for keyed errors. Lower-casing the
whole name, which Earpiece's own test queries show users doing ("moritz berg"),
is counted under punctuation, spacing and accents.

When an error cannot apply to a name (a one-word name cannot lose a word), the
next category in the list is used and the category applied is recorded. Distances
are optimal-string-alignment distances between case-folded names: `letter_edits`
counts the changes to the letters before any name word is dropped, and
`edit_distance` compares the final misspelling with the full name. In a hard name
the letter-level errors come first and must reach three letter edits on their
own (two for a name shorter than ten letters, which three would leave
unrecognisable); a name-word change, if assigned, is made last.

    cd Code && uv run python ../papers/0002-twelve-earpiece/Code/name_test_misspell.py

Reads `outputs/name-test/sample.csv`; writes `outputs/name-test/misspellings.csv`.
"""

from __future__ import annotations

import csv
import random
import unicodedata
from pathlib import Path

DIR = Path(__file__).resolve().parent / "outputs" / "name-test"
SEED = 1992
#: The study's shares, which sum to 101%; scaled to the sample below.
SHARES = [("name words", 36), ("single typing error", 39),
          ("spelling variant", 14), ("punctuation, spacing, accents", 12)]
HARD_SHARE = 0.25
HARD_MIN_DISTANCE = 3

ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
NEIGHBOURS: dict[str, str] = {}
for r, row in enumerate(ROWS):
    for c, ch in enumerate(row):
        near = [row[c + d] for d in (-1, 1) if 0 <= c + d < len(row)]
        for rr in (r - 1, r + 1):
            if 0 <= rr < len(ROWS):
                near += [ROWS[rr][cc] for cc in (c - 1, c, c + 1) if 0 <= cc < len(ROWS[rr])]
        NEIGHBOURS[ch] = "".join(near)

#: Sound-alike and cognitive respellings (Udupa and Kumar's "Erik Bryl for Eric Brill").
VARIANTS = [("ph", "f"), ("f", "ph"), ("th", "t"), ("ck", "k"), ("qu", "k"), ("x", "ks"),
            ("c", "k"), ("k", "c"), ("y", "i"), ("i", "y"), ("w", "v"), ("v", "w"),
            ("z", "s"), ("s", "z"), ("sch", "sh"), ("sh", "sch"), ("j", "y"), ("ou", "u"),
            ("ae", "e"), ("ei", "ie"), ("ie", "ei"), ("ee", "i"), ("oo", "u"),
            ("sson", "son"), ("son", "sson"), ("ski", "sky"), ("sky", "ski"),
            ("ic", "ich"), ("ich", "ic"), ("ll", "l"), ("tt", "t"), ("nn", "n"),
            ("ss", "s"), ("mm", "m"), ("rr", "r"), ("e", "a"), ("a", "e"), ("o", "u")]


def strip_accents(s: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))


def osa(a: str, b: str) -> int:
    """Optimal string alignment distance: deletions, insertions, substitutions, adjacent swaps."""
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = a[i - 1] != b[j - 1]
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[len(a)][len(b)]


def name_words(name: str, rng: random.Random):
    w = name.split()
    options = []
    if len(w) >= 2:
        options += [("surname only", w[-1]), ("initial for first name", f"{w[0][0]}. {' '.join(w[1:])}")]
    if len(w) >= 3:
        options += [("last word dropped", " ".join(w[:-1])),
                    ("middle word dropped", " ".join(w[:1] + w[2:]))]
    return rng.choice(options) if options else None


def typing_error(name: str, rng: random.Random):
    w = name.split()
    i = rng.choices(range(len(w)), weights=[len(x) for x in w])[0]
    word = w[i]
    pos = [k for k, ch in enumerate(word) if ch.isalpha()][1:]   # keep the first letter
    if len(pos) < 2:
        return None
    op = rng.choices(["substitution", "deletion", "insertion", "transposition"], [4, 3, 2, 1])[0]
    k = rng.choice(pos)
    ch = word[k].lower()
    if op == "substitution" and ch in NEIGHBOURS:
        new = word[:k] + rng.choice(NEIGHBOURS[ch]) + word[k + 1:]
    elif op == "deletion":
        new = word[:k] + word[k + 1:]
    elif op == "insertion":
        extra = rng.choice([word[k], rng.choice(NEIGHBOURS.get(ch, ch))])
        new = word[:k] + extra + word[k:]
    elif op == "transposition" and k + 1 < len(word) and word[k] != word[k + 1]:
        new = word[:k] + word[k + 1] + word[k] + word[k + 2:]
    else:
        new = word[:k] + word[k + 1:]
        op = "deletion"
    w[i] = new
    return op, " ".join(w)


def spelling_variant(name: str, rng: random.Random):
    out, used = name, []
    for _ in range(rng.choice([1, 2])):
        low = out.lower()
        options = [(a, b) for a, b in VARIANTS if a in low[1:]]
        if not options:
            break
        a, b = rng.choice(options)
        starts = [k for k in range(1, len(low)) if low.startswith(a, k)]
        k = rng.choice(starts)
        out = out[:k] + b + out[k + len(a):]
        used.append(f"{a}>{b}")
    return (" ".join(used), out) if used else None


def punctuation(name: str, rng: random.Random):
    options = [("lower case", name.lower())]
    if strip_accents(name) != name:
        options.append(("accents stripped", strip_accents(name)))
    if "-" in name:
        options.append(("hyphen to space", name.replace("-", " ")))
    w = name.split()
    if len(w) >= 2:
        options.append(("words joined", " ".join(w[:-2] + [w[-2] + w[-1].lower()])))
    return rng.choice(options)


APPLY = {"name words": name_words, "single typing error": typing_error,
         "spelling variant": spelling_variant, "punctuation, spacing, accents": punctuation}
ORDER = [c for c, _ in SHARES]


def one_error(name: str, category: str, rng: random.Random):
    """Apply the category, or the next one that applies; return (category, detail, new)."""
    start = ORDER.index(category)
    for c in ORDER[start:] + ORDER[:start]:
        got = APPLY[c](name, rng)
        if got and got[1] != name:
            return c, got[0], got[1]
    return category, "none", name


def main() -> None:
    rng = random.Random(SEED)
    sample = list(csv.DictReader((DIR / "sample.csv").open(encoding="utf-8")))
    order = list(range(len(sample)))
    rng.shuffle(order)
    total = sum(s for _, s in SHARES)
    quotas, assigned = [round(s * len(sample) / total) for _, s in SHARES], {}
    quotas[1] += len(sample) - sum(quotas)            # remainder to single typing errors
    pos = 0
    for (category, _), q in zip(SHARES, quotas):
        for idx in order[pos:pos + q]:
            assigned[idx] = category
        pos += q
    hard = set(rng.sample(range(len(sample)), round(HARD_SHARE * len(sample))))

    rows = []
    for idx, s in enumerate(sample):
        name = s["name"]
        if idx not in hard:
            category, detail, wrong = one_error(name, assigned[idx], rng)
            steps = [f"{category}: {detail}"]
            spelled = name if category == "name words" else wrong
        else:
            # Letter-level errors first, until they alone are HARD_MIN_DISTANCE from the
            # name; a name-word change, if assigned, comes last so no error is dropped.
            category, steps, spelled = assigned[idx], [], name
            letter_kinds = [c for c in ORDER if c != "name words"]
            first = category if category != "name words" else rng.choice(letter_kinds)
            tries = 0
            need = HARD_MIN_DISTANCE if len(name.replace(" ", "")) >= 10 else HARD_MIN_DISTANCE - 1
            while (osa(spelled.casefold(), name.casefold()) < need or not steps) \
                    and tries < 10:
                kind = first if not steps else rng.choice(letter_kinds)
                c2, d2, w2 = one_error(spelled, kind, rng)
                if w2 != spelled and c2 != "name words":
                    spelled = w2
                    steps.append(f"{c2}: {d2}")
                tries += 1
            wrong = spelled
            if category == "name words":
                got = name_words(spelled, rng)
                if got:
                    wrong = got[1]
                    steps.append(f"name words: {got[0]}")
        rows.append({
            "player_id": s["player_id"], "name": name, "misspelled": wrong,
            "category": category, "hard": idx in hard, "steps": " | ".join(steps),
            "letter_edits": osa(spelled.casefold(), name.casefold()),
            "edit_distance": osa(wrong.casefold(), name.casefold()),
        })

    with (DIR / "misspellings.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    print(Counter(r["category"] for r in rows))
    print("hard:", sum(r["hard"] for r in rows),
          "| mean letter edits, normal:",
          round(sum(r["letter_edits"] for r in rows if not r["hard"]) / max(1, sum(not r["hard"] for r in rows)), 2),
          "hard:", round(sum(r["letter_edits"] for r in rows if r["hard"]) / max(1, sum(r["hard"] for r in rows)), 2))


if __name__ == "__main__":
    main()
