"""Three pairs of answers from the wordalisation test, for the Discussion.

The rule: three different players and three different questions, the first repeat,
leaving out Earpiece's error or empty answers, drawn at random (seed 7). For each pair,
Earpiece's answer and the Claude agent's to the same question about the same player,
with each answer's engagement and usefulness under the basic and the detailed
instructions (raw data, explanations and synthetic text).

    cd Code && uv run python ../papers/0003-twelve-earpiece/Code/wt_examples.py

Writes `outputs/wordalisation-test/examples.json`.
"""

import csv
import json
import random
from pathlib import Path

DIR = Path(__file__).resolve().parent / "outputs" / "wordalisation-test"
SEED, LEVEL = 7, 3


def scores(name):
    out = {}
    for j in map(json.loads, (DIR / name).open(encoding="utf-8")):
        k = (j["system"], j["player_id"], j["question_id"], j["repeat"])
        if j.get("level") == LEVEL and "engagement" in j and k not in out:
            out[k] = {"engagement": j["engagement"], "usefulness": j["usefulness"]}
    return out


def main() -> None:
    players = {p["player_id"]: p for p in csv.DictReader((DIR / "players.csv").open(encoding="utf-8"))}
    ans = {s: {(a["player_id"], a["question_id"], a["repeat"]): a
               for a in map(json.loads, (DIR / f"answers-{s}.jsonl").open(encoding="utf-8"))}
           for s in ("earpiece", "claude")}
    basic, detailed = scores("judgments-control-agents-full.jsonl"), scores("judgments-defined-agents-full.jsonl")
    ok = lambda k: ans["earpiece"][k]["answer"].strip() and "error getting the data" not in ans["earpiece"][k]["answer"]
    rng = random.Random(SEED)
    pids = sorted(players)
    rng.shuffle(pids)
    questions = list(range(1, 11))
    rng.shuffle(questions)
    chosen = []
    for pid, q in zip(pids, questions):
        if len(chosen) == 3:
            break
        k = (pid, q, 1)
        if ok(k):
            chosen.append(k)
    out = []
    for k in chosen:
        p = players[k[0]]
        out.append({"player": p["name"], "gender": p["gender"], "position": p["position"],
                    "competition": p["competition"], "season": p["season"],
                    "question": ans["earpiece"][k]["question"],
                    "earpiece": ans["earpiece"][k]["answer"], "claude": ans["claude"][k]["answer"],
                    "basic": {s: basic[(s, *k)] for s in ("earpiece", "claude")},
                    "detailed": {s: detailed[(s, *k)] for s in ("earpiece", "claude")}})
    (DIR / "examples.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for e in out:
        print(json.dumps(e, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
