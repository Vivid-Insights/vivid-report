# Appendix

*The running record, filled from the first step. Everything a reviewer needs to check the report and that does not belong in it: where the material came from, what was decided and why, the workings, and what was tried and abandoned. Not published as part of the page.*

## Source Material

*Step 1. One entry per source: what it is, where it is (repository and commit, or file and checksum), why this source, what it may be used for, and any permission the user recorded. Copied files live in `Attachments/`.*

**1. Ask Ashbourne, the working example (copied).** An information chatbot for a fictional English secondary school, built by the author and recorded with a full log. Source: `K:\Vivid\school_bot`, not under version control; files dated 9 November 2026. Copied on 9 November 2026 to `Attachments/school_bot/`, 73 files, byte-for-byte (SHA-256 compared after copying). Checksums for every file: `Attachments/school_bot.sha256`. The two deliverables are identical to the v4 copies in `log/versions/`: `storyboard.json` ec32dff92d3bafcd0c494b27f6c56c5d52d0fa537b44ad7e4460a0c5f091077a and `storyboard.html` b2152eb0a0442fb24345609f03d00032ddfdedbcbf470355e4b3f3938826c247.
- What is in it: the storyboard (JSON, with the HTML rendered from it); `log/` (`LOG.md` as the index, the builder's brief and instruction, the build agent's instruction, `agents.md`, 13 question rounds in both directions, `area-changes.md`, `build-report.md`, storyboard v1 to v4 as HTML and JSON with the scripts that made v2 to v4); `app/` (the chatbot, built from v3, with `BUILD_NOTES.md`, data files, code, static pages and tests); `data/few_shot_examples.csv`.
- Why this source: it is the one example whose whole build is recorded, and its domain has areas.
- May be used for: the Methods and the Results. Anything quoted comes from these saved files.
- Permission: the author's own build; the school, staff, forms and dates are fictional and no real person's data is in it.
- Not copied: `.pytest_cache` and `__pycache__` (generated), and `CLAUDE.md` and `.storyboard-config.json`, which belong to the generator, not in this paper. No keys or credentials were found. `log/LOG.md`, `log/agents.md` and `log/builder-instruction.md` name the generator and are copied unchanged.
- To keep in mind: the storyboard's builder was an AI persona (Jordan Hale), not a person. The app was built from v3 and not rebuilt from v4. Times written in `LOG.md` and `build-report.md` differ from the file times (for example the build agent "~04:40–04:55" against app files dated 04:12–04:25), so check before quoting a time.

**2. Ask-Afya storyboard (not yet copied).** `K:\Himang\Akwaaba\Report\Original\storyboard.html` and `Chat Bot Storyboard.md`. The author's own and the author can publish it (recorded in the earlier session's `history.md`). To be copied with checksums when the author asks.

**3. BSC AI Career Coach storyboard (not copied, not to be published).** `K:\Himang\Akwaaba\Report\Original\BSC_storyboard.html`. Because She Can is a partner organisation. The author will not publish it (9 November 2026), so it is not copied here and not quoted in the paper.

**4. The author's structure notes and method outline (not copied).** `K:\Himang\Akwaaba\Report\Structure\` and `Method\Draft.md`. Drafts by the author, v2 and unfinished.

## Framing

*Step 2. The reader, the kind of report (method, application, evaluation), the three points of the paper and what will show each, whether the report has a `What We Have Built` section, and what was considered and set aside.*

Provisional, 3 November 2026. Step 2 is still open.

**Reader.** Chatbot developers, especially developers of domain-specific chatbots. After reading, they should be able to use the process when building their own chatbot.

**Kind of report.** A method paper. Ask-Afya is the worked example, and BSC AI Career Coach is the second storyboard. It is a demonstration, not a test: no comparison with other ways of building and no claim about how well it works. The paper says so. The storyboard is described as an intermediate representation of a builder's high-level requirements, which is stored as a JSON file and rendered as an HTML page for people to read. The agent builds from the JSON. Updated 9 November 2026 after the school_bot build, in which the build agent was given the JSON only; this replaces the earlier notes that the JSON was the agent's form (until 6 November) and that the HTML was the artifact. It is not presented as an elicitation method or a documentation format.

**Chatbot, domain.** The paper is about domain-specific chatbots. Every chatbot has areas. A small domain such as Ask-Afya's does not need them dealt with separately. A large domain such as BSC's, with ten areas, does. Defining areas decides which parts of the domain the chatbot includes in its scope.

**Examples.** Ask-Afya (small domain, v1 storyboard, built) and BSC AI Career Coach (large domain, v4 target spec, partly built) are the two existing examples. The author will not publish the BSC storyboard (9 November 2026), so nothing from it is quoted or copied; whether BSC is still described as an example is to be confirmed. The author built a third example as a working example throughout the paper: Ask Ashbourne, an information chatbot for a fictional English secondary school (Ashbourne High School), in `K:\Vivid\school_bot`, with its log in `log/`. Its storyboard builder was an AI persona (Jordan Hale), not a person, so the example shows the process running and not a developer using it. Storyboard versions v1 to v4; the app was built from v3 and not rebuilt from v4. Not yet decided: whether it replaces or adds to the Ask-Afya portion in ISSUE-003. The tabs the paper covers: five, confirmed 9 November 2026. They are Overview, Area Flow (called Areas in school_bot), Function Flows, Data Sources and Pages & Features. Left out: Issues, Tests, Test Conversation, Prompts, Build Plan and Thresholds. BSC has no Pages tab.

