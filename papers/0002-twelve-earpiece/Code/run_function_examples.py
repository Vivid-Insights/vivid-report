"""Run Earpiece analysts on the Results examples and save every model call.

Each example is one user question put to one analyst in one context, as a user of
Earpiece would ask it after the redirect. The analyst's own model chooses the
function; nothing here calls a function directly. Every call to a model --
the analyst's, and the separate call a function makes to write its reply -- is
recorded with its messages, tools, model and output.

It runs inside the Earpiece API's own environment, not this workspace's, because it
imports the API's code and reads its `conf/dev.env`:

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python \
        ~/GitHub/vivid-report/papers/0002-twelve-earpiece/Code/run_function_examples.py [example ...] [--repeats N]

Writes `Code/outputs/function-examples/<example>-<run>.json` and a readable
`<example>-<run>.md` beside it: the function chosen, the text the function gave
the model (the synthetic text), and the reply the user reads.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from config import config
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
from schemas.context import (
    CompetitionSeason,
    PlayerEvaluationContext,
    PlayerTransferContext,
)
from schemas.message import InternalMessageChunk, MessageRole
from schemas.user import User, WorkspaceInfo
from constants.permissions import ChatPermissionsEnum
from analysts.player.scout.analyst import Scout
from analysts.player.transfer.analyst import Transfer
from analysts.season.analysis.analyst import SeasonAnalyst
from schemas.context import SeasonEvaluationContext
from services.workspaces_integration.schemas import ProviderWorkspaceTeamSummary

OUT = Path(__file__).resolve().parent / "outputs" / "function-examples"
API_REPO = Path.cwd()

#: The Default Earpiece workspace, which Earpiece's own tests use.
WORKSPACE = "wksp_aWsUNyFPMrVh5N"
PROVIDER = "wyscout"

#: The player and competitions of the four-question walk in the paper
#: (Code/fig_conversation_walk.py), looked up in the data on 14 October 2026.
DAMALLSVENSKAN_2026 = {"id": 809, "year": 2026}
WSL_2026 = {"id": 368, "year": 2026}
KOIVISTO = {"id": 545691, "position": "MIDFIELDER"}
ARSENAL = {"id": 1934}

#: A workspace written for this paper, not a club's own. Earpiece rewrites a team
#: text only for the workspace's own club, and no workspace we may publish has
#: Arsenal as its club, so the "rewrite" example replaces the workspace summary
#: with this one. Its style and objectives are David's words (14 October 2026).
#: The name is the club's because the rewrite prompt uses the workspace name as
#: the team's name.
STANDIN_WORKSPACE = {
    "name": "Arsenal",
    "style_of_play": "Control play.",
    "objectives": "Win the league.",
    "provider_teams": [ProviderWorkspaceTeamSummary(provider_key=PROVIDER,
                                                    provider_team_id=str(ARSENAL["id"]))],
}

#: name -> (analyst class, context, question). The question is what the user types.
EXAMPLES = {
    "quality": (
        Scout,
        lambda top: PlayerEvaluationContext(
            query=None, summary=None,
            competition=DAMALLSVENSKAN_2026, player=KOIVISTO,
        ),
        # David's wording (14 October 2026); involvement is her highest-rated quality.
        "Does she get involved in games?",
    ),
    "transfer": (
        Transfer,
        lambda top: PlayerTransferContext(
            query=None, summary=None,
            competition=DAMALLSVENSKAN_2026, player=KOIVISTO,
            other_competition=WSL_2026,
        ),
        "Could she play in WSL?",
    ),
    "skills2": (
        Scout,
        lambda top: PlayerEvaluationContext(
            query=None, summary=None,
            competition=DAMALLSVENSKAN_2026, player=KOIVISTO,
        ),
        # An example question from player_answer_skills_question's description.
        "What are the player's weaknesses?",
    ),
    "rewrite": (
        SeasonAnalyst,
        lambda top: SeasonEvaluationContext(
            query=None, summary=None, competition=WSL_2026, team=ARSENAL,
        ),
        # The fourth question of the walk in the paper.
        "How has Arsenal's season progressed?",
    ),
    "similar": (
        Scout,
        lambda top: PlayerEvaluationContext(
            query=None, summary=None,
            competition=DAMALLSVENSKAN_2026, player=KOIVISTO,
        ),
        "Can you find players similar to her?",
    ),
}


def dump(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump(mode="json", exclude_none=True)
    if isinstance(obj, (list, tuple)):
        return [dump(o) for o in obj]
    if isinstance(obj, dict):
        return {k: dump(v) for k, v in obj.items()}
    return obj


class Recorder:
    """Wraps the chat client's two model entry points and keeps every call."""

    def __init__(self, chat: ChatClient):
        self.calls: list[dict] = []
        stream, no_stream = chat.generate_stream, chat.generate_no_stream

        def model_of(kwargs):
            try:
                p = chat._resolve_provider(kwargs.get("analyst"), kwargs.get("model_alias"))
                return f"{p.config.provider}/{p.config.model_name} (alias {p.config.alias})"
            except Exception as err:  # pylint: disable=broad-except
                return f"unresolved: {err}"

        async def rec_stream(messages, *args, **kwargs):
            call = {"kind": "stream", "model": model_of(kwargs),
                    "temperature": kwargs.get("temperature"),
                    "tools": [t["function"]["name"] for t in (kwargs.get("tools") or [])
                              if isinstance(t, dict) and "function" in t],
                    "messages": dump(messages), "output": "", "tool_calls": []}
            self.calls.append(call)
            async for chunk in stream(messages, *args, **kwargs):
                if chunk.content:
                    call["output"] += chunk.content
                if getattr(chunk, "tool_calls", None):
                    call["tool_calls"].append(dump(chunk.tool_calls))
                yield chunk

        async def rec_no_stream(messages, *args, **kwargs):
            result = await no_stream(messages, *args, **kwargs)
            self.calls.append({"kind": "no_stream", "model": model_of(kwargs),
                               "temperature": kwargs.get("temperature"),
                               "messages": dump(messages), "output": dump(result)})
            return result

        chat.generate_stream = rec_stream
        chat.generate_no_stream = rec_no_stream


