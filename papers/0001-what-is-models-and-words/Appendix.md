# Appendix

*The running record, filled from the first step. Everything a reviewer needs to check the report and that does not belong in it: where the material came from, what was decided and why, the workings, and what was tried and abandoned. Not published as part of the page.*

## Source Material

*Step 1. One entry per source: what it is, where it is (repository and commit, or file and checksum), why this source, what it may be used for, and any permission the user recorded. Copied files live in `Attachments/`.*

**`agentic-ai-for-statistics-and-data-science`** — David's course on doing data analysis with an agent, at `~/GitHub/agentic-ai-for-statistics-and-data-science`, commit `3d858b6`. Fifteen chapters: part 1 (1.1–1.8) runs one worked example — global forest loss against income — from a raw download to a finished report; part 2 (2.1–2.7) is on adapting the framework, ethics and how far automation can be pushed. Chapters 2.4, 2.5, 2.6 and 1.8 are empty. Read in full: `Overview.md`, 1.1, 1.3, 1.5, 1.7, 2.7. What it contains that bears on this paper:

- **The eight steps and why they exist.** One step of analysis per request, then stop; the agent proposes and waits. Built on Mitchell, Ghosh and Passi (2026), *AI Agents Push Humans Out of the Loop*, as strategic friction: step 2 is pre-commitment, steps 3 and 4 are action gating, one-step-per-request is batch review. The style rules — no grading the evidence, nothing bold, every number from a generated output — are there because people judge accuracy by fluency and the presence of citations. Also cites Bainbridge's ironies of automation, Buçinca and colleagues on cognitive forcing, and the deskilling literature.
- **Traditional against agentic statistics** (1.5). The traditional course teaches three or four weeks of theory before the student opens their own data. The agentic approach starts from the question, and the work is understanding the methods the agent proposes well enough to accept or drop them. "You will not be able to do this unless you already have a grounding in traditional statistics."
- **The hypothesis step** (1.3). Seven questions David asked about what the variables measured revealed three errors, including a false factual claim that "looked like sound inference the whole way", and an underspecified hypothesis that had variables, an outcome and a named test and still could not be estimated — "fluency hid the gap".
- **The automation benchmark** (2.7). Terminal-Bench-Science, built from a melanoma imaging study. Handed the published cell-type labels, Claude Opus 5 passed 3 of 3; with the labels removed, 1 pass in 12 trials. Fifteen conditions, 116 runs. A decision *procedure* — an order of resolution and a rule about sufficiency, no facts — moved the score from 0.7943 to 0.8665 (p = 0.0002); a precise *biology briefing* did not (0.8299, p = 0.24). Adding a fixed corpus of 29 papers to a working procedure made it worse (0.8665 → 0.8259, p = 0.015). Six marker-poor macrophage clusters were recovered 18 times in 66 under the procedure and 0 times in 36 under the briefing. The chapter's conclusion: "Giving an agent the literature is not the same intervention as giving it the context", and "the person writing the context object is the worst judge of whether it is complete."

Permission: granted by David, 2 November 2026.

**This workspace** — confirmed by David as material, 2 November 2026: the article also presents how articles will be written here. What the files hold:

- `instructions.md` — the working contract. One paper per folder; every report has the structure Abstract, optional What We Have Built, Introduction, Methods, Results, Discussion, built on three points called A, B and C that thread through every section in the same order. Six phases from David's drafting order — sketch, sketch the abstract, revise, write the start and end together, revise the abstract, simplify and revise — carried out as ten steps. The friction rules: the user's decisions, pre-commitment through an abstract written before any section, the user goes first, propose and wait, one unit at a time. Cites Mitchell, Ghosh and Passi (2026) for why.
- `WRITING.md` — how the prose is written, each rule with the correction that produced it: first person plural, the concrete case first, no "not X, it's Y", no grading the evidence, nothing bold, numbers in tables and meaning in the text, draft at about half the length that seems natural. Ends in a dated corrections log.
- `REVIEW.md` and `review/reviewers.yml` — every report is reviewed before publication. A content hash over `Report.md`, `references.yaml` and every file the page shows or quotes; a reviewer approves one hash; `publish.py` refuses anything else. Two approvals, one from an editor, authors may not approve. The agent may not write reviews or approvals, enforced by a hook as well as by the contract. **`reviewers.yml` currently lists one person, David, and carries a `[CHECK:]` saying `review.py request` refuses until at least two are listed.**
- `FORMAT.md` — the Markdown the report is written in. Not yet read.
- The specimen, `papers/0000-specimen/`, uses every kind of block and is what a step is compared against from step 3 onwards.

