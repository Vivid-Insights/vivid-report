# Appendix

*The running record, filled from the first step. Everything a reviewer needs to check the report and that does not belong in it: where the material came from, what was decided and why, the workings, and what was tried and abandoned. Not published as part of the page.*

## Source Material

*Step 1. One entry per source: what it is, where it is (repository and commit, or file and checksum), why this source, what it may be used for, and any permission the user recorded. Copied files live in `Attachments/`.*

**`agentic-ai-for-statistics-and-data-science`** — David's course repository on working through a statistical analysis with an agent: fifteen numbered chapters (1.1–1.8 on the steps of an analysis, 2.1–2.7 on frameworks, ethics and automation), plus `Overview.md`, `How I Built This Folder.md`, `CONTRIBUTOR_GUIDE.md`, `Transcripts/`, `Scripts/` and the `Uppsala Course` material. At `~/GitHub/agentic-ai-for-statistics-and-data-science`, commit `3d858b6` ("Fill in the chapters and transcripts for the Overview and 1.1 recordings"). Named by David as the source for the claim that the steps of a statistical analysis are nearly fully automated. Not yet read; nothing copied into `Attachments/` yet. Permission: David's own material, not yet confirmed as publishable in this report.

**This workspace** — `instructions.md`, `WRITING.md`, `FORMAT.md`, `REVIEW.md`, `README.md`, `review/reviewers.yml`, `templates/`, `site/` and the specimen paper are the working description of how a Models and Words article is written and reviewed. Candidate source, not yet confirmed by David.

**The other papers in the workspace** — `papers/0002-representing-data-in-words/` and `papers/0003-twelve-earpiece/` are the first two articles, and are what the journal's scope would have to cover. Candidate source, not yet confirmed.

## Framing

*Step 2. The reader, the kind of report (method, application, evaluation), the three points of the paper and what will show each, whether the report has a `What We Have Built` section, and what was considered and set aside.*

### David's starting note, 2 November 2026

Recorded as written, before step 2. Not yet worked into three points.

The idea of this paper is to explain the concept of the journal.

Basic idea: large language models mean a massive change in how we do mathematical modelling and statistics. (Material from `agentic-ai-for-statistics-and-data-science`.) The steps themselves are nearly fully automated.

An important question becomes how to relate the mathematical models to the words we say and think about it. "How do… (needs work)" — left unfinished by David.

The types of article the journal is interested in:

- Work about using agentic AI to interpret data and create models.
- Best practices in the use of agentic AI in statistics and data science.
- Applications of large language models.
- Reliable and trustworthy communication by language models.
- Tutorials about models and — left unfinished by David.

Publisher: Vivid Insights remains the responsible publisher of the journal's articles.

### Open

- The sentence beginning "How do…" and the fifth article type "Tutorials about models and…" are unfinished.
- Who the article is for, what kind of article it is, and its three points: not yet discussed.

## Literature

*Step 3, and step 6 for anything new. One row per work considered: which of the three points or which paragraph it belongs to, who found it (the user or the agent), whether it was opened in full or rests on an abstract, and whether it is cited.*

| Work | Point or paragraph | Found by | Read | Cited |
| --- | --- | --- | --- | --- |

## Method Facts

*Step 4. One row per fact the report states about the method, with the place in the code that makes it true. Re-checked in step 8 against the commit recorded here.*

| Fact | Where in the code | Commit |
| --- | --- | --- |

## Workings

*Step 5. One sub-heading per example or evaluation: how each case was chosen, which outputs were generated with what model, prompt and configuration. Only what serves the writing: no bugs, set-up problems or debugging.*

## Log

*A numbered row per step taken, added as the work happens: what was done, what it changed, and where the output is. Decisions about the paper, not the troubleshooting behind them. Superseded decisions stay, marked as such. Review rounds, the disclaimer confirmation and publication are recorded here too.*

| # | What was done | Output |
| --- | --- | --- |
| 1 | Paper created. The workspace was renumbered so this paper could take 0001: the wordalisation paper moved to `papers/0002-representing-data-in-words/` and the Earpiece paper to `papers/0003-twelve-earpiece/`, each with its front matter, script run commands and appendix paths updated. This paper was copied from `templates/paper/` and opened as `Report.md`. | `papers/0001-what-is-models-and-words/` |
| 2 | Step 1 begun. David's starting note on the journal's concept and its five article types recorded in `Framing`; `agentic-ai-for-statistics-and-data-science` recorded in `Source Material` at commit `3d858b6`, not yet read. `Report.md` untouched. | this file |

## Code Summary

*Kept current whenever code is added or changed: what each script does, how to run it, what it reads and produces, and any model, prompt, seed or setting that affects the result. Installation belongs in [Setup.md](Setup.md).*

## References

*Sources behind the material, as distinct from the works the report cites.*
