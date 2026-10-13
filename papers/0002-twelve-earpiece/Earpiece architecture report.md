# The choose-your-own-adventure architecture of Twelve Earpiece: a report from the code

A working report for the authors of paper 0002, written before the paper is revised. It describes how Earpiece's conversational architecture works, as the code shows it on 12 October 2026, and compares that with the course notes the first draft was written from. It ends with what the paper should and should not say.

Not for publication. It quotes Twelve's private code and internal diagnosis notes.

## Sources

| Source | Version | What it gave |
| --- | --- | --- |
| `twelvefootball/twelve-earpiece-api` | `dev`, commit `ff2349b4` (9 October 2026), pulled for this report | The architecture itself. All code references below are to `src/` in this repository unless stated. |
| `twelvefootball/twelve-earpiece-api/CONCEPTS.md` | same | The developers' own overview. Useful, but partly out of date (see "The course notes and CONCEPTS.md against the code"). |
| `twelvefootball/twelve-workspace` | `main`, commit `6fe657d` (8 October 2026) | The platform map (`.claude/instructions/baseline.instructions.md`) and the record of how Earpiece chat fails in production (`.claude/skills/earpiece-chat-problems/`). |
| `twelvefootball/twelve-sql` | tag `2.0.3`, the version Earpiece pins (`requirements.txt:44`), read on GitHub | The name search. |
| Course notes, section 6 of `context-engineering` | commit `dc7c387`; screenshots from June–July 2025 | What the first draft said. |

The core (the analyst base class, functions, redirects, the receptionist, the chat client and the redirect handler) was read in full for this report. Three narrower questions were traced by search agents with file and line references: name resolution, the inventory of analysts and functions, and how open questions and the match summary are produced. The claims the paper is likely to rest on were then checked by hand against the code: the search weights and threshold, the "do not guess" instruction, the Scout's function count, the temperatures, the goal sorting and the shuffling of examples.

## The architecture in one paragraph

Earpiece is a set of twelve analysts. An analyst is a system prompt, a context (what the conversation is about, as database identifiers) and a list of tools. A user always starts with the receptionist, whose tools are mostly redirects: functions that, when the model calls them, resolve the names in the user's request to identifiers and open a new chat with another analyst in that context. Analysts redirect back to the receptionist when the user changes subject, and directly to each other when the subject stays the same: a question about the same player's transfer goes straight from the Scout to the Transfer analyst. Most of what the user reads is written by description functions, which are wordalisations: the code turns data into a synthetic text, and a separate LLM call writes the reply from it, streamed straight to the user. Every model call is stateless; the conversation exists because each chat's messages are stored and sent again on every turn.

## Analysts

An analyst is a Python class with four parts (`analysts/base/analyst.py:33-131`), which map directly onto a chat-completion request:

| Part | Becomes |
| --- | --- |
| `instructions` | the system message, after "Today's date is … and you have access to data up until this date." (`services/chat_integration/chat_client.py:406-415`) |
| `describe_selection()` | appended to the system message: the current context in words |
| `functions` | the `tools` array, each with a strict JSON schema (`analysts/base/chat_function.py:146-163`) |
| `initial_function_calls` | tool calls made before the user says anything — but no analyst uses this: every one returns `[]` |

Each analyst also declares the Auth0 permissions that grant access to it (`analyst.py:72-77`) and a model, which comes from configuration (`llm_model = config.llm.default`, `analyst.py:65`), not from the code.

### The twelve analysts

Counts are of the functions an analyst can offer the model. "Base" is what every user gets; "max" is what a user with every permission gets. Talent Discovery and Search are alternatives, so the maximum counts one of them.

| Analyst | Context | Functions, base | Functions, max | Redirects to |
| --- | --- | --- | --- | --- |
| Receptionist | none | 3 | 12 | every analyst the user may use (up to 9) |
| Scout | player, competition, season | 18 | 24 | receptionist, itself, Transfer, Comparison, Team Fit, Talent Discovery or Search, Complex Player Questions |
| Comparison | two players or two seasons | 8 | 12 | receptionist, itself, Scout, Transfer, Team Fit, Talent Discovery or Search |
| Transfer | player and target league | 8 | 12 | as Comparison |
| Team Fit | player and target team | 10 | 14 | as Comparison |
| Talent Discovery | search criteria over leagues | 6 | 10 | receptionist, itself, Scout, Comparison, Transfer, Team Fit |
| Search | search criteria in one league | 7 | 11 | as Talent Discovery |
| Match Analyst | one match, one side | 15 | 16 | receptionist, itself, Match Scout |
| Match Scout | one player in one match | 7 | 8 | receptionist, itself, Match Analyst |
| Season Analyst | team, competition, season | 14 | 14 | receptionist, itself |
| Opposition Analyst | team, selected matches, optional "hero team" | 11 | 11 | receptionist, itself |
| Complex Player Questions | player, competition, season | 0 own; tools come from Twelve's MCP server | — | none |

