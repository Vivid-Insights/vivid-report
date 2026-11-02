"""Write the wordalisation test's answers and judgements as CSV, for reading by hand.

- `answers.csv`: one row per player, question and repeat, with the three systems'
  answers side by side, the functions Earpiece called, and the number of sentences
  the agents were asked for.
- `judgments.csv`: one row per judgement (system, player, question, repeat, level),
  with the three scores, the number and text of the hallucinations listed, and the
  judge's reason. Where an answer was judged twice, the first judgement is kept, as
  in the summary.

    cd Code && uv run python ../papers/0003-twelve-earpiece/Code/wt_export.py

Reads `outputs/wordalisation-test/`; writes `answers.csv` and `judgments.csv` there.
"""

import csv
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent / "outputs" / "wordalisation-test"
SYSTEMS = ["earpiece", "claude", "gpt4o"]


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["caut", "defined", "defined-agents-full", "control-agents-full"], default="caut")
    variant = ap.parse_args().variant
    suffix = "" if variant == "caut" else f"-{variant}"
    players = {r["player_id"]: r for r in csv.DictReader((DIR / "players.csv").open(encoding="utf-8"))}
    answers = {s: {(a["player_id"], a["question_id"], a["repeat"]): a
                   for a in map(json.loads, (DIR / f"answers-{s}.jsonl").open(encoding="utf-8"))}
               for s in SYSTEMS}

    with (DIR / "answers.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["player", "gender", "position", "competition", "season", "question_id",
                    "question", "repeat", "earpiece_functions", "sentences_asked",
                    "earpiece_answer", "claude_answer", "gpt4o_answer"])
        for key in sorted(answers["earpiece"], key=lambda k: (k[0], k[1], k[2])):
            p = players[key[0]]
            e, c, g = (answers[s].get(key, {}) for s in SYSTEMS)
            w.writerow([p["name"], p["gender"], p["position"], p["competition"], p["season"],
                        key[1], e.get("question", ""), key[2],
                        " + ".join(e.get("functions") or []), c.get("sentences_asked", ""),
                        e.get("answer", ""), c.get("answer", ""), g.get("answer", "")])

    seen = set()
    with (DIR / f"judgments{suffix}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["system", "player", "gender", "question_id", "question", "repeat", "level",
                    "faithfulness", "engagement", "usefulness", "n_hallucinations",
                    "hallucinations", "reason"])
        for j in map(json.loads, (DIR / f"judgments{suffix}.jsonl").open(encoding="utf-8")):
            key = (j["system"], j["player_id"], j["question_id"], j["repeat"], j["level"])
            if "faithfulness" not in j or key in seen:
                continue
            seen.add(key)
            p = players[j["player_id"]]
            q = answers[j["system"]][(j["player_id"], j["question_id"], j["repeat"])]["question"]
            w.writerow([j["system"], p["name"], p["gender"], j["question_id"], q, j["repeat"],
                        j["level"], j["faithfulness"], j["engagement"], j["usefulness"],
                        len(j["hallucinations"]), " | ".join(j["hallucinations"]),
                        j.get("reason", "")])
    print("wrote", DIR / "answers.csv", "and", DIR / f"judgments{suffix}.csv", f"({len(seen)} judgements)")


if __name__ == "__main__":
    main()
