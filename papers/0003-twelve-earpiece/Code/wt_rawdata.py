"""Save each test player's raw data, the information given to the judge at level 1.

Level 1 holds the data either system could draw on, so that a statement taken
from the data is not judged as invented. For each player in
`outputs/wordalisation-test/players.csv`:

- Earpiece's numbers: the season's quality and metric values with z-scores
  against players in the same position in the same competition
  (`get_processed_player_data`), and the zone-by-zone z-scores of each quality's
  pitch metric (`get_player_processed_pitch_metrics`, pitch and shot zones), which
  Earpiece's pitch descriptions use;
- the agents' data: the same fixed calls to Twelve's data tools for every player
  (biography, career by position, season metrics, defensive metrics, metrics by
  zone), as the agents' tools return them, written as "field: value" lines;
  the career and zone tables are cut at 6,000 and 8,000 characters.

No words, thresholds or explanations: those belong to levels 2 and 3.

Runs in the Earpiece API's environment:

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python <path>/Code/wt_rawdata.py

Writes `outputs/wordalisation-test/rawdata.json`.
"""

import asyncio
import csv
import importlib.util
import json
import math
from pathlib import Path

from config import config
from schemas.context import CompetitionSeason, PlayerPosition
from services.data_integration.data_api_client import DataAPIClient
from services.data_integration.specifications import set_data_functions_client
from services.data_integration.async_data_functions import AsyncTwelveDataFunctions
from services.workspaces_integration import WorkspacesClient, RegistryManager
from services.workspaces_integration.registry_manager import set_registry_manager

DIR = Path(__file__).resolve().parent / "outputs" / "wordalisation-test"
MCP_DATA = Path.home() / "GitHub" / "twelve-mcp-server" / "src" / "tools" / "data.py"
#: Characters kept of each tool's output, in compact "field: value" form. The season
#: aggregates are kept whole; long per-season and per-zone tables are cut.
TOOL_CHARS = {"get_players_by_id": None, "get_player_match_metrics": None,
              "get_player_match_metrics_defence": None, "get_player_career": 6000,
              "get_player_match_metrics_by_zone": 8000}


def compact(rows) -> str:
    """Tool rows as lines of "field: value", leaving out empty fields."""
    if isinstance(rows, dict):
        rows = [rows]
    lines = []
    for r in rows or []:
        if isinstance(r, dict):
            kept = [f"{k}: {v}" for k, v in r.items()
                    if v not in (None, "", [], {}) and not (isinstance(v, float) and math.isnan(v))]
            lines.append("; ".join(kept))
        else:
            lines.append(str(r))
    return "\n".join(lines) if lines else "(no rows)"
WORKSPACE = "wksp_aWsUNyFPMrVh5N"


def num(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), 3)


async def main():
    set_data_functions_client(AsyncTwelveDataFunctions(config.data_functions.token))
    api = DataAPIClient()
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
    customer_id = (await wc.get_workspace(WORKSPACE)).customer_id

    spec = importlib.util.spec_from_file_location("mcp_data_tools", MCP_DATA)
    data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data)
    data.init_data_functions(config.data_functions.token)
    pitch_metric = {}
    for q in registries.qualities.player_qualities:
        if getattr(q, "pitch_metric", None) is not None:
            pitch_metric[q.pitch_metric] = q.display_name

    out = {}
    for p in csv.DictReader((DIR / "players.csv").open(encoding="utf-8")):
        comp = CompetitionSeason(id=int(p["competition_id"]), year=int(p["season"]))
        df_m, df_q, _ = await api.get_processed_player_data(
            customer_id, comp, p["position"], comparison_player_id=int(p["player_id"]))
        mine_q = df_q[df_q["id"] == int(p["player_id"])]
        mine_m = df_m[df_m["id"] == int(p["player_id"])]
        players = await api.get_competition_players(customer_id, comp)
        row = players[players["id"] == int(p["player_id"])].iloc[0]
        full_name = str(row.get("full_name") or p["name"])
        zones = []
        for shot in (False, True):
            df_z, _ = await api.get_player_processed_pitch_metrics(
                customer_id, comp, p["position"], comparison_player_id=int(p["player_id"]),
                shot_zones=shot)
            df_z = df_z[(df_z["id"] == int(p["player_id"])) & df_z["kpi"].isin(list(pitch_metric))]
            for _, r in df_z.iterrows():
                zones.append({"quality": pitch_metric[r["kpi"]],
                              "metric": getattr(r["kpi"], "name", str(r["kpi"])),
                              "zone": getattr(r["zone"], "name", str(r["zone"])),
                              "z_score": num(r.get("value_z"))})
        pid, cid, yr = int(p["player_id"]), int(p["competition_id"]), int(p["season"])
        calls = {
            "get_players_by_id": dict(player_ids=[pid]),
            "get_player_career": dict(player_ids=pid, per_position=True),
            "get_player_match_metrics": dict(competition_ids=[cid], seasons=[yr], player_ids=[pid], per_match=False),
            "get_player_match_metrics_defence": dict(competition_ids=[cid], seasons=[yr], player_ids=[pid], per_match=False),
            "get_player_match_metrics_by_zone": dict(competition_ids=[cid], seasons=[yr], player_ids=[pid]),
        }
        tool_data = {}
        for name, kw in calls.items():
            try:
                text = compact(await getattr(data, name)(**kw))
                cap = TOOL_CHARS[name]
                tool_data[name] = text if cap is None or len(text) <= cap else text[:cap] + "\n(cut)"
            except Exception as err:  # pylint: disable=broad-except
                tool_data[name] = f"(not available: {type(err).__name__})"
        out[p["player_id"]] = {
            "player": p["name"], "full_name": full_name, "position": p["position"], "competition": p["competition"],
            "season": p["season"], "minutes": p["minutes"],
            "comparison": f"players in the same position in {p['competition']} {p['season']}",
            "qualities": [{"quality": getattr(r["kpi"], "display_name", str(r["kpi"])),
                           "z_score": num(r["value"])} for _, r in mine_q.iterrows()],
            "metrics": [{"metric": getattr(r["kpi"], "name", str(r["kpi"])),
                         "value": num(r.get("value")), "z_score": num(r.get("value_z"))}
                        for _, r in mine_m.iterrows()],
            "zones": zones,
            "tool_data": tool_data,
        }
        print(p["name"], len(out[p["player_id"]]["qualities"]), "qualities",
              len(out[p["player_id"]]["metrics"]), "metrics", len(zones), "zone values",
              {k: len(v) for k, v in tool_data.items()})
    (DIR / "rawdata.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