Sources: each analyst's `functions` property; inventory traced by agent and the Scout recounted by hand (26 entries in `analysts/player/scout/analyst.py:239-509`, of which `FindSimilarPlayers` appears twice in exclusive branches and one of Talent Discovery and Search is offered, giving 24).

Three things follow. Most analysts offer between 8 and 16 functions, so "about ten functions per analyst" in the course notes is a fair round number but not a rule. The Scout, for a user with every permission, offers 24, above the 20 that OpenAI suggests as a soft limit. And every analyst except the receptionist and Complex Player Questions includes a redirect to itself, used when the user changes player, match or team without changing the kind of question.

### Analyst groups

Analysts are filed into eight groups (`schemas/types.py:36-73`), for instance Scout, Transfer, Comparison and Team Fit in `PLAYER_SCOUT`. A group does not limit which analysts can be reached. It only decides how a redirect is filed: from the receptionist the current conversation is relabelled with the new group; into a different group a new conversation is opened; within a group a new chat is added to the same conversation (`service/message_stream_handler.py:473-497`).

## Functions and where their results go

Every function declares a destination (`chat_function.py:17-32`):

- TO_ASSISTANT: the result goes back to the model as a tool message and the model writes the reply. Used for the three general functions every analyst has — explain how the platform works (from the knowledge API), which leagues are covered, and a team's fixtures — and for finding similar players.
- TO_USER: the function writes the reply itself and streams it straight to the user, bypassing the conversational model. These are the descriptions (`analysts/base/description.py:113-136`), plus the save-report functions and Talent Discovery's ranked list.
- REDIRECT: the result is a hand-over to another analyst (next section).

### Descriptions are wordalisations

A description implements the wordalisation method of paper 0001 directly:

- `synthesize_text()` turns the data into a synthetic text (the "normative model");
- `describe_files()` names knowledge-API files of question–answer pairs that explain the domain ("tell it what it knows");
- `example_files()` names files of few-shot examples ("tell it how to answer");
- `generate()` sends instructions, the pairs and the synthetic text to a separate LLM call and streams the answer (`description.py:626-790`).

The description call uses its own configured model (`config.llm.description_function`) at temperature 1.0 (`description.py:785-790`), while the conversational loop runs at 0.2 (`chat_client.py:727-729`). Few-shot pairs are not chosen by similarity to the question: the whole file is fetched, shuffled at random (`utils/preprompts/preprompts_utils.py:34`), and trimmed to a token budget of 20 000 (`description.py:135`), half for the domain pairs and half for the examples. In conversations not in English, player, team and competition names are replaced by placeholders before generation and restored afterwards, so the model cannot alter them (`description.py:549-602`).

Analysts typically have one summary description that the instructions say to call first — for the Scout, `short_description` when the user has "ONLY given the name of a player" (`analysts/player/scout/analyst.py:66`) — and a set of descriptions of single qualities, areas of the pitch or developments over time.

### Answering open questions

Each analyst has one function for free-text questions (for example `AnswerMatchQuestions`, `analysts/match/analysis/describe_match_questions.py`). These are also descriptions. Their synthetic text is a document assembled for the question:

1. The question is matched by embedding search against a file of example questions labelled with the quality they concern (`knowledge_client.search_pairs`, up to 5 hits within distance 0.7, `describe_match_questions.py:196-216`), which picks the qualities to describe.
2. The data for those qualities is fetched, and for each quality the document gets explanatory passages from the knowledge API (again by embedding search, up to 3 hits) followed by the synthetic sentence for that quality.
3. Background such as the match's line-ups and goalscorers is appended, and the document ends with an instruction ("Answer this query in no more than three sentences …").

