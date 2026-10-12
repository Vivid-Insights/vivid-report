"""Shared paths and loaders for the report tools.

One paper per folder: `papers/NNNN-slug/` holds everything for that paper. The paper being worked
on has its Markdown at the top of the workspace as `Report.md`; the others keep theirs inside their
folders, and `tools/paper.py` moves a paper's `Report.md` in and out.

Every tool takes the path of a paper's Markdown file and resolves the paper's folder with
`paper_dir()`: for the top-level `Report.md` it is the `folder:` named in the front matter, and
for a Markdown file inside a folder it is that folder. Figure paths, `references.yaml` and the
paper's `review/` rounds are all relative to the paper's folder, so the file can move without
any of its paths changing.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
PAPERS = ROOT / "papers"
TEMPLATES = ROOT / "templates"
DEFAULT_REPORT = ROOT / "Report.md"

FRONT_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


class ReportError(Exception):
    """A fault that stops a build: the page would be wrong, not just untidy."""


def resolve_report(arg: str | None) -> Path:
    p = Path(arg) if arg else DEFAULT_REPORT
    if not p.is_absolute():
        p = (Path.cwd() / p) if (Path.cwd() / p).exists() else (ROOT / p)
    p = p.resolve()
    if not p.exists():
        if p == DEFAULT_REPORT:
            raise SystemExit("No paper is open: there is no Report.md at the top of the workspace.\n"
                             "Open one with `cd Code && uv run python tools/paper.py open <number>`, "
                             "or start one with `tools/paper.py new <slug>`.")
        raise SystemExit(f"No report at {p}")
    return p


def paper_dir(meta: dict, report: Path) -> Path:
    """The paper's own folder: where its figures, references, attachments and review rounds live."""
    if report.parent.resolve() == ROOT.resolve():
        folder = meta.get("folder")
        if not folder:
            raise ReportError(f"{report.name} is at the top of the workspace but its front matter names no `folder:`")
        d = (ROOT / folder).resolve()
        if not d.is_dir():
            raise ReportError(f"the folder named in {report.name}, {folder}, does not exist")
        return d
    return report.parent.resolve()


def load_report(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONT_RE.match(text)
    if not m:
        raise ReportError(f"{path.name} has no YAML front matter (the block between --- lines at the top)")
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, text[m.end():]


def load_yaml(path: Path, default=None):
    if not path.exists():
        return default
    return yaml.safe_load(path.read_text(encoding="utf-8")) or default


def site_config() -> dict:
    return load_yaml(SITE / "site.yml", {}) or {}


def slug_of(meta: dict, report: Path) -> str:
    s = meta.get("slug") or report.stem
    return re.sub(r"[^a-z0-9-]+", "-", str(s).lower()).strip("-")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)
