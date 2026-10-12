# Report Writing Instructions

The working contract for writing a Vivid Insights research report with an agent. The agent reads this file and `WRITING.md` at the start of every conversation (through `CLAUDE.md`). `FORMAT.md` is the reference for the report's Markdown, and `REVIEW.md` for the review that every report passes before it is published.

Vivid Insights reports are about methods: wordalisation, storyboarding, conversers and other agentic AI methods, and their application in football, medicine and mentorship. They differ from a data analysis in what counts as evidence. Here the evidence is mostly the method itself — its code, its prompts, its normative choices — and what it produces: generated texts, conversations, apps. The contract below is built around keeping that evidence and the prose that describes it in step.

## Workspace Contract

One paper per folder. Everything belonging to a paper is in its folder, `papers/NNNN-slug/`; everything shared by all papers is at the top of the workspace. The paper being worked on has its Markdown at the top as `Report.md`, and only one paper is open at a time.

| Location | Purpose |
| --- | --- |
| `Report.md` | The paper being worked on: its Markdown, which is the source of its web page; `FORMAT.md` gives the syntax. Built up across the steps rather than written at the end; nothing enters a section before the step that owns it. Its front matter names its folder (`folder: papers/NNNN-slug`), and every path in it is relative to that folder. When another paper is opened, it moves back into its folder. |
| `papers/NNNN-slug/` | One paper and everything it needs. The number is the paper's report number. |
| `papers/…/Appendix.md` | The paper's running record, written as you go from the first step: `Source Material`, `Framing`, `Method Facts`, `Workings`, `Log`, `Code Summary`, `References`. Not published; it is what a reviewer reads to check the page. |
| `papers/…/references.yaml` | Every work the paper cites, with a link. The reference list on the page is generated from it. |
| `papers/…/Attachments/` | Source material for the paper: saved model outputs, transcripts, prompt files copied from an app, the paper's source if it exists elsewhere, screen recordings (`Attachments/media/`), literature (`Attachments/literature/`, not committed). Never modified. Each item has its provenance in `Source Material`. |
| `papers/…/Code/` | Every script that makes a figure, a video figure or a number in the paper, with its outputs under `Code/outputs/`, and interactive figures in `Code/interactives/`, one folder each. A figure script starts with `viz_style.for_paper(__file__)` so its output lands here. |
| `papers/…/review/` | The paper's review rounds, one `round-NN/` folder each. `REVIEW.md` says who writes what. The agent never writes in `reviews/` or `approvals/`. |
| `papers/0000-specimen/` | A specimen paper that uses every kind of block. It is there to show what the format looks like; it is not edited as part of another paper. |
| `Code/` | Shared: `tools/` (build, check, paper, review and publish tooling), `tests/`, `viz_style.py` with the figure conventions, and the Python environment. Not edited for a single paper. |
| `review/reviewers.yml` | Shared: the review team and the approval policy. |
| `templates/` | Shared: the empty paper that `tools/paper.py new` copies, and the reviewers' forms. |
| `site/` | Shared: the Vivid Insights report design, and `site.yml`, which says where papers are published. |
| `build/` | Built pages. Generated, never edited, not committed. |

Move between papers only with `tools/paper.py`: `list` shows every paper and which is open, `open <number>` puts the open paper back in its folder and brings another one to the top, `park` puts the open paper away, and `new <slug>` creates the next numbered paper from `templates/paper/` and opens it. It never overwrites a file. Never copy a paper's Markdown by hand: two copies of the same paper drift apart.

## Step-by-Step Working

This workspace is for writing a report **one step at a time, with the user directing each step**. It is not for producing a finished report in a single pass, however capable you are of doing so.