Embedding search is not done in Earpiece; it is a call to the knowledge API (`services/knowledge_integration/knowledge_client.py:101-128`), and the embedding model is chosen there, so it cannot be named from this code. None of the four "answer" functions uses few-shot examples.

### A second router inside one analyst

Complex Player Questions, reachable only from the Scout, works differently (`analysts/complex_player_questions/`). A classifier call at temperature 0 sorts the question into one of eight types (stats, form, season comparison, positional, international, availability, opposition, none of the above; `routing.py:14-102`). A research phase then calls tools on Twelve's MCP server with a guardrail for that type, and a writing phase formats the findings, with few-shot examples this time chosen by embedding similarity (`chat_client.py:495-654`). The code itself notes "Form-question tool routing is still inconsistent in tests" (`complex_player_questions/analyst.py:26-27`). It is the same idea one level down — choose a narrow path first, then answer within it — but it is new, and probably too much for a short paper.

## Moving between analysts

### The receptionist

The receptionist (`analysts/receptionist/analyst.py`) has two modes. On first contact its job is "ask the user what they are interested in analysing and then pass on that information to the appropriate analyst" (line 87). When another analyst hands back, it receives a summary of the conversation and the user's last message, and the instructions quoted in the first draft, with one line added since the course notes: "Prioritise calling the appropriate analyst directly (option 1) over the other two options." (lines 76-83).

Its functions are the three general ones plus one redirect per analyst the user is allowed to use, at most twelve. Most of its prompt (lines 165-352) draws the boundaries between analysts: Match Analyst is for teams and Match Scout for players; one match goes to the Match Analyst, several matches against an opponent to the Opposition Analyst, a whole season to the Season Analyst; Compare Players handles exactly two players or two seasons, and anything over more than two seasons goes to the Scout. The more analysts there are, the more of these boundaries the receptionist has to be told about.

### Redirect functions

A redirect function (`analysts/base/redirect.py`) is generated from its target analyst:

- its name is `redirect_to_<analyst>` (line 114);
- its description is the target analyst's own `description`, so the text an analyst uses to describe itself is what the receptionist routes by (lines 116-122);
- its parameters are the JSON schema of a natural-language context model (`schemas/nlc/`), which asks the model for names: a player name, a team name, a competition and country, a season (lines 124-137).

Where the set of possible values is small, the schema enumerates it: the workspace's positions and qualities are injected as `enum` values (lines 139-177). Where it is large — players, teams, matches — the model gives a string and the name is resolved afterwards. When the model's arguments do not fit the schema, it is told which field was wrong and asked to call again; after two failures it is told to stop and ask the user to rephrase (lines 284-296).

### Who may go where

Access is enforced twice. An analyst only adds a redirect function if the user holds that analyst's permission (for example `receptionist/analyst.py:417-541`), so the model is never offered an analyst the user has not bought; the receptionist's instructions describe the missing ones as available from Twelve (hello@twelve.football). And when a chat with an analyst is started, the handler checks the permission again and refuses if it is missing (`service/message_stream_handler.py:187-192`).

WhatsApp users are recognised by their account's email address (`analysts/utils.py:121-137`). They reach the same analysts as other users, limited by their permissions, except that Search (one league at a time) replaces Talent Discovery.

### A hand-over

When a redirect succeeds, its tool message carries the target analyst and the resolved context (`redirect.py:369-374`). The handler creates a new chat with that context and continues the same request in it (`message_stream_handler.py:416-518`). The new chat's first user message is stored empty; the request that caused the redirect is passed to the model alongside (`handoff_query`), so the new analyst reads the real question.

Three rules keep the chain finite. A request may be handed on at most five times (`MAX_REDIRECT_HOPS = 5`, line 117). A hand-over to an analyst and context already handed to in the same request ends the chain, because a newly seeded chat reads only its instructions and context and would make the same choice forever (lines 442-448). And the last analyst in a chain is offered no redirects and told: "This request has already been passed between analysts and cannot be passed on again … Answer as much of the question as you can with the functions you have." (`chat_client.py:52-60`, `401-402`). On the turn a redirect seeds, the new analyst is also not offered a redirect back to itself, since the query it carries has already been resolved to its context (`chat_client.py:403-404`).

## Resolving names

The step the course notes describe as "fuzzy search" is a full-text search in Twelve's database followed by a second LLM call (`schemas/nlc/utils.py`; search in `twelve-sql` 2.0.3).

