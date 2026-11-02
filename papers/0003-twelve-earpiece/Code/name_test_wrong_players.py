"""Name the player each wrong-player run of the name test resolved to.

A run is scored "wrong player" when the redirect's context holds another player's
id; this looks that player up, so the report can say who Earpiece chose. Runs in
the Earpiece API's environment:

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python <path>/Code/name_test_wrong_players.py

Reads `outputs/name-test/sample.csv`, `runs-name.jsonl` and `runs-team.jsonl`;
writes `outputs/name-test/wrong-players.csv`.
"""

import asyncio
import csv
import json
from pathlib import Path

from config import config
from schemas.context import CompetitionSeason, PlayerPosition
from services.data_integration.data_api_client import DataAPIClient
from services.data_integration.specifications import set_data_functions_client
from services.data_integration.async_data_functions import AsyncTwelveDataFunctions
from services.workspaces_integration import WorkspacesClient

DIR = Path(__file__).resolve().parent / "outputs" / "name-test"
WORKSPACE = "wksp_aWsUNyFPMrVh5N"


async def main():
    set_data_functions_client(AsyncTwelveDataFunctions(config.data_functions.token))
    api = DataAPIClient()
    wc = WorkspacesClient(base_url=config.workspaces_api.base_url,
                          auth0_domain=config.auth0.domain,
                          client_id=config.auth0_mtm.client_id,
                          client_secret=config.auth0_mtm.client_secret,
                          audience=config.workspaces_api.audience)
    await wc.initialize()
    customer_id = (await wc.get_workspace(WORKSPACE)).customer_id
    sample = {r["player_id"]: r for r in csv.DictReader((DIR / "sample.csv").open(encoding="utf-8"))}
    rows = []
    for variant in ("name", "team"):
        for line in (DIR / f"runs-{variant}.jsonl").open(encoding="utf-8"):
            r = json.loads(line)
            if r["outcome"] != "wrong player":
                continue
            ctx = r["redirect"]["context"]
            s = sample[str(r["player_id"])]
            try:
                p = await api.get_player(customer_id, CompetitionSeason(**ctx["competition"]),
                                         PlayerPosition(**ctx["player"]))
                got, team, short = p.full_name, getattr(p.team, "name", ""), getattr(p, "name", "")
            except Exception as err:  # pylint: disable=broad-except
                got, team, short = f"lookup failed: {type(err).__name__}", "", ""
            rows.append({"variant": variant, "condition": r["condition"], "question": r["question"],
                         "player_id": s["player_id"], "name": s["name"],
                         "competition": s["competition"], "season": s["season"],
                         "resolved_id": ctx["player"]["id"], "resolved_name": got, "resolved_short_name": short,
                         "resolved_team": team, "resolved_competition_id": ctx["competition"]["id"]})
    with (DIR / "wrong-players.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "wrong-player runs named")


if __name__ == "__main__":
    asyncio.run(main())
