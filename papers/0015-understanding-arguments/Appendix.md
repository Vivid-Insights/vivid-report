# Appendix

*The running record, filled from the first step. Everything a reviewer needs to check the report and that does not belong in it: where the material came from, what was decided and why, the workings, and what was tried and abandoned. Not published as part of the page.*

## Source Material

*Step 1. One entry per source: what it is, where it is (repository and commit, or file and checksum), why this source, what it may be used for, and any permission the user recorded. Copied files live in `Attachments/`.*

## Framing

*Step 2. The reader, the kind of report (method, application, evaluation), the three points of the paper and what will show each, whether the report has a `What We Have Built` section, and what was considered and set aside.*

## Literature

*Step 6, and step 7 for anything new. One row per work considered: which of the three points or which paragraph it belongs to, who found it (the user or the agent), whether it was opened in full or rests on an abstract, and whether it is cited.*

| Work | Point or paragraph | Found by | Read | Cited |
| --- | --- | --- | --- | --- |

## Method Facts

*Steps 3 to 5, one point at a time. One row per fact the report states about the method, with the place in the code that makes it true. Re-checked in step 9 against the commit recorded here.*

| Fact | Where in the code | Commit |
| --- | --- | --- |

## Workings

*Steps 3 to 5. One sub-heading per example or evaluation: how each case was chosen, which outputs were generated with what model, prompt and configuration. Only what serves the writing: no bugs, set-up problems or debugging.*

## Log

*A numbered row per step taken, added as the work happens: what was done, what it changed, and where the output is. Decisions about the paper, not the troubleshooting behind them. Superseded decisions stay, marked as such. Review rounds, the disclaimer confirmation and publication are recorded here too.*

| # | What was done | Output |
| --- | --- | --- |

## Code Summary

*Kept current whenever code is added or changed: what each script does, how to run it, what it reads and produces, and any model, prompt, seed or setting that affects the result. Installation belongs in [Setup.md](Setup.md).*

## References

*Sources behind the material, as distinct from the works the report cites.*
