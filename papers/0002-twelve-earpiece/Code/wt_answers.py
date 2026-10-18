"""Answer the ten test questions about each test player with one of three systems.

The wordalisation test (David, 18 October 2026). Ten fixed questions about each
player in `outputs/wordalisation-test/players.csv`, three repeats each, from:

- earpiece: the Scout, opened in the player's context as the app opens a chat
  (`analyst.prepare()`, then `ChatClient.initialize_chat` with the question as the
  first message). Its functions choose and write the answer. The functions' own
  model calls are kept, because their question-answer pairs and synthetic texts
  are what the judge is given at levels 2 and 3.
- claude: Claude Opus 5.5 with Twelve's raw data tools, and nothing else: no
  Earpiece description tools, no knowledge tools. The tools are the data tools of
  Twelve's MCP server (`twelve-mcp-server/src/tools/data.py`), with the names,
  descriptions and parameters the server lists, run in-process on the same data
  functions rather than through the server's login.
- gpt4o: GPT-4o (Azure) with the same tools.

Both agents get the same context (player, id, position, competition, season) and
the system prompt "You are a football analyst. Answer using the tools. Answer in
exactly {n} sentences, in plain prose.", where n is the number of sentences in Earpiece's answer to the
same question about the same player in the same repeat (David, 18 October
2026) -- no other preprompting. Earpiece is therefore run first.

Runs in the Earpiece API's environment and can be resumed:

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python <path>/Code/wt_answers.py --system earpiece|claude|gpt4o \
        [--players N] [--repeats 3] [--concurrency 4]

Appends to `outputs/wordalisation-test/answers-<system>.jsonl`.
"""

from __future__ import annotations

import argparse
import os
import asyncio
import importlib.util
import re
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from openai import AsyncAzureOpenAI

from config import config
from constants.permissions import ChatPermissionsEnum
from schemas.context import PlayerEvaluationContext
from schemas.message import InternalMessageChunk, MessageRole
from schemas.user import User, WorkspaceInfo
from services.chat_integration.chat_client import ChatClient, set_chat_client
from services.chat_integration.providers.factory import build_providers
from services.data_integration.data_api_client import DataAPIClient
from services.data_integration.specifications import set_api_client, set_data_functions_client
from services.data_integration.async_data_functions import AsyncTwelveDataFunctions
from services.knowledge_integration import KnowledgeClient
from services.mcp_integration.mcp_client import MCPClientManager
from services.workspaces_integration import WorkspacesClient, RegistryManager
from services.workspaces_integration.registry_manager import set_registry_manager
from analysts.player.scout.analyst import Scout


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
WORKSPACE = "wksp_aWsUNyFPMrVh5N"
QUESTIONS = [
    "Give me a summary of {name}'s season.",
    "What are {name}'s strengths and weaknesses?",
    "How good is {name} at passing?",
    "How good is {name} at dribbling?",
    "Is {name} a threat in the box?",
    "Where on the pitch does {name} win the ball back?",
    "Could {name} play in a different position?",
    "How good is {name} at pressing?",
    "How good is {name} in the air?",
    "Does {name} get involved in games?",
]
AGENT_SYSTEM = ("You are a football analyst. Answer using the tools. "
                "Answer in exactly {n} sentences, in plain prose.")
MCP_DATA = Path.home() / "GitHub" / "twelve-mcp-server" / "src" / "tools" / "data.py"
CLAUDE_MODEL = "claude-opus-5-5"
#: Tools the agents may not use: Earpiece's own (descriptions, predictions) and the
#: knowledge tools, which explain the qualities in Earpiece's terms.
KNOWLEDGE_TOOLS = {"get_glossary", "search_knowledge", "get_player_position_information"}
MAX_TOOL_ROUNDS = 15
MAX_TOOL_TEXT = 20000


