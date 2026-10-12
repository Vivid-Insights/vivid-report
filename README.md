# Vivid Insights report workspace

A folder for writing a Vivid Insights research report with an agent, one step at a time, and publishing it as a web paper once the Vivid Insights team has reviewed it.

The reports are about methods — wordalisation, storyboarding, conversers and other agentic AI — and their use in football, medicine and mentorship. The page reads like an arXiv paper: Latin Modern type, numbered sections, equations, booktabs tables, author–date citations, and it prints as one. It also does what paper cannot: video figures, interactive figures, generated text quoted exactly from the file it was saved in, and conversations with a converser. It carries the Vivid Insights brand and follows the reader's light or dark theme.

`papers/0000-specimen/` uses every part of the format. Build it to see what a report looks like:

```bash
cd Code && ./setup_env.sh
uv run python tools/build.py ../papers/0000-specimen/Report.md --open
```

## How it works

The agent's working contract is [instructions.md](instructions.md), and the writing rules are [WRITING.md](WRITING.md); `CLAUDE.md` loads both. The agent does one step per request and then stops. It agrees each figure, example and evaluation with you before making it, quotes generated text rather than writing it, and ties every fact about a method to the place in the code that makes it true. The parts that need judgement stay with you.

| Step | What happens | What it fills in |
| --- | --- | --- |
| 1 | Gather the material: code, apps, prompts, saved outputs, transcripts | `Source Material` in the appendix |
| 2 | Frame the report: the reader, the kind of report, the contributions | `Framing`; the `Introduction` |
| 3 | Describe the method from the code, naming every normative choice | `Method`; `Method Facts` |
| 4 | Examples: figures, video and interactive figures, quoted outputs | `Examples` |
| 5 | Evidence, if the report claims the method works | `Evaluation` |
| 6 | Discussion and limitations | `Discussion`, `Limitations` |
| 7 | Background, abstract and title | `Introduction`, `Abstract` |
| 8 | Read through the built page | A list of what is still wrong |
| 9 | Review by the Vivid Insights team | the paper's `review/round-NN/` |
| 10 | Publish to the Vivid Insights site | `reports/<slug>/` on the site |

Ask for the next step when you are ready. `/where-are-we` asks the agent to say which step it thinks you are on, and `/build` builds and opens the page.

## Review before publication

Nothing is published until the team has reviewed it. [REVIEW.md](REVIEW.md) describes the process. In short: the author freezes a version by its content hash and opens a review round; reviewers write their reviews and, when satisfied, approve that exact hash and commit the approval under their own name; `publish.py` refuses anything without enough valid approvals for the current version. Any edit after approval — a comma, a regenerated figure — sends the report back. The agent cannot write reviews or approvals: the contract forbids it and a hook in `.claude/` blocks it. Every unreviewed page carries a draft banner.

## What is in the folder

| Location | What it is |
| --- | --- |
| [Report.md](Report.md) | The paper you are working on. It belongs to a folder in `papers/`, named in its front matter, and moves back there when you open another paper. |
| `papers/NNNN-slug/` | One paper per folder, with everything it needs: `Appendix.md` (the running record, read by reviewers), `references.yaml`, `Attachments/` (source material, never modified), `Code/` (its figure, video and interactive scripts and outputs) and its review rounds. |
| `papers/0000-specimen/` | The specimen: a short paper using every block. |
| `Code/` | Shared: `tools/` (build, check, paper, review, publish), `tests/`, `viz_style.py` and the Python environment. |
| `templates/` | Shared: the empty paper `paper.py new` copies, and the reviewers' forms. |
| `review/reviewers.yml` | Shared: the review team and the approval policy. |
| `site/` | The report design: template, stylesheet, fonts, and `site.yml` (where to publish). |
| [instructions.md](instructions.md) | The agent's contract. Change it by starting a message with `FRAMEWORK`. |
| [WRITING.md](WRITING.md) | How the prose is written, with a log of corrections. |
| [FORMAT.md](FORMAT.md) | The report's Markdown: figures, videos, interactives, quoted outputs, citations, cross-references. |
| [REVIEW.md](REVIEW.md) | The review process, for authors and reviewers. |
| [Setup.md](Setup.md) | Installation and everyday commands. |

## One paper per folder

Every paper has a numbered folder in `papers/` holding everything for that paper. The paper you are working on sits at the top of the workspace as `Report.md`, so you and the agent always work on the same file; its paths all point into its folder, so it can move without anything breaking.

```bash
cd Code
uv run python tools/paper.py list                 # every paper, and which one is open
uv run python tools/paper.py new mentoring-app    # start paper 0002 in papers/0002-mentoring-app/ and open it
uv run python tools/paper.py open 1               # put the open paper away and open paper 0001
uv run python tools/paper.py park                 # put the open paper back in its folder
```

Then ask the agent for step 1. All papers live together on `main`; commit each paper on its own, and keep changes to the shared tools and documents in commits of their own.

## Origins

The step-by-step contract is adapted from [human-agentic-data-analysis](../human-agentic-data-analysis), which does the same for data analyses. The writing rules come from the article on communicating individual health risk, where they were collected from David Sumpter's corrections. The design follows the Vivid Insights site.

## Licence

This template — the contract, the documents, the code and the design — is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE). Latin Modern is under the GUST Font License. Each report states its own licence in its front matter.