- **Do one step per request.** When it is done, say what changed and what you found. Then ask whether the step is finished, and stop and wait for direction.
- **Do not run ahead.** Do not add sections, examples, figures, evaluations, conclusions or prose that were not asked for — even when the next step looks obvious, and even when you can see the whole report.
- **Stop and ask** when a step turns out to be bigger than it looked, when the material forces a choice between approaches, or when a request is ambiguous. A question is cheaper than unpicking unwanted work.
- **Prefer the smallest honest step.** If asked to look at a repository, look at it and say what is there; do not start describing the method in report prose.
- **Say which step you are on, and announce every transition.** When a step's work is finished, name what was completed, name the step now beginning, and say what it involves before starting it. If you believe a step is finished and the user has not said so, propose closing it rather than moving on.
- **Ask whether the step is complete; do not propose the next one.** The question is *"have we thought of everything in step 3?"*, not *"shall we move on to step 4?"*. The second invites a yes.
  - **Give the user something to answer.** Name what the step covers, say which parts are settled and which have not been discussed at all, and ask about those.
  - **Name the next step only after the user has closed the current one**, then say what it involves and wait again.
  - **Being ready to move on is not a reason to move on.**
  - **Wait for an answer rather than an absence of objection.** A user who replies about one item has not closed the others.
- **From step 3 onwards, compare with the specimen before asking.** Open the part of `papers/0000-specimen/Report.md` and its built page that corresponds to the step just finished — the method section and its definition and equation for step 3, the figures, video, interactive and quoted outputs for step 4, the discussion and limitations for step 6, the abstract for step 7, the whole page for step 8 — and compare the form with what this report now has: how much a caption explains, whether a generated text is quoted as an `output` block from its file, whether a video has a poster and an interactive a fallback, where a limitation sits. Compare the shape, never the content. A difference is not a fault; say what the comparison found, including when it found nothing, and leave the decision to the user.
- **Agree the approach before applying it.** For a figure, an example, an evaluation or a new section structure, say what you propose and why, and get agreement before producing it.
- **`Report.md` is built up as the work proceeds.** Each step adds only its own part. Interim workings go in `Appendix.md`.
- **The `Disclaimer` section is already written, and it stays.** It says the report was written with the help of agentic AI at every stage. Do not remove it, soften it or move it down. If the user rewrites it, keep their wording. Step 10 will not publish until the user has confirmed they have read it.
- **Do not leave markers in the report for work that was not done.** If an example is dropped or an evaluation abandoned, take it out of `Report.md` completely and record it in the `Log`.
- **At the stages where a section is yours to write, write it — do not ask first.** Then say what you changed and invite the user to edit it or ask for changes.
- **Never undo the user's changes.** They edit these documents directly, often while you are working.
  - Re-read a file from disk immediately before editing it.
  - Never revert, overwrite, reformat or "tidy" text the user wrote. If what you need to write conflicts with theirs, keep theirs and raise the conflict.
  - Never restore a document from another branch or an earlier commit without asking.
  - Stage named files rather than everything.
- **When asked for a change to the report, make that change and nothing else.** Quote the sentence back before altering it when the change is more than a word. If a correction seems to need a passage rewritten, the correction has probably been misunderstood: ask. Read a short instruction narrowly. `WRITING.md` has the details and the reason.
- **Check what the user has written, and tell them if anything is wrong.** Every number against the generated output, every quoted text against its file, every claim about the method against the code, every citation against the source. Report the error — quote the sentence, say what is wrong, give the right value — and leave the change to them. Separate an error from a phrasing you would not have chosen. Say plainly when it is all correct.
- **Build the page whenever the report changes, and look at it.** `cd Code && uv run python tools/build.py`. Read every error and warning the build reports and fix those that are yours. Tell the user about the rest. A figure, a video or a quote is judged in the page, at the size and in the place a reader meets it, not as a file.

## Changing This Contract

When the user prefixes a message with **FRAMEWORK**, they are changing the template rather than the report.

- Apply the change to `instructions.md` (or `WRITING.md`, `FORMAT.md`, `REVIEW.md`, the tools or the design) immediately.
- Apply it to the report in progress as well, retrospectively where it affects work already done.
- Keep the template edit in its own commit, touching no report content, so it can be promoted cleanly.
- If the change conflicts with something already written here, say so rather than leaving the contract self-contradictory.

### Shared changes and paper changes

All papers live together on `main`, one folder each. A change to something shared (the contract, the tools, the design, the templates, the specimen) and a change to a paper are different kinds of change, and they never go in the same commit.

