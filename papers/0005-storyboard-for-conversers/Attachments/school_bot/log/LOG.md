# School chatbot via the Storyboard Generator: session log

- **Date:** 2026-11-09
- **Target project:** `K:\Vivid\school_bot`
- **Generator tool:** `K:\Vivid\Afya\Storyboard-Generator` (git HEAD `b6e5f38`)

## Contents of this log folder

| File | What it holds |
|---|---|
| `LOG.md` | This file: the chronological record and the index to everything else |
| `builder-brief.md` | What the builder knew before starting (its full context/specification) |
| `builder-instruction.md` | The exact instruction given to the builder subagent |
| `agents.md` | Every agent: type, model, instruction, date |
| `rounds/round-NN-question.md` / `-answer.md` | Every question round, verbatim in both directions |
| `area-changes.md` | Areas as first defined, and every later change with its reason |
| `versions/storyboard-vN.html` + `.json` | Each rendered version of the storyboard |
| `build-report.md` | What the build agent built, and where it guessed or went wrong |

---

## 1. The domain and why it was chosen

**Domain:** a student-facing information chatbot for a (fictional) English secondary school,
Ashbourne High School: Years 7–13, ages 11–18, including a Sixth Form.

**Why this domain:**
- **The human set the brief.** The task was a school chatbot covering resources, admin processes
  and registration, with multiple areas including "Processes". The operator first proposed a
  college, and the human switched it to a **high school**.
- **It exercises the generator's area model.** School processes (choosing options, changing
  subjects, reporting absence, exam entries) are multi-turn topics whose correct answer depends on
  *where the student is* in the process: before the deadline, inside the change window, or after
  it. That is exactly what the generator's *stages* and *facets* are meant to capture. Quick facts
  (office hours, who to contact) are discrete lookups, which exercises the *functions* model too.
  So the domain should come out "Mixed".
- **It has real hard rules.** Safeguarding, no access to personal records, and never pretending to
  submit a form are behavioural rules separate from topic scope. They exercise the generator's
  constraints section (C1).
- **It has two plausible audiences.** Students and parents/carers test whether the generator
  surfaces more than one persona.
- **It's fictional.** No real school, staff or dates are represented, so drafted content can't be
  mistaken for real school policy.

## 2. What the builder knew before starting

See `builder-brief.md` (verbatim and complete). Summary: the persona is a non-developer data
coordinator. They know the school's structure, the recurring questions, the hard rules (no
personal records, no acting on anyone's behalf, safeguarding), and that they're unsure about
parents as an audience, off-topic handling, deadlines and testing.

## 3. Generator pre-flight (before any question)

| Step | What happened |
|---|---|
| Step -1 (locate tool) | `STORYBOARD_GENERATOR_PATH` was unset. The operator already knew the path (`K:\Vivid\Afya\Storyboard-Generator`), so the builder wasn't asked. |
| Step 0 (prior state) | No `.storyboard-config.json` and no `storyboard.html` in the target, so this is a genuine first run. The regeneration safety check did not trigger. |
| Step 1 (discovery) | The target contained only `CLAUDE.md`: no code, prompts or data. Per the instructions, discovery was skipped and everything comes from questions. |
| Step 2 (tabs, provisional) | Overview, Pages, Tests and Issues are always on. Flows and Test Conversation are expected (O8 always yields a plan). Areas depends on AF1. Prompts is off (no real prompt exists). Thresholds depends on T1. Data Sources depends on F3/D1. |

## 4. Every question and answer, in order

Each round's full text is in `rounds/`. The table below gives the question ID, the question, and
the answer of record.

