ROUND 5: area shape (AF1) and out-of-scope redirects (O9)

Your edits to O7 and your scope sort are applied. The generator will treat the six questions you added as in scope.

## AF1: functions or areas?
Picklist with previews. Do these in-scope topics work better grouped as **functions** or as **areas**?
- A **function** is one request mapped to one action or lookup, answered in one turn.
- An **area** is a topic the conversation stays in over several turns. It's split into **stages** (situations that need different material) and **facets** (the sub-questions it can answer). Within an area, the LLM picks the right material for where the student is.

**The generator suggests option 3 (Mixed), and here is why.** O1 says the main job is explaining processes step by step, and O8 shows the right answer for processes depends on *when* you ask: before a deadline, inside a change window, or after the cut-off. That fits areas. Other items, like library hours, who the DSL is or resetting a password, are one-turn lookups. That fits functions. O2 ("GPT alone") means a model is available to make the judgment calls an area needs.

Below, each option shows the same three in-scope items written out in that shape.

Option 1: "Areas — conversations linger on a topic across several turns"
```
AREA: Processes
  Stages:
    · Before the deadline         (choosing; nothing submitted yet)
    · Inside the change window    (submitted; changes still allowed)
    · After the cut-off           (changes only in exceptional cases)
  Facets:
    · How do I choose my GCSE options?      → Before the deadline
    · Can I drop/change an A-level?         → Inside the change window, After the cut-off
AREA: Resources
  Facets:
    · Is the library open after school?     (no stages)
```

Option 2: "Functions — each request maps to one discrete action or lookup"
```
"When's the GCSE options deadline?"   → ExplainOptionsProcess  (WORDALISE)
"Can I drop one of my A-levels?"      → ExplainSubjectChange   (WORDALISE)
"Is the library open after school?"   → GetOpeningHours        (WORDALISE)
```

Option 3: "Mixed — some topics are areas, others are quick lookups"
```
AREA: Processes   (options, changing/dropping subjects, ...)
  Stages: Before the deadline · Inside the change window · After the cut-off
  Facets: How do I choose my GCSE options? → Before the deadline
          Can I drop/change an A-level?    → Inside the change window, After the cut-off
FUNCTION:
  "Is the library open after school?"  → GetOpeningHours  (WORDALISE)
```

## O9: out-of-scope categories and their redirects
Your three OUT items group into three categories. Each one gets its own plain-language redirect. A fourth, catch-all message covers anything else (small talk, unrelated topics), and is the same fixed message every time. Approve or edit each one.

A. **Personal records** (grades, attendance, behaviour, timetables)
   Redirect: "I can't see anyone's grades, attendance or behaviour records. I don't have access to them. Students: ask your tutor or Head of Year. Parents and carers: check the parent app or contact Reception on [TBD: number]."

B. **Doing schoolwork for them** (homework, coursework, answers)
   Redirect: "I can't do homework or coursework for you, but I can point you to help: homework club [TBD: when/where], the library, or asking your teacher to go over it again."

C. **Acting on someone's behalf** (emailing staff, submitting forms, booking or changing anything)
   Redirect: "I can't contact staff, submit forms or book anything for you. I can tell you exactly how to do it yourself." (It then gives the steps for that specific case.)

Catch-all (fixed): "I'm Ask Ashbourne. I can help with school processes (like options, absences and exams), school rules, and where to find help in school. I can't help with that one. Try asking me something about school, or contact Reception on [TBD: number]."
