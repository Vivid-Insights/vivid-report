# Instruction given to the build agent (verbatim)

Spawned 2026-11-09 with the Agent tool: `subagent_type: general-purpose`, model inherited (Claude Opus 5.5).
It is a fresh agent with no memory of the storyboard session.

---

You are a coding agent building version 1 of a chatbot from a storyboard. The storyboard is your
specification. Work only from it, so that we can see what a storyboard alone is enough to build.

INPUTS: you may read ONLY these files:
- K:\Vivid\school_bot\storyboard.json  (the specification: read all of it)
- K:\Vivid\school_bot\data\few_shot_examples.csv  (referenced by the storyboard's dataSources)
Do NOT read K:\Vivid\school_bot\storyboard.html (the same data, rendered), anything in
K:\Vivid\school_bot\log\, K:\Vivid\school_bot\CLAUDE.md, .storyboard-config.json, or anything
under K:\Vivid\Afya\. They describe how the storyboard was made, not what to build.

OUTPUT: build the chatbot in K:\Vivid\school_bot\app\ (create it). Don't modify anything outside
app\.

TECHNICAL CONSTRAINTS
- Python 3.12, standard library only (http.server, json, urllib, etc.). pytest is installed for tests.
  Do not pip install anything.
- A small local web server that serves a chat page and a JSON chat endpoint.
- If the environment variable ANTHROPIC_API_KEY is set, call the Anthropic Messages API over HTTPS
  with urllib to generate replies. If it isn't set, run in an OFFLINE mode that still works end to end
  (e.g. answers composed from the storyboard's facet answers and fixed texts), so it can be tested
  without a key. Never hard-code a key.
- Implement as much of the storyboard as you can: personas/tone, capabilities and flows, the areas
  with stages and facets, scope and redirects, constraints, the disclaimer, and the page settings and
  pages. Put the storyboard's content in data files under app\, not buried in code, where sensible.
- Turn the storyboard's planned tests into runnable pytest tests where possible (app\tests\), and run
  them. Report honestly which pass and which fail.

THE MOST IMPORTANT PART: BUILD_NOTES.md
Write app\BUILD_NOTES.md as you go. For every point where the storyboard didn't tell you what you
needed, record:
- what you needed to know,
- where the storyboard was silent, ambiguous or contradictory (cite the JSON path, e.g.
  overview.constraints[0] or areas[2].stages),
- what you guessed or decided, and
- the risk if your guess is wrong.
Also list anything in the storyboard you could NOT implement, and why. Be candid. A missing or
ambiguous spec is the finding we're looking for, not a failure on your part. Don't paper over gaps
by inventing school facts: [TBD] items must stay unconfirmed in the bot's behaviour.

FINAL REPLY: summarise what you built (files and how to run it), the test results (pass/fail
counts with the command you ran), and the 5 most significant guesses or gaps from BUILD_NOTES.md.