def dump(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json", exclude_none=True)
    if isinstance(obj, (list, tuple)):
        return [dump(o) for o in obj]
    if isinstance(obj, dict):
        return {k: dump(v) for k, v in obj.items()}
    return obj


def allowed(name: str) -> bool:
    return (not name.startswith("earpiece_") and name not in KNOWLEDGE_TOOLS
            and not name.endswith("_qualities_information"))


def count_sentences(text: str) -> int:
    """Sentences in an answer: text ending in . ! or ? followed by a space or the end."""
    parts = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    return max(1, len(parts))


def load_mcp_data(token: str):
    spec = importlib.util.spec_from_file_location("mcp_data_tools", MCP_DATA)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.init_data_functions(token)
    return module


def context_line(p: dict) -> str:
    return (f"The player is {p['name']} (player id {p['player_id']}), a "
            f"{p['position'].replace('_', ' ').lower()} in {p['competition']} "
            f"(competition id {p['competition_id']}), season {p['season']}.")


# ── Earpiece ──────────────────────────────────────────────────────────────────

async def ask_earpiece(p, question, env):
    chat, api, dfc, kc, wc = env["chat"], env["api"], env["dfc"], env["kc"], env["wc"]
    calls: list[dict] = []
    stream, no_stream = chat.generate_stream, chat.generate_no_stream

    user = User(id="vivid-report", roles=["user"], customer_id="",
                permissions=[x.value for x in ChatPermissionsEnum],
                workspaces=[WorkspaceInfo(id=WORKSPACE, name="Default Earpiece")])

    async def no_save(payload):
        raise RuntimeError("not used")

    async def no_consumption(*a, **k):
        return None

    ctx = PlayerEvaluationContext(query=None, summary=None,
                                  competition={"id": int(p["competition_id"]), "year": int(p["season"])},
                                  player={"id": int(p["player_id"]), "position": p["position"]})
    analyst = Scout(ctx, user, api, dfc, chat, kc, no_save, no_consumption,
                    workspaces_client=wc, workspace_id=WORKSPACE, data_provider="wyscout")
    await analyst.prepare()
    chunks = []

    # Record every model call this turn makes (the analyst's and each function's own).
    class Rec:
        async def generate_stream(self, messages, *args, **kwargs):
            call = {"model_alias": kwargs.get("model_alias"), "temperature": kwargs.get("temperature"),
                    "messages": dump(messages), "output": ""}
            calls.append(call)
            async for chunk in stream(messages, *args, **kwargs):
                if chunk.content:
                    call["output"] += chunk.content
                yield chunk

    chat_local = ChatClient(chat.providers)
    chat_local.generate_stream = Rec().generate_stream
    chat_local.generate_no_stream = no_stream
    analyst.chat_client = chat_local
    for fn in analyst.functions:
        if hasattr(fn, "chat_client"):
            fn.chat_client = chat_local
    first = InternalMessageChunk(index=0, role=MessageRole.USER, content=question)
    async for chunk in chat_local.initialize_chat(analyst, first_message=first):
        chunks.append(dump(chunk))
    replies: dict[int, str] = {}
    for c in chunks:
        if c.get("role") == "assistant" and c.get("content") and not c.get("is_reasoning"):
            replies[c["index"]] = replies.get(c["index"], "") + c["content"]
    return {
        "answer": "\n\n".join(replies[i] for i in sorted(replies)),
        "functions": [tc.get("function", {}).get("name") for c in chunks
                      if c.get("role") == "assistant" for tc in (c.get("tool_calls") or [])],
        "tool_results": [c.get("content") for c in chunks if c.get("role") == "tool"],
        "model_calls": calls,
    }


# ── Agents ────────────────────────────────────────────────────────────────────

async def call_tool(env, name, args):
    if not allowed(name):
        return f"Tool {name} is not available."
    fn = getattr(env["data"], name, None)
    if fn is None:
        return f"Tool {name} is not available."
    try:
        text = json.dumps(await fn(**args), ensure_ascii=False, default=str)
    except Exception as err:  # pylint: disable=broad-except
        text = f"Tool error: {type(err).__name__}: {err}"
    return text[:MAX_TOOL_TEXT]


async def ask_claude(p, question, env, n):
    client, tools = env["anthropic"], env["anthropic_tools"]
    messages = [{"role": "user", "content": context_line(p) + "\n\n" + question}]
    trace = []
    for _ in range(MAX_TOOL_ROUNDS):
        r = await client.messages.create(model=CLAUDE_MODEL, max_tokens=2000,
                                         system=AGENT_SYSTEM.format(n=n),
                                         tools=tools, messages=messages)
        messages.append({"role": "assistant", "content": [b.model_dump() for b in r.content]})
        uses = [b for b in r.content if b.type == "tool_use"]
        if not uses:
            text = "".join(b.text for b in r.content if b.type == "text")
            return {"answer": text, "tool_calls": trace}
        results = []
        for u in uses:
            out = await call_tool(env, u.name, u.input)
            trace.append({"tool": u.name, "args": u.input, "result_chars": len(out)})
            results.append({"type": "tool_result", "tool_use_id": u.id, "content": out})
        messages.append({"role": "user", "content": results})
    return {"answer": "", "tool_calls": trace, "error": "too many tool rounds"}


async def ask_gpt4o(p, question, env, n):
    client, tools, model = env["azure"], env["openai_tools"], env["azure_model"]
    messages = [{"role": "system", "content": AGENT_SYSTEM.format(n=n)},
                {"role": "user", "content": context_line(p) + "\n\n" + question}]
    trace = []
    for _ in range(MAX_TOOL_ROUNDS):
        r = await client.chat.completions.create(model=model, messages=messages, tools=tools)
        m = r.choices[0].message
        messages.append(m.model_dump(exclude_none=True))
        if not m.tool_calls:
            return {"answer": m.content or "", "tool_calls": trace}
        for tc in m.tool_calls:
            args = json.loads(tc.function.arguments or "{}")
            out = await call_tool(env, tc.function.name, args)
            trace.append({"tool": tc.function.name, "args": args, "result_chars": len(out)})
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": out})
    return {"answer": "", "tool_calls": trace, "error": "too many tool rounds"}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", required=True, choices=["earpiece", "claude", "gpt4o"])
    ap.add_argument("--players", type=int, default=None, help="only the first N players")
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args()

    env: dict = {}
    if args.system == "earpiece":
        chat = ChatClient(build_providers(config.llm.models)); set_chat_client(chat)
        api = DataAPIClient(); set_api_client(api)
        dfc = AsyncTwelveDataFunctions(config.data_functions.token); set_data_functions_client(dfc)
        wc = WorkspacesClient(base_url=config.workspaces_api.base_url, auth0_domain=config.auth0.domain,
                              client_id=config.auth0_mtm.client_id,
                              client_secret=config.auth0_mtm.client_secret,
                              audience=config.workspaces_api.audience)
        await wc.initialize()
        reg = RegistryManager(wc); await reg.initialize(); set_registry_manager(reg)
        api._metric_registry, api._quality_registry = reg.metrics, reg.qualities
        env.update(chat=chat, api=api, dfc=dfc, wc=wc,
                   kc=KnowledgeClient(config.knowledge_api.base_url, timeout=10.0))
        ask = ask_earpiece
    else:
        # Schemas as the server lists them; execution in-process on the same functions.
        mcp = MCPClientManager(server_url=config.mcp.server_url, auth_token=config.guest.token)
        data = load_mcp_data(config.data_functions.token)
        openai_tools = [t for t in await mcp.get_tools()
                        if allowed(t["function"]["name"]) and hasattr(data, t["function"]["name"])]
        env.update(data=data, openai_tools=openai_tools)
        print(len(openai_tools), "data tools:", sorted(t["function"]["name"] for t in openai_tools))
        sentences = {}
        for line in (DIR / "answers-earpiece.jsonl").open(encoding="utf-8"):
            r = json.loads(line)
            sentences[(r["player_id"], r["question_id"], r["repeat"])] = count_sentences(r["answer"])
        env["sentences"] = sentences
        if args.system == "claude":
            env["anthropic"] = anthropic.AsyncAnthropic(api_key=workspace_anthropic_key())
            env["anthropic_tools"] = [{"name": t["function"]["name"],
                                       "description": t["function"].get("description", "")[:1000],
                                       "input_schema": t["function"]["parameters"]} for t in openai_tools]
            ask = ask_claude
        else:
            m = next(c for c in config.llm.models if c.alias == "azure-4o")
            env["azure"] = AsyncAzureOpenAI(api_key=m.api_key, azure_endpoint=m.azure_endpoint,
                                            api_version=m.azure_api_version)
            env["azure_model"] = m.model_name
            ask = ask_gpt4o

    out = DIR / f"answers-{args.system}.jsonl"
    done = set()
    if out.exists():
        for line in out.open(encoding="utf-8"):
            r = json.loads(line)
            done.add((r["player_id"], r["question_id"], r["repeat"]))
    players = list(csv.DictReader((DIR / "players.csv").open(encoding="utf-8")))[: args.players]
    todo = [(p, qi, k) for p in players for qi in range(len(QUESTIONS))
            for k in range(1, args.repeats + 1) if (p["player_id"], qi + 1, k) not in done]
    print(len(todo), "answers to make")
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                            text=True).stdout.strip()
    sem, lock = asyncio.Semaphore(args.concurrency), asyncio.Lock()
    stop = asyncio.Event()     # set when the API account has no credit: stop, record nothing

    async def one(p, qi, k):
        async with sem:
            if stop.is_set():
                return
            question = QUESTIONS[qi].format(name=p["name"])
            n = None
            if args.system != "earpiece":
                n = env["sentences"].get((p["player_id"], qi + 1, k))
                if n is None:
                    print(f"skipped {p['name']} q{qi + 1} r{k}: no Earpiece answer yet")
                    return
            try:
                got = await (ask(p, question, env) if n is None else ask(p, question, env, n))
            except Exception as err:  # pylint: disable=broad-except
                if "credit balance is too low" in str(err):
                    stop.set()
                    return
                got = {"answer": "", "error": f"{type(err).__name__}: {err}"}
            rec = {"system": args.system, "player_id": p["player_id"], "question_id": qi + 1,
                   "repeat": k, "question": question, "sentences_asked": n, **got,
                   "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                   "earpiece_api_commit": commit}
            async with lock:
                with out.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            print(f"{args.system} {p['name']} q{qi + 1} r{k}: {len(got.get('answer', ''))} chars"
                  + (f" ERROR {got['error'][:80]}" if got.get("error") else ""))

    await asyncio.gather(*(one(p, qi, k) for p, qi, k in todo))
    if stop.is_set():
        print("stopped: the API account has no credit")
        raise SystemExit(3)


if __name__ == "__main__":
    asyncio.run(main())