**The three points, revised 16 November 2026, in the author's words.**
A. Listing the conversations the chatbot should handle, breaking them down and gathering them into areas and functions. Flow belongs here: the flow of a function, like a flowchart of when it is triggered and which action happens next.
B. Exploring what the structure of the prompt looks like, by explaining what it contains and then where each part came from.
C. The general category of data each function must use, and the data the prompt mentions or uses, explained further here.

Shape for these three: not yet decided. Pages & Features is on hold, neither in nor out. Whether the Prompts tab (Prompts & Instructions) is one of the tabs is not yet decided; it is where B's subject sits in the storyboard.

What the Ashbourne files hold for each (found 16 November 2026, to be checked when the Methods is written):
- A: round 12 sorted 12 likely questions in or out of scope and added 6; AF1 chose a mix of areas and functions; 4 process areas with stages and facets; 7 flows, each with trigger, type, status, inputs, outputs and steps.
- B: `app/data/system_prompt.txt` (the storyboard's prompt, word for word) and `build_system()` in `app/ashbourne/llm.py`, which appends five parts every turn (the school information for the reply, the rule on unconfirmed details, a rule on names, the routing note, the few-shot examples). The storyboard's `prompts[0].stalenessNote` says what the file leaves out. Live mode was only run against a mock; no real model output exists. The log records two agreed rules that a prompt drafted from the storyboard dropped (round 29).
- C: 7 data sources in the storyboard, each with a type (few-shot examples, area-facet knowledge, reference list, classifier rules), `usedBy` (the function) and `origin` (synthetic or newly wired up).

Step 2 closed by the author, 16 November 2026, after revising the points and the latter half of the abstract. For this state of the report the working example is the Ask-Afya storyboard, which the author will attach; the Ashbourne files stay in `Attachments/` for later. The Prompts tab stays in; Pages & Features is on hold. Carried forward, not settled: whether the report has a `What We Have Built` section; whether BSC is still a described example; how the paper says the Ashbourne storyboard was made (an AI persona answered its questions); the weights of the three points; the Ask-Afya portion in ISSUE-003.

Superseded by the revision above (6 to 9 November 2026):
1. How to represent the builder's context or high-level specification as a structured storyboard in HTML. The storyboard is the result. (Earlier wording, superseded 6 November 2026: the storyboard is a set of questions a developer asks and answers when building a chatbot for a domain.)
2. Breaking the domain into areas, and how information flows between them. This is the heaviest point.
3. Handling function flows within an area, with their inputs, outputs and calls.

**Shape.** Weighted. Point 2 carries more than the others. The order and the shared sub-headings in the Methods and Results do not change.

**What will show each point (to confirm).**
1. The question list for each tab, and the two storyboards themselves.
2. The Area Flow tab of the BSC storyboard. Its area lifecycle (flows A to C) is marked PROPOSED in v4, so what the agent has built of it is to be confirmed. Ask-Afya has no areas, so the demonstration below does not cover this point.
3. The function tables of both storyboards, and the portion of Ask-Afya the author will build (discuss variables, and the greeting), with its logs. See ISSUE-003.

**What We Have Built section.** Not yet decided.

**Considered and set aside.**
- A comparison with the usual software development life cycle or with prompting back and forth. Removed from the abstract on 3 November 2026.
- Testing the generated app as the third point. Replaced by a demonstration with no test.
- The storyboard generator, which asks the developer the questions. Not included in this paper (author's decision, 9 November 2026): the paper describes the storyboard method only. The school_bot example was produced with the generator, so how the paper says the example storyboard was made is still to be settled.
- The questions in the Overview tab that instruct the generator ("give suggestions", "generate→ask"). Not listed explicitly. The questions are presented as things a reader should ask themselves.

**Open.** Whether the Ask-Afya demonstration will include an area; what has been built of BSC's area model; what "information flows between areas" means in the method; permission to publish the BSC storyboard; one vocabulary for the steps of a function flow (the two storyboards label them differently); tracked in ISSUE-001 to ISSUE-003 in `Report/Issues.md`.

## Literature

*Step 3, and step 6 for anything new. One row per work considered: which of the three points or which paragraph it belongs to, who found it (the user or the agent), whether it was opened in full or rests on an abstract, and whether it is cited.*

| Work | Point or paragraph | Found by | Read | Cited |
| --- | --- | --- | --- | --- |
| Silva and Canedo (2022), ICAART, DOI 10.5220/0010801800003116 | Abstract: chatbot requirements include conversation flows | Agent, earlier session | Abstract and metadata re-checked 3 Nov 2026; earlier session read pp. 1–2 | Abstract |
| Gonçalves, Silva and Canedo (2024), WER 2024, DOI 10.29327/1407529.27-19 | Abstract: chatbot requirements include conversation flows and context-dependent behaviour | Agent, earlier session | Abstract and metadata re-checked 3 Nov 2026; earlier session read pp. 1–2 | Abstract |
| Yang et al. (2025), arXiv:2505.13360 v3, preprint | Abstract: the agent fills in missing context itself | Agent, earlier session | Abstract only, re-checked 3 Nov 2026 | Abstract |

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
| 1 | 17 November 2026. The author wrote an outline under "What the Overview fixes": Overview > Definition (Domain; Audience/Tone) > Scope (What it does; How it decides; What is out of scope; Disclaimer). The agent replaced it with prose in that order and added the conversation states, which the outline did not have. Written from the Ask-Afya Ver3 storyboard only; not yet checked against the code. | `Report.md`, Methods |

## Code Summary

*Kept current whenever code is added or changed: what each script does, how to run it, what it reads and produces, and any model, prompt, seed or setting that affects the result. Installation belongs in [Setup.md](Setup.md).*

## References

*Sources behind the material, as distinct from the works the report cites.*
