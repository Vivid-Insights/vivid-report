"""One paper per folder: list the papers, open one, put it away, or start a new one.

    cd Code && uv run python tools/paper.py list               # every paper, and which one is open
    cd Code && uv run python tools/paper.py open 0002          # put the open paper away, open paper 0002
    cd Code && uv run python tools/paper.py park               # put the open paper back in its folder
    cd Code && uv run python tools/paper.py new mentoring-converser --title "…"   # start the next paper

Each paper lives in `papers/NNNN-slug/` with everything it needs: Appendix.md, references.yaml,
Attachments/, Code/ and review/. The paper being worked on has its Markdown at the top of the
workspace as `Report.md`; its front matter names its folder (`folder:`), and every path in it is
relative to that folder, so moving it changes nothing else. Only one paper is open at a time.

Moving is done by renaming the file. Nothing is ever overwritten: if the destination already
exists, the command stops and says why.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import DEFAULT_REPORT, PAPERS, ROOT, TEMPLATES, load_report, rel  # noqa: E402

ACTIVE = DEFAULT_REPORT


def papers() -> list[Path]:
    return sorted(p for p in PAPERS.glob("[0-9][0-9][0-9][0-9]-*") if p.is_dir()) if PAPERS.exists() else []


def active_folder() -> Path | None:
    if not ACTIVE.exists():
        return None
    meta, _ = load_report(ACTIVE)
    if not meta.get("folder"):
        raise SystemExit("Report.md at the top of the workspace names no `folder:` in its front matter; add it before moving it.")
    return (ROOT / meta["folder"]).resolve()


def find(which: str) -> Path:
    hits = [p for p in papers() if p.name == which or p.name.startswith(which.zfill(4) + "-") or p.name.split("-", 1)[1] == which]
    if len(hits) != 1:
        names = ", ".join(p.name for p in papers()) or "(none)"
        raise SystemExit(f"No single paper matches '{which}'. Papers: {names}")
    return hits[0]


def cmd_list() -> int:
    open_dir = active_folder()
    for p in papers():
        md = ACTIVE if open_dir == p.resolve() else p / "Report.md"
        title = ""
        if md.exists():
            meta, _ = load_report(md)
            title = meta.get("title", "")
        mark = "open  →" if open_dir == p.resolve() else "      "
        print(f"{mark} {p.name:<44} {title}")
    if open_dir is None:
        print("\nNo paper is open. `paper.py open <number>` opens one.")
    return 0


def cmd_park() -> int:
    folder = active_folder()
    if folder is None:
        print("No paper is open; nothing to put away.")
        return 0
    dest = folder / "Report.md"
    if dest.exists():
        if dest.read_bytes() == ACTIVE.read_bytes():
            ACTIVE.unlink()
            print(f"{rel(dest)} already held the same text; removed the top-level copy.")
            return 0
        raise SystemExit(f"Not moved: {rel(dest)} already exists and differs from Report.md. Compare them and keep one.")
    shutil.move(str(ACTIVE), str(dest))
    print(f"Put away: Report.md → {rel(dest)}")
    return 0


def cmd_open(which: str) -> int:
    target = find(which)
    if active_folder() == target.resolve():
        print(f"{target.name} is already open as Report.md.")
        return 0
    src = target / "Report.md"
    if not src.exists():
        raise SystemExit(f"{rel(src)} does not exist.")
    if ACTIVE.exists():
        cmd_park()
    shutil.move(str(src), str(ACTIVE))
    print(f"Opened: {rel(src)} → Report.md")
    return 0


def cmd_new(slug: str, title: str | None) -> int:
    slug = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-")
    numbers = [int(p.name[:4]) for p in papers()]
    number = f"{(max(numbers) + 1) if numbers else 1:04d}"
    folder = PAPERS / f"{number}-{slug}"
    if folder.exists():
        raise SystemExit(f"{rel(folder)} already exists.")
    shutil.copytree(TEMPLATES / "paper", folder)
    md = folder / "Report.md"
    text = md.read_text(encoding="utf-8")
    text = text.replace("{{slug}}", slug).replace("{{folder}}", rel(folder)).replace("{{number}}", number)
    if title:
        text = re.sub(r'^title: .*$', f'title: "{title}"', text, count=1, flags=re.M)
    md.write_text(text, encoding="utf-8")
    (folder / "review").mkdir(exist_ok=True)
    print(f"Created {rel(folder)}/ from templates/paper/")
    return cmd_open(number)


def main(argv=None):
    ap = argparse.ArgumentParser(description="One paper per folder", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("park")
    o = sub.add_parser("open")
    o.add_argument("paper", help="number (2 or 0002), slug, or folder name")
    n = sub.add_parser("new")
    n.add_argument("slug")
    n.add_argument("--title")
    a = ap.parse_args(argv)
    if a.cmd == "list":
        return cmd_list()
    if a.cmd == "park":
        return cmd_park()
    if a.cmd == "open":
        return cmd_open(a.paper)
    return cmd_new(a.slug, a.title)


if __name__ == "__main__":
    sys.exit(main())
