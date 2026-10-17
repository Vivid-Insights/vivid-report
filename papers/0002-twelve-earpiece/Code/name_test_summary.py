"""Summarise the name test: outcome rates with 95% Wilson intervals.

Reads only `outputs/name-test/sample.csv`, `misspellings.csv` and `runs-name.jsonl`
(or, with `--with-team`, also `teams.csv` and `runs-team.jsonl`)
(made by name_test_sample.py, name_test_misspell.py and name_test_run.py) and
writes `outputs/name-test/summary-name.json` (or `summary-team.json`): the rate of each outcome for the
misspelled and the correctly spelled questions, overall, for women and men, for
each category of error, for normal and hard misspellings, and by edit distance, and the players whose correct spelling was resolved while the
misspelling led to another player.

    cd Code && uv run python ../papers/0002-twelve-earpiece/Code/name_test_summary.py [--with-team]
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

DIR = Path(__file__).resolve().parent / "outputs" / "name-test"
OUTCOMES = ["right", "asked the user", "wrong player", "other"]


def wilson(k: int, n: int, z: float = 1.96) -> list[float]:
    if n == 0:
        return [math.nan, math.nan]
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [round(max(0.0, centre - half), 3), round(min(1.0, centre + half), 3)]


def rates(runs: list[dict]) -> dict:
    n = len(runs)
    out = {"n": n}
    for o in OUTCOMES:
        k = sum(r["outcome"] == o for r in runs)
        out[o] = {"count": k, "rate": round(k / n, 3) if n else None, "ci95": wilson(k, n)}
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-team", action="store_true")
    args = parser.parse_args()
    variant = "team" if args.with_team else "name"
    sample = {int(r["player_id"]): r for r in csv.DictReader((DIR / "sample.csv").open(encoding="utf-8"))}
    for m in csv.DictReader((DIR / "misspellings.csv").open(encoding="utf-8")):
        sample[int(m["player_id"])].update(m)
    if args.with_team:
        for t in csv.DictReader((DIR / "teams.csv").open(encoding="utf-8")):
            sample[int(t["player_id"])].update({"team": t["team"], "team_error": t["team_error"],
                                                "team_kind": t["team_kind"]})
    runs = [json.loads(line) for line in (DIR / f"runs-{variant}.jsonl").open(encoding="utf-8")]
    # One run per player and condition; if a run was repeated, the first counts.
    seen, kept = set(), []
    for r in runs:
        key = (r["player_id"], r["condition"])
        if key not in seen:
            seen.add(key)
            kept.append(r)

    by = defaultdict(list)
    for r in kept:
        s = sample[r["player_id"]]
        by[(r["condition"], "all")].append(r)
        by[(r["condition"], s["gender"])].append(r)
        if r["condition"] == "misspelled":
            by[("misspelled", s["category"])].append(r)
            by[("misspelled", "hard" if s["hard"] == "True" else "normal")].append(r)
            d = int(s["edit_distance"])
            by[("misspelled", f"distance {d if d < 4 else '4+'}")].append(r)
            if args.with_team:
                by[("misspelled", f"team {s['team_kind']}")].append(r)

    outcome = {(r["player_id"], r["condition"]): r["outcome"] for r in kept}
    regressions = [
        {"player_id": pid, "name": s["name"], "misspelled": s["misspelled"],
         "category": s["category"], "hard": s["hard"], "steps": s["steps"],
         "gender": s["gender"], "competition": s["competition"]}
        for pid, s in sample.items()
        if outcome.get((pid, "correct")) == "right"
        and outcome.get((pid, "misspelled")) == "wrong player"
    ]
    summary = {
        "players": len(sample),
        "runs": len(kept),
        "groups": {f"{c} / {g}": rates(v) for (c, g), v in sorted(by.items())},
        "correct_right_misspelled_wrong_player": regressions,
    }
    (DIR / f"summary-{variant}.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    for name, g in summary["groups"].items():
        print(f"{name:<32} n={g['n']:<4} " + "  ".join(
            f"{o}: {g[o]['rate']:.2f} [{g[o]['ci95'][0]:.2f}-{g[o]['ci95'][1]:.2f}]" for o in OUTCOMES))
    print(len(regressions), "players right when spelled correctly, wrong player when misspelled")


if __name__ == "__main__":
    main()