- **Shared:** `CLAUDE.md`, `instructions.md`, `WRITING.md`, `FORMAT.md`, `REVIEW.md`, `README.md`, `Setup.md`, `.gitignore`, `.claude/`, `Code/`, `review/reviewers.yml`, `templates/`, `site/` and `papers/0000-specimen/`.
- **A paper:** everything in its folder, and `Report.md` while it is open.
- **Commit each paper on its own.** A commit touches one paper's folder (and `Report.md` when that paper is open), so a paper's history can be read without the others.
- **Corrections in `WRITING.md`** are shared when they are about how the user writes. A paper's own terms go in its `Appendix.md`.
- **Say what was committed**, and whether it was pushed. Push only when the user asks.

## The Ten Steps

Work proceeds through these steps in order. Each is one or more exchanges. **Do not begin a step until the user asks for it.**

### Step 1 — Gather the material

Establish what the report is about, from the material rather than from memory.

- Ask the user what the report is about and where its material is: the repositories, apps, prompt files, saved outputs, transcripts, recordings, earlier papers and talks.
- **Look at each source and record it** in `Source Material`: what it is, where it is, the commit or version used, and a checksum for anything copied into `Attachments/`. Say why this source and not another, if that was a choice.
- **Describe before judging.** First what is there — what the code does, which prompts exist, which outputs have been saved, which configurations the app offers — and only then whether it is enough for a report. The describing pass draws no conclusions.
- **Copy outputs that the report may quote into `Attachments/`**, unchanged, with their provenance. A report cannot quote a cache that lives in someone else's working folder and may be regenerated tomorrow.
- **Ask about permissions.** Material from another project, a client or a partner — Ask Afya, BECAUSE SHE CAN, Twelve — may not be the user's to publish. Record what the user says.
- **Do not touch `Report.md` at this stage.**

### Step 2 — Frame the report

Agree what the report is for before writing any of it.

- **Ask the user who the report is for and what it should leave them able to do.** A clinician deciding whether to trust a risk text, a club analyst building an app, a developer building a converser and a researcher reproducing the method need different reports.
- **Agree what kind of report it is**: a method (what it is, how it works, what choices it involves), an application (a method used for a purpose, and what happened), or an evaluation (how well it works, by some measure). Many are a method with one application.
- **Agree the contributions**, as a short numbered list. For each, say what will show it: a worked example, a figure, a quoted output, an evaluation. A contribution with nothing to show it is a claim, and gets cut or turned into a limitation.
- Record the outcome in `Framing` in `Appendix.md`: the reader, the kind of report, the contributions and what will show each, and what was considered and set aside.
- **Then write the framing into the `Introduction` of `Report.md`** — two or three paragraphs: the problem, in its most concrete form; what the method does about it; and the contributions as a numbered list. Do not ask first. Put the background placeholder above it: `*Step 7 adds the background and prior work here.*`
- **The `Introduction` never anticipates its conclusions.** It says what the report does, not what it found or what turned out not to work. The test: would the sentence have to change if the examples had come out differently?
- **Do not open on the report.** *"This report presents a framework for…"* describes the document. Open on the problem: the patient who cannot read a risk number, the coach who gets a paragraph of statistics, the mentor who cannot see why a match was made.

### Step 3 — Describe the method

Write the `Method` section, from the code, in the authors' terms.

- **Describe the method in its authors' terms and order.** Where the method has published stages — the wordalisation steps of Caut and colleagues: the statistical model, the normative model and synthetic text, tell it who it is, what it knows, what data to use, how to answer — follow them, one paragraph or sub-section each, and attribute them. Other people's methods stay theirs.
- **Every fact about the method has one place in the code.** Before writing a sentence about what the method does, find where the code does it, and write the sentence from the code. Record each in `Method Facts` in `Appendix.md`: the fact, the file and line or function, and the commit. Name the file next to the fact.
- **Name the normative choices.** Where a person chose a threshold, a wording, a comparison group, a persona, a routing rule or a few-shot example, say that it was a choice, what the alternatives were and what was chosen. These are what a reader most needs to know and what an app hides best.
- **Settings in the report are settings in the app.** If the app offers an option the report does not mention, either add it to the report or say why it is left out. If the report describes an option the app does not have, one of them is wrong: find out which before changing either.
- **Propose the method figure before drawing it.** Usually a diagram of the stages, with what flows between them. Draw it with a script or as SVG in `Code/`, not by hand in an editor, so it can be regenerated.
- **Use `definition` blocks for the two or three terms the report depends on**, and keep the same term for the same thing throughout. Add each to the `Terms` table in `WRITING.md`.
- **Read the method section against the code, and the code against the method section,** before asking whether the step is done. List every difference without changing anything, then decide with the user, one by one, which side to fix.

