# Appendix

*The running record, filled from the first step. Everything a reviewer needs to check the report and that does not belong in it: where the material came from, what was decided and why, the workings, and what was tried and abandoned. Not published as part of the page.*

## Source Material

*Step 1. One entry per source: what it is, where it is (repository and commit, or file and checksum), why this source, what it may be used for, and any permission the user recorded. Copied files live in `Attachments/`.*

## Framing

*Step 2. The reader, the kind of report (method, application, evaluation), the contributions and what will show each, and what was considered and set aside.*

## Method Facts

*Step 3. One row per fact the report states about the method, with the place in the code that makes it true. Re-checked in step 8 against the commit recorded here.*

| Fact | Where in the code | Commit |
| --- | --- | --- |

## Workings

*Steps 4 and 5. One sub-heading per example or evaluation: how each case was chosen, which outputs were generated with what model, prompt and configuration, the diagnostics, and anything made but not used.*

## Log

*A numbered row per step taken, added as the work happens: what was done, what it changed, and where the output is. Superseded decisions stay, marked as such. Review rounds, the disclaimer confirmation and publication are recorded here too.*

| # | What was done | Output |
| --- | --- | --- |

## Code Summary

*Kept current whenever code is added or changed: what each script does, how to run it, what it reads and produces, and any model, prompt, seed or setting that affects the result. Installation belongs in [Setup.md](Setup.md).*

## References

*Sources behind the material, as distinct from the works the report cites.*
