"""Conversation engine: state, dispatch, writers, output checks."""
from __future__ import annotations

import json
import re
import threading
import time
import uuid
from dataclasses import dataclass, field

from . import llm, offline
from .content import load
from .router import Route, audience_hint, classify, speaker_hint
from .safeguarding import is_risk
from .textfilter import (apply_voice, clean_placeholders, redact_names, violates_constraints,
                         volunteered_names)

SESSION_TTL_S = 2 * 60 * 60  # BUILD GUESS: storyboard says 'this conversation only', no duration
LLM_KINDS = {"area", "area_audience", "medical", "reassurance", "who_to_contact", "opening_hours", "school_rule", "find_support"}


@dataclass
class Session:
    id: str
    area_states: dict = field(default_factory=dict)   # area -> {"stage": str, "covered": [ids]}
    current_area: str | None = None
    pending_contacts_line: bool = False
    asked_sixth_form: bool = False
    awaiting_audience: tuple | None = None              # (area, stage) after asking 'Are you in Sixth Form?'
    audience: str | None = None                       # "sixth_form" | "years_7_11" (never a name)
    names: list = field(default_factory=list)         # volunteered names, used ONLY to redact
    history: list = field(default_factory=list)       # redacted, for the LLM only
    last_seen: float = field(default_factory=time.time)

    @property
    def current_stage(self):
        if self.current_area and self.current_area in self.area_states:
            return self.area_states[self.current_area]["stage"]
        return None


