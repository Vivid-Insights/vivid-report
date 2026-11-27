# Appendix

*The running record, filled from the first step. Everything a reviewer needs to check the report and that does not belong in it: where the material came from, what was decided and why, the workings, and what was tried and abandoned. Not published as part of the page.*

## Source Material

*Step 1. One entry per source: what it is, where it is (repository and commit, or file and checksum), why this source, what it may be used for, and any permission the user recorded. Copied files live in `Attachments/`.*

### 1. `xT_Model_comparison` repository (Axsumwit)

- **Where.** `~/GitHub/xT_Model_comparison`, remote `https://github.com/atassew/xT_Model_comparison`. Commit `d7a75ab0b5a8cf4b672a07dcb8db8dc963c342ea` (10 November 2026), "Add goals-target window test, slide deck and validation note". The working copy has uncommitted changes beyond it: edits to `README.md` and `run.py`, and the untracked `tests/test_window_test.py` and `results/window_{coefficients,metrics,predictions}.csv` (the window-sensitivity test with npxG as target).
- **What it is.** Asks whether a team's average expected-threat value over its last 10 matches predicts its non-penalty xG in the next match. Three action-valuation methods built from raw StatsBomb JSON: Karun Singh's xT, Sumpter's action-based xT (Soccermatics), and VAEP (Decroos et al.). StatsBomb open data 2015/16, five leagues, leave-one-league-out training, walk-forward forecasts per league (1,994 forecasts). Eleven regression models: baseline on past npxG, each method alone, Model 2 (past npxG + method), and opponent models (Baseline+opp, M3). Tests: Clark–West, Diebold–Mariano, team-block bootstrap of ΔRMSE, clustered t and F tests. A window-sensitivity test over windows of 1 to 20 matches, with npxG and goals as targets.
- **Code.** `xtn/` (data conversion, the three methods in `xtn/methods/`, features, forecasting, inference, window test), `run.py`, `checks/` (one check script per method and the panel), `tests/`, `plot_goals.py`, `plot_window.py`.
- **Copied to `Attachments/xT_Model_comparison/`**, unchanged: `README.md`, `docs/V3.docx`, and `results/` including the uncommitted window files, but without the large `results/checks/*.parquet` and `*.npy` files (VAEP values and Karun grids per fold, which can be regenerated). Checksums in `Attachments/xT_Model_comparison/SHA256SUMS` (38 files).
- **Inside the copy.** `docs/V3.docx`: a plain-language write-up, "Does past xT predict a team's next-match xG?", dated 29 October 2026, by Axsumwit. `results/validation_note.pdf`/`.html`: a validation note. `results/xt_slides.pdf`/`.html`: a slide deck. CSVs of metrics, predictions, coefficients and the four tests; the window-sensitivity figures; run logs.
- **Also mentioned.** The README's step 7 links a plain-language report as a claude.ai artifact. It has not been opened.
- **Permission.** [CHECK: ask Axsumwit and record whether the repository, results and write-up may be published.]

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
