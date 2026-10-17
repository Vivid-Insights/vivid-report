"""Ask the receptionist about each player in the name-test sample, and score it.

For every player in `outputs/name-test/sample.csv`, two questions, each once:
"How has {name} played this season?" with the misspelled name from
`outputs/name-test/misspellings.csv` and with the name as the data spells it. Each goes to the receptionist as the first message of a new
chat, as in the app (`ChatClient.initialize_chat`, after `analyst.prepare()`).

A run is scored from what the receptionist did:

- right: a redirect whose context holds the sampled player's id;
- wrong player: a redirect whose context holds another player;
- asked the user: the redirect's resolution declined ("Selection failed ...")
  and no redirect followed;
- other: anything else (no function called, another kind of redirect, an error).

The name the model put in the redirect's arguments is kept, since the model may
correct a spelling before the search ever sees it.

Runs in the Earpiece API's environment and can be stopped and restarted; runs
already in the output are skipped:

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python <path>/Code/name_test_run.py [--with-team] [--concurrency 6]

With `--with-team` the question is "How has {name} played for {team} this
season?", the team from `outputs/name-test/teams.csv`, misspelled or shortened in
the misspelled case.

Appends to `Code/outputs/name-test/runs-name.jsonl`, or `runs-team.jsonl` with
`--with-team`.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from config import config
from constants.permissions import ChatPermissionsEnum
from schemas.message import InternalMessageChunk, MessageRole
from schemas.user import User, WorkspaceInfo
from schemas.context import BaseContext
from services.chat_integration.chat_client import ChatClient, set_chat_client
from services.chat_integration.providers.factory import build_providers
from services.data_integration.data_api_client import DataAPIClient
from services.data_integration.specifications import (
    set_api_client,
    set_data_functions_client,
)
from services.data_integration.async_data_functions import AsyncTwelveDataFunctions
from services.knowledge_integration import KnowledgeClient
from services.workspaces_integration import WorkspacesClient, RegistryManager
from services.workspaces_integration.registry_manager import set_registry_manager
from analysts.receptionist.analyst import Receptionist

DIR = Path(__file__).resolve().parent / "outputs" / "name-test"
SAMPLE, MISSPELT, TEAMS = DIR / "sample.csv", DIR / "misspellings.csv", DIR / "teams.csv"
WORKSPACE = "wksp_aWsUNyFPMrVh5N"
PROVIDER = "wyscout"
QUESTION = "How has {name} played this season?"
QUESTION_TEAM = "How has {name} played for {team} this season?"


def dump(obj):
    return obj.model_dump(mode="json", exclude_none=True) if hasattr(obj, "model_dump") else obj


def score(chunks, truth: int):
    redirects = [c["redirect"] for c in chunks if isinstance(c.get("redirect"), dict)]
    tool_text = [c.get("content") or "" for c in chunks if c.get("role") == "tool"]
    for r in redirects:
        player = ((r.get("context") or {}).get("player") or {}).get("id")
        if player is not None:
            return ("right" if int(player) == truth else "wrong player"), r
    if any(t.startswith("Selection failed") for t in tool_text):
        return "asked the user", None
    return "other", (redirects[0] if redirects else None)


async def run_one(row, condition, clients, commit, lock, runs_file, with_team):
    chat, api, dfc, kc, wc = clients
    name = row["misspelled"] if condition == "misspelled" else row["name"]
    if with_team:
        team = row["team_error"] if condition == "misspelled" else row["team"]
        question = QUESTION_TEAM.format(name=name, team=team)
    else:
        question = QUESTION.format(name=name)
    user = User(id="vivid-report", roles=["user"],
                permissions=[p.value for p in ChatPermissionsEnum], customer_id="",
                workspaces=[WorkspaceInfo(id=WORKSPACE, name="Default Earpiece")])

    async def no_save(payload):
        raise RuntimeError("not used")

    async def no_consumption(*args, **kwargs):
        return None

    analyst = Receptionist(BaseContext(query=None, summary=None), user, api, dfc, chat, kc,
                           no_save, no_consumption, workspaces_client=wc,
                           workspace_id=WORKSPACE, data_provider=PROVIDER)
    chunks, error = [], None
    try:
        await analyst.prepare()
        first = InternalMessageChunk(index=0, role=MessageRole.USER, content=question)
        async for chunk in chat.initialize_chat(analyst, first_message=first):
            chunks.append(dump(chunk))
    except Exception as err:  # pylint: disable=broad-except
        error = f"{type(err).__name__}: {err}"
    outcome, redirect = score(chunks, int(row["player_id"]))
    calls = [tc for c in chunks if c.get("role") == "assistant"
             for tc in (c.get("tool_calls") or [])]
    reply = "".join(c.get("content") or "" for c in chunks
                    if c.get("role") == "assistant" and not c.get("is_reasoning"))
    record = {
        "player_id": int(row["player_id"]), "condition": condition, "question": question,
        "outcome": outcome if error is None else "other",
        "redirect": redirect, "tool_calls": calls,
        "tool_results": [c.get("content") for c in chunks if c.get("role") == "tool"],
        "reply": reply, "error": error,
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "earpiece_api_commit": commit,
    }
    async with lock:
        with runs_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{row['player_id']:>8} {condition:<10} {record['outcome']:<15} {name}")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=6)
    parser.add_argument("--limit", type=int, default=None, help="only the first N runs")
    parser.add_argument("--with-team", action="store_true",
                        help="name the player's team too (misspelled or shortened in the error case)")
    args = parser.parse_args()

    chat = ChatClient(build_providers(config.llm.models)); set_chat_client(chat)
    api = DataAPIClient(); set_api_client(api)
    dfc = AsyncTwelveDataFunctions(config.data_functions.token); set_data_functions_client(dfc)
    kc = KnowledgeClient(config.knowledge_api.base_url, timeout=10.0)
    wc = WorkspacesClient(base_url=config.workspaces_api.base_url,
                          auth0_domain=config.auth0.domain,
                          client_id=config.auth0_mtm.client_id,
                          client_secret=config.auth0_mtm.client_secret,
                          audience=config.workspaces_api.audience)
    await wc.initialize()
    registries = RegistryManager(wc); await registries.initialize()
    set_registry_manager(registries)
    api._metric_registry = registries.metrics
    api._quality_registry = registries.qualities
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                            text=True).stdout.strip()

    rows = list(csv.DictReader(SAMPLE.open(encoding="utf-8")))
    wrong = {r["player_id"]: r["misspelled"] for r in csv.DictReader(MISSPELT.open(encoding="utf-8"))}
    for row in rows:
        row["misspelled"] = wrong[row["player_id"]]
    if args.with_team:
        teams = {r["player_id"]: r for r in csv.DictReader(TEAMS.open(encoding="utf-8"))}
        for row in rows:
            row.update({k: teams[row["player_id"]][k] for k in ("team", "team_error")})
    RUNS = DIR / ("runs-team.jsonl" if args.with_team else "runs-name.jsonl")
    done = set()
    if RUNS.exists():
        for line in RUNS.open(encoding="utf-8"):
            r = json.loads(line)
            done.add((r["player_id"], r["condition"]))
    todo = [(row, cond) for row in rows for cond in ("misspelled", "correct")
            if (int(row["player_id"]), cond) not in done]
    todo = todo[:args.limit] if args.limit else todo
    print(len(todo), "runs to do")

    sem, lock = asyncio.Semaphore(args.concurrency), asyncio.Lock()

    async def guarded(row, cond):
        async with sem:
            await run_one(row, cond, (chat, api, dfc, kc, wc), commit, lock, RUNS, args.with_team)

    await asyncio.gather(*(guarded(r, c) for r, c in todo))


if __name__ == "__main__":
    asyncio.run(main())
