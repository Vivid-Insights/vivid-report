"""Verify the report environment and print exact versions.

Run with:  cd Code && uv run python check_env.py

Reads nothing and writes nothing. Prints one line per required package and
exits non-zero if any is missing, so it doubles as a reproducibility record:
paste the output into Appendix.md when environment versions affect results.
"""

from __future__ import annotations

import importlib
import importlib.metadata as md
import platform
import sys

REQUIRED = [
    ("markdown_it", "markdown-it-py"),
    ("mdit_py_plugins", "mdit-py-plugins"),
    ("yaml", "pyyaml"),
    ("numpy", "numpy"),
    ("pandas", "pandas"),
    ("matplotlib", "matplotlib"),
    ("imageio", "imageio"),
    ("imageio_ffmpeg", "imageio-ffmpeg"),
]


def main() -> int:
    print(f"Python   {platform.python_version()}  ({sys.executable})")
    print("-" * 62)

    missing: list[str] = []
    for import_name, dist_name in REQUIRED:
        try:
            importlib.import_module(import_name)
            print(f"{dist_name:<14} {md.version(dist_name)}")
        except Exception:
            print(f"{dist_name:<14} MISSING")
            missing.append(dist_name)

    print("-" * 62)
    if missing:
        print(f"FAIL: {len(missing)} package(s) missing: {', '.join(missing)}")
        print("Run ./setup_env.sh to install them.")
        return 1
    print("OK: environment complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
