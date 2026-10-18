"""Judge every answer of the wordalisation test, blind, at three levels of information.

Agreed with David, 18 October 2026. Each answer (Earpiece, Claude agent, GPT-4o
agent; 20 players x 10 questions x 3 repeats) is rated by a separate call to
Claude Opus 5.5 that sees one answer only and does not know which system wrote it,
as in the human evaluation of Caut et al. (2025), where no rater saw two
descriptions of the same entity. The criteria are theirs: the faithfulness of the
answer to the information, its engagement, and its usefulness for understanding or
decision-making, each rated 1-5 here (their paper gives no scale), and its
hallucinations, defined as unsupported or fabricated claims, which the judge lists.

The judge is given one of three levels of information, each judged independently:

1. raw data: the data either system could draw on (`rawdata.json`): the
   player's quality and metric values with z-scores against players in the same
   position, the zone-by-zone z-scores Earpiece's pitch descriptions use, and the
   same fixed calls to Twelve's data tools that the agents could make;
2. level 1 plus what Earpiece's model is told it knows: the question-answer pairs
   that explain the data in the prompt of the Earpiece function(s) that answered
   this question for this player ("tell it what it knows", Caut et al.);
3. level 2 plus Earpiece's synthetic text for this question and player.

Levels 2 and 3 come from Earpiece's first repeat, so every answer to the same
question about the same player is judged against the same information. Markdown
bold and italics are removed from answers so formatting does not identify the
system; the words are unchanged.

Runs in the Earpiece API's environment (for the Anthropic key) and can be resumed:

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python <path>/Code/wt_judge.py [--limit N] [--concurrency 10]

Reads `players.csv`, `rawdata.json`, `answers-*.jsonl`; appends to `judgments.jsonl`.
"""

from __future__ import annotations

import argparse
import os
import asyncio
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import anthropic

from config import config


def workspace_anthropic_key() -> str:
    """The Anthropic key of the report workspace: ANTHROPIC_API_KEY from the environment,
    or from the `.env` at the top of the workspace (not committed). Never Twelve's key."""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    env = Path(__file__).resolve().parents[3] / ".env"
    if not key and env.exists():
        for line in env.read_text().splitlines():
            if line.strip().startswith("ANTHROPIC_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not key:
        raise SystemExit("Set ANTHROPIC_API_KEY in the environment or in the workspace's .env")
    return key

DIR = Path(__file__).resolve().parent / "outputs" / "wordalisation-test"
JUDGE_MODEL = "claude-opus-5-5"
SYSTEMS = ["earpiece", "claude", "gpt4o"]
LEVELS = [1, 2, 3]

JUDGE_SYSTEM = (
    "You are evaluating one answer written for a scout at a football club, who asked a "
    "question about a player. You are given information about the player, the question and "
    "the answer. Rate the answer on three criteria, each from 1 (very poor) to 5 (very good):\n"
    "- faithfulness: how faithfully the answer represents the information given;\n"
    "- engagement: how engaging the answer is to read;\n"
    "- usefulness: how useful the answer is for understanding the player or for making a "
    "decision about them.\n"
    "Also list every hallucination in the answer, that is every unsupported or fabricated claim: "
    "a statement the information does not support or that contradicts it. Quote each one "
    "briefly. Judge only this answer against the information given.\n"
    "Reply with JSON only, in this form: "
    '{"faithfulness": 1-5, "engagement": 1-5, "usefulness": 1-5, '
    '"hallucinations": ["..."], "reason": "one or two sentences"}'
)


def strip_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text, flags=re.S)
    text = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", text, flags=re.S)
    text = re.sub(r"(?<!\w)__(.+?)__(?!\w)", r"\1", text, flags=re.S)
    return text.strip()


def raw_text(raw: dict) -> str:
    also = f" (full name {raw['full_name']})" if raw.get("full_name") and raw["full_name"] != raw["player"] else ""
    lines = [f"Player: {raw['player']}{also}, {raw['position'].replace('_', ' ').lower()}, "
             f"{raw['competition']} {raw['season']}, {raw['minutes']} minutes.",
             f"z-scores compare the player with {raw['comparison']} (0 = average, "
             "positive = above average).", "", "Qualities (z-score):"]
    lines += [f"- {q['quality']}: {q['z_score']}" for q in raw["qualities"]]
    lines += ["", "Metrics (value per 90 minutes or share, and z-score):"]
    lines += [f"- {m['metric']}: {m['value']} (z = {m['z_score']})" for m in raw["metrics"]]
    if raw.get("zones"):
        lines += ["", "Zones of the pitch: for each quality, the z-score of its pitch metric in "
                  "each zone, against players in the same position:"]
        by_q: dict[str, list[str]] = {}
        for z in raw["zones"]:
            by_q.setdefault(f"{z['quality']} ({z['metric']})", []).append(f"{z['zone']} {z['z_score']}")
        lines += [f"- {q}: " + ", ".join(v) for q, v in by_q.items()]
    for name, text in (raw.get("tool_data") or {}).items():
        lines += ["", f"From Twelve's data ({name}):", text]
    return "\n".join(lines)