1. The model's string is cleaned of accents and split into overlapping three-letter fragments, and a BM25 full-text search over indexes of player names and their fragments returns up to 20 candidates (`utils.py:765-779`; `data_api/queries/wyscout/search/players_search.sql` in `twelve-sql` 2.0.3).
2. Candidates are scored as 0.50 × name match + 0.35 × fragment match + 0.15 × market value, the last capped at €100 million, so better-known players rank higher; those scoring 0.5 or less are dropped (`utils.py:773-782`; `players_search.sql:65, 88-92`).
3. If none are left, the search is repeated without the team, then without the competition, before giving up (`utils.py:785-829`).
4. The candidates are written out as sentences ("… (player id …) played for … in …") and a second LLM call, given the user's original words, chooses one and returns it as JSON. It is told: "If you cannot confidently determine a match, do not guess. Please state that and return an empty JSON object" (`utils.py:43-196`, `720-739`).
5. If nothing is chosen, the redirect fails and the model is told "Selection failed due to the following: … Ask the user for missing/incorrect information." (`redirect.py:337-348`).

Teams are resolved the same way but take two choosing calls, one for the team and one for its competition and season (`utils.py:1199-1340`). Matches are searched by both team names, and the focal side is picked by fuzzy string matching (`utils.py:986-1154`). Analysts that keep the same player — Transfer, Team Fit, Comparison — reuse the identifiers already in the context instead of resolving them again (`player_transfer_context.py:49-83`). Nothing in the code or its comments says how many players the database holds, so the course's "around a hundred thousand" cannot be confirmed from it.

Every resolution is counted in telemetry as an attempted, successful or failed player search (`redirect.py:325, 342, 367`). Those counts, in Application Insights, are the nearest thing to an evaluation of this step that already exists.

## Context and state

The resolved context is stored as JSON on the chat (`Chat.context`), shown to the user in the side pane, written into the analyst's system message by `describe_selection()`, and used by every function to fetch data. The model never sees a database query; it sees the context in words and the functions it may call.

The model providers keep no state. Each turn sends the chat's whole stored history again (`chat_client.py:692-729`). The platform is now provider-agnostic: models are named in configuration by task — conversation, descriptions, disambiguation, classification, translation and others — and can come from OpenAI, Azure OpenAI, Anthropic, Google or xAI (`config/llm_config.py`). No model name appears in the code.

## What goes wrong

The workspace's diagnosis notes (`earpiece-chat-problems`, from incidents on 10–14 September 2026) are the best evidence of how this architecture fails in use. The ones that bear on the design:

- One rule governs hand-overs: "The resolution that creates a chat is authoritative for that chat." When a seeded chat resolved the same query again, the side pane and the chat text named different players. The guards above (no self-redirect on a seeded turn, ending repeated hand-overs) were added for this, and are in the code pulled for this report, although the notes still describe them as unmerged.
- Name resolution is not repeatable. The disambiguation call sets no temperature, so it runs at the provider's default, and one query resolved to nothing, then to one player, then to a third across three attempts. Another ignored the gender, birth date and competition the user gave. The reply is parsed by splitting on colons rather than as JSON (`utils.py:541-584`).
- "Prompt instructions lose to other prompt instructions": an appended "do not redirect" lost to the Scout's "Always call redirect_to_scout". The notes' conclusion — "Withhold the tool; do not argue with the model" — is the principle behind both the access control and the chain guards.
- Because each turn re-sends the whole history, a message stored wrongly once breaks that chat on every later turn.

Smaller things found while reading, for the Twelve team rather than the paper:

- The receptionist's prompt lists "the following 6 actions" and then says "If you can't do one of these five actions"; one address is written `hello@twelve.footall` (receptionist line 310; Scout line 103).
- A WhatsApp user with Talent Discovery but not Search is offered `redirect_to_search` and then refused when the Search analyst starts, since Search requires its own permission; a user with only the Search permission is never offered a redirect to it.
- `AmbiguousContextError` is caught but never raised.
- In `answer_comparison_question.py:64-68` the role sentence is assigned and then overwritten, so it is never sent.
- The match summary's score line comes from the results table and its list of goals from shot events, and nothing checks that they agree. This explains the course's example: "Internazionale scored 3 goals" under a 4–0 score line. The goals listed in descending order there (56, 47 and 10 minutes) match the code before 3 December 2025 (`dcc7ebab`), which did not sort them; the current code sorts them in ascending order (`descriptions.py:3195-3202`). A goal missing from the shot events, for instance one with no expected-goals value, would still give three.