async def top_quality(api, customer_id, registries) -> str:
    """Koivisto's highest-rated quality in the context: the rule for the quality example."""
    ctx = PlayerEvaluationContext(query=None, summary=None,
                                  competition=DAMALLSVENSKAN_2026, player=KOIVISTO)
    _, df_q, _ = await api.get_processed_player_data(
        customer_id, ctx.competition, ctx.player.position,
        comparison_player_id=ctx.player.id, provider=PROVIDER,
    )
    mine = df_q[df_q["id"] == KOIVISTO["id"]].sort_values("value", ascending=False)
    return mine.iloc[0]["kpi"].display_name.lower()


async def run_one(name, run, clients, top):
    chat, api, dfc, kc, wc = clients
    analyst_cls, make_ctx, question = EXAMPLES[name]
    question = question.format(top=top)
    recorder = Recorder(chat)
    user = User(id="vivid-report", roles=["user"],
                permissions=[p.value for p in ChatPermissionsEnum],
                customer_id="", workspaces=[WorkspaceInfo(id=WORKSPACE, name="Default Earpiece")])

    async def no_save(payload):  # the report examples are not run here
        raise RuntimeError("save_report not available in this script")

    async def no_consumption(*args, **kwargs):
        return None

    real_get_workspace = wc.get_workspace
    if name == "rewrite":
        async def standin(workspace_id):
            summary = await real_get_workspace(workspace_id)
            return summary.model_copy(update=STANDIN_WORKSPACE)
        wc.get_workspace = standin

    analyst = analyst_cls(make_ctx(top), user, api, dfc, chat, kc, no_save, no_consumption,
                          workspaces_client=wc, workspace_id=WORKSPACE, data_provider=PROVIDER)
    # As message_stream_handler does before every turn: loads the registries that
    # fill each function's list of allowed qualities.
    await analyst.prepare()

    # The app's own path for a new chat with a typed first message: it adds the
    # system message (date, the analyst's instructions and the selected context).
    first = InternalMessageChunk(index=0, role=MessageRole.USER, content=question)
    chunks = []
    try:
        async for chunk in chat.initialize_chat(analyst, first_message=first):
            chunks.append(dump(chunk))
    finally:
        wc.get_workspace = real_get_workspace

    # Replies are grouped by chunk index: one function's reply is one message.
    replies: dict[int, str] = {}
    for c in chunks:
        if c.get("role") == "assistant" and c.get("content") and not c.get("is_reasoning"):
            replies[c["index"]] = replies.get(c["index"], "") + c["content"]
    shown = "\n\n".join(replies[i] for i in sorted(replies))
    tool_msgs = [c for c in chunks if c.get("role") == "tool"]
    chosen = [tc for c in chunks if c.get("role") == "assistant"
              for tc in (c.get("tool_calls") or [])]
    record = {
        "example": name, "run": run, "question": question,
        "analyst": analyst.name, "context": dump(analyst.context),
        "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "earpiece_api_commit": subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                              capture_output=True, text=True,
                                              cwd=API_REPO).stdout.strip(),
        "workspace": WORKSPACE,
        "standin_workspace": ({k: dump(v) for k, v in STANDIN_WORKSPACE.items()}
                              if name == "rewrite" else None),
        "functions_offered": [f["function"]["name"] for f in analyst.construct_function_schema()],
        "tool_calls": chosen, "tool_results": tool_msgs,
        "reply_shown_to_user": shown, "replies": [replies[i] for i in sorted(replies)],
        "model_calls": recorder.calls, "stream": chunks,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    stem = OUT / f"{name}-{run}"
    stem.with_suffix(".json").write_text(json.dumps(record, indent=2, ensure_ascii=False))

    names = []
    for tc in chosen:
        fn = tc.get("function", {}) if isinstance(tc, dict) else {}
        if fn.get("name"):
            names.append(f"{fn['name']}({fn.get('arguments', '')})")
    synthetic = "\n\n".join(m.get("content") or "" for m in tool_msgs)
    stem.with_suffix(".md").write_text(
        f"Question: {question}\n\nAnalyst: {analyst.name}\n\n"
        f"Functions called: {'; '.join(names) or 'none'}\n\n"
        f"## Function output given to the model\n\n{synthetic}\n\n"
        f"## Reply shown to the user\n\n{shown}\n"
    )
    print(f"{stem.name}: {', '.join(names) or 'no function'}")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("examples", nargs="*", default=list(EXAMPLES))
    parser.add_argument("--repeats", type=int, default=3)
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
    set_registry_manager(registries)  # as main.py's lifespan does
    api._metric_registry = registries.metrics
    api._quality_registry = registries.qualities
    customer_id = (await wc.get_workspace(WORKSPACE)).customer_id

    top = await top_quality(api, customer_id, registries)
    print("Koivisto's highest-rated quality:", top)
    for name in args.examples:
        for run in range(1, args.repeats + 1):
            await run_one(name, run, (chat, api, dfc, kc, wc), top)


if __name__ == "__main__":
    asyncio.run(main())
