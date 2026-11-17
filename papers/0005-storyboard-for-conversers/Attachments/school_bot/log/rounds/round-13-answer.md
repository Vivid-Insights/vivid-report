# Round 13: builder's answer (verbatim)

## Q13a
Choice: Other — Options 1 and 3 together: "An LLM risk classifier runs first, with a keyword list as a backstop, and it over-triggers when in doubt. No version launches to students until the DSL has signed off the detection method and its results on a held-out test set that the builder never saw."
3 out of 14 is not acceptable, so this is a launch blocker, not just a design choice. The storyboard should also state:
- A risk signal wins even when it's mixed with a normal question, as in the French and library examples.
- Concerns about a friend or someone else count, as in the "pills" example.
- Joking or slang phrasing ("kms lol") still triggers.
- Risk messages must never reach the catch-all.
Whether online-exploitation messages (the "pictures" one) need any additional reporting route in the response is for the DSL to decide [TBD] (decided now).

## Q13b
Approved. Add `sc-options-steps` with the 4 steps and the O7 edits: the booklet's distribution is [TBD], and point to the tutor/careers adviser for advice on choices.

## Q13c
Choice: "Answer from drafts during the staff pilot only, with a visible 'draft' banner; approved-only at go-live"
Condition (decided now): the pilot is staff only. Staff type in real questions collected from students and parents, but no student uses the draft version directly. At go-live, any unapproved facet gives the "not confirmed yet" fallback.

## Q13d
Yes. Keep the version without the placeholder as the only one until the DSL approves the wording. A crisis reply must never get a "check with Reception" line tacked on.

## Q13e
Corrections:
- **Access arrangements → the SENCO**, not the Exams Officer.
- **Subject choices:** GCSE questions → Head of Year. Sixth Form/A-level questions → the Sixth Form Office. Don't give both in one answer when the year group is known.
- **Term-time leave:** the owning office is [TBD]. Until it's confirmed, fall back to Reception, not the Attendance Officer.
- **Lookups:** library/revision → the Library/Learning Resource Centre; IT and passwords → the IT Helpdesk; trips and lunches → the Finance Office; everything else → Reception.
- **Confirmed:** Exams → Exams Officer, Absence → Attendance Officer, Joining → Reception/admissions.

## Q13f
Yes to both. Record it as needing Data Protection Officer sign-off, and run offline mode only until then. Add:
- Removing names isn't enough. A tutor group plus details can still identify a child, so the DPO should judge the risk on that basis.
- Safeguarding messages are especially sensitive. Whether they're sent to the provider at all is a question for the DPO and the DSL together [TBD].
- The provider's data handling (retention, whether data is used for training, where it's stored) is [TBD: DPO to confirm].

Noted on the builder notes and `sc-struggling-midyear`. Both fixes are fine.
