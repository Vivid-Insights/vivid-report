# Review

No Vivid Insights report is published until the Vivid Insights team has reviewed it. This file says how that works: who reviews, what they check, how an approval is given, and what stops a report being published without one.

## The rule

A report is published only in the exact form its reviewers approved.

Every version of a report has a content hash, computed from `Report.md`, `references.yaml` and every file the page shows or quotes — figures, videos, interactives, saved outputs. A reviewer approves one hash. Change a comma, regenerate a figure or update a quoted output, and the hash changes, the approval no longer applies, and the report goes back to its reviewers. `tools/publish.py` checks this and refuses to publish anything else.

## Who

`review/reviewers.yml`, at the top of the workspace and shared by every paper, lists the team, each with an id, a name, the email address they commit with, and a role: `editor` or `reviewer`. It also sets the policy. By default:

- two approvals are needed,
- at least one of them from an editor,
- an author of the report cannot approve it.

The author chooses the reviewers with the editor when they request review. At least one should know the method well and one should not, since the report has to work for a reader who was not in the room.

## How a round works

Each paper keeps its own rounds in its folder: `papers/NNNN-slug/review/round-01/`, `round-02/`, and so on. The paths below are inside that folder. The commands act on the paper that is open as `Report.md`.

1. **The author requests review** after the read-through (step 8 of `instructions.md`). The report must pass the release check and be committed. `cd Code && uv run python tools/review.py request` freezes the version, opens `review/round-01/`, writes `request.md` with the hash, and builds a review copy in `build/<slug>-review-round-01/`, marked as a review copy with its hash in the banner. The author commits `review/` and sends the review copy to the reviewers — as the folder, through the pushed branch, or however the team prefers.
2. **The author does not change the report while it is being reviewed.**
3. **Each reviewer writes a review.** `cd Code && uv run python tools/review.py form <your-id>` creates `review/round-01/reviews/<your-id>.md` from the template. Fill it in and set `recommendation:` to `accept`, `minor`, `major` or `reject`. Commit it yourself.
4. **If any reviewer asks for changes**, the author revises the report, answers every point in `review/round-01/response.md`, commits, and requests round 2. Reviewers read the response and the revised version and write a new review in `round-02/`.
5. **When a reviewer is satisfied**, they recommend `accept` and approve: `cd Code && uv run python tools/review.py approve <your-id>`, in their own terminal. It shows the version, asks them to type the first eight characters of its hash, writes `review/round-NN/approvals/<your-id>.yml`, and tells them to commit it. They commit it themselves, with their own git identity.
6. **When the policy is met for the current version**, the author confirms the disclaimer and runs `tools/publish.py`. The published page carries a review record: who reviewed it, over how many rounds, when it was approved, and the approved hash.

`cd Code && uv run python tools/review.py status` shows where a report stands at any point, and why.

## What a reviewer checks

The review form lists these. A reviewer is not asked to rewrite the report; they are asked whether it is right, whether it can be followed, and whether Vivid Insights should put its name to it.

- **Structure and the three points.** Does the report have the standard structure (Abstract, Introduction, Methods, Results, Discussion)? Are its three points stated in the abstract, given background in the Introduction, and answered in the Discussion, in the same order? Does the Introduction review the area properly, with at least 20 works, including ones that disagree?
- **Claims.** Is every claim about the method true of the code? Is every number traceable to a saved output? Does the report claim anything its examples or evaluation do not show?
- **Generated text.** Is every output, prompt and conversation quoted from a file (the build checks the words; the reviewer checks the file is what the report says it is)? Are hand-written examples labelled? Are the model's errors reported, not hidden?
- **Normative choices.** Does the report say where a person made a choice — a threshold, a persona, a few-shot example, a comparison group — and what the alternatives were?
- **Evidence.** If the report says the method works, is there a stated procedure behind it, a sample size, and an honest statement of what it cannot show? If there is no evaluation, does the report say so?
- **Attribution and permission.** Are other people's methods credited? Is client or partner material published with permission? Is anything personal, confidential or licensed exposed?
- **References.** Do they say what the report says they say? Do the links resolve?
- **Writing.** Does it follow `WRITING.md` — plain, concrete first, no grading words, no sales language? Comment on what obscures the argument, not on phrasings you would have chosen.
- **The page.** Read the review copy, not the Markdown: figures readable in both themes, videos play, interactives work, the page works on a phone and in print preview.
- **Disclaimer.** It is present and says the report was written with agentic AI.

## What stops a report being published without review

Each layer is there for a different failure.

- **`publish.py` refuses** unless the current content hash has enough valid approvals. An approval is valid only if: the reviewer is in `reviewers.yml`; they are not an author; their written review in the same round recommends `accept`; it names the current hash; and the approval file was committed to git by the reviewer's own email address. An uncommitted approval, or one committed by someone else, does not count.
- **`review.py approve` will not run without a person at a terminal**, and checks the reviewer's git identity before it writes anything.
- **The agent may not write reviews or approvals.** `instructions.md` forbids it, and a hook in `.claude/settings.json` blocks the agent's file tools and shell commands from writing in `review/*/reviews/` or `review/*/approvals/`, or running `review.py form` or `review.py approve`.
- **Unreviewed pages say so.** Every page built without approval carries a "Draft · not reviewed" or "Review copy" banner and a `noindex` tag, in print as well as on screen.
- **Publishing is a commit to the site repository**, which a person makes. For a hard guarantee, protect the main branch of `Vivid-Insights/Vivid-Insights-Profile` on GitHub so that changes need a pull request approved by an editor; the review record in `review/` is then what that pull request is checked against.

These are guardrails for an honest team working with agents, not security against a determined person: anyone who can commit as a reviewer can forge an approval, which is why the branch protection on the site repository is the final gate.

## Changing the process

The review process is template-level. Change it with a `FRAMEWORK` message, as `instructions.md` describes, so that every report uses the same process. Changing `policy` in `reviewers.yml` for a single report needs an editor's agreement, recorded in that report's `Log`.
