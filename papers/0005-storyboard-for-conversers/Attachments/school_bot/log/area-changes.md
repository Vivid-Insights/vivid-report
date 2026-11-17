# Areas: first definition and every change, with reasons

Each entry records what the areas looked like before and after, which question caused the change, who
asked for it, and why. The storyboard version where each change first appears is noted, so you can
open `versions/storyboard-vN.html` to see it rendered.

---

## A0. First definition: the generator's AF1 preview (round 5, before any change)

**Source:** the generator's own draft, shown to the builder as the AF1 "Areas" and "Mixed" previews.
This is the first time areas existed in the session.

```
AREA: Processes   (options, changing/dropping subjects, ...)
  Stages: Before the deadline · Inside the change window · After the cut-off
  Facets: How do I choose my GCSE options?  → Before the deadline
          Can I drop/change an A-level?     → Inside the change window, After the cut-off
AREA: Resources   (Areas preview only; in the Mixed preview this became the function GetOpeningHours)
  Facets: Is the library open after school?  (no stages)
```

**Why the generator drafted it this way:** the human's original instruction named "Processes" as an
area (including registration and dropping courses), and O1/O8 showed process answers depend on
timing. The generator applied one timeline-shaped stage set to all processes.

---

## C1. Processes split into separate process areas; stages no longer universal (round 5, AF1)

- **Before:** one area, "Processes", with one stage set shared by every process.
- **After (to be drafted in round 6):** one area per process, kept grouped by a shared name prefix
  ("Processes · …"). Each area gets its own stages, or none.
- **Requested by:** the builder, at AF1 (round 5), "decided now".
- **Reason (builder's words, summarised):** options, subject changes, exams, absence/leave and
  joining "are different processes with different staff and forms". The before/window/after
  stages "don't apply to every process". For example, reporting an illness absence has no stages.
- **Generator's reasoning for the naming:** the human's instruction asked for a "Processes" area.
  The "Processes · " prefix keeps that grouping visible while honouring the builder's split.
- **Methodological note:** the generator's AF1 preview over-generalised one process's timeline to
  all processes. The instructions (AF2) already say a stage split "isn't universal", but the AF1
  preview step itself gives no prompt to check that. The builder caught it, not the generator.

## C2. Safeguarding removed from the area/function model entirely (round 5, AF1)

- **Before:** in O8b, safeguarding items (bullying, self-harm) were tagged "IN, special handling",
  so the generator would have placed them as a function or a facet.
- **After:** safeguarding is a **global override**, outside every area and function. A risk signal
  at any point, in any area, interrupts the topic. It also overrides the out-of-scope catch-all
  (O9).
- **Requested by:** the builder, at AF1 and O9 (round 5).
- **Reason:** "It must override everything." An area or function only fires when the conversation
  is routed to it, while a safeguarding signal can appear mid-topic.
- **Storyboard gap:** the schema has nowhere to put a global override. Neither `capabilities`
  (routing) nor `areas` (topics) models "interrupts everything". It will be represented as a
  `constraints[]` entry plus a dedicated flow, and logged as an Issue.

---

## A1. Areas after O8c/AF2 drafting (round 6, generator's draft)

Four areas, all PROPOSED:
- **Processes · Subject choices**: stages *Choosing* / *Change window* / *After the cut-off*
- **Processes · Exams**: stages *Before entries close* / *Exam season* / *After results*
- **Processes · Absence & leave**: stages *Unplanned absence* / *Planned absence* (a split by situation, not a timeline; offered with an explicit "reject it if forced")
- **Processes · Joining the school**: stages *Applying* / *Just joined*

Plus 6 functions (GetOpeningHours, WhoToContact, ExplainSchoolRule, FindSupport, OpenProcessArea,
RedirectOutOfScope) and the safeguarding override.

## C3. Boundary between Subject choices and Joining the school (round 6, O8d)

- **Before:** "Joining the school" included Sixth Form applications in general, which overlapped
  with "Subject choices" (A-level subjects for Year 11 going into 12).
- **After:** internal Year 11 students applying to the Sixth Form → **Subject choices**.
  **Joining the school** → only students from *other* schools (Year 7, mid-year, or into Year 12).
  Both area summaries state the boundary. Sixth Form entry requirements are [TBD].
- **Requested by:** the builder.
- **Reason:** the two areas would otherwise both claim the same question, and the processes differ
  for internal and external applicants.
- **Methodological note:** the generator's plan step didn't check for overlap *between* areas. AF2
  and AF3 look inside one area at a time.

## C4. Exams stages refined (round 6, AF2)

- **Exam season:** now explicitly separates internal mocks (handled by teachers) from real
  GCSE/A-level exams (handled by the Exams Officer).
- **After results:** now includes summer staff availability, as [TBD: summer contact arrangements].
- **Reason (builder):** the same mock/real distinction was already corrected once in O7. Results
  arrive in August while school is closed, so "contact the Exams Officer" may not work then.

## C5. Absence & leave: three stages instead of two (round 6, AF2)

- **Before:** *Unplanned absence* / *Planned absence* (appointments and term-time leave together).
- **After:** *Unplanned absence* / *Planned appointment* / *Term-time leave request*.
- **Requested by:** the builder, "decided now".
- **Reason:** appointments are "normally just reported with notice". Only holiday-type leave goes
  to the headteacher and needs "exceptional circumstances". Mixing them risks applying the leave
  rules to a dentist visit, or the reverse.
- **Note:** the builder had said in round 5 that illness absence has no stages. It accepted a
  split *by situation* once it was framed that way. "Stage" in the generator's vocabulary means
  "situation needing different material", which is broader than a timeline.

## Cross-area note (round 6, not an area change)

The builder flagged that the lateness *rule* (function ExplainSchoolRule) and the lateness
*procedure* (Absence & leave → Unplanned absence) must not contradict each other. The schema has no
way to link a function and a facet as "must stay consistent". This will be recorded as an Issue.

## A2. Facets as first drafted (round 7, AF3, generator's draft)

27 facets in total: Subject choices 7, Exams 8, Absence & leave 7, Joining 5. Full text is in
`rounds/round-07-question.md`. Four stages were flagged THIN: *After the cut-off* (2), *Planned
appointment* (1), *Term-time leave request* (2), *Just joined* (2).

## C6. Thin stages filled: 9 facets added (round 7, AF3)

- **Subject choices / After the cut-off:** + `sc-struggling-midyear`, + `sc-late-change-impact`
- **Absence & leave / Planned appointment:** + `ab-leaving-site`, + `ab-appointment-attendance`
- **Absence & leave / Term-time leave request:** + `ab-exceptional`, + `ab-religious-observance`
- **Joining / Just joined (and Applying):** + `jn-accounts`, + `jn-settling`, + `jn-send`
- **Requested by:** the builder, responding to the generator's THIN flags.
- **Reason:** the THIN flag worked as designed. The builder filled stages instead of merging them.
  `jn-send` also gives a home to the parent goal (additional needs) from O4c that no area had
  picked up. `jn-settling` and `sc-struggling-midyear` are explicitly linked to the safeguarding
  override.
- **Result:** 36 facets.

## C7. Two drafted facts corrected as guesses (round 7, AF3)

- `ex-entries`: "Tiers are decided by your teachers" → "Tiers (foundation or higher), where a
  subject has them, are decided by the school [TBD: confirm who]."
- `ab-appointment`: "ideally with an appointment card or letter" → "[TBD: whether evidence such as
  an appointment card is needed]". Added: "Where possible, book routine appointments outside school
  hours."
