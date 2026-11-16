---
description: Say which step the report is on, what is settled, what is open, and where review stands
---
Run `cd Code && uv run python tools/paper.py list` to see which paper is open. Read `Report.md`, that paper's `Appendix.md` (the `Log` in particular, in the folder its front matter names), and the output of `cd Code && uv run python tools/review.py status`. Then tell me, briefly:

1. Which paper is open, which of the eleven steps in `instructions.md` it is on, and how you can tell.
2. What that step covers, which parts are settled, and which have not been discussed.
3. What the latest build reports (`cd Code && uv run python tools/build.py`): errors, warnings, and the style hints worth my attention.
4. Where review stands.

Do not start any work. Ask me what to do next.
