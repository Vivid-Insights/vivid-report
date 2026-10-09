"""Publish an approved report to the Vivid Insights site.

    cd Code && uv run python tools/publish.py                        # into the site checkout named in site/site.yml
    cd Code && uv run python tools/publish.py --target /tmp/try      # anywhere else, e.g. to look first

Refuses unless the report's current content hash carries enough valid approvals, each committed to
git by the reviewer who gave it (REVIEW.md). It then builds the release page — no draft banner, the
review record in the footer — copies it to `<site>/reports/<slug>/`, and updates the site's report
index. It does not commit or push the site: a person does that, after looking at the result.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, SITE, load_report, rel, resolve_report, site_config, slug_of  # noqa: E402
from reviewlib import review_dir, review_status, today  # noqa: E402


def target_dir(arg: str | None) -> Path:
    if arg:
        return Path(arg).expanduser().resolve()
    cfg = site_config()
    site = (ROOT / cfg.get("site-repo", "../Vivid-Insights-Profile")).resolve()
    return site / cfg.get("reports-path", "reports")


def update_index(target: Path, entry: dict) -> None:
    idx_file = target / "index.json"
    items = json.loads(idx_file.read_text(encoding="utf-8")) if idx_file.exists() else []
    items = [i for i in items if i.get("slug") != entry["slug"]] + [entry]
    items.sort(key=lambda i: str(i.get("date", "")), reverse=True)
    idx_file.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cards = []
    for i in items:
        e = lambda s: html.escape(str(s or ""))  # noqa: E731
        cards.append(
            f'<a class="ri-card" href="{e(i["slug"])}/"><div class="ri-num">{e(i.get("number"))} · {e(i.get("date"))}</div>'
            f'<h2>{e(i.get("title"))}</h2><p class="ri-authors">{e(", ".join(i.get("authors", [])))}</p>'
            f'<p class="ri-abs">{e(i.get("summary"))}</p>'
            f'<div class="ri-tags">{"".join(f"<span>{e(k)}</span>" for k in i.get("keywords", []))}</div></a>')
    tpl = (SITE / "reports-index.html").read_text(encoding="utf-8")
    page = tpl.replace("{{cards}}", "\n".join(cards)).replace("{{home}}", html.escape(site_config().get("home-url", "../vivid-insights.html")))
    (target / "index.html").write_text(page, encoding="utf-8")
    assets = target / "assets"
    assets.mkdir(exist_ok=True)
    for f in ("vivid-report.css", "vivid-mark.svg"):
        shutil.copy2(SITE / "assets" / f, assets / f)
    shutil.copytree(SITE / "assets" / "fonts", assets / "fonts", dirs_exist_ok=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Publish an approved report to the Vivid Insights site")
    ap.add_argument("report", nargs="?")
    ap.add_argument("--target", help="reports folder to publish into (default: from site/site.yml)")
    args = ap.parse_args(argv)
    report = resolve_report(args.report)
    from build import build, print_issues

    st = review_status(report, strict=True)
    if st["state"] not in ("approved", "published"):
        print(f"Not published: the report is '{st['state']}', and only an approved version can be published.")
        print(f"  {st.get('policy', 'no review round has been opened')}")
        for p in st["problems"]:
            print(f"  ! {p}")
        print("REVIEW.md describes the process. `review.py status` shows where it stands.")
        return 1

    meta, _ = load_report(report)
    slug = slug_of(meta, report)
    out = ROOT / "build" / f"{slug}-release"
    res, _ = build(report, out, release=True, status=st, style=False)
    if res.errors:
        print("Not published: the release build has errors.")
        print_issues(res.errors)
        return 1

    target = target_dir(args.target)
    if not target.parent.exists():
        print(f"Not published: {target.parent} does not exist. Clone the site repository there or pass --target.")
        return 1
    dest = target / slug
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(out, dest)
    abstract = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", re.search(r'<section class="vr-abstract".*?</section>', res.html, re.S).group(0)
                                            if 'class="vr-abstract"' in res.html else "")).replace("Abstract", "", 1).strip()
    update_index(target, {
        "slug": slug, "title": meta.get("title"), "number": meta.get("report-number", ""), "date": str(meta.get("date", "")),
        "authors": [a.get("name") if isinstance(a, dict) else str(a) for a in meta.get("authors") or []],
        "keywords": meta.get("keywords") or [], "summary": abstract[:280] + ("…" if len(abstract) > 280 else ""),
        "hash": st["hash"], "reviewers": (st.get("record") or {}).get("reviewers", []),
    })
    (review_dir(report) / "publication.yml").write_text(
        f"hash: {st['hash']}\ndate: {today()}\ntarget: {target / slug}\n", encoding="utf-8")
    print(f"Published version {st['hash'][:12]} to {dest}")
    print(f"Report index updated: {target / 'index.html'}")
    print("Open the page and look at it. Then, in the site repository, commit and push it yourself:")
    print(f'  cd "{target.parent}" && git add "{target.name}" && git commit -m "Publish {meta.get("report-number") or slug}" && git push')
    print(f"Also commit {rel(review_dir(report) / 'publication.yml')} in this repository.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