- `ex-review-marking`: added "Reviews are requested by the school with your consent, so you can't
  contact the exam board directly."
- **Requested by:** the builder.
- **Reason:** the generator had stated these as facts. **This is the third time (after O7's app
  button and catch-up paper) that the generator's drafts invented a plausible detail, despite the
  generator's own AF3 rule "ground any figure/claim … in a real source".** The rule as written
  covers figures and dates. It doesn't catch *procedural* claims (who decides, what evidence is
  needed), which are where these slipped through.

## Facet ownership (round 7, AF4)

All four areas: `origin: drafted`, `reviewStatus: needs-review`. The builder named a sign-off owner
per area (Subject choices → Head of Year / Head of Sixth Form; Exams → Exams Officer + SENCO;
Absence & leave → Attendance Officer; Joining → admissions/Reception). **Schema gap:** there's no
field for a facet's or area's reviewer/owner, so this goes into each area's `summary` text and an
Issue.

## C8. Who reports an absence, made explicit (round 8, WE1)

- **Facet:** `ab-report-illness` (Absence & leave / Unplanned absence).
- **Before:** "Give the child's full name, tutor group and the reason." This implied a parent but
  never said so. The generator's WE1 transcript even had the bot offer the steps to a Year 10
  student.
- **After:** "In Years 7–11, a parent or carer reports the absence: …". Sixth Form stays [TBD]
  in `ab-sixth-form-own`.
- **Requested by:** the builder, in its WE1 review.
- **Reason:** "In Years 7–11, a parent/carer reports absences." A student-facing bot giving a
  Year 10 student steps they're not allowed to take would be wrong.
- **Methodological note:** this fact surfaced only when a *worked example* was reviewed, not when
  the facet itself was reviewed in AF3. A transcript makes the audience concrete in a way a facet
  table doesn't.

## Area lifecycle (round 8, AF5)