def knowledge_and_synthetic(earpiece_record: dict) -> tuple[str, str]:
    """The explanatory question-answer pairs and the synthetic text Earpiece's functions used."""
    pairs, seen = [], set()
    for call in earpiece_record.get("model_calls", []):
        msgs = call.get("messages", [])
        if call.get("model_alias") is None or not msgs or msgs[0].get("role") != "system":
            continue                                   # the analyst's own call, not a function's
        for i in range(1, len(msgs) - 1):
            if msgs[i]["role"] == "system":
                break                                  # the worked examples ("how to answer") begin
            if msgs[i]["role"] == "user" and msgs[i + 1]["role"] == "assistant":
                q, a = msgs[i]["content"], msgs[i + 1]["content"]
                if q not in seen:
                    seen.add(q)
                    pairs.append(f"Q: {q.strip()}\nA: {a.strip()}")
    synthetic = "\n\n".join(t for t in earpiece_record.get("tool_results", []) if t)
    return "\n\n".join(pairs), synthetic


def information(level: int, raw: str, knowledge: str, synthetic: str) -> str:
    parts = ["## Data about the player\n" + raw]
    if level >= 2:
        parts.append("## What the data means\nExplanations of the qualities and metrics, as "
                     "question-and-answer pairs:\n\n" + (knowledge or "(none)"))
    if level >= 3:
        parts.append("## Rule-based description of this player's data\n" + (synthetic or "(none)"))
    return "\n\n".join(parts)


def parse(text: str) -> dict:
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        raise ValueError("no JSON in judge reply")
    out = json.loads(m.group(0))
    for k in ("faithfulness", "engagement", "usefulness"):
        out[k] = int(out[k])
        if not 1 <= out[k] <= 5:
            raise ValueError(f"{k} out of range")
    out["hallucinations"] = list(out.get("hallucinations") or [])
    return out


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--concurrency", type=int, default=10)
    args = ap.parse_args()

    client = anthropic.AsyncAnthropic(api_key=workspace_anthropic_key(), max_retries=6)
    raw = json.loads((DIR / "rawdata.json").read_text())
    answers = {s: [json.loads(l) for l in (DIR / f"answers-{s}.jsonl").open(encoding="utf-8")]
               for s in SYSTEMS if (DIR / f"answers-{s}.jsonl").exists()}
    ear1 = {(r["player_id"], r["question_id"]): r for r in answers["earpiece"] if r["repeat"] == 1}

    out = DIR / "judgments.jsonl"
    done = set()
    if out.exists():
        for line in out.open(encoding="utf-8"):
            j = json.loads(line)
            if "faithfulness" in j:                      # failed calls are tried again
                done.add((j["system"], j["player_id"], j["question_id"], j["repeat"], j["level"]))
    todo = [(s, a, lv) for s, rows in answers.items() for a in rows for lv in LEVELS
            if a.get("answer") and (a["player_id"], a["question_id"]) in ear1
            and (s, a["player_id"], a["question_id"], a["repeat"], lv) not in done]
    # Calls that share the same information run together, so the cached prefix is reused.
    todo.sort(key=lambda t: (t[1]["player_id"], t[2], t[1]["question_id"] if t[2] > 1 else 0,
                             t[1]["question_id"], t[0], t[1]["repeat"]))
    todo = todo[: args.limit] if args.limit else todo
    print(len(todo), "judgements to make")
    sem, lock = asyncio.Semaphore(args.concurrency), asyncio.Lock()
    stop = asyncio.Event()     # set when the API account has no credit: stop, record nothing

    async def judge(system, a, level):
        async with sem:
            if stop.is_set():
                return
            knowledge, synthetic = knowledge_and_synthetic(ear1[(a["player_id"], a["question_id"])])
            info = information(level, raw_text(raw[a["player_id"]]), knowledge, synthetic)
            content = [{"type": "text", "text": info, "cache_control": {"type": "ephemeral"}},
                       {"type": "text", "text": f"## Question\n{a['question']}\n\n## Answer\n"
                                                f"{strip_markdown(a['answer'])}"}]
            rec = {"system": system, "player_id": a["player_id"], "question_id": a["question_id"],
                   "repeat": a["repeat"], "level": level, "judge_model": JUDGE_MODEL}
            for attempt in range(3):
                try:
                    r = await client.messages.create(model=JUDGE_MODEL, max_tokens=3000,
                                                     system=JUDGE_SYSTEM,
                                                     messages=[{"role": "user", "content": content}])
                    text = "".join(b.text for b in r.content if b.type == "text")
                    rec.update(parse(text), raw_reply=text,
                               usage={k: v for k, v in r.usage.model_dump().items()
                                      if isinstance(v, int)})
                    break
                except Exception as err:  # pylint: disable=broad-except
                    if "credit balance is too low" in str(err):
                        stop.set()
                        return
                    rec["error"] = f"{type(err).__name__}: {err}"
            rec["date"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if "faithfulness" in rec:
                rec.pop("error", None)
            async with lock:
                with out.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    await asyncio.gather(*(judge(s, a, lv) for s, a, lv in todo))
    if stop.is_set():
        print("stopped: the API account has no credit")
        raise SystemExit(3)


if __name__ == "__main__":
    asyncio.run(main())
