# Round 8: builder's answer (verbatim)

## AF5
Choice: "Remember and resume — most multi-area advice bots want this"
That should apply within the same conversation only. Nothing should be remembered between separate visits (decided now), which keeps it in line with collecting as little personal data as possible.

## C1
- **CONSTRAINT-1 Safeguarding:** approved. **Code AND prompt.** If in doubt, it should over-trigger: a false alarm is far better than a miss. Our DSL must approve the fixed response wording before go-live (decided now). Open question for the DSL: whether risk conversations are logged or flagged to staff at all. I don't know the answer, so please leave it as an open issue rather than deciding it.
- **CONSTRAINT-2 Grounding:** approved. **Prompt + code check** blocking "[TBD" text from reaching users.
- **CONSTRAINT-3 Honesty about capability:** approved. **Prompt.**
- **CONSTRAINT-4 No implied approvals:** approved. **Prompt.**
- **CONSTRAINT-5 Minimal personal data:** approved. **Prompt.** Add: "If a user volunteers a name or other personal details, don't repeat them back." Data retention and the privacy notice: [TBD: check with the school's Data Protection Officer].
- **CONSTRAINT-6 Role contacts only:** approved. **Prompt.**
- **CONSTRAINT-7 School material only:** approved. **Prompt.**
- **Add CONSTRAINT-8 · No medical advice** (decided now): never advise on whether a child is well enough for school or on symptoms. Point to the school's attendance/illness guidance if it's published [TBD], or to NHS 111 or a GP. **Prompt.**

## WE1
Accurate. Keep this example. Two small notes:
- Approve the bot dropping the absence steps and not probing. That's right.
- Add to the explanation: "In Years 7–11, a parent/carer reports absences, so even if the conversation had continued, the bot would not have helped the student report it themselves." That's a second non-obvious point the same transcript shows.

## O10
Choice: Other — Yes: "Ask Ashbourne gives general information about school processes and policies. It can't see your records or act for you. Always check important dates and decisions with the school. If you or someone else is in danger, call 999." (decided now)
Neither offered option fits. It isn't a demo tool, and "medical/legal/financial" isn't the point.

## O11
Choice: "Not yet — still deciding"
The plan is to hand the storyboard to a coding agent to build version 1, but I haven't picked a specific tool and don't have a name for it.
