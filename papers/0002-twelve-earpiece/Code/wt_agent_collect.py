"""Collect the subagents' second judgement and compare it with the first on the same answers.

Reads `outputs/wordalisation-test/agent-judge/key.json` and `results-NN.jsonl`, and
writes `judgments-defined-agents.jsonl` (the same fields as the first judgement,
level 3, variant "defined-agents") and `summary-defined-agents.json`: for the 300
sampled answers, each system's mean faithfulness, engagement, usefulness and
hallucinations under the first judgement (level 3, Caut et al.'s criteria
undefined) and under the second (David's definitions), with 95% intervals from a
bootstrap over players, the share of question-player cells in which each system
scores highest, and the number of figures per sentence in each system's answers
(digits, counted by script, no model).

    cd Code && uv run python ../papers/0002-twelve-earpiece/Code/wt_agent_collect.py [--full]

With `--full`: collects `agent-judge-full/results-*.jsonl` into
`judgments-defined-agents-full.jsonl`, in the first judgement's format, for
`wt_summary.py --variant defined-agents-full`.
"""

import json
import random
import re
from collections import defaultdict
from pathlib import Path

DIR = Path(__file__).resolve().parent / "outputs" / "wordalisation-test"
AJ = DIR / "agent-judge"
SYSTEMS = ["earpiece", "claude", "gpt4o"]
CRITERIA = ["faithfulness", "engagement", "usefulness", "hallucinations"]
BOOT, SEED = 2000, 19


def val(j, c):
    return len(j["hallucinations"]) if c == "hallucinations" else int(j[c])


def ci(rows, c):
    by = defaultdict(list)
    for j in rows:
        by[j["player_id"]].append(val(j, c))
    ps = list(by)
    allv = [v for p in ps for v in by[p]]
    rng = random.Random(SEED)
    boots = []
    for _ in range(BOOT):
        vs = [v for p in (rng.choice(ps) for _ in ps) for v in by[p]]
        boots.append(sum(vs) / len(vs))
    boots.sort()
    return {"mean": round(sum(allv) / len(allv), 2),
            "ci95": [round(boots[int(.025 * BOOT)], 2), round(boots[int(.975 * BOOT)], 2)],
            "n": len(allv)}


def best(rows):
    out = {}
    for c in ["faithfulness", "engagement", "usefulness"]:
        cells = defaultdict(dict)
        for j in rows:
            cells[(j["player_id"], j["question_id"])][j["system"]] = int(j[c])
        wins, n = defaultdict(float), 0
        for sc in cells.values():
            if len(sc) < 3:
                continue
            n += 1
            top = max(sc.values())
            lead = [s for s, v in sc.items() if v == top]
            for s in lead:
                wins[s] += 1 / len(lead)
        out[c] = {s: round(wins[s] / n, 3) for s in SYSTEMS} | {"cells": n}
    return out


def figures_per_sentence(text):
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()] or [text]
    return len(re.findall(r"\d+(?:[.,]\d+)?%?", text)) / len(sentences)


def collect_full(folder="agent-judge-full", key_name="key.json",
                 out_name="judgments-defined-agents-full.jsonl", variant="defined-agents") -> None:
    """A batch judgement (all answers) in the first judgement's format."""
    aj = DIR / folder
    key = json.loads((aj / key_name).read_text())
    level4 = key_name == "key-level4.json"
    rows, problems, seen = [], [], set()
    pattern = "results-*-L4.jsonl" if level4 else "results-*-L[123].jsonl"
    for f in sorted(aj.glob(pattern)):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                k = key[r["id"]]
                if r["id"] in seen:
                    continue
                seen.add(r["id"])
                rec = {**k, "variant": variant, "faithfulness": int(r["faithfulness"]),
                       "hallucinations": list(r.get("hallucinations") or []),
                       "reason": r.get("reason", "")}
                if not level4:
                    rec.update(engagement=int(r["engagement"]), usefulness=int(r["usefulness"]))
                rows.append(rec)
            except Exception as err:  # pylint: disable=broad-except
                problems.append(f"{f.name}: {type(err).__name__} {err}")
    with (DIR / out_name).open("w", encoding="utf-8") as f:
        for j in rows:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")
    missing = sorted(set(key) - seen)
    batches = sorted({m.rsplit("-", 1)[0] for m in missing})
    print(out_name, ":", len(rows), "of", len(key), "judged;", len(problems), "problems;",
          len(missing), "missing in", len(batches), "batches", batches[:20])
    if level4:
        summary = {s: {c: ci([j for j in rows if j["system"] == s], c)
                       for c in ("faithfulness", "hallucinations")} for s in SYSTEMS}
        (DIR / "summary-level4-agents.json").write_text(json.dumps(summary, indent=1))
        for s_, b in summary.items():
            print(f"  level 4 {s_:<9} faith {b['faithfulness']['mean']:.2f} {b['faithfulness']['ci95']}"
                  f"  hallu {b['hallucinations']['mean']:.2f} {b['hallucinations']['ci95']}")


