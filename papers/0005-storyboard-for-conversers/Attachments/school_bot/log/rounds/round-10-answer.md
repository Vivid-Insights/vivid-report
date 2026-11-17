# Round 10: builder's answer (verbatim)

## TC1
- **Demo A:** approved.
- **Demo B:** approved, with one change to the last line. Replace "contact the office that handles leave requests" with "contact [the office that handles leave requests, TBD]". It should name the office once the school confirms which one.
- **Demo C:** change turn 3. "Not personal details" sounds as if the SENCO's name is a secret. Replace it with: "You can contact the SENCO through [contact route]. [SENCO's name, if the school confirms it can be shared]." Named role holders are fine if the school publishes them. Personal emails and phone numbers are never given (decided now).
- Payload example: fine as long as it's labelled illustrative.

## TC2
Mostly approved. Changes:
- Remove "(fictional)" from the bot's own prompt. The bot should just be Ask Ashbourne. The fictional note belongs in the storyboard, not in character.
- Add to Rules: "Don't state national or exam-board rules unless they're in the school information you're given." (CONSTRAINT-7)
- Add to Rules: "Don't recommend which subjects someone should choose. Point them to their tutor, teachers and the careers adviser."
- Mark the safeguarding reply text as "draft, pending DSL approval" in the storyboard. It's fine to use in the sandbox.

## TC3
Choice: Anthropic (Claude) (decided now)
Either is fine according to my brief. This is just the sandbox default.

## TC4
Customise. Add one sentence at the end: "Please don't type real names or personal information into this preview." Keep the rest.

## D1
No. I don't have an exported folder or database to share. The policies and calendar are on the school website, but I have no path to give you. Please list the planned reference files as you describe. The school will fill them in, and each area's sign-off owner checks theirs.

## T1
Choice: No
There's no scoring or thresholds. It doesn't use attendance percentages or anything like that, since it can't see records anyway.

## P1
None to list from the project. The bot will sit on the school website and should link out to the website's policies page and calendar page [TBD: URLs]. The parent app is separate, and the bot only mentions it.

## P2
Choice: No sign-in — fully open
There's no login integration in v1, and the bot never sees records anyway.

## P4
Choice: Text with suggestion chips
One rule (decided now): no chips after a safeguarding response, and chips never suggest sensitive topics. They're only for process follow-ups such as "What if I miss the deadline?"

## P5
Yes. Keep it short: what it can and can't do, a few example questions, safeguarding contacts, and a privacy note (privacy wording [TBD: Data Protection Officer]).