**`Davids-Vault/Twelve Models (do not share externally)/Algorithms and Models`** — Twelve's internal index of its models, exported from Notion. The hub page states three principles: models are explainable in football terms ("understandable"), they relate to goals scored and conceded ("help teams win"), and each problem gets the best motivated approach ("advanced AI"). Its child page `Modelling Philosophy` is the closest thing in the material to a statement of the journal's position: it separates the **mathematical model** of the data from the **normative model** that says what the model means in words, defines normative as setting a standard for judging behaviour or outcomes, says stakeholders define the norms, and argues against black-box methods on Rudin's grounds that high-stakes decisions need interpretable models rather than post-hoc explanations. Other child pages: `Building a Twelve Analyst`, `Qualities, Metrics and Summaries`, `Wordalisations`, `Visualisations`, `Context Engineering for Football`, `Automated documentation`, and the model pages (transfer, team strength, league strength, Total Football, financial, zonal threat, zonal xG, Twelve Index, player name search, van Dijk metrics, coach analysis). **Permission: granted by David, 2 November 2026, although the folder is marked "do not share externally". Named individuals and clubs still need care.** Copied unchanged to `Attachments/twelve-algorithms-and-models/`: `Algorithms and Models.md` (sha256 `ed842073…`) and `Modelling Philosophy.md` (sha256 `64829c72…`).

**`Davids-Vault/Models and AI/`** — David's own writing on modelling, and the academic framing the Twelve philosophy points back to. Four pieces bear on the journal's concept:

- *Building models in the age of machine learning and AI* — research notes. Machine learning gives the biggest recent advances but no mechanistic understanding, which challenges the traditional modelling cycle of formulating a mechanism, fitting it and predicting. Proposes integrative pluralism: many models of the same system rather than one. Opens on Breiman's two cultures; uses football and complex-systems models (cellular automata, self-propelled particles, current-reinforced oscillators) as the two extremes.
- *The Lost Art of Mathematical Modelling* — Gyllingberg, Birhane and Sumpter. Published; PDF at `Attachments/Lost art.pdf`. Of the three modelling activities — formulating, analysing, fitting — researchers over-invest in analysing at the cost of formulating.
- *Coherence, charity and triangulation in statistical modelling* — Sumpter, August 2025. Uses Davidson's third dogma to argue that model and data are parts of one belief system, and that a belief system should be coherent, charitable and triangulated.
- *Most models are true, because they are useful* — short note against Box's aphorism: a model is judged by its assumptions, how it relates to earlier models, the view of the world it constructs and the consequences for those who take that view.

Permission: granted by David, 2 November 2026. All four copied unchanged to `Attachments/models-and-ai/`: *Building models…* (sha256 `7b148f85…`), *The Lost Art* (`5edcd042…`), *Coherence, charity and triangulation* (`d0e03c6e…`), *Most models are true…* (`6e22d77c…`). The vault working tree was not clean when these were taken, so the checksums rather than a commit identify what was read.

**`context-engineering`** — the course repository beside the vault, at `~/GitHub/context-engineering`, commit `dc7c387`. Seven lessons: `0. Context Engineering` (hub), `1. Introduction`, `2. Prompting and Parroting`, `3. Wordalisation`, `4. Interpretable Models`, `5. Embedding, annotation and function calling`, `6. Conversational context`, plus `List of Projects` and `Transcripts/`. The hub states the course's claim: build a data context for any question a user poses, then turn the data into insight, for building AI analysts that advise users making decisions — "the examples are from football … but the methodology can be applied to any complex system where decisions are made". Lesson 4 opens on Breiman's two cultures and works the mechanistic and data-driven approaches to expected goals side by side. Lesson 1 opens on having a mission, and says what a person needs before building an analyst: a reason, competence in the area, and access to the data decisions rest on. The accompanying code is in a separate repository, `Context-Engineering-Course`. Not yet read in full; lessons 0, 1 and 4 opened.

