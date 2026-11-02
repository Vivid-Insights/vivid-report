"""Add each name-test player's team, and an informal or misspelled form of it.

For the second run of the name test (David, 17 October 2026: "rerun the same
players but this time with the teams, also with spelling errors or nicknames in
the error case"). The team is the player's team in the sampled competition and
season, as the data names it.

A player whose team has no name in the data is marked "no team name" and left
out of the team run.

The error case gets one of two forms, half the teams each (seed 17):

- an informal name: the club's name without its generic parts (FC, IF, CD,
  Club, Futebol Clube, a women's-team suffix and the like), the form people use
  in speech ("IFK Norrköping" -> "Norrköping"); where nothing generic can be
  removed from a name of several words, its longest word ("Red Bull
  Bragantino" -> "Bragantino"). A one-word name gets a misspelling instead,
  recorded as such. We had no source
  for clubs' real nicknames ("the Bees"), so none are invented;
- a misspelling: one error from name_test_misspell.py, a single typing error, a
  spelling variant, or punctuation, spacing and accents, in turn.

Runs in the Earpiece API's environment:

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python <path>/Code/name_test_teams.py

Reads `outputs/name-test/sample.csv`; writes `outputs/name-test/teams.csv`.
"""

from __future__ import annotations

import asyncio
import csv
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from name_test_misspell import one_error  # noqa: E402

from config import config  # noqa: E402
from schemas.context import CompetitionSeason  # noqa: E402
from services.data_integration.data_api_client import DataAPIClient  # noqa: E402
from services.data_integration.specifications import set_data_functions_client  # noqa: E402
from services.data_integration.async_data_functions import AsyncTwelveDataFunctions  # noqa: E402
from services.workspaces_integration import WorkspacesClient  # noqa: E402

DIR = Path(__file__).resolve().parent / "outputs" / "name-test"
WORKSPACE = "wksp_aWsUNyFPMrVh5N"
SEED = 17
GENERIC = {
    "fc", "f.c.", "afc", "cf", "sc", "sv", "fk", "sk", "if", "ik", "bk", "ff", "cd", "ca",
    "cs", "ac", "as", "us", "ss", "ssd", "gd", "ec", "se", "cr", "ad", "ud", "rc", "sd",
    "kf", "nk", "fsv", "tsv", "vfb", "vfl", "club", "clube", "futebol", "football", "soccer",
    "de", "del", "da", "do", "w", "women", "ladies", "femenino", "feminino", "frauen",
    "damen", "dff", "(w)", "u23", "ii", "b", "esporte", "atlético", "atletico", "deportivo",
    "sport", "sports", "calcio", "1.", "the",
}
SPELLING = ["single typing error", "spelling variant", "punctuation, spacing, accents"]


def informal(team: str) -> str | None:
    words = team.split()
    kept = [w for w in words if w.lower().strip(".,") not in GENERIC and not re.fullmatch(r"\d{4}", w)]
    if not kept:
        return None
    if kept != words:
        return " ".join(kept)
    if len(words) >= 2:            # "Red Bull Bragantino" -> "Bragantino"
        return max(words, key=len)
    return None


async def main() -> None:
    rng = random.Random(SEED)
    dfc = AsyncTwelveDataFunctions(config.data_functions.token)
    set_data_functions_client(dfc)
    api = DataAPIClient()
    wc = WorkspacesClient(base_url=config.workspaces_api.base_url,
                          auth0_domain=config.auth0.domain,
                          client_id=config.auth0_mtm.client_id,
                          client_secret=config.auth0_mtm.client_secret,
                          audience=config.workspaces_api.audience)
    await wc.initialize()
    customer_id = (await wc.get_workspace(WORKSPACE)).customer_id

    sample = list(csv.DictReader((DIR / "sample.csv").open(encoding="utf-8")))
    team_of: dict[tuple[int, int], dict[int, int]] = {}
    names: dict[tuple[int, int], dict[int, str]] = {}
    rows, turn = [], 0
    order = list(range(len(sample)))
    rng.shuffle(order)
    informal_half = set(order[: len(sample) // 2])
    for idx, s in enumerate(sample):
        comp = (int(s["competition_id"]), int(s["season"]))
        if comp not in team_of:
            cs = CompetitionSeason(id=comp[0], year=comp[1])
            players = await api.get_competition_players(customer_id, cs)
            team_of[comp] = dict(zip(players["id"].astype(int), players["team_id"].astype(int)))
            teams = await api.get_competition_teams(customer_id, cs)
            names[comp] = dict(zip(teams["id"].astype(int), teams["name"].astype(str)))
        team_id = team_of[comp][int(s["player_id"])]
        team = names[comp].get(team_id)
        if team is None:  # a team missing from the competition's list
            got = await dfc.get_team_by_id(customer_id, "wyscout", team_id)
            if len(got):
                first = got.iloc[0] if hasattr(got, "iloc") else got[0]
                team = str(first["name"])
        if team is None:  # the team has no name in the data: left out of the team run
            rows.append({"player_id": s["player_id"], "team_id": team_id, "team": "",
                         "team_error": "", "team_kind": "no team name", "team_detail": ""})
            continue
        kind, error = None, None
        if idx in informal_half:
            error = informal(team)
            kind = "informal name" if error else None
        if error is None:
            category, detail, error = one_error(team, SPELLING[turn % len(SPELLING)], rng)
            turn += 1
            kind = f"misspelled: {category}: {detail}"
        rows.append({"player_id": s["player_id"], "team_id": team_id, "team": team,
                     "team_error": error, "team_kind": kind.split(":")[0]
                     if kind.startswith("misspelled") else kind, "team_detail": kind})

    with (DIR / "teams.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    print(Counter(r["team_kind"] for r in rows))


if __name__ == "__main__":
    asyncio.run(main())
