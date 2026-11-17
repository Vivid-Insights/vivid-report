ROUND 12 (last): issues to check (I1, I2)

Your round 11 answers are applied: the help page, 10 planned tests, and the test limits statement.

## I1: discovered issues
Your project has no code, TODOs, changelog or issue tracker, so nothing was discovered automatically.

## I2: everything left unresolved during this session (draft)
The generator kept a running list. Each issue has a priority. Some have a tag: "specific" (only this chatbot) or "general" (a lesson any chatbot project could hit). One issue is marked as BLOCKING a whole tab, which shows a warning banner on that tab until it's resolved.

| # | Issue | Priority | Tag | Blocks |
|---|---|---|---|---|
| 1 | Safeguarding response wording is a draft and must be approved by the DSL before go-live. | high | specific | – |
| 2 | DSL to decide whether risk conversations are logged or flagged to staff. This also decides the help-page sentence "telling Ask Ashbourne doesn't tell staff". | high | specific | – |
| 3 | The safeguarding risk check (code) isn't built. It needs a varied, DSL-reviewed set of risk phrasings and must over-trigger when in doubt. | high | general | – |
| 4 | All school specifics are still [TBD] (dates, deadlines, contacts, hours, policies, URLs, Sixth Form absence procedure, entry requirements). The 36 facet answers are drafted and need review. Each area's owner must sign off: Head of Year / Head of Sixth Form; Exams Officer + SENCO; Attendance Officer; admissions/Reception. | high | specific | **Areas tab** |
| 5 | Data retention and privacy notice wording: check with the Data Protection Officer. | medium | specific | – |
| 6 | The lateness RULE (ExplainSchoolRule) and lateness PROCEDURE (Absence & leave) must be checked against each other so they never conflict. | medium | specific | – |
| 7 | Parents are only "partly" supported in v1. Revisit a separately tuned parent audience after launch. | low | specific | – |
| 8 | Run a staff pilot with real student and parent questions before go-live. | medium | specific | – |
| 9 | **Storyboard tool lesson:** the generator's drafts stated unverified procedure as fact 5 times (app button, mock catch-up paper, exam tiers, appointment card, exam-day procedure, and a March cut-off in a test). Its grounding rule covers figures and dates but not procedural claims (who decides, what evidence is needed). | medium | general | – |
| 10 | **Storyboard tool lesson:** the storyboard format has no place for a global override (safeguarding was modelled as a constraint plus a flow), no owner/reviewer field for areas or facets, no way to record "code AND prompt" enforcement, and no way to link two items that must stay consistent. | medium | general | – |
| 11 | **Storyboard tool lesson:** compiling the live system prompt from the storyboard dropped two already-agreed rules until you caught them. Any generated prompt should be checked against the constraints list. | medium | general | – |

Confirm, change priorities or tags, or add anything that's missing. Is it right that #4 blocks the Areas tab?
