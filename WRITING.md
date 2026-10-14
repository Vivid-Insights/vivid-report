# Writing the report

How the prose in `Report.md` is written, edited and checked. The rules are derived from David Sumpter's own writing and his corrections to drafts, and each comes with the sentence that produced it wherever that survives, because a rule without its before and after stops being usable a week later.

They are adapted from three places: the article rules in `communicating-individual-health risk/article/WRITING.md`, the house style in `agentic-ai-for-statistics-and-data-science/.claude/skills/writing-style/SKILL.md`, and the `Writing` section of `human-agentic-data-analysis/instructions.md`. `Code/tools/check.py` checks the part of this file a machine can check; the rest needs a reader.

## Which rule wins

1. **A correction an author has just made.** It outranks everything here. Write it into the corrections log at the end of this file in the same turn, with the sentence it came from, before and after.
2. **This file.**
3. **The three source files above**, for anything this file does not cover.

## Editing the report

**Only edit `Report.md` when an author asks for the edit in that turn.** Agreeing that a proposal is good, or saying "yes", is not the instruction to write it in. Wait for "add that", "make the edit", "do it". No step makes a section yours to write: you help the user write, and they decide (`Helping the User Write` in `instructions.md`).

**When someone asks for a change, make that change and nothing else.** The failure has a shape: it starts from a real defect, such as a number that is now wrong, and instead of repairing it rewrites the surrounding prose so the repair sits comfortably. The result reads well, which is why it slips past. Reading well is not the test.

> "It takes me more time to formulate than you and it is my words which count." — David, 11 August 2026

- **Quote the sentence back before altering it**, when the change is more than a word.
- **If a correction seems to require rewriting a passage, the correction has probably been misunderstood.** Ask.
- **When a fact must be added and there is no clean slot, add a sentence** rather than reshaping the ones around it.
- **Read a short instruction narrowly.** "Get rid of the boxes" meant the three just added, and ten were deleted.
- **Never put a sentence in a co-author's section that they will read as their own.**

**Commit before editing.** Before an edit to `Report.md`, commit the current state, including any changes an author has made by hand, so each edit is a diff of its own. Push only when asked.

**When an author rewrites a passage by hand**: while they say they are working in the document, leave it alone. When they say `done`, compare with the last commit before their pass (`git diff`) and read the pass as a whole. Write the rules it implies into the corrections log, each with its before and after, stated as something checkable ("give the number before the qualification", not "write more clearly"). Say which were seen once and which recur, and ask about anything that might be an accident. Then apply them to the passages they did not rewrite.

**Leave the authors' typos alone and do not mention them.** A factual error — a wrong number, name or reference — is still raised.

## Voice

**First person plural.** "We built", "we found", "what we can say is". The report is an account of what people did.

**Plain and direct, to a reader who is an equal and not a specialist.** A coach, a clinician, a mentor and a developer may all read a Vivid report; none should need the others' jargon.

**Short to medium sentences, one idea each.** Split three clauses joined by "and … so" into two sentences. Paragraphs of two to five sentences; merge a one-sentence paragraph into its neighbour.

**Contractions are fine.** "so we can't say which direction the relationship runs".

**Prose, not bullet points**, in the body. A list is for something that is genuinely a list, such as the four prompt steps. The three points of the paper are stated in prose, in the `Abstract`.

**British spelling**: wordalisation, visualisation, behaviour, modelling, organisation, analyse. A quoted output keeps its own spelling.

## The concrete case comes first

Within a paragraph, and in the `Results`, open on the real example and let the general claim follow. The `Introduction` is the exception in its order of paragraphs, which build from the general to the specific; a paragraph within it can still open on a case. In a Vivid report the concrete cases are the player, patient or mentee, the text written about them, the configuration that changed it, and the specific mistake the model made.

> **Before (abstract):** Feature-specific thresholding over-emphasised the effects of categorical or low-variance features.
> **After (concrete first):** For an obese woman of 54 with normal blood pressure, the global scale says her body-mass index has no significant effect on its own; the feature-specific scale says it strongly increases her risk.

**Name a technical term once, gloss it in a clause, and do not let it return as an unglossed label.**

## What not to write

**No "not X, it's Y"**, in any costume: *not X but Y*, *isn't X — it's Y*, *not just X*, *less X than Y*. David: *"this is so AI sounding."* Say Y. Keep a negation only when a named person holds X and the report answers them.

> **Before:** Wordalisation isn't a replacement for the model — it's a way of communicating it.
> **After:** Wordalisation communicates what the model says.

**No reversal openers** that name the subject and announce it is not really the subject (*…is only half the story*, *…and that is the easy part*).

> **Before:** This is step one of the eight, and most of it is not about data at all.
> **After:** Most of step one is setting up how you and the agent will work.