class Engine:
    def __init__(self):
        self.content = load()
        self._sessions: dict[str, Session] = {}
        self._lock = threading.Lock()

    # ---------------- sessions ----------------
    def session(self, session_id: str | None) -> Session:
        now = time.time()
        with self._lock:
            for sid in [k for k, s in self._sessions.items() if now - s.last_seen > SESSION_TTL_S]:
                del self._sessions[sid]
            if session_id and session_id in self._sessions:
                s = self._sessions[session_id]
            else:
                s = Session(id=str(uuid.uuid4()))
                self._sessions[s.id] = s
            s.last_seen = now
            return s

    def reset(self, session_id: str | None):
        with self._lock:
            self._sessions.pop(session_id or "", None)

    # ---------------- main entry ----------------
    def handle(self, session_id: str | None, message: str, facet_id: str | None = None) -> dict:
        s = self.session(session_id)
        message = (message or "").strip()[:2000]
        bot = self.content.bot
        for n in volunteered_names(message):
            if n not in s.names:
                s.names.append(n)
        hint = audience_hint(message)
        if hint:
            s.audience = hint

        route = self._route(s, message, facet_id)
        result = {"label": "Ask Ashbourne", "chips": [], "facets": [], "office": "Reception", "writer": "fixed"}

        if route.kind == "safeguarding":
            # Override: topic paused (area state kept), no chips, no probing.
            text = bot["safeguardingResponse"]
            s.pending_contacts_line = True
            result.update(label="Ask Ashbourne", text=text)
            return self._finish(s, message, route, result, post_check=False)

        if route.kind == "greeting":
            result["text"] = bot["greeting"]
        elif route.kind == "redirect_records":
            result["text"] = bot["redirects"]["records"]
        elif route.kind == "redirect_schoolwork":
            result["text"] = bot["redirects"]["schoolwork"]
        elif route.kind == "catch_all":
            result["text"] = bot["redirects"]["catchAll"]
        elif route.kind == "redirect_acting":
            prefix = bot["redirects"]["actingOnBehalf"]
            if route.inner:
                inner = self._compose(s, message, route.inner, facet_id=None)
                result.update(inner)
                result["text"] = prefix + "\n" + inner["text"]
            else:
                result["text"] = prefix + " " + bot["actingOnBehalfNoTopic"]
            result["chips"] = []
        else:
            result.update(self._compose(s, message, route, facet_id))

        return self._finish(s, message, route, result)

    # ---------------- routing ----------------
    def _route(self, s: Session, message: str, facet_id: str | None) -> Route:
        if s.awaiting_audience and not is_risk(message):
            area_name, stage = s.awaiting_audience
            s.awaiting_audience = None
            hint = audience_hint(message)
            low = message.strip().lower()
            if hint is None and re.match(r"^(yes|yeah|yep|y)\b", low):
                s.audience = "sixth_form"
            elif hint is None and re.match(r"^(no|nope|nah|n)\b", low):
                s.audience = "years_7_11"
            if s.audience and (hint or re.match(r"^(yes|yeah|yep|y|no|nope|nah|n)\b", low)):
                return Route("area_audience", area=area_name, stage=stage)
        if facet_id and not is_risk(message):
            area, facet = self.content.facet(facet_id)
            if facet:
                stage = s.area_states.get(area["name"], {}).get("stage")
                if stage not in facet["stageRefs"]:
                    stage = facet["stageRefs"][0]
                return Route("area", area=area["name"], stage=stage)
        return classify(message, s.current_area, s.current_stage)

    # ---------------- composition ----------------
    def _compose(self, s: Session, message: str, route: Route, facet_id: str | None) -> dict:
        bot = self.content.bot
        out = {"chips": [], "facets": [], "writer": "offline"}

        if route.kind in ("who_to_contact", "opening_hours", "school_rule", "find_support"):
            text, office = offline.compose_function(route.kind, route.target)
            label = {"who_to_contact": "Who to contact", "opening_hours": "Opening hours",
                     "school_rule": "School rules", "find_support": "Support"}[route.kind]
            context = [f"{label} reference entry:\n{json.dumps(route.target, ensure_ascii=False) if route.target else '(no matching entry)'}"]
            out.update(label=f"Ask Ashbourne · {label}", text=text, office=office)
            return self._maybe_llm(s, message, route, out, context, office)

        # area-based kinds: area, medical, reassurance
        area = self.content.area(route.area)
        st = s.area_states.setdefault(area["name"], {"stage": route.stage, "covered": []})
        st["stage"] = route.stage
        s.current_area = area["name"]
        office = area["owningOffice"]
        label = f"Ask Ashbourne · {area['shortName']}"

        if route.kind == "reassurance":
            deciders = [f for f in area["facets"] if route.stage in f["stageRefs"] and "decide" in f["answer"].lower()]
            facets = deciders[:1]
            body = bot["noPredictionPrefix"]
            if facets:
                body += "\n" + offline.compose_area(area, facets)
            else:
                body += " Please check with " + office + "."
        else:
            few = None
            if route.kind == "area" and not facet_id:
                few = offline.few_shot_match(message, flow="OpenProcessArea")
                if few and few["area"] != area["name"]:
                    few = None
            if route.kind in ("medical", "area_audience"):
                facets = [f for f in area["facets"] if f["id"] == "ab-report-illness"]
            else:
                facets = offline.select_facets(area, route.stage, message, st["covered"], forced=facet_id)
            facets = self._audience_adjust(s, area, facets)
            if few:
                body = few["ideal_answer"]
                out["few_shot_used"] = few["user_message"]
                # the few-shot row, not a facet, grounds this reply; the matching
                # facets still count as covered so chips don't repeat the question
                for f in facets:
                    if f["id"] not in st["covered"]:
                        st["covered"].append(f["id"])
                facets = []
            else:
                body = offline.compose_area(area, facets)
            if route.kind == "medical":
                body = bot["medicalSignpost"] + "\n" + body
            if (any(f["id"] == "ab-report-illness" for f in facets) and s.audience is None
                    and not s.asked_sixth_form and speaker_hint(message) == "student_or_unknown"):
                body += "\n" + bot["sixthFormQuestion"]
                s.asked_sixth_form = True
                s.awaiting_audience = (area["name"], route.stage)

        for f in facets:
            if f["id"] not in st["covered"]:
                st["covered"].append(f["id"])
        out.update(label=label, text=body, office=office, facets=[f["id"] for f in facets],
                   area=area["name"], stage=route.stage)
        if route.kind == "area":
            out["chips"] = offline.chips_for(area, route.stage, st["covered"], out["facets"])

        stage_facets = [f for f in area["facets"] if route.stage in f["stageRefs"]]
        context = [f"Area: {area['name']} | Stage: {route.stage}\nFacets for this stage (id: question -> answer):\n"
                   + "\n".join(f"- {f['id']}: {f['question']} -> {f['answer']}" for f in stage_facets)]
        if route.kind == "medical":
            context.append("The user asked for a medical judgement. Do not give one (CONSTRAINT-8). Signpost: "
                           + bot["medicalSignpost"])
        if route.kind == "reassurance":
            context.append("The user is pushing for reassurance about a staff decision. Never predict or imply the outcome; say who decides (CONSTRAINT-4).")
        return self._maybe_llm(s, message, route, out, context, office)

    def _audience_adjust(self, s: Session, area: dict, facets: list[dict]) -> list[dict]:
        """Ask for / use year group only where the answer depends on it (CONSTRAINT-5)."""
        if s.audience == "sixth_form":
            swapped = []
            for f in facets:
                if f["id"] == "ab-report-illness":
                    f = next(x for x in area["facets"] if x["id"] == "ab-sixth-form-own")
                swapped.append(f)
            return swapped
        return facets

    def _maybe_llm(self, s: Session, message: str, route: Route, out: dict, context: list[str], office: str) -> dict:
        if not llm.live_mode() or route.kind not in LLM_KINDS:
            return out
        note = f"flow={route.kind}; area={route.area}; stage={route.stage}; audience={s.audience or 'unknown'}"
        system = llm.build_system(context, note, office)
        msgs = (s.history[-12:] + [{"role": "user", "content": redact_names(message, s.names) or "(empty)"}])
        text = llm.call(system, msgs)
        if text and not violates_constraints(text):
            out = dict(out, text=text, writer="llm")
        else:
            out = dict(out, writer="offline (llm unavailable or rejected)")
        return out

    # ---------------- output checks ----------------
    def _finish(self, s: Session, message: str, route: Route, result: dict, post_check: bool = True) -> dict:
        text = result["text"]
        if post_check:
            text = apply_voice(text)
            text, had_tbd = clean_placeholders(text, result.get("office"))
            text = redact_names(text, s.names)
            if s.pending_contacts_line:
                text = text + "\n" + self.content.bot["safeguardingContactsLine"]
                s.pending_contacts_line = False
        # history kept for the live model only, with volunteered names removed
        s.history.append({"role": "user", "content": redact_names(message, s.names) or "(empty)"})
        s.history.append({"role": "assistant", "content": text})
        s.history = s.history[-24:]
        return {
            "session_id": s.id,
            "reply": text,
            "label": result.get("label", "Ask Ashbourne"),
            "chips": [] if route.kind == "safeguarding" else result.get("chips", []),
            "debug": {
                "route": route.kind,
                "area": result.get("area"),
                "stage": result.get("stage"),
                "facets": result.get("facets", []),
                "writer": result.get("writer", "fixed"),
                "mode": "live" if llm.live_mode() else "offline",
                "few_shot_used": result.get("few_shot_used"),
            },
        }
