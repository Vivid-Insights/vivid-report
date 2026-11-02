"""The numbers in the report's two wordalisation-test tables.

Faithfulness: the second judgement (David's definitions, batch) at levels 1-3 and
level 4 (synthetic text only). Engagement and usefulness: the control ("basic
instructions") against the second judgement ("detailed instructions"), at levels 1-3.
Each a mean with the standard deviation of the ratings over answers (and a 95% interval
from a bootstrap over players, not used in the report), leaving out Earpiece's
error or empty answers, as in `wt_summary.py`.

    cd Code && uv run python ../papers/0003-twelve-earpiece/Code/wt_tables.py

Writes `outputs/wordalisation-test/tables.json`.
"""

import json
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("wt_summary", HERE / "wt_summary.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
DIR = S.DIR


def load(name):
    rows, seen = [], set()
    for j in map(json.loads, (DIR / name).open(encoding="utf-8")):
        k = (j["system"], j["player_id"], j["question_id"], j["repeat"], j["level"])
        if "faithfulness" in j and k not in seen:
            seen.add(k)
            rows.append(j)
    return rows


def mean_sd(rows, c):
    """Mean and standard deviation (n - 1) of the ratings, over answers."""
    v = [S.value(j, c) for j in rows]
    m = sum(v) / len(v)
    return {"mean": round(m, 2), "sd": round((sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5, 2), "n": len(v)}


def head_to_head(rows, c):
    """Share of answers (player, question, repeat) where Earpiece's rating is higher than
    the Claude agent's, and lower; the rest are ties. Only where both were rated."""
    cells = {}
    for j in rows:
        if j["system"] in ("earpiece", "claude"):
            cells.setdefault((j["player_id"], j["question_id"], j["repeat"]), {})[j["system"]] = j[c]
    pairs = [v for v in cells.values() if len(v) == 2]
    e = sum(v["earpiece"] > v["claude"] for v in pairs)
    a = sum(v["earpiece"] < v["claude"] for v in pairs)
    return {"earpiece_won": round(e / len(pairs), 3), "claude_won": round(a / len(pairs), 3),
            "tied": round(1 - (e + a) / len(pairs), 3), "pairs": len(pairs)}


def main() -> None:
    errors = set()
    for a in map(json.loads, (DIR / "answers-earpiece.jsonl").open(encoding="utf-8")):
        if not a["answer"].strip() or "error getting the data" in a["answer"]:
            errors.add((a["player_id"], a["question_id"], a["repeat"]))

    def keep(rows):
        return [j for j in rows if not (j["system"] == "earpiece"
                and (j["player_id"], j["question_id"], j["repeat"]) in errors)]

    runs = {"detailed": keep(load("judgments-defined-agents-full.jsonl")),
            "basic": keep(load("judgments-control-agents-full.jsonl")),
            "level4": keep(load("judgments-level4-agents.jsonl"))}
    out = {"earpiece_error_answers_left_out": len(errors), "faithfulness": {}, "engagement_usefulness": {}}
    for level in (1, 2, 3, 4):
        rows = runs["level4"] if level == 4 else [j for j in runs["detailed"] if j["level"] == level]
        out["faithfulness"][f"level {level}"] = {
            s: {c: S.boot_ci([j for j in rows if j["system"] == s], c)
                | {"sd": mean_sd([j for j in rows if j["system"] == s], c)["sd"]}
                for c in ("faithfulness", "hallucinations")} for s in S.SYSTEMS}
        out["faithfulness"][f"level {level}"]["head_to_head"] = head_to_head(rows, "faithfulness")
    for name in ("basic", "detailed"):
        for level in (1, 2, 3):
            rows = [j for j in runs[name] if j["level"] == level]
            out["engagement_usefulness"][f"{name} level {level}"] = {
                s: {c: S.boot_ci([j for j in rows if j["system"] == s], c)
                    | {"sd": mean_sd([j for j in rows if j["system"] == s], c)["sd"]}
                    for c in ("engagement", "usefulness")} for s in S.SYSTEMS}
            out["engagement_usefulness"][f"{name} level {level}"]["head_to_head"] = {
                c: head_to_head(rows, c) for c in ("engagement", "usefulness")}
    (DIR / "tables.json").write_text(json.dumps(out, indent=1))
    for part in ("faithfulness", "engagement_usefulness"):
        for k, v in out[part].items():
            print(part[:5], k, {s_: {c: (b["mean"], b["sd"]) for c, b in v[s_].items()} for s_ in ("earpiece", "claude")})


if __name__ == "__main__":
    main()