## The course notes and CONCEPTS.md against the code

The fourteen facts the first draft took from the course notes:

| Claim in the draft | In the code | Verdict |
| --- | --- | --- |
| Each analyst has about ten functions | 6 to 24 depending on analyst and permissions; most 8–16; Scout up to 24 | Round number; say "a handful to two dozen" or give the range |
| Analyst = context object + list of functions; Scout Player (season), Match (match) | Yes, plus a system prompt; Scout's context is player, competition and season | Confirmed |
| The Scout calls a Compare Player analyst without telling the user | No analyst calls another out of sight; all hand-overs are visible redirects. Descriptions reuse other descriptions' synthetic text internally | Wrong; drop |
| Receptionist is first; has redirects to all others; analysts redirect back to it | Yes, but analysts also redirect directly to related analysts | Confirmed, needs the addition |
| Receptionist instructions as quoted; the rest limit it to analysts the user can access | Quote correct, one line added since; access is enforced by withholding redirect functions and a second check | Confirmed; update the quote |
| WhatsApp offers only scouting and hides the switches | WhatsApp users reach analysts by permission; Search replaces Talent Discovery | Wrong; drop or correct |
| Around a hundred thousand players | No figure in the code | Unverified; drop or ask for the number |
| GPT-4o returns a name; fuzzy search; GPT-4o chooses; teams the same | String from the model; BM25 search over name fragments with a market-value term; LLM chooses with "do not guess"; teams need two choosing calls; models set in configuration | Confirmed in outline; correct the details |
| Talent Discovery context as quoted | The quoted fields are now the Search analyst's context; Talent Discovery has lists of competitions, seasons and positions | Relabel or use Talent Discovery's |
| Opposition Analyst with opposition and hero team | Yes (`schemas/nlc/opposition_evaluation_context.py:32-89`) | Confirmed |
| Functions designed in Figma; three types | Figma not in the code; the three types correspond to summary descriptions, single-quality descriptions and answer functions | Confirmed in substance |
| Scout summary: basic stats, summary, strengths and weaknesses | Short description, summary, strengths, weaknesses and visualisation functions exist | Confirmed |
| Match synthetic text as quoted, three goals for a 4–0 win | Explained above: two data sources, older code | Explained |
| Answering questions: one long document from data and texts, using embeddings | Yes: an assembled document, with qualities and background chosen by embedding search in the knowledge API | Confirmed |

`CONCEPTS.md` is mostly right about the design, but out of date in places: it names `gpt-4o` and `/api/src/` paths, and presents initial function calls as the way data is pre-loaded, which no analyst now uses.

## What the paper should say

The first draft's account holds up in outline. The paper should stay short; the code adds a lot that it should leave out. Proposed changes:

Keep: the hub of analysts around a receptionist; analysts as instructions, context and functions; redirect functions; names resolved in two steps; the three kinds of function, with descriptions as wordalisations.

Correct:

1. The map is a hub with some direct paths, not a pure star: a change of subject goes through the receptionist, a different question about the same player goes straight to the analyst that answers it, carrying the context with it.
2. Function counts as a range, and the honest point that the Scout exceeds OpenAI's suggested twenty for users with every permission.
3. Name resolution: a database text search returns a short list, and the model chooses from it or asks the user. Mention the market-value term only if it helps.
4. Drop the hidden Compare Player call, the WhatsApp claim and the hundred thousand players (unless Twelve gives a number).
5. Relabel the quoted context as the Search analyst's, or replace it.
6. Explain the three-goals example in one sentence, or replace it with a current synthetic text.

Add, briefly, because they are the design lessons:

7. Small sets are offered to the model as enumerations; large sets are resolved after the call.
8. What the model is not offered it cannot do: access control, and the end of a chain, are done by withholding tools, not by instructions.
9. A chain of hand-overs is bounded: at most five, no repeats, and the last analyst must answer.
10. The resolution that creates a chat is authoritative for it.

Leave out: providers and model configuration, analyst groups, the research pipeline of Complex Player Questions (or one sentence), localisation and name masking, telemetry, MCP.

For the evaluation the draft lacks, the player-search counts in Application Insights could give a success rate for name resolution without new work, if Twelve is willing to share them.