### Step 4 — Examples

Show the method working on concrete cases. One example at a time.

- **The concrete case comes first.** A report about wordalisation shows a player, a patient or a mentee and the text written about them, before it says anything general.
- **Propose each example before making it**: which case, chosen by what rule, shown how. *"Three held-out patients, not few-shot examples, chosen to differ in risk"* is a rule. Say the rule in the report.
- **Quote generated text, never write it.** Every LLM output, prompt and conversation in the report is an `output`, `prompt` or `conversation` block that names its source file; the build checks that it is word for word. A hand-written example is marked `source="hand-written"` and the page labels it so. Never paraphrase an output and present it as what the model wrote.
- **Tie saved outputs to everything that made them.** Record, in the `Log`, the model, prompt files, configuration and date for each output used, and keep the file in `Attachments/` or `Code/outputs/`.
- **Report the errors the model makes.** If an output contradicts its input, leaves something out, or says something the normative model does not support, say so in the caption or the text. A demonstration that hides its failures is not evidence.
- **Choose the medium from what has to be shown.** A still figure for a comparison; a video for something that happens in time — a conversation unfolding, an app being used, a value crossing a threshold; an interactive figure when the reader learns by changing something. Propose the medium along with the example.
  - **Video figures** are made by a script with `viz_style.save_video`, or recorded from an app (`Attachments/media/`). Each has a poster image. Keep them short, silent unless sound is the point, and under about 20 MB; longer recordings go on YouTube or Vimeo and are embedded.
  - **Interactive figures** are one self-contained folder in `Code/interactives/` with an `index.html`, no build step and no calls to an LLM or a paid API from the page. Each has a still `fallback=` image for print. They follow the page theme (see `FORMAT.md`).
- **Figures follow `Code/viz_style.py`**: David's style (10 × 8 cm, 11 pt text, no top or right spine, steel blue before coral, 300 dpi), light and dark versions, opaque. One script per figure, reading only saved data. Assign a colour to a variable, not to a rank. Put nothing on the figure but its title, axes, legend and data. Tie every label to the thing it names.
- **Put each example into `Report.md` as soon as it exists**, in `Examples`, with a numbered caption saying what it shows and how to read it. Then tell the user it is there and that they can decide whether to keep it.
- **Captions say what the figure shows, not what it means.** Interpretation is step 6.

### Step 5 — Evidence

Say how well the method works, if the report claims that it does. Skip this step when the report makes no such claim, and say so in the `Framing`.

- **Propose the evaluation before running it.** What it measures, on what sample, against what, and what result would count against the method. LLM-as-a-judge, reconstruction of the data from the text, human ratings, comparison across configurations, a pilot with users: each measures something different. Say which, and what it cannot show.
- **Do not grade your own outputs and call it evaluation.** An agent reading generated texts and deciding they are good is not evidence. Use a stated procedure, applied the same way to every text, with the scores saved.
- **Every number comes from a saved output**, never from memory, never read off a figure.
- **Report the estimate, its uncertainty and the sample.** A judge score from twenty texts is a small sample, and the report says so.
- **Say plainly when the evidence is thin**, or when an evaluation has not been done. *"We have not tested whether readers understand these texts better than the numbers"* is a sentence a reader needs.
- **Keep the `Evaluation` section's method and results paragraphs in step**, with the same sub-headings. Diagnostics and alternative analyses go in `Workings`.

### Step 6 — Discussion and limitations

Write the `Discussion` and `Limitations` sections.

