ROUND 6: the capabilities plan (O8c/d) and stages per area (AF2)

Your pushbacks are applied. "Processes" is now split into one area per process. The areas keep a shared "Processes · " name prefix so they still read as one group. Safeguarding sits outside the plan as an override (see the bottom of this message). All items are tagged PROPOSED, because no code exists yet.

## O8c/d: draft plan. What would you change?

**AREAS** (multi-turn topics; stages and facets are drafted in AF2/AF3)
1. **Processes · Subject choices**: choosing GCSE options (Year 9) or A-level subjects (Year 11 into 12), and changing or dropping a subject afterwards.
2. **Processes · Exams**: exam entries, resits, access arrangements (e.g. extra time) and special consideration.
3. **Processes · Absence & leave**: reporting an absence (illness, appointments), lateness procedure, and requesting term-time leave.
4. **Processes · Joining the school**: applying for a place (Year 7 or Sixth Form), in-year transfers, and the first weeks after joining.

**FUNCTIONS** (one-turn lookups)
| Trigger | Function | Type | What it does |
|---|---|---|---|
| "Is the library open after school?" / "When is Reception open?" | GetOpeningHours | WORDALISE | Answers from the school's opening-hours list. |
| "Who do I talk to about…?" / "Who is the DSL?" | WhoToContact | WORDALISE | Names the right office or role and how to reach them. Names of people stay [TBD]. |
| "Can I use my phone at lunch?" / "What's the uniform rule?" | ExplainSchoolRule | WORDALISE | Explains a published policy in plain language. |
| "Where can I get revision help?" / "How do I see the counsellor?" / "I forgot my password" | FindSupport | WORDALISE | Points to the right resource (library, revision sessions, counselling, careers, IT Helpdesk) and how to access it. |
| Any process question ("how do I…", "can I still…") | OpenProcessArea | CHANGE_CONTEXT | Works out which process area and stage the user is in, and remembers it for the following turns. |
| Out of scope (records, schoolwork, acting on someone's behalf, anything else) | RedirectOutOfScope | INSTRUCTIONS | Gives the fixed redirect for the category (your O9 wording). |

**OVERRIDE (not a function or area, per your AF1 answer)**
- **Safeguarding response**: checked on every message, before any routing. If a message suggests risk, it drops the current topic and gives a short, kind, fixed response: trusted adult or DSL, Childline 0800 1111, and 999 if in immediate danger. It also overrides the out-of-scope catch-all.

## AF2: stages per area. Edit them, or say "no stages".
Each stage is described by what makes it **different from the other stages** in that area.

1. **Processes · Subject choices**
   - *Choosing*: before the options or A-level deadline. Nothing is submitted, so the material is about how to choose, what's compulsory, and the form and deadline.
   - *Change window*: choices are submitted, but changes are still allowed. The material is about who to ask, whether there's space, and the cut-off.
   - *After the cut-off*: changes are exceptional only. The material is about who decides and what counts as exceptional, without promising anything.

2. **Processes · Exams**
   - *Before entries close*: entries, tiers and access arrangements still being set up. The material covers entry deadlines and the SENCO/Exams Officer process.
   - *Exam season*: exams under way. The material covers what to do if ill on the day, special consideration, and exam rules.
   - *After results*: the material covers resits, reviews of marking and post-results deadlines.

3. **Processes · Absence & leave**
   - *Unplanned absence*: illness or an emergency, today. The material covers the same-day reporting steps and evidence for long absences.
   - *Planned absence*: an appointment or a term-time leave request, in advance. The material covers the request form, that the headteacher decides, and that approval is only in exceptional circumstances (never implied).
   (You said illness has no stages. These two are a split by *situation*, not a timeline. Reject it if it still feels forced.)

4. **Processes · Joining the school**
   - *Applying*: no place yet. The material covers the Year 7 or Sixth Form application route and in-year transfers (possibly via the council, [TBD]).
   - *Just joined*: a place is confirmed or the student has started. The material covers first-week practicalities (uniform, IT account, who your tutor is, where things are).
