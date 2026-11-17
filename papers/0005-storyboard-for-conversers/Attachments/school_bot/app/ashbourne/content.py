"""Loads every data file under app/data once. No school content lives in code."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from functools import lru_cache

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load(name: str):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as fh:
        return json.load(fh)


@dataclass
class Content:
    bot: dict
    areas: list
    routing: dict
    safeguarding_patterns: list
    opening_hours: list
    role_contacts: list
    policies: list
    resources: list
    few_shot: list = field(default_factory=list)

    def area(self, name: str) -> dict:
        for a in self.areas:
            if a["name"] == name:
                return a
        raise KeyError(name)

    def facet(self, facet_id: str):
        for a in self.areas:
            for f in a["facets"]:
                if f["id"] == facet_id:
                    return a, f
        return None, None


@lru_cache(maxsize=1)
def load() -> Content:
    few_shot = []
    with open(os.path.join(DATA_DIR, "few_shot_examples.csv"), encoding="utf-8") as fh:
        # dataSourcesHelp says columns are separated by ';'. The file is NOT valid
        # quoted CSV (answers begin with literal '"Options"'), so the csv module
        # would eat the quotes. Split manually: every row has exactly 5 fields.
        lines = [ln.rstrip("\n") for ln in fh if ln.strip()]
    header = lines[0].split(";")
    for ln in lines[1:]:
        few_shot.append(dict(zip(header, ln.split(";", len(header) - 1))))
    return Content(
        bot=_load("bot.json"),
        areas=_load("areas.json")["areas"],
        routing=_load("routing.json"),
        safeguarding_patterns=_load("safeguarding_phrases.json")["patterns"],
        opening_hours=_load("opening_hours.json")["places"],
        role_contacts=_load("role_contacts.json")["roles"],
        policies=_load("policy_summaries.json")["policies"],
        resources=_load("resources.json")["resources"],
        few_shot=few_shot,
    )
