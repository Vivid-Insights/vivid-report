"""Tests that the review gate does what REVIEW.md says: only an approved version is published.

    cd Code && uv run python tests/test_review_gate.py

Builds a throwaway git repository in a temporary folder holding a copy of the specimen and three
synthetic team members (an editor, a reviewer, and an author who may not approve), then checks each
rule in turn. Nothing outside the temporary folder is touched except build/, which is regenerated.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tools"))
import publish  # noqa: E402
import review  # noqa: E402
from reviewlib import content_hash, review_status  # noqa: E402

ROOT = HERE.parents[1]
TEAM = """policy:
  required_approvals: 2
  require_editor: true
  authors_may_not_approve: true
team:
  - {id: ed, name: Edith Editor, email: ed@example.org, role: editor}
  - {id: rev, name: Rafa Reviewer, email: rev@example.org, role: reviewer}
  - {id: dsumpter, name: David Sumpter, email: author@example.org, role: editor}
"""


def git(repo, *args, email="author@example.org"):
    env = {**os.environ, "GIT_AUTHOR_NAME": email.split("@")[0], "GIT_AUTHOR_EMAIL": email,
           "GIT_COMMITTER_NAME": email.split("@")[0], "GIT_COMMITTER_EMAIL": email}
    subprocess.run(["git", *args], cwd=repo, env=env, check=True, capture_output=True)


def write_review(rnd: Path, rid: str, rec: str):
    (rnd / "reviews" / f"{rid}.md").write_text(f"---\nreviewer: {rid}\nrecommendation: {rec}\n---\n\nFixture.\n")


def write_approval(rnd: Path, rid: str, h: str):
    (rnd / "approvals" / f"{rid}.yml").write_text(f"reviewer: {rid}\ndecision: approve\nhash: {h}\ndate: 2026-10-09\nround: 1\n")


def main():
    tmp = Path(tempfile.mkdtemp(prefix="vivid-review-test-"))
    repo = tmp / "report"
    shutil.copytree(ROOT / "papers" / "0000-specimen", repo, ignore=shutil.ignore_patterns("build", ".DS_Store"))
    report = repo / "Report.md"
    (repo / "review").mkdir(exist_ok=True)
    (repo / "review" / "reviewers.yml").write_text(TEAM)
    git(repo, "init", "-q")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "fixture")
    target = tmp / "site" / "reports"
    target.parent.mkdir()
    results = []

    def check(name, cond):
        results.append((name, bool(cond)))
        print(f"  {'ok  ' if cond else 'FAIL'} {name}")

    st = review_status(report, strict=True)
    check("a report with no review round is a draft", st["state"] == "draft")
    check("publish refuses a draft", publish.main([str(report), "--target", str(target)]) == 1)

    check("review request opens round 1", review.cmd_request(report, False) == 0)
    rnd = repo / "review" / "round-01"
    git(repo, "add", "review")
    git(repo, "commit", "-qm", "request round 1")
    h = content_hash(report)
    check("the round froze the current hash", h in (rnd / "request.md").read_text())
    check("a second request for the same version is refused", review.cmd_request(report, False) == 1)

    write_review(rnd, "ed", "minor")
    git(repo, "add", ".", email="ed@example.org")
    git(repo, "commit", "-qm", "ed reviews", email="ed@example.org")
    check("a review asking for changes gives 'changes-requested'", review_status(report)["state"] == "changes-requested")

    write_review(rnd, "ed", "accept")
    write_review(rnd, "rev", "accept")
    write_approval(rnd, "ed", h)
    write_approval(rnd, "rev", h)
    st = review_status(report, strict=True)
    check("uncommitted approvals do not count", st["state"] != "approved" and any("commit" in p for p in st["problems"]))

    git(repo, "add", "review/round-01/reviews/ed.md", "review/round-01/approvals/ed.yml", email="ed@example.org")
    git(repo, "commit", "-qm", "ed approves", email="ed@example.org")
    git(repo, "add", "review/round-01/reviews/rev.md", "review/round-01/approvals/rev.yml", email="author@example.org")
    git(repo, "commit", "-qm", "author commits rev's approval", email="author@example.org")
    st = review_status(report, strict=True)
    check("an approval committed by someone else does not count",
          st["state"] != "approved" and any("committed by author@example.org" in p for p in st["problems"]))

    # The reviewer re-approves and commits it themselves: the last commit to the file is now theirs.
    write_approval(rnd, "rev", h)
    p = rnd / "approvals" / "rev.yml"
    p.write_text(p.read_text() + "note: re-approved by the reviewer\n")
    git(repo, "add", "review/round-01/approvals/rev.yml", email="rev@example.org")
    git(repo, "commit", "-qm", "rev approves", email="rev@example.org")
    st = review_status(report, strict=True)
    check("two valid approvals, one from an editor: approved", st["state"] == "approved")

    # Someone else then edits the reviewer's approval: it stops counting.
    p = rnd / "approvals" / "rev.yml"
    p.write_text(p.read_text() + "note: edited\n")
    git(repo, "add", "-A", "review", email="author@example.org")
    git(repo, "commit", "-qm", "author edits rev's approval", email="author@example.org")
    check("an approval edited by someone else after the reviewer stops counting", review_status(report, strict=True)["state"] != "approved")
    git(repo, "revert", "--no-edit", "HEAD", email="rev@example.org")
    check("the reviewer restoring it under their own commit makes it count again", review_status(report, strict=True)["state"] == "approved")

    check("publish succeeds for the approved version", publish.main([str(report), "--target", str(target)]) == 0)
    page = (target / "specimen" / "index.html").read_text()
    check("the published page has no draft banner", "vr-banner" not in page.split("<body")[1].split("vr-layout")[0])
    check("the published page carries the review record", "Reviewed by the Vivid Insights team" in page and "Edith Editor" in page)
    check("the site index lists the report", "specimen/" in (target / "index.html").read_text())

    text = report.read_text()
    report.write_text(text.replace("This specimen makes no empirical claim.", "The specimen makes no empirical claim."))
    st = review_status(report, strict=True)
    check("one edit after approval makes the approvals stale", st["state"] != "approved" and any("changed after approval" in p for p in st["problems"]))
    check("publish refuses the edited version", publish.main([str(report), "--target", str(target)]) == 1)
    report.write_text(text)
    check("reverting the edit restores the approved state", review_status(report, strict=True)["state"] in ("approved", "published"))

    # The author may not approve their own report, even as an editor.
    write_review(rnd, "dsumpter", "accept")
    write_approval(rnd, "dsumpter", h)
    git(repo, "add", "-A", "review", email="author@example.org")
    git(repo, "commit", "-qm", "author approves", email="author@example.org")
    st = review_status(report, strict=True)
    check("an author's approval is rejected", any("is an author" in p for p in st["problems"]))

    # Without the editor's approval the policy is not met.
    git(repo, "rm", "-q", "review/round-01/approvals/ed.yml", email="ed@example.org")
    git(repo, "commit", "-qm", "ed withdraws", email="ed@example.org")
    st = review_status(report, strict=True)
    check("approvals without an editor do not meet the policy", st["state"] != "approved")

    shutil.rmtree(tmp)
    # The pages built from the fixture name the synthetic reviewers: do not leave them lying around.
    for d in ("specimen-release", "specimen-review-round-01"):
        shutil.rmtree(ROOT / "build" / d, ignore_errors=True)
    failed = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(failed)} of {len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