def main() -> None:
    import sys
    if "--full" in sys.argv:
        collect_full()
        return
    if "--control" in sys.argv:
        collect_full("agent-judge-control", "key.json", "judgments-control-agents-full.jsonl",
                     "control-agents")
        collect_full("agent-judge-control", "key-level4.json", "judgments-level4-agents.jsonl",
                     "level4-agents")
        return
    key = json.loads((AJ / "key.json").read_text())
    second, problems = [], []
    for f in sorted(AJ.glob("results-*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                k = key[r["id"]]
                second.append({**k, "level": 3, "variant": "defined-agents",
                               "faithfulness": int(r["faithfulness"]), "engagement": int(r["engagement"]),
                               "usefulness": int(r["usefulness"]),
                               "hallucinations": list(r.get("hallucinations") or []),
                               "reason": r.get("reason", "")})
            except Exception as err:  # pylint: disable=broad-except
                problems.append(f"{f.name}: {err}")
    with (DIR / "judgments-defined-agents.jsonl").open("w", encoding="utf-8") as f:
        for j in second:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")
    sample = {(k["system"], k["player_id"], k["question_id"], k["repeat"]) for k in key.values()}
    first, seen = [], set()
    for j in map(json.loads, (DIR / "judgments.jsonl").open(encoding="utf-8")):
        kk = (j["system"], j["player_id"], j["question_id"], j["repeat"])
        if j.get("level") == 3 and "faithfulness" in j and kk in sample and kk not in seen:
            seen.add(kk)
            first.append(j)
    answers = {s: {(a["player_id"], a["question_id"], a["repeat"]): a["answer"]
                   for a in map(json.loads, (DIR / f"answers-{s}.jsonl").open(encoding="utf-8"))}
               for s in SYSTEMS}
    density = {}
    for s in SYSTEMS:
        texts = [answers[s][(k["player_id"], k["question_id"], k["repeat"])]
                 for k in key.values() if k["system"] == s]
        density[s] = round(sum(map(figures_per_sentence, texts)) / len(texts), 2)
    summary = {
        "answers_in_sample": len(key), "second_judgements": len(second), "problems": problems,
        "figures_per_sentence": density,
        "first_judgement_level3": {s: {c: ci([j for j in first if j["system"] == s], c) for c in CRITERIA}
                                   for s in SYSTEMS},
        "second_judgement_defined": {s: {c: ci([j for j in second if j["system"] == s], c) for c in CRITERIA}
                                     for s in SYSTEMS},
        "highest_first": best(first), "highest_second": best(second),
    }
    (DIR / "summary-defined-agents.json").write_text(json.dumps(summary, indent=1))
    print(len(second), "second judgements of", len(key), "answers;", len(problems), "problems")
    print("figures per sentence:", density)
    for name in ("first_judgement_level3", "second_judgement_defined"):
        print("==", name)
        for s in SYSTEMS:
            b = summary[name][s]
            print(f"  {s:<9}" + "  ".join(f"{c[:5]} {b[c]['mean']:.2f} [{b[c]['ci95'][0]:.2f}-{b[c]['ci95'][1]:.2f}]"
                                          for c in CRITERIA))
    print("highest (usefulness), first:", summary["highest_first"]["usefulness"])
    print("highest (usefulness), second:", summary["highest_second"]["usefulness"])


if __name__ == "__main__":
    main()
