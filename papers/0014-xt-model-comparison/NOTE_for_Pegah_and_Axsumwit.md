# Note for Pegah and Axsumwit: writing report 0014 here

27 November 2026, from David

Hi Pegah and Axsumwit,

Please write up the xT model comparison as Vivid Report 0014 in this workspace. It's set up and ready for you.

## Getting started

1. Clone or pull `vivid-report` and read `README.md` and `Setup.md`. Then run `cd Code && ./setup_env.sh`.
2. Open the paper: `cd Code && uv run python tools/paper.py open 14`. Its Markdown appears at the top of the workspace as `Report.md`. Everything else for the paper is in `papers/0014-xt-model-comparison/`.
3. Open the workspace with Claude Code (or Obsidian Copilot) and say you're working on report 0014. The agent follows `instructions.md` and `WRITING.md`. It helps you write, but the decisions about what the report says are yours.

## Where it stands

We're in step 1 of eleven: gathering the material.

- The `xT_Model_comparison` repository (commit `d7a75ab`) is recorded in `Appendix.md` under `Source Material`.
- Its results, the slides, the validation note and Axsumwit's write-up (`docs/V3.docx`) are copied into `Attachments/xT_Model_comparison/`.
- `Report.md` is still the empty template.

## What we need from you first

- Axsumwit: please commit and push the window-sensitivity test that has npxG as its target. It's still uncommitted in the repository, so we can't cite it yet.
- Please export the plain-language report that sits as a claude.ai artifact, which the README links in step 7, and add it here.
- Say whether `xT_app` belongs to this report.
- Add any other material you have, such as talks, notes or feedback on the analysis.
- Confirm in `Appendix.md` that the material can be published.

Once step 1 is done, step 2 is finding the three points of the paper and writing a working abstract. Have a look at `Writing workflow.key` and `papers/0000-specimen/` for the process and what a finished report looks like.

David
