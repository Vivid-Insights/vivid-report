# Round 1: builder's answer (verbatim)

## REVIEW-MODE
Choice: Inline in the chat
I'd rather not keep switching between files and the chat. Pasting the drafts here is easier, and I can reply with the changes.

## O1
It's a help chatbot for the Ashbourne High School website, a state secondary school in England with Years 7–11 (ages 11–16) and a Sixth Form (Years 12–13, ages 16–18). Students can ask it the questions that Reception, the Heads of Year and the Sixth Form Office answer over and over. Parents and carers will probably use it too, but I haven't decided whether to support them in version 1.

Its main job is to explain school processes step by step: who to contact, which form to use and what the deadline is. That covers things like:
- choosing GCSE options or A-level subjects
- changing or dropping a subject
- reporting an absence or asking for term-time leave
- exam entries, resits and access arrangements
- joining the school or transferring in mid-year

It should also point students to resources (revision help, the library, counselling, the IT Helpdesk) and explain school rules in plain language, such as phones, uniform, late arrival and homework.

Hard limits:
- It can't see any individual student's records (grades, attendance, behaviour), and there's no login.
- It must never pretend to submit a form, book something or contact staff for anyone. It tells people how to do it themselves.
- Safeguarding: if a student says anything suggesting they're at risk, it doesn't try to counsel them. It directs them to a trusted adult or the school's Designated Safeguarding Lead, and to 999 or Childline if they're in immediate danger.

It'll run on a hosted LLM (Claude or GPT). We have a small budget and no in-house developers. I don't have this year's exact deadlines yet, so those need to be placeholders the school can fill in.
