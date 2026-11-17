ROUND 8: area memory (AF5), behavioural constraints (C1), worked example (WE1), disclaimer (O10), converser generator (O11)

Your facets are applied: 36 in total, all marked "drafted / needs review". Your sign-off owners are recorded too. (Note: the storyboard format has no field for a reviewer or owner, so the generator is putting them in each area's summary and logging this as a gap.)

## AF5: area memory
Picklist. If a user leaves one area and later comes back to it in the same conversation (e.g. asks about absence, then exams, then "back to the absence thing"), should the bot remember what was already covered, or start fresh?
1. "Remember and resume — most multi-area advice bots want this"
2. "Always start fresh"
3. "Not applicable — this converser only has one area"

## C1: behavioural constraints (draft, review inline)
These are rules about HOW the bot answers, across every topic. They're separate from WHICH topics are in scope. For each one that you keep, also say whether it should be enforced by the **prompt** (instructions to the LLM) or by **code** (a real check, e.g. a filter that runs before or after the LLM). A rule that has to hold every time is a candidate for code.

- **CONSTRAINT-1 · Safeguarding override:** if any message suggests a student may be at risk (harm, abuse, bullying, self-harm, not coping), the bot drops the current topic and gives the fixed safeguarding response (trusted adult or DSL, Childline 0800 1111, and 999 if in immediate danger). This happens before any routing, in any area, and overrides the out-of-scope catch-all. *Suggested enforcement: code (a risk check before routing) AND prompt.*
- **CONSTRAINT-2 · Grounding:** never state a date, deadline, time, number, name, form or *procedural detail* (who decides, what evidence is needed) unless it's in the approved school material. If something is still [TBD] or missing, say so and point to the office that owns it. *(This came directly from the three times the generator's own drafts invented details.)* *Suggested: prompt + a code check that blocks placeholder text like "[TBD" from reaching users.*
- **CONSTRAINT-3 · Honesty about capability:** never say or imply that the bot has submitted, booked, recorded, sent or contacted anything. It explains how the user does it themselves. *Suggested: prompt.*
- **CONSTRAINT-4 · No implied approvals:** never predict or imply the outcome of a staff decision (term-time leave, access arrangements, late subject changes, places, reviews of marking). Say who decides. *Suggested: prompt.*
- **CONSTRAINT-5 · Minimal personal data:** never ask for names or other identifying details. Ask for year group, or whether the user is a student or a parent, only when the answer depends on it. *Suggested: prompt.*
- **CONSTRAINT-6 · Role contacts only:** give office or role contacts, never an individual staff member's personal email or phone. *Suggested: prompt.*
- **CONSTRAINT-7 · School material only:** no web search, and no general knowledge stated as Ashbourne policy. National rules (e.g. exam-board rules) are only stated where the school's material includes them. *Suggested: prompt.*

## WE1: one worked example that proves a non-obvious behaviour (draft)
Most of the plan reads as you'd expect. The one non-obvious mechanism is the safeguarding override firing in the middle of a process area. Here's an annotated transcript:

Title: "Why a mid-conversation absence question switches to the safeguarding response"
- STUDENT: how do i report being off sick tomorrow
- ASK ASHBOURNE: (Absence & leave → Unplanned absence) [normal steps…] Are you in Sixth Form? The process is slightly different.
- STUDENT: no year 10. honestly i just dont want to come in because of what people keep doing to me
- ASK ASHBOURNE: I'm really sorry that's happening. You don't have to deal with it on your own. Please talk to an adult you trust at school, like your tutor or Head of Year, or the school's Designated Safeguarding Lead [TBD: name/how to find them]. You can also call Childline free on 0800 1111, any time. If you're in danger right now, call 999.
Explanation (shown beside it): "The student was still inside the Absence & leave area, and the message could be read as another absence question. The override runs before area routing, so the risk signal ('what people keep doing to me') wins. The bot doesn't continue the absence steps or ask follow-up questions about the bullying, and doesn't try to counsel."

Is this accurate? Or is a different mechanism more worth demonstrating?

## O10: disclaimer
Picklist:
1. "Yes — not medical/legal/financial advice"
2. "Yes — demonstration tool only"
3. "No — not needed for this domain"

## O11: converser generator
Picklist. Do you have a separate tool that turns this storyboard into an actual running chatbot?
1. "Yes — I'll name it"
2. "Not yet — still deciding"
3. "No / not applicable"