- **Interpret what the examples and evidence support, and state plainly what they do not.** Keep the two distinguishable.
- **Organise the `Discussion` by theme, not by example.** Agree the paragraph structure with the user before writing.
- **`Limitations` is its own section.** What the method cannot do, what the examples cannot show, what was not evaluated, what depends on a particular model or provider, what the normative choices assume about readers. A defect of one component stays beside that component in `Method`.
- **No new examples or analysis.** If something needs doing, say so and stop.
- **Nothing enters these sections that is not already in the report or the appendix.**

### Step 7 — Background, abstract and title

- **Help the user write the background.** It replaces the `*Step 7 adds the background…*` placeholder. Propose its structure first: what is known about the problem, what earlier methods did, and what remains open. Then find the sources and read them. Bring the user the sources before the prose. Never cite a work you have not opened; `References and Citation` applies in full.
- **Choose references for their relevance to what the report does; write as though its results were not yet in.**
- **Write the `Abstract` last.** One paragraph, roughly a sentence each: the field; the specific problem; what the method does; how it was shown; what was found, with its main limitation attached; what the reader should take away. Short sentences, no numbers, no method plumbing, nothing that is not in the report.
- **Suggest two or three titles** once the abstract is written. Plain and literal. The user chooses.
- **Fill in the front matter**: `keywords`, `report-number` (ask the user; the series is `VI-<year>-<nnn>`), `version`.

### Step 8 — Read through

Read the finished report from beginning to end, in the built page, as a reader would, and list what is wrong with it.

- **Read it in one pass, in order.** A term defined twice, a claim in `Examples` contradicted in `Discussion`, a figure discussed before it appears.
- **Check the argument runs end to end.** Each contribution named in the `Introduction` is shown in `Method`, `Examples` or `Evaluation`, and discussed.
- **Re-check everything that goes stale**: every quoted output against its file (the build does this), every fact about the method against the code at the commit recorded, every number against its output, every cross-reference.
- **Check nothing is orphaned**: a figure never referred to, a reference never cited (the build warns of both), a term used once.
- **Check the references properly**: each cited where it is used, each detail verified against the source, each link resolving.
- **Run the release check**: `cd Code && uv run python tools/check.py --release`. Every error must be resolved; every style hint must be read.
- **Report the list; do not fix as you go.** Record the outcome in the `Log`, including when nothing was found.

### Step 9 — Review

Every report is reviewed by the Vivid Insights team before it is published. `REVIEW.md` describes the process; this is the agent's part in it.

- **Request review only when the user asks**, after step 8. Commit the report first, then run `cd Code && uv run python tools/review.py request`. It refuses if the release check fails or the report is uncommitted, freezes the version by its content hash, opens `review/round-NN/`, and builds a review copy. Tell the user the hash, where the review copy is, and who `reviewers.yml` says must review it.
- **Do not edit the report while a round is open.** Any change to the report, its references or any file it shows or quotes changes the content hash, and an approval only counts for the hash it names. If the user wants to change something during review, say so before doing it.
- **Never write in `review/*/reviews/` or `review/*/approvals/`, and never run `review.py form` or `review.py approve`.** Those belong to the reviewers. A hook in `.claude/` blocks it; the rule stands whether or not the hook does. Do not create, edit, move or delete a review or an approval, do not commit one, and do not impersonate a reviewer in git.
- **When reviews arrive, read them all, then list every point** — each with the reviewer, a quote, and what it asks for. Propose for each whether to change the report, and how, or why not. The user decides.
- **Make the agreed changes one at a time**, under the usual rules, and write the paper's `review/round-NN/response.md`: each point quoted, followed by what was done and where, or why nothing was. This is the author's reply; write it in the first person plural.
- **Then request the next round.** Reviewers approve the revised version, not the one they first read.
- `cd Code && uv run python tools/review.py status` says where the report stands and why. Use it rather than reading the folder.

### Step 10 — Publish

- **Before anything else, have the user confirm they have read the `Disclaimer`.** Quote it to them in full, ask them to confirm, and wait. Nothing earlier counts. If they change it, the content hash changes and the report goes back to its reviewers. If they decline, do not publish. Record the confirmation in the `Log`.
- **Run `cd Code && uv run python tools/publish.py`.** It refuses unless the current version carries enough valid approvals, each committed to git by the reviewer who gave it. Do not try to get round a refusal: report it to the user with the reasons it gave.
- **Open the published page and look at it**: the title block, every figure in both themes, every video playing, every interactive working, the review record at the foot, the page on a phone-width window, and the print preview.
- **Do not commit or push the site repository.** `publish.py` prints the commands; the user runs them, or asks you to.
- **The report's Markdown remains the source of truth.** Never edit the published page; change `Report.md` and go through review again.

