# Setup

*Part of the [Vivid Insights report workspace](README.md).* Everything needed to get the workspace running. Do this once per machine.

## 1. Claude Code, and optionally Obsidian

The agent is Claude Code. Install it following <https://code.claude.com/docs/en/setup>, run `claude` once in a terminal and sign in. Then work from this folder in a terminal, in VS Code with the Claude Code extension, or in Obsidian.

For Obsidian, choose *Open folder as vault* and select this folder; the vault settings come with the repository. Install the [Claudian](https://github.com/YishenTu/claudian) community plugin to have the agent beside the documents, and check that Claude Code is the provider selected in its settings.

## 2. uv

[uv](https://docs.astral.sh/uv/) manages the Python version and every package.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh     # macOS / Linux
```

## 3. The Python environment

```bash
cd Code && ./setup_env.sh
```

This reads `Code/uv.lock`, creates `Code/.venv`, and prints the versions it installed. Re-run it whenever `uv.lock` changes. Video figures need no system ffmpeg: `imageio-ffmpeg` brings its own.

## 4. Check it works

```bash
cd Code && uv run python tools/build.py "../Sample Report/Specimen.md" --open
```

The specimen should open in your browser with a yellow "Draft" banner, four figures (one of them a video and one interactive), and no errors.

## Everyday commands

All from `Code/`:

```bash
uv run python tools/build.py --open               # build Report.md and open it
uv run python tools/check.py                      # errors, warnings and writing-style hints
uv run python tools/check.py --release            # as review and publishing will: unfinished work is an error
uv run python tools/review.py status              # where the report stands in review
uv run python tools/review.py request             # open a review round (after step 8, committed)
uv run python tools/publish.py                    # publish an approved report to the site
uv run python my_figure.py                        # a figure script
uv add <package>                                  # add a dependency, updating uv.lock
uv run python tests/test_review_gate.py           # test that the review gate refuses what it should
```

Reviewers, in their own terminal:

```bash
uv run python tools/review.py form <your-id>
uv run python tools/review.py approve <your-id>
```

## Publishing target

`site/site.yml` says where approved reports go: by default `../Vivid-Insights-Profile/reports/<slug>/`, so the site repository should be cloned beside this one. Set `base-url` there once the site has a public address.

## What the environment contains

| Component | Version | For |
| --- | --- | --- |
| Python | 3.12.13 | |
| markdown-it-py | 4.2.0 | building the page |
| mdit-py-plugins | 0.6.1 | footnotes and maths in the page |
| pyyaml | 6.0.3 | front matter, references, review files |
| numpy | 2.5.3 | figures |
| pandas | 3.0.6 | figures |
| matplotlib | 3.11.2 | figures and video frames |
| imageio | 2.38.1 | video figures |
| imageio-ffmpeg | 0.6.0 | video encoding (bundled ffmpeg 7.1) |

Verified by `uv run python check_env.py` on 9 October 2026. The page itself loads KaTeX 0.16.11 from jsDelivr when a report has maths, and the Space Grotesk, Inter and IBM Plex Mono fonts from Google Fonts. Latin Modern, the body font, is included in `site/assets/fonts/` under the GUST Font License.

## Troubleshooting

**`uv: command not found`** — restart the shell after installing uv.

**The page shows an old figure** — browsers cache images. Reload with Shift held down.

**A video does not play in the built page opened from disk** — some browsers restrict `file://` pages. Serve the folder instead: `cd build/<slug> && python3 -m http.server 8000`, then open <http://localhost:8000>.

**An interactive figure is blank** — open its `index.html` on its own and look at the browser console. Interactives must be self-contained.