| # | ID | Question (short) | Answer of record | Notes |
|---|---|---|---|---|
| 1 | REVIEW-MODE | Review long drafts inline or as editable files? | **Inline in the chat** | Saved as `reviewMode: "inline"` in `.storyboard-config.json`. Every draft and its edits are therefore inside the round files. |
| 2 | O1 | What does your converser do? (free text) | A help chatbot on the school website for students, maybe parents. Main job: explain processes step by step (options, changing/dropping subjects, absence and leave, exam entries/resits/access arrangements, joining/transfers). Also resources and rules. Hard limits: no personal records, never acts on anyone's behalf, safeguarding redirect. Hosted LLM, placeholder dates. | Restates the brief almost exactly. Parents left explicitly undecided. |
| 3 | O2 | What powers its responses? | **GPT alone** (hosted LLM grounded in school material) | No calculation, so the Thresholds tab is unlikely (still asked at T1). |
| 4 | O3 | Name? | **Ask Ashbourne** (decided now) | Rejected "AshBot" (too gimmicky for safeguarding) and "Helpdesk" (clashes with the IT Helpdesk). |
| 5 | O4a | Main student persona | **Year 9 choosing GCSE options** | Builder warned: don't make the tone too young for Sixth Formers. |
| 6 | O4b | Second audience? | **Partly**: parents can use it, but it's not tuned for them (decided now) | Generator rule "never document only one audience" means a parent persona is still recorded. |
| 7 | O4c | Parent goal | **Reporting an illness absence** | New hard rule raised unprompted: never imply term-time leave will be approved (head's decision). Carried to C1. |
| 8 | O5a | Student tone | **Adaptive**: plain/friendly with numbered steps and school terms explained, more detail for Sixth Form. **No emoji** (decided now). | Feeds `personas[].tone`. |
| 9 | O5b | Parent tone | **Same as students**, no separate tuning in v1 | |
| 10 | O6 | Up-front data needed? | **No: open conversation**. Ask for year group or student/parent only when the answer depends on it. Never ask for names. (decided now) | So `conversationStates` is omitted. The "minimal data" rule is carried to C1 as a constraint candidate. |
| 11 | O7 | Two example conversations (generated draft, review inline) | **Both approved with edits.** Options: add tutor/careers adviser for personal advice, and make parent-app distribution [TBD]. Absence: remove the invented "Report absence" app button (now [TBD]), have the parent give the child's name to the attendance line (not to the bot), don't promise a mock catch-up paper, and tell the Exams Officer "on the day of the exam". | **The builder caught the generator inventing facts** (an app button and a catch-up paper). This is evidence for the grounding constraint at C1. |
| 12 | O8a/b | Sort 12 likely questions IN/OUT | IN: 1, 2, 3, 4*, 5*, 7, 8, 10**, 12. OUT: 6 (records), 9 (doing homework), 11 (acting on their behalf). *special handling: never imply leave approval or access arrangements. **safeguarding redirect, highest priority. **6 questions added:** joining/transfer (council [TBD]), resits, uniform/late, counselling, self-harm (safeguarding), who the DSL is. | The builder treated safeguarding as IN-scope with a fixed redirect rather than OUT. |
| 13 | AF1 | Functions, areas or mixed? (previews shown; generator suggested Mixed) | **Mixed.** Pushbacks (decided now): (a) don't make one big "Processes" area; split it by process, and don't force stages where none exist; (b) safeguarding is neither function nor area, it overrides everything. | **Area change C1 and C2**, see `area-changes.md`. C2 exposes a schema gap: there's no "global override" construct. |
| 14 | O9 | Redirects for 3 out-of-scope categories + catch-all | A (records) approved. B (homework) approved, with homework club now [TBD: confirm it exists]. C (acting on someone's behalf) approved. Catch-all approved, **plus a rule: never use the catch-all for anything that might be a safeguarding concern.** | `outOfScope.mode = "fixed"`. |
| 15 | O8c/d | Capabilities plan: 4 process areas + 6 functions + safeguarding override (all PROPOSED) | **Approved with changes:** (a) internal Y11→Sixth Form goes to Subject choices; Joining = external students only; entry requirements [TBD]. (b) WhoToContact gives office/role contacts only, never personal staff details (decided now). (c) Counselling questions pass the safeguarding check first. (d) The lateness rule (function) and procedure (area) must not conflict. | Area change C3. (d) exposes a schema gap: no way to link related items for consistency. |
| 16 | AF2 | Stages for each of the 4 areas | Subject choices approved. Exams approved, plus mock-vs-real in Exam season and [TBD] summer contacts in After results. Absence & leave split by situation accepted, but appointments must be separate from term-time leave (decided now). Joining approved (external only). | Area changes C4, C5. |
| 17 | AF3 | Facets per area (27 drafted, 4 thin stages flagged) | **Approved with changes:** 9 facets added to fill the thin stages. 3 facets corrected where the generator had stated unverified procedure as fact (exam tiers, appointment evidence, review of marking). | Area changes C6, C7. The third instance of the generator inventing detail (see C7). |
| 18 | AF4 | Are facet answers real or drafted? | **Drafted — write them and I'll review** (all areas). Source for the [TBD]s = the school's published policies and calendar. Each area signed off by its process owner before go-live (decided now). | Schema gap: no owner/reviewer field. |
| 19 | AF5 | Remember covered areas or start fresh? | **Remember and resume, within one conversation only**. Nothing between visits (decided now). | `areas[].lifecycle`. |
| 20 | C1 | 7 drafted behavioural constraints + enforcement | **All 7 approved.** Safeguarding: code + prompt, over-trigger if in doubt, wording to be approved by the DSL, and whether risk chats are logged/flagged left OPEN for the DSL. Grounding: prompt + code ([TBD] blocker). Minimal data: + "don't repeat volunteered details back"; retention [TBD: DPO]. **Added CONSTRAINT-8: no medical advice** (NHS 111 / GP). | Schema gap: `enforcement` is single-valued ("prompt" or "code"), so "code AND prompt" can't be expressed. Recorded as `code`, with the prompt part in the text. |
| 21 | WE1 | Annotated example of a non-obvious mechanism (safeguarding mid-area) | **Accurate, kept.** Added to the explanation: in Years 7–11 a parent/carer reports absences. | Area change C8. |
| 22 | O10 | Disclaimer? | **Other (custom):** "Ask Ashbourne gives general information about school processes and policies. It can't see your records or act for you. Always check important dates and decisions with the school. If you or someone else is in danger, call 999." (decided now) | None of the 3 generated options fit a school. |
| 23 | O11 | Separate converser-generator tool? | **Not yet — still deciding** (it'll be "a coding agent") | So `meta.converserGeneratorName` stays unset. TC4/X2 must say "the connected converser generator". |

> **STORYBOARD VERSION 1 rendered** at 04:01 → `versions/storyboard-v1.html` + `.json`.
> It contains everything after rounds 1–8: the Overview (pitch, 2 personas, 2 example conversations,
> 1 worked example, 6 capabilities, scope, out-of-scope, disclaimer, 8 constraints) and **the areas
> as first fully defined**: 4 process areas, 11 stages, 36 facets, all PROPOSED / drafted /
> needs-review. Pages, Tests and Issues are deliberately empty (not yet asked). Rendered tabs:
> Overview, Pages & Features, Issues To Check, Tests & Results, Areas & Coverage.
>
> **Gap noted while writing v1:** the builder's sign-off owners (AF4) and the "code AND prompt"
> enforcement (C1) had no schema field. They're placed in `summary` and `enforcedBy` text instead.

| 24 | F1+F2 | 7 flows + a 4-step message pipeline (risk check → router → handler → [TBD] output block) | **All approved.** Make it explicit in flow 2 that the risk check runs on every follow-up inside an area too. | Flows tab ON. |
| 25 | Q-F1a | (Raised by the flows) After the safeguarding response, the user returns to the original question? | **(b)** Answer normally + one line repeating the contacts, once only. Never raise the concern again (decided now). | New behaviour. Not covered by any instruction step; it surfaced only from drawing the flow. |
| 26 | Q-F1b | (Raised by the flows) What does the bot say when the only answer is [TBD]? | "I don't have that detail confirmed yet. Please check with [owning office]". If the office is also [TBD] → "Please check with Reception." Never guess (decided now). | Interaction between CONSTRAINT-2's code check and content gaps. |
| 27 | F3 | Few-shot file `data/few_shot_examples.csv` (13 rows), written into the project | 11 rows approved. **Row 5 corrected:** "tell the Exams Officer before you start" was an invented procedure that nudges an ill student into an exam → [TBD]. **Row 6:** NHS 111/GP only when the parent asks something medical. **+3 rows** (attendance records, essay writing, Year 12 dropping Further Maths). Now 16 rows. | **The fourth invented procedural detail caught by the builder.** Data Sources tab ON (synthetic, review required). |
| 28 | TC1 | 3 scripted demos with illustrative payloads | A approved. B: the leave office becomes [TBD]. **C corrected:** "not personal details" implied the SENCO's name was secret. Named role holders are fine if published; personal emails/phones never (decided now). | Refines CONSTRAINT-6 (v2). |
| 29 | TC2 | Live-mode system prompt | Approved with changes: remove "(fictional)" from the in-character prompt; **add two rules the generator had dropped** (no national/exam-board rules unless in school material; don't recommend subjects); label the safeguarding text "draft, pending DSL approval". | **The generator's prompt draft lost two already-agreed rules** (CONSTRAINT-7 and the facet rule from sc-how-to-choose). Compiling a prompt from the storyboard isn't lossless. |
| 30 | TC3 | Default live provider | **Anthropic (Claude)** (decided now) | |
| 31 | TC4 | Sandbox banner | Default kept + "Please don't type real names or personal information into this preview." | No generator name (O11 unset), so "the connected converser generator" is used. |
| 32 | D1 | Existing codebase/database? | **No.** List the planned reference files; each area's owner checks theirs. | Data Sources: 1 synthetic file + 5 planned files. |
| 33 | T1 | Calculation/thresholds? | **No** | Thresholds tab OFF (asked, not inferred). |
| 34 | P1 | Existing site pages? | None in the project. The bot sits on the school website and links to its policies and calendar pages [TBD: URLs]. The parent app is only mentioned. | |
| 35 | P2 | Sign-in? | **No sign-in — fully open** | |
| 36 | P3 | Audience input method | **Skipped by the generator** (O6 = no up-front data) | |
| 37 | P4 | Reply mode | **Text with suggestion chips**. No chips after a safeguarding response, and no sensitive-topic chips (decided now). | |
| 38 | P5 | Help page? | **Yes, short:** can/can't do, example questions, safeguarding contacts, privacy note [TBD: DPO]. | Draft shown in round 11. |

> **STORYBOARD VERSION 2 rendered** at ~04:20 → `versions/storyboard-v2.html` + `.json`, built
> from v1 by `versions/make_v2.py` (every edit in that script is commented with the question that
> caused it). New tabs: Function Flows (7 flows), Test Conversation (3 scripted demos with
> illustrative payloads, live mode = Anthropic, DSL-pending safeguarding text), Data Sources (1
> synthetic + 5 planned files). Edits to v1 content: CONSTRAINT-6 and WhoToContact refined (C10),
> CONSTRAINT-1 marked "draft, pending DSL", area lifecycle note extended (C9), and flow 2 states that
> the risk check runs on every follow-up. Pages has 3 planned entries. Tests and Issues are still
> empty.

| 39 | P5 | Help page draft (6 sections) | Approved + **"Telling Ask Ashbourne something does not tell a member of staff…"** (wording [TBD] until the DSL decides on logging). | Important for safeguarding: a student might believe a disclosure reached staff. |
| 40 | X1 | Tests elsewhere that discovery missed? | **No** | |
| 41 | X2 | 7 planned scenario tests (claim + transcript) | 6 approved. **Test 4 corrected:** "its march" assumed an unconfirmed cut-off date. **+3 tests:** honesty about capability, minimal personal data (no name echo), no medical advice. **Safeguarding coverage widened:** a varied set of risk phrasings, DSL-reviewed (decided now). | **The fifth time a generator draft assumed an unconfirmed fact.** 10 planned tests. |
| 42 | X3 | What the tests don't verify | Approved + "They also don't replace a staff pilot with real student and parent questions before go-live." | `testsNotCovered`. |
| 43 | I1 | Discovered issues | **None** (no code, TODOs or tracker) | |
| 44 | I2 | Review of 11 session issues | 10 approved. **#9 count corrected** from 5 to 6 (the builder caught the generator miscounting its own errors). #4 confirmed as the only blocking issue (Areas tab). **+3 issues:** content upkeep each school year (general), readability/accessibility for ages 11+ and SEND (not covered by any storyboard question), no build tool chosen. | 14 issues. |

> **STORYBOARD VERSION 3 (complete) rendered** at ~04:35 → `versions/storyboard-v3.html` + `.json`
> (built from v2 by `versions/make_v3.py`), and also as the project deliverable
> `K:\Vivid\school_bot\storyboard.html` + `storyboard.json`. Additions: help page (Pages, 4 entries),
> **11 planned tests** (the builder's 10, with "extend test 7" implemented as a separate
> "Safeguarding phrase coverage" test whose phrase list is [TBD: DSL]), `testsNotCovered`, and
> **14 issues** (ISSUE-4 blocks the Areas tab). No area content changed between v2 and v3.
> `.storyboard-config.json` written (Step 7).
>
> **Question count:** 44 answer rows across 12 rounds. The builder used "(decided now)" on 24
> occasions: decisions the storyboard process forced that weren't in its brief.

## 5. The build

See `agents.md` §3 (agent, model, instruction, date) and `build-report.md` (what was built, and
where it guessed or went wrong because the storyboard was missing something).

### Build summary (details in `build-report.md`)

- **Built:** a Python standard-library chatbot in `K:\Vivid\school_bot\app\`, offline and live
  modes, and 25 self-reported gaps in `app\BUILD_NOTES.md`.
- **Tests:** `python -m pytest tests -q` → **59 passed, 1 xfailed**. Re-run independently by the
  operator, same result.
- **Operator's held-out probe:** **3/14 risk messages caught by the safeguarding check**, and 9 of
  the misses went to the catch-all. A paraphrased options question lost the 4 steps.
- **Root causes in the storyboard:** no detection/classification method; author notes mixed into
  user-facing text; content specified only in examples; internal contradictions; no owning-office
  mapping; an unstated third-party data flow.

## 6. Post-build round

| # | ID | Question (short) | Answer of record | Notes |
|---|---|---|---|---|
| 45 | Q13a | How should risk detection be specified? (3/14 held-out) | **LLM classifier first + keyword backstop, over-trigger, AND no student launch until the DSL signs off held-out results.** Must fire on mixed messages, concerns about others and slang, and never reach the catch-all. Exploitation reporting route [TBD: DSL]. | Area change C15, CONSTRAINT-1 rewritten, ISSUE-15. |
| 46 | Q13b | Add a facet for the options steps? | **Approved** | Area change C11. |
| 47 | Q13c | Drafts vs approved-only | **Drafts only in a staff-only pilot with a "draft" banner; approved-only at go-live** (decided now) | CONSTRAINT-9. |
| 48 | Q13d | One safeguarding text without the placeholder? | **Yes**: a crisis reply must never get a "check with Reception" line | Few-shot row 1 and the mechanism example updated. |
| 49 | Q13e | Owning office per detail | **Corrected the build's guesses:** access arrangements → SENCO; GCSE → Head of Year vs Sixth Form → Sixth Form Office; term-time leave → [TBD], else Reception; lookups mapped to Library/IT Helpdesk/Finance/Reception | Area change C14. |
| 50 | Q13f | Third-party data flow in live mode | **DPO sign-off required; offline only until then.** Names removed isn't enough (tutor group + details); safeguarding messages to the provider [TBD: DPO + DSL]; provider data handling [TBD: DPO] | CONSTRAINT-10, ISSUE-16. |

> **STORYBOARD VERSION 4 rendered** → `versions/storyboard-v4.html` + `.json` (built from v3 by
> `versions/make_v4.py`), and as the project deliverable `K:\Vivid\school_bot\storyboard.html`.
> 9 tabs.

## 7. Step 6: diff-aware regeneration report (v3 → v4)

| What | Change |
|---|---|
| Tabs | **+ Prompts** (Step 1 re-discovery found a real prompt at `app/data/system_prompt.txt`, copied verbatim and checked byte-for-byte; staleness note: the code appends per-turn context not in the file) |
| Capabilities | No new capabilities. All stay PROPOSED (see ISSUE-19 for why not LIVE). |
| Flows | Safeguarding override → **CHANGED**. The risk-check step now names the detection method in every flow. WhoToContact gets the office mapping. |
| Areas | +1 facet (C11); 8 facets rewritten (C12, C13); owning office per area (C14) |
| Constraints | CONSTRAINT-1 rewritten with migration note; **+ CONSTRAINT-9** (approved-only at go-live); **+ CONSTRAINT-10** (live mode off until DPO) |
| Scope | Acting-on-behalf redirect and catch-all cleaned (the catch-all no longer says "contact Reception on (not confirmed yet)") |
| Personas | No change |
| Tests | 11 planned → **pass** (lastRun 2026-11-09); **+2 fail** (held-out safeguarding 3/14; smoke paraphrase) |
| Issues | ISSUE-3 → in-progress; **+ ISSUE-15 to 19**; none resolved |
| Data sources | 4 reference files → newly-wired-up (they exist in `app/data/`, still [TBD]); + keyword lists (synthetic, DSL review) |
| Not propagated | The running app in `app/` was **not** rebuilt from v4. It still reflects v3. v4 is the spec for the next build. |

## 8. Index of the required log items

| Required item | Where |
|---|---|
| The domain and why it was chosen | §1 above |
| What the builder knew before starting | `builder-brief.md` (verbatim); §2 summary |
| Every question asked and the answer, in order | §4 and §6 tables (50 rows) + `rounds/` verbatim, 13 rounds both ways |
| Each storyboard version as HTML, areas as first defined, changes with reasons | `versions/storyboard-v1…v4.html` (+ `.json`, `make_v2/3/4.py`); `area-changes.md` (A0–A2, C1–C15, evolution table) |
| Agent, model, instruction, date | `agents.md`; `builder-instruction.md`; `build-agent-instruction.md` |
| What the agent built, and where it guessed or went wrong | `build-report.md`; `app/BUILD_NOTES.md` |
