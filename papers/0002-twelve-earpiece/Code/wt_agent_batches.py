"""Build the batches for the second judgement, made by Claude Code subagents.

David chose (19 October 2026) to run the second judgement -- engagement and
usefulness in his own definitions -- through subagents on his Claude account, on a
sample: 10 players (5 women, 5 men, seed 19) x 10 questions x repeat 1 x 3 systems
= 300 answers, judged at level 3. One batch per player: the player's data, each
question's explanations and synthetic text (as in `wt_judge.py`, level 3), then the
30 answers shuffled across questions and systems under opaque ids. The key from id
to system is kept in a separate file the subagent does not read.

Runs in the Earpiece API's environment (it reuses `wt_judge.py`'s functions):

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python <path>/Code/wt_agent_batches.py

Writes `outputs/wordalisation-test/agent-judge/batch-NN.md` and `key.json`.
"""

import csv
import importlib.util
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("wt_judge", HERE / "wt_judge.py")
J = importlib.util.module_from_spec(spec)
spec.loader.exec_module(J)

DIR = HERE / "outputs" / "wordalisation-test"
OUT = DIR / "agent-judge"
SEED, PER_GENDER, REPEAT, LEVEL = 19, 5, 1, 3

INSTRUCTIONS = """# Judging task

You are judging answers written for a scout at a football club, who asked questions
about one player. Below are the information about the player, the explanations and
rule-based descriptions for each question, and then 30 answers, each with an id.

Rate each answer on its own, against the information for its question. Do not compare
answers with each other, and do not try to work out who wrote them.

Rate three criteria, each from 1 (very poor) to 5 (very good):
- faithfulness: how faithfully the answer represents the information given;
- engagement: an engaging answer tells the scout about the player in footballing terms,
  without overwhelming them with numbers and statistics. If it gives a number, it does so
  in the context of comparing the player with other players;
- usefulness: an answer is only useful if it compares the player with other, similar
  players. If it gives numbers, it explains what they mean.
Also list every hallucination in the answer, that is every unsupported or fabricated claim:
a statement the information does not support or that contradicts it. Quote each briefly.

Write your ratings to the results file named at the end, one JSON object per line, one
line per answer, in this form:
{"id": "...", "faithfulness": 1-5, "engagement": 1-5, "usefulness": 1-5, "hallucinations": ["..."], "reason": "one or two sentences"}
"""


def main() -> None:
    rng = random.Random(SEED)
    raw = json.loads((DIR / "rawdata.json").read_text())
    players = list(csv.DictReader((DIR / "players.csv").open(encoding="utf-8")))
    chosen = []
    for g in ("female", "male"):
        group = sorted([p for p in players if p["gender"] == g], key=lambda p: p["player_id"])
        chosen += rng.sample(group, PER_GENDER)
    answers = {s: {(a["player_id"], a["question_id"], a["repeat"]): a
                   for a in map(json.loads, (DIR / f"answers-{s}.jsonl").open(encoding="utf-8"))}
               for s in J.SYSTEMS}
    OUT.mkdir(parents=True, exist_ok=True)
    key = {}
    for n, p in enumerate(chosen, 1):
        pid = p["player_id"]
        parts = [INSTRUCTIONS, "## Data about the player\n" + J.raw_text(raw[pid])]
        items = []
        for q in range(1, 11):
            ear = answers["earpiece"][(pid, q, REPEAT)]
            knowledge, synthetic = J.knowledge_and_synthetic(ear)
            parts.append(f"## Question {q}: {ear['question']}\n\n### What the data means\n"
                         f"{knowledge or '(none)'}\n\n### Rule-based description of this "
                         f"player's data for this question\n{synthetic or '(none)'}")
            for s in J.SYSTEMS:
                a = answers[s][(pid, q, REPEAT)]
                if a["answer"].strip():
                    items.append((s, q, a))
        rng.shuffle(items)
        parts.append("## Answers to rate")
        for s, q, a in items:
            item_id = f"b{n:02d}-{rng.randrange(16**6):06x}"
            key[item_id] = {"system": s, "player_id": pid, "question_id": q, "repeat": REPEAT}
            parts.append(f"### Answer {item_id} (to question {q})\n{J.strip_markdown(a['answer'])}")
        results = OUT / f"results-{n:02d}.jsonl"
        parts.append(f"## Results file\nWrite your ratings to: {results}")
        (OUT / f"batch-{n:02d}.md").write_text("\n\n".join(parts), encoding="utf-8")
        print(f"batch-{n:02d}: {p['name']} ({p['gender']}), {len(items)} answers,",
              f"{len(chr(10).join(parts))} characters")
    (OUT / "key.json").write_text(json.dumps(key, indent=1))


if __name__ == "__main__":
    main()
