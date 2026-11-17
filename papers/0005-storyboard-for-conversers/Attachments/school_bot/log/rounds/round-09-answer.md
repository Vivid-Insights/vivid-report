# Round 9: builder's answer (verbatim)

## F1 + F2
The pipeline and all seven flows are approved. One addition: the safeguarding risk check (step 1) runs on **every** message, including follow-ups inside an area. The pipeline shows that, but please state it explicitly in flow 2 as well.

**Q-F1a:** (b). Answer the original question normally, but add one short line repeating the contacts, e.g. "And remember, your tutor, Head of Year or Childline (0800 1111) are there if you want to talk." Do this once only. The bot doesn't bring the concern up again or ask about it (decided now). In the absence example, the normal answer for a Year 7–11 student is still that a parent/carer reports it.

**Q-F1b:** approved, with one addition. If the owning office is itself [TBD], fall back to "Please check with Reception." It must never fall back to a guess (decided now).

## F3
- **Rows 1–4, 7–13:** approved. Row 1's wording is still subject to DSL approval, as agreed in C1.
- **Row 5:** change it. "If you're well enough to sit it, tell the Exams Officer before you start" is an invented procedure, and it edges towards nudging an ill student into an exam. Replace that sentence with "[TBD: the Exams Officer's procedure if a candidate is unwell on the day]". Keep "tell the Exams Officer today", the special consideration explanation and "a parent/carer reports the absence".
- **Row 6:** approved, but mention NHS 111 / GP only if the parent asks something medical, e.g. "should I keep her off?" A plain absence report shouldn't get medical signposting tacked on.
- **Add row 14:** RedirectOutOfScope (records), "whats my attendance this year": can't see records; students ask their tutor/Head of Year, parents check the parent app or contact Reception [TBD: number].
- **Add row 15:** RedirectOutOfScope (schoolwork), "can you write my history essay": can't do homework or coursework; homework club [TBD: confirm it exists], library, ask your teacher.
- **Add row 16:** Subject choices / Change window (Sixth Form), "im in year 12 and want to drop further maths, how": Sixth Form Office / Head of Sixth Form, depends on space and timetable, minimum subjects [TBD], cut-off [TBD], careers adviser if it affects university plans.
