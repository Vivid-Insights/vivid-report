"""LIVE writer: Anthropic Messages API over HTTPS with urllib (stdlib only).

Used only when ANTHROPIC_API_KEY is set. The code still does all routing and the
safeguarding check; the model only writes the wording of WORDALISE / area replies
from the material injected below. Any failure returns None and the engine falls back
to the offline writer.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from .content import DATA_DIR, load

API_URL = os.environ.get("ANTHROPIC_API_URL", "https://api.anthropic.com/v1/messages")
DEFAULT_MODEL = "claude-opus-5-5"
TIMEOUT_S = 60


def api_key() -> str | None:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    return key or None


def live_mode() -> bool:
    return api_key() is not None


def base_system_prompt() -> str:
    with open(os.path.join(DATA_DIR, "system_prompt.txt"), encoding="utf-8") as fh:
        return fh.read()


def build_system(context_blocks: list[str], route_note: str, office: str) -> str:
    few = "\n".join(
        f"- [{r['flow']} | {r['area']} | {r['stage']}] User: {r['user_message']}\n  Ideal: {r['ideal_answer']}"
        for r in load().few_shot
    )
    material = "\n\n".join(context_blocks) or "(no school material applies to this message)"
    return (
        base_system_prompt()
        + "\n\n## School information for this reply (the ONLY facts you may state)\n"
        + material
        + "\n\nItems marked [TBD...] are NOT confirmed. Never copy a [TBD...] marker and never guess its value. "
        + f"Instead say: \"I don't have that detail confirmed yet. Please check with {office}"
        + ("" if office == "Reception" else " (or Reception)") + ".\""
        + "\nNever say the user's name, even if they gave it."
        + f"\n\n## Routing decided by the app\n{route_note}"
        + "\n\n## Examples of ideal answers (style only; their facts are also unconfirmed)\n" + few
    )


def call(system: str, messages: list[dict], max_tokens: int = 2000) -> str | None:
    key = api_key()
    if not key:
        return None
    model = os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL)
    body = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": messages,
        "output_config": {"effort": "low"},
        "fallbacks": "default",
    }
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "anthropic-beta": "server-side-fallback-2026-07-01",
    }
    for attempt in range(2):
        req = urllib.request.Request(API_URL, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 400 and attempt == 0:
                # retry once without the optional fallback beta in case the account/model rejects it
                body.pop("fallbacks", None)
                headers.pop("anthropic-beta", None)
                continue
            return None
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            return None
        if data.get("stop_reason") == "refusal":
            return None
        text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text").strip()
        return text or None
    return None
