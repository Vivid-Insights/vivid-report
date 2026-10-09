"""Review state for a report: what has been asked for, what reviewers said, and whether it may be published.

The rule this module enforces: a report is published only in the exact form the Vivid Insights team
approved. An approval names a content hash — of the report's Markdown, its references and every
file the page shows or quotes — so any edit after approval, however small, makes the approval stale
and the report has to go back to its reviewers.

Layout, beside the report's Markdown file:

    review/reviewers.yml                     the team, their roles, and the approval policy
    review/round-01/request.md               written by `review.py request` (author side)
    review/round-01/reviews/<id>.md          written by the reviewer, by hand, from the template
    review/round-01/response.md              the author's point-by-point reply
    review/round-01/approvals/<id>.yml       written by the reviewer with `review.py approve`
    review/publication.yml                   written by `publish.py`
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from datetime import date
from pathlib import Path

import yaml

from common import FRONT_RE, ROOT, load_report, load_yaml

BLOCK_HDR_RE = re.compile(r"^:{3,}[ \t]*(\w+)[ \t]*(\{[^\n]*\})", re.M)
PATH_ATTRS = ("src", "dark", "poster", "fallback", "source")


def review_dir(report: Path) -> Path:
    return report.parent / "review"


def referenced_files(report: Path) -> list[Path]:
    """Every file the report page shows or quotes, so that changing any of them changes the hash."""
    from build import parse_attrs  # local import: build imports this module too
    meta, body = load_report(report)
    base = report.parent
    files = {report, base / meta.get("references", "references.yaml")}
    for m in BLOCK_HDR_RE.finditer(body):
        a = parse_attrs(m.group(2))
        for k in PATH_ATTRS:
            v = a.get(k)
            if not v or v == "hand-written" or not isinstance(v, str):
                continue
            p = base / v
            if m.group(1) == "interactive" and k == "src" and p.exists():
                files.update(f for f in p.parent.rglob("*") if f.is_file() and ".DS_Store" not in f.name)
            else:
                files.add(p)
            if m.group(1) in ("figure", "video", "panel") and k in ("src", "poster"):
                files.add(p.parent / "dark" / p.name)
    return sorted(f.resolve() for f in files if f.exists() and f.is_file())


def content_hash(report: Path) -> str:
    h = hashlib.sha256()
    base = report.parent.resolve()
    for f in referenced_files(report):
        h.update(str(f.relative_to(base) if f.is_relative_to(base) else f.name).encode())
        h.update(b"\0")
        h.update(f.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def front(path: Path) -> dict:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if path.suffix in (".yml", ".yaml"):
        return yaml.safe_load(text) or {}
    m = FRONT_RE.match(text)
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def team(report: Path) -> tuple[dict, dict]:
    cfg = load_yaml(review_dir(report) / "reviewers.yml", {}) or {}
    members = {m["id"]: m for m in cfg.get("team", []) if m.get("id")}
    policy = {"required_approvals": 2, "require_editor": True, "authors_may_not_approve": True}
    policy.update(cfg.get("policy") or {})
    return members, policy


def rounds(report: Path) -> list[Path]:
    d = review_dir(report)
    return sorted(p for p in d.glob("round-[0-9][0-9]") if p.is_dir()) if d.exists() else []


def git(*args, cwd: Path) -> str | None:
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def committed_by(path: Path) -> tuple[str | None, str]:
    """Email of whoever last committed the file, and a problem description if it cannot be attributed."""
    cwd = path.parent
    if git("rev-parse", "--is-inside-work-tree", cwd=cwd) != "true":
        return None, "the report is not under git, so the approval cannot be attributed to its reviewer"
    if git("status", "--porcelain", "--", path.name, cwd=cwd):
        return None, "the approval file has uncommitted changes; the reviewer must commit it themselves"
    # The last commit to touch the file is the one that put its current content there, so if anyone
    # but the reviewer edits an approval after them, it no longer counts.
    log = git("log", "-1", "--format=%ae", "--", path.name, cwd=cwd)
    if not log:
        return None, "the approval file has not been committed; the reviewer must commit it themselves"
    return log.strip().lower(), ""


def author_names(report: Path) -> set[str]:
    meta, _ = load_report(report)
    out = set()
    for a in meta.get("authors") or []:
        out.add(str(a.get("name", "") if isinstance(a, dict) else a).strip().lower())
    return out


def check_approvals(report: Path, rnd: Path, current: str, strict: bool) -> tuple[list[dict], list[str]]:
    members, policy = team(report)
    authors = author_names(report)
    valid, problems = [], []
    for f in sorted((rnd / "approvals").glob("*.yml")):
        a = front(f)
        rid = a.get("reviewer") or f.stem
        who = members.get(rid)
        tag = f"{rnd.name}/approvals/{f.name}"
        if not who:
            problems.append(f"{tag}: '{rid}' is not in review/reviewers.yml")
            continue
        if a.get("decision") != "approve":
            problems.append(f"{tag}: decision is '{a.get('decision')}', not 'approve'")
            continue
        if a.get("hash") != current:
            problems.append(f"{tag}: approves version {str(a.get('hash'))[:12]}, but the report is now {current[:12]} — it changed after approval")
            continue
        if policy.get("authors_may_not_approve") and who.get("name", "").strip().lower() in authors:
            problems.append(f"{tag}: {who.get('name')} is an author of this report and cannot approve it")
            continue
        form = rnd / "reviews" / f"{rid}.md"
        rec = str(front(form).get("recommendation", "")).lower()
        if not form.exists():
            problems.append(f"{tag}: no written review at {rnd.name}/reviews/{rid}.md")
            continue
        if rec != "accept":
            problems.append(f"{tag}: the written review recommends '{rec or 'nothing'}', not 'accept'")
            continue
        if strict:
            email, why = committed_by(f)
            if why:
                problems.append(f"{tag}: {why}")
                continue
            if who.get("email") and email != str(who["email"]).lower():
                problems.append(f"{tag}: committed by {email}, but {who.get('name')}'s address is {who['email']}")
                continue
        valid.append({"id": rid, "name": who.get("name", rid), "role": who.get("role", "reviewer"), "date": str(a.get("date", ""))})
    return valid, problems


def policy_met(valid: list[dict], policy: dict) -> tuple[bool, str]:
    need = int(policy.get("required_approvals", 2))
    if len(valid) < need:
        return False, f"{len(valid)} of {need} required approvals"
    if policy.get("require_editor") and not any(v["role"] == "editor" for v in valid):
        return False, "no approval from an editor"
    return True, f"{len(valid)} approvals, policy met"


def review_status(report: Path, strict: bool = False) -> dict:
    current = content_hash(report)
    rs = rounds(report)
    st = {"state": "draft", "hash": current, "round": len(rs), "problems": []}
    if not rs:
        return st
    last = rs[-1]
    req = front(last / "request.md")
    st["round_hash"] = req.get("hash", "")
    members, policy = team(report)
    valid, problems = check_approvals(report, last, current, strict)
    st["approvals"], st["problems"] = valid, problems
    ok, why = policy_met(valid, policy)
    st["policy"] = why
    recs = {f.stem: str(front(f).get("recommendation", "")).lower() for f in (last / "reviews").glob("*.md")}
    st["reviews"] = recs
    if ok:
        pub = front(review_dir(report) / "publication.yml")
        st["state"] = "published" if pub.get("hash") == current else "approved"
        reviewers = []
        for r in rs:
            for f in sorted((r / "reviews").glob("*.md")):
                n = members.get(f.stem, {}).get("name", f.stem)
                if n not in reviewers:
                    reviewers.append(n)
        meta, _ = load_report(report)
        repo = meta.get("repository")
        st["record"] = {"reviewers": reviewers, "rounds": len(rs), "approved": max(v["date"] for v in valid),
                        "link": f"{repo.rstrip('/')}/tree/main/review" if repo else ""}
    elif any(v in ("minor", "major", "reject") for v in recs.values()):
        st["state"] = "changes-requested"
    else:
        st["state"] = "in-review"
    if st.get("round_hash") and st["round_hash"] != current and not ok:
        st["problems"].append(f"the report has changed since round {len(rs)} was requested; reviewers are reading {st['round_hash'][:12]}")
    return st


def today() -> str:
    return date.today().isoformat()


__all__ = ["content_hash", "review_status", "rounds", "team", "review_dir", "referenced_files", "front", "ROOT", "today"]
