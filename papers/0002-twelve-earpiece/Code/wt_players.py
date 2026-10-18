"""Choose the 20 players of the wordalisation test.

Agreed with David, 18 October 2026: 10 women and 10 men from the name-test
sample, outfield players only (Earpiece does not analyse goalkeepers), with at
least 900 minutes. Within each gender the players are spread over positions:
eligible players are shuffled (seed 18) and taken in turn from each position.

    cd Code && uv run python ../papers/0002-twelve-earpiece/Code/wt_players.py

Reads `outputs/name-test/sample.csv`; writes `outputs/wordalisation-test/players.csv`.
"""

import csv
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "outputs" / "name-test" / "sample.csv"
OUT = HERE / "outputs" / "wordalisation-test" / "players.csv"
SEED, PER_GENDER, MIN_MINUTES = 18, 10, 900


def main() -> None:
    rng = random.Random(SEED)
    rows = [r for r in csv.DictReader(SAMPLE.open(encoding="utf-8"))
            if r["position"] != "GOALKEEPER" and int(r["minutes"]) >= MIN_MINUTES]
    chosen = []
    for gender in ("female", "male"):
        by_pos = defaultdict(list)
        for r in rows:
            if r["gender"] == gender:
                by_pos[r["position"]].append(r)
        for group in by_pos.values():
            rng.shuffle(group)
        positions = sorted(by_pos)
        rng.shuffle(positions)
        taken = []
        while len(taken) < PER_GENDER and any(by_pos.values()):
            for pos in positions:
                if by_pos[pos] and len(taken) < PER_GENDER:
                    taken.append(by_pos[pos].pop())
        chosen += taken
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(chosen[0]))
        w.writeheader()
        w.writerows(chosen)
    for r in chosen:
        print(r["gender"][0], r["name"], "|", r["position"], "|", r["competition"], r["season"], r["minutes"])


if __name__ == "__main__":
    main()