**The first two papers in the workspace** — named by David as giving the flavour of the journal. `papers/0002-representing-data-in-words/` introduces wordalisation: a method for generating narratives from data, applied to football scouting, personality tests and international survey data, evaluated by LLM-as-a-judge and human-as-a-judge, with a section on open and transparent development of communication about data. `papers/0003-twelve-earpiece/` describes a conversational football analyst built as a choose-your-own-adventure: specialised analysts with redirects, name resolution, wordalisation functions and embedding search, tested on a hand-written set of queries and judged blind against a general coding agent. Both are in the workspace and are the journal's own output.

**The CONTEXT MSCA Doctoral Network application** — at `~/GitHub/MSCA doctoral network`, commit `d138195`, a live application to HORIZON-MSCA-2026-DN-01-01 with Uppsala as coordinator and David as the coordinating applicant, for submission 20 November 2026, declaring interest in RAISE. Fifteen doctoral candidates at eight universities (Uppsala, Groningen, Luxembourg, Stellenbosch, Makerere, Addis Ababa, Lagos, Coventry), with Because She Can, ForensiFAI, Twelve Football AB, NC3 and Nithub as associated partners. Read: `README.md`, `Overview and Plan.md`, `03 Part B1/1.1 Quality and pertinence…`, and one doctoral one-pager (Bissyandé's, from `~/Downloads/Re__MSCA_doctoral_school.zip`). What the network is trying to achieve:

- **One definition, three properties.** "A language system is trustworthy to the extent that it signals when it is likely to be wrong, ties what it asserts to identifiable evidence, and is evaluated by the people who live with its consequences." The first is calibration and selective prediction, the second attribution and verification, the third participatory method, consent and governance. The fifteen projects are an attempt to establish all three on the same artefacts and systems, so that each thesis reports one of the three measures on a shared logged object.
- **Two senses of context, evaluated on the same systems.** In the engineering sense, context is what a system knows at the moment of answering, held in an inspectable *context object* to which each assertion can be traced. In the Afrofeminist sense, it is the social, linguistic and economic setting that decides whether a technically sound system deserves trust. The proposal states that a system can be faithful to its context object and still fail the second test.
- **The layer above the model.** The stated position is that the frontier laboratories are elsewhere, and that Europe's and Africa's prospects lie in making tools that analyse specific data dependably: laboratory instruments, health records, field imagery, and speech in the languages people actually use.
- **Why the problem is structural.** Next-token pretraining and accuracy-scored evaluation both reward a confident guess over abstention (Kalai and colleagues, *Nature* 2026; Zhou and colleagues, *Nature* 2024); retrieval moves the question to whether what was retrieved suffices, and strong models answer rather than abstain when it does not (Joren and colleagues, ICLR 2025). The margin is thinnest in under-resourced languages: Ethiopic script costs seven to nine times the tokens of English, cutting the effective context window to as little as 11%.
- **Six objectives.** Measurable, actionable error in frozen models; an open toolkit in which every assertion is traceable (the context object, wordalisation, prompt cards, program analysis of generated code); testing where trust is hardest (a maternal and newborn health assistant that knows when to refer, microscopy description tied to measured uncertainty, gendered hate speech in Amharic and Afaan Oromoo, football tactics explained to the coaches who use them); evaluation by those affected made continuous and binding; carrying components into use (a crop-disease advisory with calibrated referral); and RO6, a pre-registered test of whether uncertainty-triggered referral and clause-level attribution actually change how affected users judge a system.

What it gives this paper. It is the first source in the material that is not David's own position: fifteen projects and about twenty researchers across machine learning, speech, vision, software verification, law, gender studies and governance, each with their own approach to how models and words relate. It also supplies a definition of trustworthiness and of the context object that the journal's area could be stated against, and a second meaning of "context" that the context-engineering material does not carry. RO2(c) — whether documentation quality or benchmark score better predicts field reliability — asks the same question as chapter 2.7 of the statistics course, from the other end.

**Permission: not yet given.** This is an unsubmitted application with named individuals, partner commitments and David's declared financial interest in Twelve. Nothing has been copied into `Attachments/`; the entry rests on the repository at the commit above. David decides what, if anything, of it the article may use.

**`mechanisms-and-constraints`** — *Mechanisms and constraints in behavioural ecology*, by Malou Bastiaanse (Cambridge), Linnéa Gyllingberg (KTH), James E. Herbert-Read (Cambridge), Kathryn Nave (Edinburgh) and David Sumpter (Uppsala), listed alphabetically. At `~/GitHub/mechanisms-and-constraints`, commit `5c502a3`; a draft, front matter dated 7 August 2026, with the Discussion still in note form. Named by David, 7 November 2026, as **an example of a theory contribution to this journal**. Read: `README.md`, `AGENTS.md`, the article's abstract, Introduction, Theory, Discussion and its note on agentic AI.

- **What it argues.** Sara Green distinguishes mechanistic explanations, which say how a system works by naming its parts and their organisation, from constraint-based explanations, which say what a whole class of systems can and cannot do whatever their parts are made of. The paper crosses that with Mayr's proximate and ultimate — how it works against why it is there — which is David's extension and not Green's, and adds a third family, **predictive explanation**, for accounts whose content lies in a model learned from data. Six types, each with a template: an ordered list of the parts an explanation of that kind must have. The claim is that several long-running debates in behavioural ecology are not disagreements about the world but about what kind of explanation is being offered, and that saying which kind dissolves them. Worked cases: marching locusts, the origin of eusociality, niche construction, worker policing.
- **Why it is the example.** It is the fifth note worked out for another field, with a mechanism rather than a sentiment: different approaches answer different questions, improve in different directions, and are mistaken for rivals. It also puts machine learning inside the scheme rather than beside it — Breiman's two cultures again, but as a third family of explanation whose content is a learned model, which is the question this journal is about.
- **The classification is done by a language model.** The templates are filled by an agent applying a written procedure to pairs of papers, over a corpus of more than 150 read in full from their PDFs; the procedure, the corpus and the checking scripts go in the supplementary material. So the paper is also an application of the journal's own subject to a theory problem.
- **Its note on the use of agentic AI** is a precedent for this workspace's `Disclaimer`: what the model did (retrieval, classification, drafting), what it did not ("It was not used to decide what the paper argues… several were adopted over the model's stated objection"), the three checks that were necessary, and the errors reported rather than concealed — papers reported as filed that were not, guessed identifiers returning unrelated work, a cautionary passage inside a positive account read as that account's thesis, and a sentence that reads as a finding and cannot be checked. "None would have been caught by reading the output and finding it plausible."
- **Four of the five authors are not David**, from zoology, computational science and philosophy. It is the second source, after CONTEXT, that carries approaches other than his.

Permission: the repository is private and its `Attachments/` holds 153 PDFs shared among the five authors only. Nothing copied into `Attachments/` here. The paper is an unpublished draft with four co-authors, so what this article may say about it, and whether it can be cited before it appears, is David's to settle with them.

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

### The picture from David's previous writing

My reading of the sources above, assembled 2 November 2026 so David can correct it. Not his words and not a decision; six positions that recur across the material, with where each is stated.

1. **A model is built to be interpreted, not only to predict.** Rudin's distinction between interpretable and explainable models, taken up directly in Twelve's `Modelling Philosophy` and worked as a teaching example in lesson 4 of the context engineering course, where a mechanistic expected-goals model fitted on shot angle sits beside a gradient-boosting model explained after the fact by SHAP. Breiman's two cultures is the opening move in three separate documents.
2. **The mathematical model and the normative model are different things, and both are the modeller's responsibility.** Twelve's `Modelling Philosophy`: the mathematical model is of the data, the normative model "describes what our model says in words", and the norms come from stakeholders and are subjective. Wordalisation (paper 0002) is the mechanism that carries the second; Earpiece (paper 0003) is the system that delivers it.
3. **Many models of one system, rather than the right one.** Integrative pluralism in *Building models in the age of machine learning and AI*; *The Lost Art* argues that of formulating, analysing and fitting, researchers over-invest in analysing.
4. **A model is part of a belief system answerable to other people and to a shared world.** *Coherence, charity and triangulation*. And in *Most models are true, because they are useful*: judge a model by its assumptions, its relation to earlier models, the view of the world it builds and the consequences for those who take that view.
5. **What large language models automate is not the hard part.** The statistics course hands the agent importing, wrangling, plotting and fitting. The melanoma benchmark in 2.7 makes the same point as a measurement: given the labels, the task is solved 3 times out of 3; without them, once in twelve.
6. **What is hard is the judgement nobody wrote down, and the writer cannot see what is missing.** The strongest evidence in the material: a decision procedure moved the score and a precise statement of the biology did not; adding twenty-nine papers made it worse. Its conclusion — "the person writing the context object is the worst judge of whether it is complete" — is the same claim the friction rules in this workspace act on, from Mitchell, Ghosh and Passi: a human in the loop is only meaningful if the human can see into the loop.

How this meets David's sentence. Positions 1, 3 and 4 are *how we use and interpret models*. Position 2 is *how we build systems which communicate the conclusions from models*. Positions 5 and 6 are what changed, and are the reason the two halves now belong in one journal rather than two literatures.

### David's third note, 2 November 2026

The journal's scope is wider than David's own position. His position is one within a variety of positions on this area. What he wants is a forum to discuss different positions and approaches of this type.

This changes what the paper has to do. The six positions above are then the editor's position, not the journal's line, and the paper's job is to say what the *area* is — the thing these are positions about — and what makes a position one of them. The material gathered so far is almost all David's own side of it.

### David's fourth note, 2 November 2026

The article is also a presentation of how more articles will be written, using the approach in this folder.

So it has two jobs: say what the area is and that the journal is a forum for positions within it, and present the writing method. How those sit together — whether the method is one of the paper's three points, its `What We Have Built` section, or the frame around the whole thing — is a step 2 decision.

### David's fifth note, 7 November 2026

The journal is not organised around disagreement. What the forum holds is a diversity of approaches within the context of using models and words to understand the world. Two people working differently are not two sides of an argument.

This changes what the paper has to state: not the axes along which positions oppose each other, but the thing the approaches are approaches to, and what makes one of them belong. CONTEXT is an example of that diversity rather than of disagreement — fifteen projects taking different routes to the same object.

### Step 2 — what kind of report, 7 November 2026

**The reader: a researcher deciding whether to submit.** David's decision, 7 November 2026. The reader is weighing their own work against the journal, so the paper has to leave them able to say whether what they do belongs here. That is the same job the fifth note set — state what the approaches are approaches to — now with a reader attached to it. What else the reader should be able to do is not yet settled.

**This paper is an editorial.** David's decision, 7 November 2026, with the contract changed in the same turn so that editorial and opinion are kinds of paper alongside method, application and evaluation: an editorial says what the journal is for, or what an area is, and is written on behalf of the publication; an opinion is a position argued by its authors, which the journal publishes without taking as its own.

Open, raised with David and not yet decided: `The Structure of a Report` fixes the sections as Abstract, optional What We Have Built, Introduction, Methods, Results, Discussion, built on three points. An editorial has no method it carried out and no results it obtained in that sense.

### What the paper says — David, 7 November 2026

Recorded as written, in his words, before any questioning. This is what step 2 works from.

> Articles in model and words are about understanding social, biological and technological systems and building applications which help people make descisions about those systems. Agentic AI provides new opportunities and presents new challenges in how we build models: writing code and mathematical analysis of models is greatly simplified by these tools, but finding the clearest insight when these models generate vast quantities of text and calculations can be more challenging. We are looking for three types of contributions
> 1, Applications which combine models and words to produce insight for stakeholders.
> 2, Methodological and theoretical contributions where models and words are combined.
> 3, Description of Agentic AI solutions, where human decision-making is placed in the centre.
> Models and words is itself an AI agent. Submissions are written together with an agent, reviews are semi-automated and it can provide help and support to application builders and researchers. In this article, we outline the type of article we are looking for, how to work with the model-and-words agent to write your article and how the paper will be reviewed.

Raised with David in reply, not yet settled:

- There are now two triples — the three kinds of contribution and the paper's three points — and they are different axes.
- "Reviews are semi-automated" overstates what the workspace does. `review/reviewers.yml` lists one person and the policy needs two with one of them an editor; a hook in `.claude/settings.json` blocks the agent from writing in the reviews and approvals folders or running the reviewers' own commands. What is automated is the release check, the content hash and the build. The judgement is not.
- Whether the opening scope sentence is meant to admit approaches that differ from David's, as the fifth note requires.

**The scope sentence is to be open.** David, 7 November 2026: the opening sentence should be open and must not imply certain methods; how explicit the openness needs to be is undecided. Read against that aim, the sentence as written is narrower than the list of three kinds of contribution that follows it, because "building applications which help people make decisions" asks every contribution to ship an application — which the constraints paper, named by David the same day as the example of a theory contribution, does not.

**The three points.** David, 7 November 2026: the three after "In this article," — **A**, the type of article we are looking for; **B**, how to work with the Models and Words agent to write your article; **C**, how the paper will be reviewed. The three kinds of contribution sit inside A, so the two triples nest rather than compete. What will show each: for A the three kinds with one example apiece (applications by the wordalisation and Earpiece papers; methodological and theoretical by the constraints paper; agentic AI solutions with human decision-making at the centre — example not settled, the asylum case assistant put to David as a candidate); for B the contract, the six phases and ten steps, the writing rules, and this paper's own `Log`; for C the content hash, two approvals with one from an editor, the agent blocked from writing reviews, and the editors-only review agent still to be built.

**Keep the editorial timeless.** David, 7 November 2026: "We should make the editorial as timeless as possible and avoid too much talk of exactly what is happening now." On his instruction the sentence beginning "Agentic AI provides new opportunities…" was cut from the `Abstract` and belongs in the `Introduction` instead:

> Agentic AI provides new opportunities and presents new challenges in how we build models: writing code and mathematical analysis of models is greatly simplified by these tools, but finding the clearest insight when these models generate vast quantities of text and calculations can be more challenging.

A paper-level rule for now; it can be promoted to `WRITING.md` if it is to hold for every paper.

**The scope sentence, revised at David's instruction, 7 November 2026.** He asked for the defect fixed and confirmed that understanding models, and in particular how they relate to words, is part of the scope. Written by the agent, not yet in `Report.md`, and open to his edit:

> Articles in Models and Words are about understanding social, biological and technological systems, about the models we build of them, and about how those models relate to the words we use about them. Some articles stay with the model and what it says; others build applications which help people make decisions about these systems.

Two changes from his version: the application is one thing an article may do rather than something every article must do, which lets the constraints paper in as a theory contribution; and the models themselves, with their relation to words, are named as an object of study.

**The review agent.** David, 7 November 2026: a review agent will be built later, in a separate GitHub repository accessible only to the editors. So semi-automated review is a plan, not something the workspace does today. In the article the claim is therefore written as a plan, and what the reader is told about review as it stands now is: two approvals with at least one from an editor, the version frozen by a content hash, the agent blocked from writing reviews or approvals, and reviewers writing their own. `review/reviewers.yml` still lists one person, which blocks a round being opened for this paper.

**The working abstract accepted as it stands.** David, 7 November 2026: "This is ok as is. Even if A, B and C have short descriptions in the abstract this is OK." The list of three kinds of contribution stays inside the abstract for now, and B and C keep their short mentions in the agent paragraph. To be read again in step 7.

### The material, in summary — step 1 closed, 7 November 2026

Given to David in this form and open to his correction. The kinds of material, not the file list:

- **David's own writing on what a model is and what it is for.** The four `Models and AI` pieces, and Twelve's modelling philosophy, which separates the mathematical model of the data from the normative model that says what it means in words.
- **A theory paper, written with four other people, on what counts as an explanation.** The constraints paper: six kinds of explanation, each with a template, with machine learning placed inside the scheme as a third family rather than beside it.
- **Courses on doing this work with an agent.** The statistics course and the context engineering course — one on handing the steps of an analysis to an agent, one on building the data context an AI analyst answers from.
- **Working systems that turn data into words.** Wordalisation and Earpiece, both already written up as papers in this workspace, and the Twelve models behind them.
- **A funding application carrying fifteen other researchers' projects.** CONTEXT, with its definition of a trustworthy language system and its two senses of context.
- **The rules this workspace runs on.** The contract, the writing rules, the review process, and the two papers written under them.

How they relate. The first two kinds are about models and what they explain; the fourth is about getting a model's conclusions into words someone can act on. That pair is David's sentence in *Algorithms and Models*, and it is the journal's subject. The courses sit between them, and they are also where the evidence is that the steps of an analysis automate while the judgement does not. CONTEXT and the constraints paper are the only material carrying approaches other than David's: CONTEXT brings about twenty working researchers, the constraints paper a way of saying why different approaches are not rivals, which is what the fifth note asked for. The workspace rules are a different kind of thing — not the subject but the method — and they are material because the article presents them too. They rest on the same argument as the statistics course, so the two halves of the paper have one source in common. The two newest sources are also the two whose permission is unsettled.

Left open when step 1 closed: whether an example exists in David's folders for each of the other kinds of contribution the journal would publish; a talk where the argument has been given; an email thread, referee report or collaborator's draft putting another approach; an earlier attempt at the journal; and any application other than CONTEXT that states what this area is.

### Approaches present in the material

Recorded 2 November as "axes of disagreement"; superseded as a framing by David's fifth note. The rows stay as a record of where the material shows more than one way of working, read as approaches that coexist rather than as sides.

| Where the material differs | One approach | Another |
| --- | --- | --- |
| Mechanism or data | Build a model of how the system works and interpret it | Breiman's second culture: treat the mechanism as unknown and predict well. Named as the opening move in *Building models* and lesson 4 |
| Is the modelling cycle still needed | Formulate, fit, predict, refine | *Building models*: "some researchers have even questioned whether such a modelling cycle is needed at all in the age of AI" |
| Interpretable or explained after the fact | Rudin: build interpretable models for high-stakes decisions | Post-hoc explanation of a black box, SHAP on gradient boosting, used as the contrast case in lesson 4 |
| Who chooses the next step | The code offers options and the model picks: Earpiece's choose-your-own-adventure | The agent directs its own use of tools. Schluntz and colleagues' distinction, cited in paper 0003 |
| How much the LLM writes | Wordalisation: the LLM writes every text from a synthetic text the code generates | Dale and colleagues: keep the templates, because reliability is what sets them apart, and use the LLM to help a person write them. Cited in paper 0003 |
| How far automation goes | The steps automate; the judgement does not (2.7) | Fully automated research as a goal; the benchmark literature 2.7 draws on |
| What a model is for | A model in serious use is made largely true of the world (*Coherence*) | Box: all models are wrong, some are useful — the position argued against in *Most models are true* |

### Questions this raises

- Superseded by David's third note: the journal's scope is wider than the argument above. Open instead: what is the area, stated so that someone who disagrees with David still recognises their work as belonging in it?
- Where do the other approaches come from? Until CONTEXT, everything gathered was David's own. A forum paper needs the people it is inviting.
- The review process the article would describe cannot currently run: `reviewers.yml` lists one person and the policy needs two approvals with one from an editor. This blocks step 9 of this paper as well as the article's account of the process.
- The first note says the steps of statistical analysis are "nearly fully automated". The benchmark in 2.7 supports it for the steps and contradicts it for the analysis as a whole. Which does the paper claim?
- Chapter 2.7's finding — that a decision procedure transfers and domain content does not — cuts slightly against the Twelve philosophy's emphasis on stakeholders' normative knowledge. Both may be right, but the paper would have to say how.

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
| 4 | Step 1 continued. David granted permission for the Twelve and vault material. Six source files copied unchanged into `Attachments/` with checksums. `agentic-ai-for-statistics-and-data-science` read (Overview, 1.1, 1.3, 1.5, 1.7, 2.7) and described. A reading of David's position across all the sources written into `Framing` as `The picture from David's previous writing`, for him to correct. `Report.md` untouched. | this file, `Attachments/` |
| 5 | Step 1 continued. David set the scope: the journal is a forum for a variety of positions on the area, and his own position is one of them. Recorded in `Framing` with the axes of disagreement already present in the material. The six positions recorded in entry 4 stand as the editor's position, not the journal's line. `Report.md` untouched. | this file |
| 6 | Step 1 continued. David confirmed the workspace's own contract files as material: the article also presents how further articles will be written here. `instructions.md`, `WRITING.md`, `REVIEW.md` and `reviewers.yml` read and described in `Source Material`. Noted that `reviewers.yml` lists one person and the review policy needs two. `Report.md` untouched. | this file |
| 7 | Step 1 continued. David named the CONTEXT MSCA Doctoral Network application as further material. The application repository read at commit `d138195` (README, `Overview and Plan.md`, §1.1) and described in `Source Material`, with what the network is trying to achieve and what it gives this paper. Permission not yet given and nothing copied into `Attachments/`. `Report.md` untouched. | this file |
| 8 | Step 1 continued. David set the framing: the journal holds a diversity of approaches within the context of using models and words to understand the world, not a set of disagreements. Recorded in `Framing` as his fifth note; the table of 2 November kept as a record of where the material shows more than one way of working, marked superseded as a framing. `Report.md` untouched. | this file |
| 9 | Step 1 continued. FRAMEWORK: step 1 now keeps probing for material and offers to search the user's folders (`instructions.md`, committed separately as `490ee61`). The search was run and candidates brought. David named `mechanisms-and-constraints` as an example of a theory contribution to the journal; read at commit `5c502a3` and recorded in `Source Material`. Permission unsettled: private repository, four co-authors, unpublished draft. `Report.md` untouched. | this file |
| 10 | FRAMEWORK: step 1 now closes with a plain summary of the kinds of material and how they relate (`instructions.md`, committed separately as `5dbc420`). The summary was given to David and is recorded in `Framing`. **David closed step 1.** `Report.md` untouched. | this file |
| 11 | Step 2 begun. David: the paper is an editorial, and editorial and opinion were added to the contract as kinds of paper (committed separately as `f4ca2f9`). Recorded in `Framing`. The question of what the fixed section structure means for an editorial raised and left to David. `Report.md` untouched. | this file |
| 12 | Step 2 continued. The reader set: a researcher deciding whether to submit. David wrote what the paper says, recorded verbatim in `Framing`, with three kinds of contribution sought and the claim that Models and Words is itself an AI agent. Questions put back to him on the two triples, on what is actually automated in review, and on whether the scope sentence admits other approaches. `Report.md` untouched. | this file |
| 13 | Step 2 continued. FRAMEWORK: the working abstract now lives in `Report.md` and is edited there (`d1f4d6a`); the three points are explained to the author and suggested from their own text (`8cb7152`). David's statement went into the `Abstract`; he set the three points as the three after "In this article,"; and on his instruction the agentic-AI sentence was cut from the `Abstract` and parked for the `Introduction`, under a rule to keep the editorial timeless. | `Report.md`, this file |
| 14 | Step 2 continued. The `Abstract` states A, B and C in order — the three kinds of contribution (A), then submissions written with an agent (B), then review (C) — so the closing sentence that named them again was cut as a repeat. David then moved to Obsidian to edit the `Abstract` himself; the state before his pass is committed, and nothing is to be changed in `Report.md` until he says he is done. | `Report.md`, this file |

## Code Summary

*Kept current whenever code is added or changed: what each script does, how to run it, what it reads and produces, and any model, prompt, seed or setting that affects the result. Installation belongs in [Setup.md](Setup.md).*

## References

*Sources behind the material, as distinct from the works the report cites.*