**No throat-clearing.** Do not announce what a sentence will do and then do it. "The odds-ratio scale adds something the log-odds scale cannot" is a promise; the next sentence is the content. Keep the content.

**No figures of speech.**

> **Before:** The association is not simply the control variable wearing another name.
> **After:** The association holds even when the control variable is accounted for.

**No abstract gesturing.** Name the concrete thing: which configuration, which patient, what the text says, what is wrong with it.

> **Before:** Temporal precedence is not identification, though, and here it is weaker than it looks.
> **After:** A predictor built partly from later observations cannot establish which came first.

**No figurative shorthand for a model or a method.** "The mirror model" → "A further model."

**Do not state a measurement as though it were the definition.** "Productivity is measured as output per hour" → "One way of measuring productivity is output per hour."

**Say it once.** An idea in the introduction and again under its own heading has been given twice; cut the weaker version. No closing line that recaps the paragraph, no summarising flourish, no short sentence dropped in for emphasis (*"Nothing comes to rest there."* was deleted, and nothing was lost).

**No hedging pile-ups**, no "in today's rapidly evolving landscape", no jargon as shorthand for rigour, no sales language. A research report from Vivid is not a pitch for the method.

**Do not grade the evidence.** No *striking*, *reassuring*, *worrying*, *encouraging*, *impressive*, *remarkable*, *powerful*, *novel*. Give the magnitude and let the reader weigh it. What an analysis *can and cannot establish* is different, and belongs.

**The test for all of these: could a reader disagree with this sentence?** If not, it is decoration.

## Emphasis

**Nothing in the report body is bold.** Not a sentence, a phrase or a run-in heading. Bold makes the argument for the reader; the prose has to earn its emphasis through sentence order and word choice. The bold labels the build adds — *Figure 1.*, *Definition 1.* — are labels, not emphasis. `Appendix.md` and the working documents are scanned rather than read, and bold lead-ins are fine there.

## Honesty and grounding

**Every number, finding and quotation comes from a file in this workspace or a cited source.** `[CHECK: …]` or `[TO WRITE: …]` beats a plausible invention. The release build refuses to publish with either in place.

**Quote LLM output exactly, from the saved file**, in an `output`, `prompt` or `conversation` block. Never paraphrase an output and present it as what the model wrote. Hand-written examples are marked hand-written.

**Report the errors the model makes.** When an output contradicts its input, say so in the caption or the text.

> Three successive versions of a figure gave age the risk-age years that belong to body-mass index, until the synthetic text named the factor in each risk-age sentence. The paper says so.

**A model's estimate is not an observation.** A logistic regression gives the share with an outcome among people with the same measurements; it does not say what happened to the individual, and it is not causal. A converser's answer is what the converser said, not a fact about football.

**Do not overstate to sharpen a contrast.** *Nothing else*, *only*, *always*, *never* are usually both false and unnecessary.

**Say plainly when the evidence is thin**, such as a judge score from 20 texts or an evaluation not yet done.

**Other people's methods stay theirs.** The wordalisation stages and the LLM-as-a-judge and reconstruction evaluations are Caut and colleagues'; say so where they are used.

## Length

**Cut the length at the end.** Phase 6 of the drafting order is simplify and revise, and that is where a report gets shorter. Do not write short to begin with and then pad; write, then cut.

**Draft at about half the length that seems natural.** A methods section went from 782 to 319 words on David's instruction ("Half the length"), and a data paragraph to two sentences ("at most 2 sentences! One about data removed and observations removed and one about stepwise regression"). Keep only what the reader needs to follow the figure. Both corrections recur.

**Thorough is not long.** The `Methods` covers everything a reader needs to rebuild the method with the repository; it does that in short sentences, and the half-length rule still applies to each paragraph.

**Keep it the length asked for.** A summary is a sentence or two; three paragraphs means three.

## Terms used in this report

Use these consistently. If an author changes one, change it here in the same turn. This table belongs to the report, not the template: start it in step 3.

