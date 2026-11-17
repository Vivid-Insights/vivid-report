ROUND 9: function flows (F1), inputs/outputs and sequencing (F2), few-shot examples file (F3)

Your round 8 answers are applied. Storyboard version 1 has been rendered: Overview plus the four process areas.

## F1 + F2: flows (draft, review inline)
One flow per capability, plus the safeguarding override and the out-of-scope flow. For the areas, the flow is deliberately short: classify → inject facets → the model replies. The detail lives in the facet coverage map, not in a fake step-by-step procedure.

**Every message goes through the same pipeline (F2 sequencing):**
`message → (1) safeguarding risk check [code] → (2) router: process area / function / out-of-scope → (3) handler → (4) output check: block "[TBD" text [code] → reply`

| # | Flow | Type | Inputs | Steps | Outputs |
|---|---|---|---|---|---|
| 1 | Safeguarding override | INSTRUCTIONS | user message; current area (if any) | risk check flags it → current topic dropped → fixed safeguarding response (DSL-approved wording) → no probing questions | fixed response |
| 2 | OpenProcessArea | CHANGE_CONTEXT | user message; remembered area/stage/covered facets (this conversation only) | classify into area + stage (asking year group or student/parent only if the answer depends on it) → inject that stage's approved facets → the model replies in the persona tone | reply; stored current area + stage + facets covered |
| 3 | GetOpeningHours | WORDALISE | the place asked about | look up the opening-hours list → reply | reply (or "not confirmed yet, ask Reception" if [TBD]) |
| 4 | WhoToContact | WORDALISE | the topic | look up the role/office directory → reply with a role contact only | reply |
| 5 | ExplainSchoolRule | WORDALISE | the rule asked about | look up the published policy summary → plain-language reply (the lateness rule must match the Absence & leave procedure) | reply |
| 6 | FindSupport | WORDALISE | the need | look up the resources list → reply with how to access it | reply |
| 7 | RedirectOutOfScope | INSTRUCTIONS | user message | match a category (records / schoolwork / acting on someone's behalf / other) → that category's fixed redirect; for "acting on behalf", the self-service steps | fixed redirect |

Two questions the flows raise that the plan doesn't answer yet:
- **Q-F1a:** after the safeguarding response, what if the user then goes back to their original question (e.g. "ok but how do I report being off")? Should the bot (a) answer it normally, (b) answer it but repeat the safeguarding contacts once more, or (c) something else?
- **Q-F1b:** what does the bot say when the only answer it has is still [TBD]? The output check blocks "[TBD" text, so the user would otherwise get nothing. Draft rule: "I don't have that detail confirmed yet. Please check with [owning office]." Approve or change it.

## F3: few-shot examples file (written into your project)
The generator has written a real project file: **`data/few_shot_examples.csv`** (columns: flow; area; stage; user_message; ideal_answer). It has 13 examples, covering every flow and every area, and keeps all [TBD] placeholders. It will be registered as synthetic and needing review. Its rows are:

1. Safeguarding: "i dont want to come in because of what people keep doing to me" → the fixed safeguarding response
2. Subject choices / Choosing: "how do i pick my gcse options" → the 4 steps + tutor/careers adviser
3. Subject choices / After the cut-off: "its past the deadline but i really want to drop chemistry, can i?" → exceptional only, [TBD] decides; talk to the teacher and tutor first; no promise
4. Exams / Before entries close: "how do i get extra time in my exams" → SENCO, assessment and evidence, the Exams Officer applies, not guaranteed
5. Exams / Exam season: "im ill and my gcse english is today" → tell the Exams Officer today; special consideration; "If you're well enough to sit it, tell the Exams Officer before you start"; a parent reports the absence
6. Absence / Unplanned: "my daughter has a temperature and wont be in today" → parent reports, 3 steps, can't record it, no medical advice (NHS 111 / GP)
7. Absence / Term-time leave: "can we take him out for a week in june for a family holiday" → request form, headteacher decides, exceptional only, can't say if approved, unauthorised → possible penalty notice [TBD]
8. Joining / Applying: "were moving to the area in january, how does my son join ashbourne" → in-year application via [TBD], Reception/admissions, SENCO if SEN/EHCP
9. GetOpeningHours: "is the library open after school" → [TBD] hours
10. WhoToContact: "who do i talk to about extra time in exams" → SENCO, then the Exams Officer
11. ExplainSchoolRule: "can i use my phone at lunch" → [TBD: published policy in plain language], ask your tutor if unsure
12. FindSupport: "i forgot my school password" → IT Helpdesk, [TBD] location, take student ID [TBD: confirm], can't reset it
13. RedirectOutOfScope: "can you email mr patel and tell him ill be late" → can't contact staff; sign in at Reception, email your teacher from your school account

Approve or edit rows by number.
