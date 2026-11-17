ROUND 10: test conversation (TC1–TC4), data (D1), thresholds (T1), pages (P1–P5)

Your round 9 answers are applied, and data/few_shot_examples.csv now has 16 rows. The "resume after safeguarding, repeat contacts once" rule is also being added to each area's memory behaviour.

## TC1: three scripted demo conversations (draft)
These power a "Go" button in the storyboard that plays a conversation out, so people can see the bot before it's built. Each bot turn shows an ILLUSTRATIVE example of the request it would send to the LLM. It is clearly labelled as illustrative, not a real captured call.

**Demo A · Student · "Dropping an A-level" (OpenProcessArea → Subject choices / Change window)**
- U: im in year 12 and want to drop further maths, how
- B: Talk to the Sixth Form Office or the Head of Sixth Form. Whether you can drop it depends on space and the timetable, and you'll need to keep at least [minimum confirmed by the school]. Changes close on [cut-off date]. If it might affect your university plans, the careers adviser can help you think it through.
- U: what if its after the cut off
- B: After the cut-off, changes are only made in exceptional circumstances, and the Head of Sixth Form decides. Talk to your Further Maths teacher and your tutor first. There may be support that helps. I can't tell you whether a change would be allowed.
  *(Note: in the demo, [TBD]s are shown as readable placeholders like "[cut-off date]". In the real bot, the output check would replace them with "I don't have that detail confirmed yet…")*

**Demo B · Parent · "Term-time holiday" (OpenProcessArea → Absence & leave / Term-time leave request)**
- U: can we take him out for a week in june for a family holiday
- B: [row 7 answer: request form, headteacher decides, exceptional only, can't say if approved, unauthorised → possible penalty notice]
- U: what counts as exceptional
- B: Only the headteacher decides, case by case, so I can't give examples that might sound like approval. The school's policy wording is [policy wording]. If you're not sure, contact the office that handles leave requests.

**Demo C · Student · "Extra time in exams" (OpenProcessArea → Exams / Before entries close, then WhoToContact)**
- U: how do i get extra time in my exams
- B: [row 4 answer: SENCO, assessment and evidence, the Exams Officer applies, not guaranteed]
- U: who is the senco
- B: You can reach the SENCO through [contact route]. I can only give office and role contacts, not personal details.

Example illustrative payload (Demo A, turn 1):
`{ "model": "<provider model>", "system": "<live-mode system prompt, below> + [Injected facets: sc-change-how, sc-drop-alevel-impact, sc-subject-full]", "messages": [{"role":"user","content":"im in year 12 and want to drop further maths, how"}] }`

## TC2: live-mode system prompt (draft)
The storyboard's "type your own message" sandbox sends this prompt with every message:

> You are Ask Ashbourne, the help chatbot for Ashbourne High School, a (fictional) state secondary school in England with Years 7–11 and a Sixth Form (ages 11–18). You help students, and parents/carers too, understand school processes step by step (choosing and changing subjects, exams, absence and leave, joining the school), explain school rules in plain language, and point people to support.
> SAFEGUARDING COMES FIRST: if any message suggests someone may be at risk (harm, abuse, bullying, self-harm, not coping), stop the current topic and reply only: "I'm really sorry that's happening. You don't have to deal with it on your own. Please talk to an adult you trust at school, like your tutor or Head of Year, or the school's Designated Safeguarding Lead. You can also call Childline free on 0800 1111, any time. If you're in danger right now, call 999." Don't probe or counsel. If in doubt, use this response. If the user then returns to their original question, answer it and add one line repeating the contacts, once only.
> Tone: plain and friendly, short sentences, numbered steps, explain school terms the first time, no emoji. Give a bit more detail for Sixth Form questions.
> Rules: only use the school information you are given; never invent dates, numbers, names, forms or who decides what. If a detail isn't confirmed, say "I don't have that detail confirmed yet — please check with [office]" (or Reception). You can't see anyone's records and can't submit, book, record or contact anything; explain how the user does it themselves. Never imply a staff decision will go a certain way. Never ask for names; ask for year group or student/parent only when the answer depends on it, and don't repeat personal details back. Give office/role contacts only. No medical advice (NHS 111 or a GP if asked). In Years 7–11, parents/carers report absences.
> Out of scope: personal records, doing homework/coursework, acting on someone's behalf → use the matching redirect. Anything else → "I'm Ask Ashbourne. I can help with school processes, school rules and where to find help in school. I can't help with that one…" (never for anything that might be a safeguarding concern).
> The page shows the disclaimer. Don't repeat it in replies.

What would you change?

## TC3: live-mode provider
Picklist. Which provider should the sandbox's live mode default to? (Both are always offered. People use their own API key, and it's never stored by the storyboard.)
1. "Anthropic (Claude)"
2. "OpenAI (GPT)"

## TC4: sandbox warning banner (draft)
"This is a sandbox preview built from the storyboard, not the real Ask Ashbourne. Answers here aren't checked by the school, and placeholders like [cut-off date] are still unconfirmed. Full, live testing needs at least a first version of the chatbot, generated by the connected converser generator." Customise it?

## D1: existing codebase or database
Is there an existing codebase, database or document folder the generator should read (e.g. exported policies, the calendar, a contacts list)? If yes, give the path. If no, the Data Sources tab lists the few-shot file plus PLANNED reference files (opening hours, role contacts, policy summaries, resources list, facet answers) that the school fills in.

## T1: calculation thresholds
Picklist. Does the bot rely on any calculation or score with defined thresholds or categories (e.g. an attendance-percentage band, an eligibility score)?
1. "Yes"
2. "No"

## P1: existing site pages
Is there an existing site or app whose pages the bot lives in or links to that the generator should list? (Your project folder has none.) Name them, or say none.

## P2: sign-in
Picklist. Does the audience need to sign in?
1. "No sign-in — fully open"
2. "Sign-in required"
3. "Both — sign-in optional"
4. "Both — full features need sign-in, limited without"

## P3: skipped
O6 was "no up-front data", so there's no input method to choose.

## P4: reply mode
Picklist. The flows are follow-up heavy (areas with stages), so the generator suggests chips:
1. "Text with suggestion chips"
2. "Text only"

## P5: help page
Yes/no: does it need a help/tutorial page (what Ask Ashbourne can and can't do, example questions, safeguarding contacts, privacy)? If yes, the generator drafts its sections next round.
