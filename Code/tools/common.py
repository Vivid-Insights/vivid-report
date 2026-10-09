"""Shared paths and loaders for the report tools.

Every tool takes the path of a report's Markdown file. The folder that file sits in is the
report's own root: figure paths, `references.yaml` and `review/` are all resolved against it,
so `Report.md` at the top of the workspace and `Sample Report/Specimen.md` build the same way.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
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
        raise SystemExit(f"No report at {p}")
    return p


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
