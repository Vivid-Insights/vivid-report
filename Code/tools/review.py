"""The Vivid Insights review process for a report. REVIEW.md describes it in full.

Author side (the agent may run these):
    cd Code && uv run python tools/review.py status            # where the report stands, and why
    cd Code && uv run python tools/review.py request           # freeze this version and open a review round

Reviewer side (a person runs these, in their own terminal — never the agent):
    cd Code && uv run python tools/review.py form <your-id>    # start your written review for the open round
    cd Code && uv run python tools/review.py approve <your-id> # approve the exact version you read
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, rel, resolve_report, slug_of, load_report  # noqa: E402
from reviewlib import (content_hash, front, git, referenced_files, review_dir, review_status,  # noqa: E402
                       rounds, team, today)

TEMPLATES = ROOT / "review" / "templates"


def cmd_status(report: Path) -> int:
    st = review_status(report, strict=True)
    members, policy = team(report)
    print(f"Report:        {rel(report)}")
    print(f"State:         {st['state']}")
    print(f"Content hash:  {st['hash'][:12]}  (changes whenever the report or anything it shows or quotes changes)")
    print(f"Review rounds: {st['round']}")
    if st["round"]:
        print(f"Round {st['round']} froze: {st.get('round_hash', '')[:12]}")
        for rid, rec in (st.get("reviews") or {}).items():
            print(f"  review   {rid:<14} recommends {rec or '(not stated)'}")
        for a in st.get("approvals") or []:
            print(f"  approval {a['id']:<14} {a['role']}, {a['date']}  ✓ valid")
        print(f"Policy:        {st.get('policy', '')}  (needs {policy.get('required_approvals')} approvals"
              f"{', one from an editor' if policy.get('require_editor') else ''}; authors may not approve)")
    for p in st["problems"]:
        print(f"  ! {p}")
    if not members:
        print("  ! review/reviewers.yml lists nobody: add the team before requesting review")
    nxt = {"draft": "finish the read-through (step 8), then `review.py request`",
           "in-review": "wait for the written reviews; do not edit the report while reviewers are reading it",
           "changes-requested": "revise, write review/round-NN/response.md, then `review.py request` for the next round",
           "approved": "step 10: confirm the disclaimer with the author, then `publish.py`",
           "published": "nothing: the published page matches the approved version"}
    print(f"Next:          {nxt.get(st['state'], '')}")
    return 0


def cmd_request(report: Path, force_dirty: bool) -> int:
    from build import Builder, build, print_issues
    members, policy = team(report)
    if len(members) < int(policy.get("required_approvals", 2)):
        print("review/reviewers.yml does not list enough reviewers to meet the approval policy. Add the team first.")
        return 1
    st = review_status(report)
    if st["state"] in ("approved", "published"):
        print(f"The current version is already {st['state']}. Nothing to request.")
        return 1
    rs = rounds(report)
    if rs and st.get("round_hash") == st["hash"]:
        print(f"Round {len(rs)} already covers this exact version ({st['hash'][:12]}). Wait for its reviews.")
        return 1
    if rs and not (rs[-1] / "response.md").exists():
        print(f"Round {len(rs)} has no response.md. Answer every reviewer point before asking for another round.")
        return 1

    b = Builder(report, release=True, status=st)
    res = b.build()
    if res.errors:
        print("The report is not ready for review — these would stop it being published:")
        print_issues(res.errors)
        return 1

    repo = report.parent
    if git("rev-parse", "--is-inside-work-tree", cwd=repo) == "true":
        dirty = git("status", "--porcelain", "--", *[str(f) for f in referenced_files(report)], cwd=repo)
        if dirty and not force_dirty:
            print("Commit the report before requesting review, so the version reviewers read is in the history:")
            print(dirty)
            return 1

    n = len(rs) + 1
    rnd = review_dir(report) / f"round-{n:02d}"
    (rnd / "reviews").mkdir(parents=True, exist_ok=True)
    (rnd / "approvals").mkdir(parents=True, exist_ok=True)
    for d in ("reviews", "approvals"):
        (rnd / d / ".gitkeep").touch()
    meta, _ = load_report(report)
    who = git("config", "user.name", cwd=repo) or ""
    commit = git("rev-parse", "--short", "HEAD", cwd=repo) or ""
    files = "\n".join(f"  - {f.relative_to(report.parent) if f.is_relative_to(report.parent) else f.name}" for f in referenced_files(report))
    changes = ("" if n == 1 else
               "\n## Changes since round {p}\n\n[TO WRITE: what changed in response to round {p}, pointing to review/round-{p:02d}/response.md]\n".format(p=n - 1))
    (rnd / "request.md").write_text(
        f"---\nround: {n}\nhash: {st['hash']}\ncommit: {commit}\nrequested-by: {who}\ndate: {today()}\n---\n\n"
        f"# Review request, round {n}\n\n"
        f"Report: *{meta.get('title', '')}*{(' (' + str(meta['report-number']) + ')') if meta.get('report-number') else ''}.\n\n"
        f"Read the review copy built from version `{st['hash'][:12]}`. Write your review with `cd Code && uv run python tools/review.py form <your-id>`, "
        f"following `REVIEW.md`. Approve only the version you read: if the hash on the review copy differs from the one above, stop and tell the author.\n"
        f"{changes}\n## Files in this version\n\n{files}\n", encoding="utf-8")

    out = ROOT / "build" / f"{slug_of(meta, report)}-review-round-{n:02d}"
    build(report, out, status={**st, "state": "in-review", "review_copy": True, "round": n}, style=False)
    print(f"Opened review round {n} at {rel(rnd)} for version {st['hash'][:12]}.")
    print(f"Review copy: {rel(out / 'index.html')}")
    print("Next: commit review/ and push, then send the review copy to the reviewers named in review/reviewers.yml.")
    print("Do not edit the report while it is being reviewed: any change makes the version they approve stale.")
    return 0


def open_round(report: Path) -> Path | None:
    rs = rounds(report)
    return rs[-1] if rs else None


def cmd_form(report: Path, rid: str) -> int:
    members, _ = team(report)
    if rid not in members:
        print(f"'{rid}' is not in review/reviewers.yml. Ids: {', '.join(members) or '(none)'}")
        return 1
    rnd = open_round(report)
    if not rnd:
        print("No review round is open.")
        return 1
    dest = rnd / "reviews" / f"{rid}.md"
    if dest.exists():
        print(f"{rel(dest)} already exists; edit it directly.")
        return 1
    req = front(rnd / "request.md")
    tpl = (TEMPLATES / "review-form.md").read_text(encoding="utf-8")
    tpl = (tpl.replace("{{reviewer}}", rid).replace("{{name}}", members[rid].get("name", rid))
              .replace("{{round}}", str(req.get("round", ""))).replace("{{hash}}", str(req.get("hash", "")))
              .replace("{{date}}", today()))
    dest.write_text(tpl, encoding="utf-8")
    print(f"Your review form is {rel(dest)}. Fill it in, set `recommendation:`, and commit it yourself.")
    return 0


def cmd_approve(report: Path, rid: str) -> int:
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("Approval needs a person at a terminal. It cannot be given by a script or an agent.")
        return 2
    members, policy = team(report)
    who = members.get(rid)
    if not who:
        print(f"'{rid}' is not in review/reviewers.yml.")
        return 1
    rnd = open_round(report)
    if not rnd:
        print("No review round is open.")
        return 1
    form = rnd / "reviews" / f"{rid}.md"
    rec = str(front(form).get("recommendation", "")).lower()
    if rec != "accept":
        print(f"Your written review ({rel(form)}) must exist and recommend 'accept' before you approve. It says: '{rec or 'nothing'}'.")
        return 1
    meta, _ = load_report(report)
    if who.get("name", "").strip().lower() in {str(a.get('name', '') if isinstance(a, dict) else a).strip().lower() for a in meta.get("authors") or []}:
        print("You are an author of this report, so you cannot approve it.")
        return 1
    email = (git("config", "user.email", cwd=report.parent) or "").lower()
    if who.get("email") and email != str(who["email"]).lower():
        print(f"git is configured as {email or '(nobody)'}, but your address in reviewers.yml is {who['email']}. "
              "Approvals are attributed through git; fix `git config user.email` first.")
        return 1
    current = content_hash(report)
    req = front(rnd / "request.md")
    if req.get("hash") != current:
        print(f"The report has changed since round {req.get('round')} was requested ({str(req.get('hash'))[:12]} → {current[:12]}).")
        print("You can only approve the version you read. Ask the author to request a new round.")
        return 1
    print(f"You are approving '{meta.get('title')}', version {current[:12]}, for publication by Vivid Insights.")
    typed = input(f"Type the first 8 characters of the version ({current[:8]}) to approve: ").strip()
    if typed != current[:8]:
        print("Not approved.")
        return 1
    dest = rnd / "approvals" / f"{rid}.yml"
    dest.write_text(f"reviewer: {rid}\ndecision: approve\nhash: {current}\ndate: {today()}\nround: {req.get('round')}\n", encoding="utf-8")
    print(f"Recorded {rel(dest)}. Now commit it yourself, so the approval is attributed to you:")
    print(f'  git add "{rel(dest)}" "{rel(form)}" && git commit -m "Approve {meta.get("report-number") or "report"} round {req.get("round")}"')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Vivid Insights review process", formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=__doc__)
    ap.add_argument("command", choices=["status", "request", "form", "approve"])
    ap.add_argument("reviewer", nargs="?", help="your reviewer id (form, approve)")
    ap.add_argument("--report", help="report Markdown (default: Report.md)")
    ap.add_argument("--allow-uncommitted", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    report = resolve_report(args.report)
    if args.command == "status":
        return cmd_status(report)
    if args.command == "request":
        return cmd_request(report, args.allow_uncommitted)
    if not args.reviewer:
        ap.error(f"{args.command} needs your reviewer id")
    return cmd_form(report, args.reviewer) if args.command == "form" else cmd_approve(report, args.reviewer)


if __name__ == "__main__":
    sys.exit(main())