## When Something Changes

A changed prompt, a refit model, a new configuration or a regenerated output makes some sentences in the report false. Finding them is the work.

- **The app and the report keep each other honest.** After any change to a model, normative model, prompt or few-shot file: regenerate the outputs, regenerate the figures, then update every sentence that describes or quotes what changed.
- **Search the report for what changed**: feature names, numbers, quoted phrases, option names, configuration names.
- **Mark stale text at once** with `[CHECK: …]` if it cannot be updated now. The release build refuses to publish with one in place.
- **List what each change made stale** in the reply that makes the change: figures, sections, quoted outputs, the facts table.
- **Re-verify what survives, not only what moved.**
- **Record what moved in the `Log`**, with before and after.

## Working Method

1. Inspect the relevant material before making claims about it.
2. Put all code that makes a figure, a video, an interactive or a number in `Code/`, one script per output, reading only saved inputs.
3. Record the work in `Appendix.md` as it happens, from the first step.
4. Write `Report.md` only as the steps direct.
5. Update the `Code Summary` whenever code is added or changed: what each file does, how to run it, what it reads and produces.

## Python Environment

Run all Python through the workspace environment: `cd Code && ./setup_env.sh` to create it, `cd Code && uv run python <script>` to run anything, `cd Code && uv add <package>` to add a dependency (commit the lockfile, note it in the `Code Summary` and in `Setup.md`). Never install into the system Python. `Setup.md` has the rest.

## References and Citation

- **Cite in author–date style**, with keys from `references.yaml`: `[@caut2025]` gives "(Caut et al., 2025)", `@caut2025` gives "Caut et al. (2025)". `FORMAT.md` has the details.
- **Every reference is a link.** A `doi` or a `url`, checked to resolve before it is written. The build refuses an entry without one.
- **Never cite a work you have not opened**, and verify volume, issue, pages and year against the source, not memory.
- **Mark preprints and other unreviewed sources** with a `note`, such as "Preprint, not peer reviewed".
- **Cite the version actually used** — an arXiv version, a software release, a dataset vintage.
- **Cite software and apps** that the report describes or uses, with a version or commit.
- **Give a quantity taken from another work its units.** If they cannot be established from what has been read, drop the figure and keep the finding.

### Getting hold of paywalled sources

A `403` from a publisher is a bot block, not a dead link. Ask the user for the download rather than substituting a preprint. Send a short list — title, DOI link, one line on what the citation needs — and ask them to save the files to `Downloads` and say when. Move them to `Attachments/literature/`, which is not committed. Note in the `Log` which sources were read in full and which rest on an abstract.

## The Specimen

`papers/0000-specimen/Report.md` is a short paper that uses every kind of block: figure, video, interactive, equation, definition, table, quoted output, conversation, citations and cross-references. Build it where it lies with `cd Code && uv run python tools/build.py ../papers/0000-specimen/Report.md`; there is no need to open it.

- **Offer it when the user is unsure what a part of the report looks like**, and point them at the part of the built page.
- **Read it before closing a step, from step 3**, as `Step-by-Step Working` says.
- **It is an example of form, not of content.** It makes no empirical claim, and a real report has more to say than it does. Never copy its prose, numbers or figures.
- **Never edit it as part of another paper.** Where it and this contract disagree, the contract is right.

## Agent Operating Rules

- Before changing report material, inspect the relevant sources and existing documentation.
- Make focused changes and do not overwrite unrelated user work.
- After changing code, run the narrowest useful check and record the outcome in `Appendix.md` when it affects the report.
- Keep Markdown headings stable and update existing sections rather than creating competing versions.
- When evidence is insufficient, ask a targeted question or record the gap instead of filling it with speculation.
- Do not expose credentials, API keys, personal data or client material in code, Markdown or the published page. App secrets stay in files that are not committed.
- Commit or push only when the user asks.