| Term | Meaning |
|---|---|
| wordalisation | the method, and one generated text ("a wordalisation"); British *-isation* throughout |
| normative model | the rules that turn numbers into words: thresholds, wording, comparisons |
| synthetic text | the rule-based text given to the LLM (Caut and colleagues' term) |
| converser | a domain-specific conversational agent built on the Vivid framework |
| normative choice | one decision in the normative model, such as where a threshold sits |

## Mechanics

- **One paragraph per line, no hard wraps**, with a blank line between paragraphs; diffs then show which paragraph changed.
- **`[TO WRITE: …]`** marks text still to write; **`[CHECK: …]`** marks something to verify. Never remove a `[CHECK]` without doing the check.
- **Captions say what the figure shows and how to read it**, not what it means.
- `FORMAT.md` has everything about the Markdown itself.

## Corrections log

New rules from the authors' corrections go here, newest first, each with the date, who made it, and the sentence before and after. Say whether it was seen once or recurs.

- **14 October 2026, David: the Discussion has no sub-headings.** "FRAMEWORK the discussion should not have subheaders." Before: the Discussion carried a `###` for each of the three points, then `### Limitations` and `### Looking ahead`, sharing the Methods and Results sub-headings. After: it runs as continuous prose, one paragraph per point in the order of the Methods, then the limitations, then looking ahead; each paragraph's subject is clear from its first sentence. The Methods and Results keep their shared sub-headings. `The Structure of a Report` in `instructions.md`. *Seen once.*

- **14 October 2026, David: store only what serves the writing.** "I am not in the least bit interested in small errors or bugs you picked up along the way. Take away any random extra documentation of this sort. It will confuse things later." Before: the Appendix logged a script's mistakes, a library's label mismatch and which services were dev, and the Results reported a software bug. After: bugs, set-up problems and debugging are left out of the Appendix, the `Log` and the report; errors in a model's quoted text are still reported. `Working Method` in `instructions.md`. *Seen once.*

- **13 October 2026, David: the six-phase drafting order.** From David's `Writing workflow` keynote. Sketch; sketch the abstract; revise; write the start and end together; revise the abstract; simplify and revise. The ten steps now sit inside these six phases, and the paragraph plans for the `Abstract` (seven moves), `Introduction` (five paragraphs) and `Discussion` (five paragraphs) come from the same deck. The three points are called A, B and C when planning, equal by default, with a weighted shape allowed where the material needs it. `The Six Phases and the Ten Steps` in `instructions.md`. *Seen once.*

- **13 October 2026, David: FRAMEWORK suspends the friction rules.** Told to make every block visible in Obsidian, the agent had already asked twice and was about to ask a third time whether to change the build. Before: a FRAMEWORK message answered with a proposal and a question. After: the prefix is the decision; carry the change out in full, including the tools, the templates and the specimen, and report what was done. `Changing This Contract` in `instructions.md`. *Seen once.*

- **13 October 2026, David: the friction is for the writing, not for the workspace.** Asked to make an `output` block render in Obsidian, the agent spent three turns asking which of several options was meant, quoting "the decisions are yours", and ended by offering a menu instead of a fix. Before: a formatting request answered with questions about what the user intended. After: work out the route and do it; ask only when the task would be destructive, would change shared tooling or the contract, or would alter what the report claims. `What the friction is for` in `instructions.md`. *Seen once.*

- **13 October 2026, David: every report has the same structure, built on three points.** Abstract, an optional What We Have Built, Introduction, Methods, Results, Discussion. The three points are found early, put in a drafted abstract that serves as the template, given one background paragraph each in an Introduction of four to six paragraphs citing at least 20 papers, covered in the same order in the Methods and Results, and answered in a Discussion of ideally five paragraphs (one per point, limitations, looking ahead) that links back to the Introduction's literature. Before: Introduction, Method, Examples, Evaluation, Discussion, Limitations, with the background written last. After: `The Structure of a Report` in `instructions.md`. Also: the agent helps the user write and the user decides; the agent adds text when asked, never by default. *Seen once.*

The entries below were carried over from the health-risk article, where they were made, because they are about how David writes rather than about that article.

- **6 October 2026, David: keep sections short.** "Half the length of An example application." The section went from 782 to 319 words. *Recurs*: draft at about half the length that seems natural.
- **6 October 2026, David: an out-of-range value is stated as a bound.** Before: "equivalent to that of a 65 year old" (clipped). After: "equivalent to that of someone older than 65, the oldest age in the data". Say what the model was fitted to rather than giving a number it cannot support.
- **5 October 2026, David: unfinished sections carry a visible warning.** A section kept as notes opens with "[TO WRITE: …]". *Seen once.*
- **5 October 2026, David: "normative choices", not "decision axes".** Before: "We identified four key decision axes". After: "We identified four key normative choices". *Recurs.*
- **5 October 2026, David: describe a method in its authors' terms and order.** "Rewrite this paragraph using the original wordalisation paper as reference. Six sentences, one about each stage, and refer to the figure." *Seen once.*
- **5 October 2026, David: "interpretation", not "understanding".** Before: "can vastly change understanding of what is conveyed". After: "can vastly change interpretation of what is conveyed". *Seen once.*
- **3 October 2026, David: no reversal openers.** See `What not to write`.
- **1 August 2026, David: no "not X, it's Y".** "This is so AI sounding." See `What not to write`.
