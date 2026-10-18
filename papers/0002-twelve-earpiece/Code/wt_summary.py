"""Summarise the judgements of the wordalisation test.

Reads `outputs/wordalisation-test/judgments.jsonl`, `players.csv` and
`answers-earpiece.jsonl`, and writes `summary.json`: for each level of
information and each system, the mean faithfulness, engagement and usefulness
(1-5) and the mean number of hallucinations per answer, with 95% intervals from a
bootstrap over players (answers about the same player are not independent); how
often each system scores highest on a question for a player in a repeat; and the
same by question and by women and men; and the mean length of each system's
answers, in characters and sentences.

Every figure is given twice: with all answers, and leaving out Earpiece's answers
that were its error message or empty ("Earpiece without its error answers"); the
agents' answers are the same in both.

    cd Code && uv run python ../papers/0002-twelve-earpiece/Code/wt_summary.py [--variant defined]
"""

from __future__ import annotations

import csv
import json
import random
import re
from collections import defaultdict
from pathlib import Path

DIR = Path(__file__).resolve().parent / "outputs" / "wordalisation-test"
SYSTEMS = ["earpiece", "claude", "gpt4o"]
CRITERIA = ["faithfulness", "engagement", "usefulness", "hallucinations"]
BOOT, SEED = 2000, 18


def value(j, c):
    return len(j["hallucinations"]) if c == "hallucinations" else j[c]


def boot_ci(rows, c):
    """Mean and 95% interval, resampling players."""
    by_player = defaultdict(list)
    for j in rows:
        by_player[j["player_id"]].append(value(j, c))
    players = list(by_player)
    if not players:
        return None
    mean = sum(v for p in players for v in by_player[p]) / sum(len(by_player[p]) for p in players)
    rng = random.Random(SEED)
    stats = []
    for _ in range(BOOT):
        pick = [rng.choice(players) for _ in players]
        vals = [v for p in pick for v in by_player[p]]
        stats.append(sum(vals) / len(vals))
    stats.sort()
    return {"mean": round(mean, 2), "ci95": [round(stats[int(0.025 * BOOT)], 2),
                                             round(stats[int(0.975 * BOOT)], 2)], "n": sum(len(v) for v in by_player.values())}


def best_share(rows):
    """Share of (player, question, repeat) where each system has the highest score; ties split."""
    out = {}
    for c in ["faithfulness", "engagement", "usefulness"]:
        cells = defaultdict(dict)
        for j in rows:
            cells[(j["player_id"], j["question_id"], j["repeat"])][j["system"]] = j[c]
        wins, n = defaultdict(float), 0
        for scores in cells.values():
            if len(scores) < len(SYSTEMS):
                continue
            n += 1
            top = max(scores.values())
            leaders = [s for s, v in scores.items() if v == top]
            for s in leaders:
                wins[s] += 1 / len(leaders)
        out[c] = {s: round(wins[s] / n, 3) if n else None for s in SYSTEMS} | {"cells": n}
    return out


def describe(rows):
    res = {}
    for level in (1, 2, 3):
        lv = [j for j in rows if j["level"] == level]
        res[f"level {level}"] = {
            "by_system": {s: {c: boot_ci([j for j in lv if j["system"] == s], c) for c in CRITERIA}
                          for s in SYSTEMS},
            "highest_score_share": best_share(lv),
        }
    return res


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["caut", "defined", "defined-agents-full", "control-agents-full"], default="caut")
    variant = ap.parse_args().variant
    suffix = "" if variant == "caut" else f"-{variant}"
    players = {r["player_id"]: r for r in csv.DictReader((DIR / "players.csv").open(encoding="utf-8"))}
    J = [json.loads(l) for l in (DIR / f"judgments{suffix}.jsonl").open(encoding="utf-8")]
    J = [j for j in J if "faithfulness" in j]
    seen, rows = set(), []
    for j in J:
        k = (j["system"], j["player_id"], j["question_id"], j["repeat"], j["level"])
        if k not in seen:
            seen.add(k)
            rows.append(j)
    errors = set()
    for line in (DIR / "answers-earpiece.jsonl").open(encoding="utf-8"):
        a = json.loads(line)
        if not a["answer"].strip() or "error getting the data" in a["answer"]:
            errors.add((a["player_id"], a["question_id"], a["repeat"]))
    without = [j for j in rows if not (j["system"] == "earpiece"
                                      and (j["player_id"], j["question_id"], j["repeat"]) in errors)]
    lengths = {}
    for sname in SYSTEMS:
        ans = [json.loads(l) for l in (DIR / f"answers-{sname}.jsonl").open(encoding="utf-8")]
        ans = [a["answer"] for a in ans if a["answer"].strip()]
        sent = [len([x for x in re.split(r"(?<=[.!?])\s+", a.strip()) if x.strip()]) for a in ans]
        lengths[sname] = {"answers": len(ans), "mean_characters": round(sum(map(len, ans)) / len(ans)),
                          "mean_sentences": round(sum(sent) / len(sent), 2)}
    summary = {
        "judgements": len(rows),
        "answer_length": lengths,
        "earpiece_error_or_empty_answers": len(errors),
        "all_answers": describe(rows),
        "earpiece_without_error_answers": describe(without),
        "by_question": {q: describe([j for j in without if j["question_id"] == q])
                        for q in sorted({j["question_id"] for j in rows})},
        "by_gender": {g: describe([j for j in without if players[j["player_id"]]["gender"] == g])
                      for g in ("female", "male")},
    }
    (DIR / f"summary{suffix}.json").write_text(json.dumps(summary, indent=1))
    print(len(rows), "judgements;", len(errors), "Earpiece error or empty answers")
    print("answer length:", lengths)
    for name in ("all_answers", "earpiece_without_error_answers"):
        print("\n==", name)
        for level, d in summary[name].items():
            print(level)
            for s in SYSTEMS:
                b = d["by_system"][s]
                print(f"  {s:<9}" + "  ".join(
                    f"{c[:5]} {b[c]['mean']:.2f} [{b[c]['ci95'][0]:.2f}-{b[c]['ci95'][1]:.2f}]"
                    if b[c] else f"{c[:5]} -" for c in CRITERIA))
            print("  highest:", {c: {s: v for s, v in d["highest_score_share"][c].items()}
                                 for c in ("faithfulness", "usefulness")})


if __name__ == "__main__":
    main()