All areas: `remembersCoveredAreas: true`, **within the same conversation only**. Nothing is kept
between visits (the builder's data-minimisation reason).

## C9. Area lifecycle: resuming after a safeguarding interruption (round 9 Q-F1a → v2)

- **Before (v1):** lifecycle note = "remember and resume within the conversation; nothing between
  visits". It said nothing about what happens to an open area when the safeguarding override fires.
- **After (v2):** the area is *paused, not deleted*. If the user returns to their question, the bot
  answers normally and adds one line repeating the contacts, once only, and never raises the concern
  again. No chips are shown directly after the safeguarding response (P4).
- **Requested by:** the builder, answering a question the generator raised while drafting flows.
- **Reason:** the builder wanted the student to still get their answer without the concern being
  ignored or pushed.
- **Methodological note:** the instructions' AF5 question only asks "resume or restart when moving
  between AREAS". The interaction between an area and the override only became visible when
  the generator drew the flow (F1), so the area definition was completed by a *later* tab's
  question. The same happened with C8 (WE1).

## C10. Role-contact rule refined, affecting facets that name roles (round 10 TC1 → v2)

- **Before:** "office/role contacts only".
- **After:** a role holder's *name* may be given if the school publishes it; personal emails and
  phones never.
- **Reason (builder):** the demo reply "not personal details" made the SENCO's name sound secret.
- **Effect on areas:** none of the facet texts changed, but facets that name roles (SENCO, Exams
  Officer, Head of Sixth Form) can now include published names when filled in.

---

## Changes caused by the BUILD (round 13 → v4)

These changes came from a fresh coding agent building v1 from the v3 storyboard alone, and from
the operator probing that build with messages it had never seen. Each was decided by the builder in
round 13.

## C11. New facet `sc-options-steps` (Subject choices / Choosing)

- **Before:** the 4 options steps (Options Evening, booklet, form + reserve, Head of Year) lived
  only in the O7 example conversation and the few-shot file, not in any facet.
- **After:** a facet with those steps (and the O7 edits: booklet distribution [TBD], tutor/careers
  adviser for advice). 37 facets in total.
- **Caused by:** build gap G7. The smoke test passed only because its input exactly matched a
  few-shot row. The operator's paraphrase "what do i have to do to choose my gcses?" got no steps.
- **Reason:** the schema only grounds answers from facets, so content agreed in an *example* is lost
  to a builder.

## C12. Facet answers rewritten as plain user-facing text

- **Facets changed:** `sc-how-to-choose`, `sc-after-cutoff`, `sc-late-change-impact`,
  `ab-report-illness`, `ab-leave-request`, `ab-exceptional` ("The bot can't…" → "I can't…"),
  `ab-late-procedure` (cross-reference note removed), `jn-settling` (safeguarding note removed;
  the override is global anyway).
- **Caused by:** build gap G8. The facets mixed reply text with notes for the builder, and the build
  had to strip them by pattern.
- **Reason:** any note left in a facet can reach a student.

## C13. Who decides a late subject change: [TBD] consistently

- `sc-struggling-midyear` stated "the Head of Year / Head of Sixth Form decides" as fact, while
  `sc-after-cutoff` marked the same decider [TBD]. Both now use
  `[TBD: Head of Year / Head of Sixth Form]`.
- **Caused by:** build gap G19 (one reply showed both versions).

## C14. Owning office for unconfirmed details, stated per area

- Each area summary now ends with where unconfirmed details send people:
  - Subject choices: GCSE → Head of Year; Sixth Form → Sixth Form Office (not both when the year
    group is known).
  - Exams: Exams Officer, except **access arrangements → SENCO**.
  - Absence & leave: Attendance Officer, except **term-time leave → [TBD], falling back to
    Reception**.
  - Joining: Reception/admissions.
- **Caused by:** build gap G4. The storyboard never mapped an owner; the build agent guessed, and
  sent access-arrangement gaps to the Exams Officer.
- **Corrected by:** the builder (round 13, Q13e).

## C15. Safeguarding detection specified (affects every area)

- **Before (v1–v3):** "risk overrides everything, before any routing" was specified as an
  outcome, with no detection method.
- **After (v4):** an LLM risk classifier first, with a keyword backstop; over-trigger; must fire on
  mixed messages, third-party concerns and slang; never the catch-all. **Launch blocker** until the
  DSL signs off results on a held-out set. The safeguarding flow is now tagged CHANGED.
- **Caused by:** the operator's held-out probe: 3/14 caught. In two misses a risk sentence *inside
  an area* got that area's answer ("can i drop french? also i keep scratching my arms" → Subject
  choices). The override existed as a rule but not as a working mechanism.
- **Reason (builder):** "3 out of 14 is not acceptable, so this is a launch blocker."

## Summary of area evolution

| Version | Areas | Stages | Facets | Main reason for change |
|---|---|---|---|---|
| A0 (AF1 preview) | 1 ("Processes") | 3 (shared) | 2 | Generator's first draft |
| v1 | 4 | 11 | 36 | Split by process (C1); boundary (C3); stages refined (C4, C5); thin stages filled (C6); guesses corrected (C7); who reports absence (C8) |
| v2 | 4 | 11 | 36 | Lifecycle after a safeguarding interruption (C9); role-contact rule (C10) |
| v3 | 4 | 11 | 36 | No area change |
| v4 | 4 | 11 | 37 | Build-driven: missing facet (C11), author notes removed (C12), consistency (C13), owning offices (C14), detection (C15) |
