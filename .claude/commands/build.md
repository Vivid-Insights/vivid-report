---
description: Build the report page, open it, and summarise what the build found
---
Run `cd Code && uv run python tools/build.py --open` (or on the file I name: $ARGUMENTS). Then list the errors, the warnings, and the style hints, grouped, with the line each refers to. For each error say what is wrong and what would fix it, but do not fix anything until I ask. For style hints, say which you think are real and which are false alarms (a quotation, a name), and why.
