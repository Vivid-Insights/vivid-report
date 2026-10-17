"""Draw the players for the name test.

The sample, as agreed with David on 17 October 2026: 300 men and 100 women from
Earpiece's own data, so each comes with the player id a correct resolution must
reach. Domestic adult leagues only, each in its latest season (2025 or 2026), with
at least 450 minutes played, leaving out the best-known top divisions: the men's
Big Five (England, Spain, Italy, Germany, France) and the women's top divisions of
England, the United States, Spain, Germany and France. Competitions are shuffled
with a fixed seed and up to three players drawn from each, so no league dominates.

The misspellings are made separately, by name_test_misspell.py, so that
changing the error model never changes the sample.

Runs in the Earpiece API's environment:

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python <path>/Code/name_test_sample.py

Writes `Code/outputs/name-test/sample.csv`.
"""

from __future__ import annotations

import asyncio
import csv
import random
from pathlib import Path

from config import config
from schemas.context import CompetitionSeason
from services.data_integration.data_api_client import DataAPIClient
from services.data_integration.specifications import set_data_functions_client
from services.data_integration.async_data_functions import AsyncTwelveDataFunctions
from services.workspaces_integration import WorkspacesClient

OUT = Path(__file__).resolve().parent / "outputs" / "name-test" / "sample.csv"
WORKSPACE = "wksp_aWsUNyFPMrVh5N"
SEED = 2026
WANT = {"male": 300, "female": 100}
PER_COMPETITION = 3
MIN_MINUTES = 450
SEASONS = (2025, 2026)
EXCLUDED_TOP = {
    "male": {"England", "Spain", "Italy", "Germany", "France"},
    "female": {"England", "United States", "USA", "Spain", "Germany", "France"},
}
def typed_name(row) -> str:
    """The name a user would type: the short name unless it is abbreviated."""
    name = str(row.get("name") or "").strip()
    full = str(row.get("full_name") or "").strip()
    return full if ("." in name or not name) and full else name


async def main():
    rng = random.Random(SEED)
    set_data_functions_client(AsyncTwelveDataFunctions(config.data_functions.token))
    api = DataAPIClient()
    wc = WorkspacesClient(base_url=config.workspaces_api.base_url,
                          auth0_domain=config.auth0.domain,
                          client_id=config.auth0_mtm.client_id,
                          client_secret=config.auth0_mtm.client_secret,
                          audience=config.workspaces_api.audience)
    await wc.initialize()
    customer_id = (await wc.get_workspace(WORKSPACE)).customer_id

    comps = await api.get_competitions(customer_id)
    league = comps["domestic_league"].astype(object).to_numpy(dtype=bool)
    youth = comps["youth"].astype(object).to_numpy(dtype=bool)
    in_season = comps["year"].astype(int).isin(SEASONS).to_numpy()
    comps = comps[league & ~youth & in_season]
    comps = comps.sort_values("year").drop_duplicates("id", keep="last")  # latest season

    rows = []
    for gender, want in WANT.items():
        is_female = comps["gender"].astype(object).map(
            lambda g: "FEMALE" in str(g).upper()).to_numpy(dtype=bool)
        pool = comps[is_female if gender == "female" else ~is_female]
        top = ((pool["division"].astype(int) == 1).to_numpy()
               & pool["country"].astype(str).isin(EXCLUDED_TOP[gender]).to_numpy())
        pool = pool[~top]
        order = sorted(pool["id"].tolist())
        rng.shuffle(order)
        taken = []
        for comp_id in order:
            if len(taken) >= want:
                break
            comp = pool[pool["id"] == comp_id].iloc[0]
            try:
                players = await api.get_competition_players(
                    customer_id, CompetitionSeason(id=int(comp_id), year=int(comp["year"])))
            except Exception:  # pylint: disable=broad-except
                continue
            if "minutes" not in players.columns:
                continue
            players = players[players["minutes"] >= MIN_MINUTES]
            if players.empty:
                continue
            ids = sorted(players["id"].tolist())
            for pid in rng.sample(ids, min(PER_COMPETITION, len(ids), want - len(taken))):
                p = players[players["id"] == pid].iloc[0]
                name = typed_name(p)
                taken.append({
                    "player_id": int(pid), "name": name,
                    "gender": gender, "competition_id": int(comp_id),
                    "season": int(comp["year"]), "competition": comp["synthesized_name"],
                    "country": comp["country"], "division": int(comp["division"]),
                    "position": p.get("position"), "minutes": round(float(p["minutes"])),
                })
        print(gender, len(taken), "players from", len({t["competition_id"] for t in taken}),
              "competitions")
        rows += taken

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("wrote", OUT)


if __name__ == "__main__":
    asyncio.run(main())
