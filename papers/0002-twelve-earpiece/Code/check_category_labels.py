"""Save the evidence for why `player_answer_skills_question` fails on one question.

Runs the function's own first embedding search for the question, and lists the
category labels of `describe/general/category_questions` beside the player quality
keys of the workspace's registry. Runs in the Earpiece API's environment, like
run_function_examples.py:

    cd ~/GitHub/twelve-earpiece-api
    PYTHONPATH=src .venv/bin/python <path>/Code/check_category_labels.py

Writes `Code/outputs/function-examples/category-labels.json`.
"""

import asyncio
import collections
import json
from pathlib import Path

from config import config
from models.quality import QualityType
from services.knowledge_integration import KnowledgeClient
from services.workspaces_integration import WorkspacesClient
from services.workspaces_integration.registry_manager import get_workspace_qualities

OUT = Path(__file__).resolve().parent / "outputs" / "function-examples" / "category-labels.json"
WORKSPACE = "wksp_aWsUNyFPMrVh5N"
QUESTION = "Do you think they would struggle playing out from the back?"


async def main():
    kc = KnowledgeClient(config.knowledge_api.base_url, timeout=30)
    # The same call as PlayerAnswerSkillsQuestion.qualities_from_query.
    hits = await kc.search_pairs(QUESTION, heading="",
                                 files_filter=["describe/general/category_questions"],
                                 max_results=5, max_distance=0.7)
    pairs = await kc.list_pairs(files_filter=["describe/general/category_questions"])
    wc = WorkspacesClient(base_url=config.workspaces_api.base_url,
                          auth0_domain=config.auth0.domain,
                          client_id=config.auth0_mtm.client_id,
                          client_secret=config.auth0_mtm.client_secret,
                          audience=config.workspaces_api.audience)
    await wc.initialize()
    registry = await get_workspace_qualities(wc, WORKSPACE)
    OUT.write_text(json.dumps({
        "question": QUESTION,
        "knowledge_api": config.knowledge_api.base_url.split("//")[-1].split("/")[0],
        "search_hits": [{"question": p.question, "distance": p.distance,
                         "properties": p.properties} for p in hits],
        "category_labels": dict(collections.Counter(
            (p.properties or {}).get("category") for p in pairs)),
        "registry_player_quality_keys": sorted(
            k for (t, k) in registry._by_type_and_key if t == QualityType.PLAYER),
    }, indent=2, ensure_ascii=False))
    print("wrote", OUT)


if __name__ == "__main__":
    asyncio.run(main())
