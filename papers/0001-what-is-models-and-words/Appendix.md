# Appendix

*The running record, filled from the first step. Everything a reviewer needs to check the report and that does not belong in it: where the material came from, what was decided and why, the workings, and what was tried and abandoned. Not published as part of the page.*

## Source Material

*Step 1. One entry per source: what it is, where it is (repository and commit, or file and checksum), why this source, what it may be used for, and any permission the user recorded. Copied files live in `Attachments/`.*

**`agentic-ai-for-statistics-and-data-science`** — David's course repository on working through a statistical analysis with an agent: fifteen numbered chapters (1.1–1.8 on the steps of an analysis, 2.1–2.7 on frameworks, ethics and automation), plus `Overview.md`, `How I Built This Folder.md`, `CONTRIBUTOR_GUIDE.md`, `Transcripts/`, `Scripts/` and the `Uppsala Course` material. At `~/GitHub/agentic-ai-for-statistics-and-data-science`, commit `3d858b6` ("Fill in the chapters and transcripts for the Overview and 1.1 recordings"). Named by David as the source for the claim that the steps of a statistical analysis are nearly fully automated. Not yet read; nothing copied into `Attachments/` yet. Permission: David's own material, not yet confirmed as publishable in this report.

**This workspace** — `instructions.md`, `WRITING.md`, `FORMAT.md`, `REVIEW.md`, `README.md`, `review/reviewers.yml`, `templates/`, `site/` and the specimen paper are the working description of how a Models and Words article is written and reviewed. Candidate source, not yet confirmed by David.

**`Davids-Vault/Twelve Models (do not share externally)/Algorithms and Models`** — Twelve's internal index of its models, exported from Notion. The hub page states three principles: models are explainable in football terms ("understandable"), they relate to goals scored and conceded ("help teams win"), and each problem gets the best motivated approach ("advanced AI"). Its child page `Modelling Philosophy` is the closest thing in the material to a statement of the journal's position: it separates the **mathematical model** of the data from the **normative model** that says what the model means in words, defines normative as setting a standard for judging behaviour or outcomes, says stakeholders define the norms, and argues against black-box methods on Rudin's grounds that high-stakes decisions need interpretable models rather than post-hoc explanations. Other child pages: `Building a Twelve Analyst`, `Qualities, Metrics and Summaries`, `Wordalisations`, `Visualisations`, `Context Engineering for Football`, `Automated documentation`, and the model pages (transfer, team strength, league strength, Total Football, financial, zonal threat, zonal xG, Twelve Index, player name search, van Dijk metrics, coach analysis). **Permission: the folder is marked "do not share externally". Nothing from it can be quoted or paraphrased in the report without David confirming Twelve's agreement.**

**`Davids-Vault/Models and AI/`** — David's own writing on modelling, and the academic framing the Twelve philosophy points back to. Four pieces bear on the journal's concept:

- *Building models in the age of machine learning and AI* — research notes. Machine learning gives the biggest recent advances but no mechanistic understanding, which challenges the traditional modelling cycle of formulating a mechanism, fitting it and predicting. Proposes integrative pluralism: many models of the same system rather than one. Opens on Breiman's two cultures; uses football and complex-systems models (cellular automata, self-propelled particles, current-reinforced oscillators) as the two extremes.
- *The Lost Art of Mathematical Modelling* — Gyllingberg, Birhane and Sumpter. Published; PDF at `Attachments/Lost art.pdf`. Of the three modelling activities — formulating, analysing, fitting — researchers over-invest in analysing at the cost of formulating.
- *Coherence, charity and triangulation in statistical modelling* — Sumpter, August 2025. Uses Davidson's third dogma to argue that model and data are parts of one belief system, and that a belief system should be coherent, charitable and triangulated.
- *Most models are true, because they are useful* — short note against Box's aphorism: a model is judged by its assumptions, how it relates to earlier models, the view of the world it constructs and the consequences for those who take that view.

Permission: David's own unpublished writing, except *The Lost Art*, which is published.

**`context-engineering`** — the course repository beside the vault, at `~/GitHub/context-engineering`, commit `dc7c387`. Seven lessons: `0. Context Engineering` (hub), `1. Introduction`, `2. Prompting and Parroting`, `3. Wordalisation`, `4. Interpretable Models`, `5. Embedding, annotation and function calling`, `6. Conversational context`, plus `List of Projects` and `Transcripts/`. The hub states the course's claim: build a data context for any question a user poses, then turn the data into insight, for building AI analysts that advise users making decisions — "the examples are from football … but the methodology can be applied to any complex system where decisions are made". Lesson 4 opens on Breiman's two cultures and works the mechanistic and data-driven approaches to expected goals side by side. Lesson 1 opens on having a mission, and says what a person needs before building an analyst: a reason, competence in the area, and access to the data decisions rest on. The accompanying code is in a separate repository, `Context-Engineering-Course`. Not yet read in full; lessons 0, 1 and 4 opened.

**The first two papers in the workspace** — named by David as giving the flavour of the journal. `papers/0002-representing-data-in-words/` introduces wordalisation: a method for generating narratives from data, applied to football scouting, personality tests and international survey data, evaluated by LLM-as-a-judge and human-as-a-judge, with a section on open and transparent development of communication about data. `papers/0003-twelve-earpiece/` describes a conversational football analyst built as a choose-your-own-adventure: specialised analysts with redirects, name resolution, wordalisation functions and embedding search, tested on a hand-written set of queries and judged blind against a general coding agent. Both are in the workspace and are the journal's own output.

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

### David's second note, 2 November 2026

Brainstorming, recorded as given. The paper could start the way David wrote it in *Algorithms and Models*, in the Twelve section of his vault: that this is a journal about **how we use and interpret models, and how we build systems which can communicate the conclusions from models**. The context engineering course may give further ideas, and the workspace's first two papers give the flavour of what the journal publishes.

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
| 3 | Step 1 continued. David's second note recorded in `Framing`: the journal is about how we use and interpret models and how we build systems that communicate the conclusions from models. Four further sources opened and described in `Source Material`: Twelve's `Algorithms and Models` and its `Modelling Philosophy` page (marked do not share externally), the `Models and AI` folder of David's vault, the `context-engineering` course at commit `dc7c387`, and the workspace's first two papers. `Report.md` untouched. | this file |

## Code Summary

*Kept current whenever code is added or changed: what each script does, how to run it, what it reads and produces, and any model, prompt, seed or setting that affects the result. Installation belongs in [Setup.md](Setup.md).*

## References

*Sources behind the material, as distinct from the works the report cites.*
