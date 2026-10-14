---
title: "A choose your own adventure approach to context engineering"
slug: "twelve-earpiece"
folder: "papers/0002-twelve-earpiece"
report-number: "0002"
authors:
  - name: David J. T. Sumpter
    affiliation: [1]
    email: david.sumpter@it.uu.se
  - name: Matthias Green
    affiliation: [2]
    email: matthias@twelve.football
  - name: Lars Ekman
    affiliation: [2]
  - name: Ágúst Pálmason
    affiliation: [2]
    email: agust@twelve.football
affiliations:
  1: Department of Information Technology, Uppsala University, Box 524, 751 20 Uppsala, Sweden
  2: Twelve Football, Bränkyrkagatan 95, Stockholm, Sweden
date: 2026-10-13
version: "0.2"
keywords: [conversational agents, function calling, context engineering, wordalisation, football]
references: references.yaml
---

## Abstract

Chatbots built on large language models (LLMs) are asked about data the models have never seen, through services that remember nothing between calls. We describe how we built Twelve Earpiece, a conversational analyst for football data, around these limits. Its functionality is split between specialised analysts, each a system prompt, a context that records what the conversation is about, and a short list of functions. A receptionist moves the user between analysts through redirect functions; analysts working on the same player hand over directly. A name given by the user is resolved by a database search followed by a second model call that chooses a candidate or asks the user. Most replies are wordalisations, written by separate model calls from texts the code generates from data, and open questions are answered from documents assembled with embedding search. Access, and the end of a chain of hand-overs, are enforced by withholding functions from the model rather than by instructing it. In a nightly test of 81 queries on routing and name resolution, every suite met its threshold on nine of ten nights; the one miss was a season resolved wrongly.

## Introduction

Four of the most important uses of large language models include: chat completion, embedding search, annotation and function calling (or tool use).[^1] In chat completion, which most casual LLM users experience, the application sends the whole conversation history and the model returns the next message. The history starts with system messages, which set the model's role and behaviour, followed by pairs of user questions and assistant answers [@openai2026]. These can be earlier turns of the conversation or few-shot examples of the questions and answers the application expects [@brown2020]. Nothing is remembered between calls: the history is the only thing the model has, and the application is what keeps it. 

[^1]: We provide worked examples of embedding search, annotation and function calling for Guardian football articles in [github.com/Twelve-Educational/Context-Engineering-Course](https://github.com/Twelve-Educational/Context-Engineering-Course).

Embedding search turns a piece of text into a vector chosen so that texts with similar meaning lie close together [@reimers2019]. A question is embedded the same way and compared with a set of stored texts by cosine similarity, and the closest ones are put into the prompt for the model to answer from. This is the basis of retrieval-augmented generation, introduced by @lewis2020: the retrieval step chooses what the model sees, and the model writes the answer from it. Models that take a million tokens have since made it possible to pass whole documents instead, which works better when the evidence is spread across them, while embedding search remains cheaper and stronger when the evidence is sparse [@li2024; @li2025lara]. A long context is not read evenly, either: models use what sits at the start and the end of it more reliably than what sits in the middle [@liu2023lost]. Embedding search also makes it possible to say which texts an answer was written from, where a long context leaves no record of which part of it the model used. 

Annotation uses an LLM to label text. LLMs have been found to match or exceed crowd workers on several annotation tasks [@gilardi2023], although agreement with human labels varies a great deal between labels and tasks [@zhu2023]. Finally, function calling gives the model a list of functions, each with a description and parameters, and the model returns one or more functions the user most likely wants together with the values of its parameters [@wang2026]. Choosing the right one, and knowing when no function applies, is itself a task models vary at [@huang2023]. Function calling is often referred to as tool use, though the two words describe different amounts of work. The model never runs anything: it returns a name and some arguments, and the application decides whether to call the function and what to do with the result. Tool use usually means the loop around that, in which the result is given back to the model and it chooses again, until it has what it needs [@yao2023]. 

Agentic coding tools, like Claude Code, are built upon these same methods [@claudecode2026]. Indeed, Claude is chat completion, with the tool calls happening as part of the reply. Along with the usual text tokens, function calls are are also output: it writes the name and the arguments, then it runs the function and appends what comes back as another message in the history. As a result agentic coding tools carry on from a conversation that now contains the answer [@openai2026]. The program that holds the conversation, declares the functions, executes the ones the model names, and calls the model again is often referred to as the harness. The 46 functions defined as part of Claude Code include `Glob` which lists the files matching a pattern, `Grep` which searches their text, `Read` which returns numbered lines, and `Edit` and `Bash` change the repository and run commands in it [@claudecode2026]. Delegation is itself one of the functions: `Agent` starts a second model, with its own context window and a narrowed set of the same tools, whose result returns to the first as a function result. A catalogue extracted from Claude Code's compiled source lists 896 separate prompt strings, together around 488 000 tokens, of which 229 are descriptions of the tools [@piebald2026]. No conversation sees all of this at once, since the harness assembles a prompt from the parts a session needs, but the instructions for using the functions are longer than the functions themselves.

Beyond agentic coding tools, there are many other potential new ways in which LLM methods can be combined to build software applications. In this article we refer to combining LLM methods with other software engineering approaches as *context engineering*, a term proposed by Tobi Lütke in June 2025, as "the art of providing all the context for the task to be plausibly solvable by the LLM" [@lutke2025], and taken up a week later by Andrej Karpathy [@karpathy2025]. @chase2025 fram context engineering as building dynamic systems that provide the right information and tools, in the right format, for the model to accomplish the task; @mei2025 survey the field and treat the context as components that are sourced, filtered, formatted and assembled. 

LATER ADD MORE REFERENCES HERE FOR SIMILAR APPROACHS

Although coding agents are flexible, they are not always (or even most of the time) what application users want.  @wang2026humans argue coding agents are measured on tasks they complete alone, while the problems users actually have are communicating what they want, checking the result and steering the agent when it goes wrong. Work in human–computer interaction has been making a related case for longer. A text box gives the user no structure, no sense of what the system can do and no way to orientate what context it is working on [@ma2023]. In the context of the application area we now look at, the questions a football analyst asks are also not the kind an agent can be left to answer. "Who should we sign at left back?" has no single correct reply, and a user who cannot see which data the answer came from has no way to judge it. 

Context engineering requires software design which is aware of the weaknesses of agentic AI in certain situations. For example, a naive solution to answering footballing questions is to build a function for every question. If the user asks "How many goals has Messi scored this season?", the model calls a function `get_goals` with the player and the season, and so on for passes, cards and every other statistic. This fails as the number of functions increases. OpenAI advises keeping fewer than twenty available at any one time [@openai2026], and models are measurably worse at choosing when shown a long list than a short one picked for the question [@huang2023; @repantis2026]. Choosing well also gets harder as the task gets more complicated [@song2025]. The difficulty is not going away as models improve: on benchmarks where an agent must use tools under written policies while talking to a user, the best models still fail more tasks than they complete, and lose ground again when the user has to be guided rather than simply informed [@yao2024tau; @barres2025]. Asking the model to write a database query instead does not help with many of the questions people actually ask, such as "Do you think Messi will perform well now he is playing in the USA?". Real questions are often ambiguous, in that more than one query would answer them, or unanswerable from the data at hand, and systems handle neither well [@dong2024practiq]. The failure is often quiet rather than obvious: an agent that could ask the user what they meant will instead settle on an assumption of its own and return a result that looks like an answer [@li2026underspec]. 

Some of our earlier work proposed a method, we called wordalisation, turns statistics into an engaging text [@caut2025; @rahimian2025]. These provide a special type of function, which is built to answer general questions — how a player performs, how he would do in another league — instead of fetching single numbers. In this article, we describe how we use the methods decribed above to ensure that the correct wordalisation is provided for a given question. In doing so, we describe how this works in Twelve Earpiece, an AI scouting and performance application. The contributions are as follows:

1. Analysts and redirects. Rather than give one model every function, we split them between specialised analysts, each with a short list and a context of its own, and let a receptionist move the user between them through redirect functions. The model never sees a long list, and what it is allowed to do is enforced by withholding functions rather than by instructing it.
2. Contexts and names. A question names a player or a team in words; the data has identifiers. We fill the context by searching the database for candidates and asking the model to choose among them, or to ask the user when it cannot. The ambiguity is resolved openly, where the user can see and correct it, instead of being assumed.
3. Functions that answer in words. The functions reply with wordalisations rather than numbers, and open questions are answered from documents assembled with embedding search, so the user can see which data an answer came from.

We also report an automated test of routing and name resolution, run nightly, which is how we know whether the design holds.

## The Earpiece Application

[^2]: Earpiece is at [earpiece.twelve.football](https://earpiece.twelve.football). It is a product of Twelve Football and needs an account with access to the data a question asks about.

Twelve Earpiece answers questions about football data in conversation, for scouts, analysts and coaches at clubs.[^2] The user talks to a set of specialised analysts, and the application moves between them as the subject changes. A scout looking at a Hammarby midfielder asks four questions in a row, and is answered by three analysts without naming any of them (@fig-walk). The first question names the player, the competition and the season, and the receptionist redirects to the Scout, which reports what she did this season. "Could she play in WSL?" is a question about another league, which the Scout has no function for, so it hands over to the Transfer analyst; the player is already resolved, so the hand-over is direct rather than back through the receptionist, and "she" is never ambiguous because the player is in the context rather than in the conversation. "How would she fit in at Arsenal?" stays with the same analyst and adds a club to compare against, so the prediction is made against Arsenal's own midfielders rather than the league as a whole. The fourth question drops the player altogether and asks about Arsenal's season, which moves the conversation to the Season analyst and replaces a player context with a team one. The right-hand pane changes with it, from the player's profile to the league table.



::: figure {#fig-walk src="Code/outputs/figures/fig_conversation_walk.png" width=wide alt="Four screenshots of Earpiece in a two by two grid, each headed by the question asked and the analyst that answered it: the Scout on a player, the Transfer analyst on a move to the WSL, the Transfer analyst on Arsenal's midfielders, and the Season analyst on Arsenal's season."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/fig_conversation_walk.png]]
Four questions, three analysts. Each panel is one screen of the same conversation, headed by the question the user typed and the analyst that answered it. The player is resolved once, in the first question, and carried through the second and third without being named again. The fourth question names a team instead, and the context switches from the player to Arsenal in the Women's Super League.
:::

## Methods {#sec-architecture}

Earpiece is built around two constraints that every application on LLM services has. The first is that the services are stateless [@patil2025]. Each request is treated as new, so a conversation exists only because the application stores every message and sends the whole chat again on every turn (@fig-stateless).  The second is that a model knows nothing beyond its training data, which has a cut-off date and none of a club's data. The application has to bring the right information into the conversation, at the right moment, in a form the model can use. 

::: figure {#fig-stateless src="Code/outputs/figures/diagram_stateless.svg" width=wide alt="The client sends a chat id and a new message to the Earpiece API, which reads the stored chat from its database and sends the whole chat to the LLM API, which returns the next message."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_stateless.svg]]
Where the state lives. The client sends only the chat's identifier and the new message. The Earpiece API reads the stored chat from its database and sends all of it to the LLM API, which returns the next message.
:::

We now describe how we overcome these limitations.
### Analysts and redirects

#### Analysts

An analyst is the part of Earpiece the user talks to. It has a system prompt, a context and a list of functions, and these map directly onto a chat-completion request: the prompt and a description of the context become the system message, and the functions become the tools the model may call. The Scout's context is a player in a competition and season; the Match Analyst's is one team in one match. There are twelve analysts, among them the Scout, a comparison of two players, a prediction of a player's performance in another league or team, a search for players, and analysts of a match, a season and an opponent. The user meets six (@fig-receptionist): the receptionist, and the five subjects it can hand over to — a player, a match, a search for players, a season and an opponent. The rest are sub-analysts within those subjects. Four analysts share the player subject, the Scout among them, and two share the match subject, so a user who asks about a player is handed to one of four without choosing between them. Most offer the model between 8 and 16 functions, depending on what the user has access to; the Scout offers 24. 

::: figure {#fig-receptionist src="Code/outputs/figures/diagram_receptionist.svg" width=wide alt="The receptionist in the centre, connected by two-way arrows to the player analysts, the match analysts, Talent Discovery or Search, the Season Analyst and the Opposition Analyst. A dashed arrow joins the player analysts and Talent Discovery directly."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_receptionist.svg]]
How the analysts are connected. Each box is a subject the receptionist can hand the user to, and the analysts inside it are the sub-analysts that share that subject. Each solid arrow is a pair of redirects: from the receptionist into an analyst's context, and back to the receptionist when the user changes subject. Analysts in the same box hand over to each other directly, as do the player analysts and the player search (dashed).
:::

#### Redirects

A user always starts with the receptionist (@fig-receptionist). Its functions are three general ones — explaining how the platform works, which leagues are covered, and a team's fixtures — and one redirect function for each analyst the user may use, at most twelve in all. A redirect function is generated from its target analyst: its name is `redirect_to_` and the analyst's name, its description is the analyst's own description of what it does, and its parameters ask for the names the analyst needs, such as a player, a team, a competition and a season. When the model calls it, the names are resolved to identifiers and a new chat is opened with that analyst in that context (@fig-redirect).

::: figure {#fig-redirect src="Code/outputs/figures/diagram_context_switch.svg" width=wide alt="Three boxes: the user names a player; the model calls a redirect function; a new chat with the Scout in a resolved player context. Below each, the messages, the tool call and the resulting context."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_context_switch.svg]]
A context switch. Left: the system message tells the model to call `redirect_to_scout` when the user names a player, and the user does. Middle: the model's tool call, with the player's name among its arguments (abbreviated). Right: the context the Scout then works in, with identifiers in place of names. The identifiers are the examples given in Earpiece's own schemas.
:::

When an analyst sees that the user wants something outside its context, it redirects back to the receptionist, which receives a summary of the conversation and the user's last message:

::: prompt {source="Attachments/earpiece-code/receptionist_analyst.py"}
> f"You have been called because another analyst in the platform was unable to give the user the information they were looking for."
> f"The analyst provided the following summary of the previous conversation: '{self.context.summary}'.",
> f"The very last thing the user said, which caused the analyst to call you, was: '{self.context.query}'.",
> "Your ONLY valid actions are: (1) call the most appropriate analyst immediately, ",
> "OR (2) ask the user a specific clarifying question to determine which analyst is appropriate, ",
> "OR (3) explain how the platform works, if the user asks a question about the platform.",
> "You MUST NOT greet the user, chit-chat, or respond in any other way. ",
> "Prioritise calling the appropriate analyst directly (option 1) over the other two options.",
:::

When the subject stays the same, the hand-over is direct. A user who asks the Scout how the same player would do in another league is sent straight to the Transfer analyst, which reuses the player already resolved. One way of describing the result is as a choose-your-own-adventure: the receptionist sends the user off with the Match Analyst, the Match Analyst sends them back when they ask about something else, and the receptionist finds the analyst who can answer.

No single call has to choose among many functions: the receptionist chooses an analyst, and the analyst chooses among its own functions. The cost is in the receptionist's prompt, most of which draws the boundaries between analysts — the Match Analyst is for teams and the Match Scout for players; one match goes to the Match Analyst, several against one opponent to the Opposition Analyst — and the more analysts there are, the more boundaries it has to be told about.

A chain of hand-overs could go on forever, since a newly opened chat reads only its instructions and context and can make the same choice again. A request may therefore be handed on at most five times, a hand-over to an analyst and context already visited in the same request ends the chain, and the last analyst in a chain is offered no redirect functions and told that the request "cannot be passed on again". On the turn a redirect opens, the new analyst is not offered a redirect back to itself, because the name it carries has already been resolved and resolving it a second time can give a different answer. The resolution that creates a chat is the one that chat keeps.

The same principle enforces access. An analyst only offers redirects to analysts the user may use, and the receptionist's prompt describes the others as available from Twelve. A prompt saying "do not call this" can lose to another prompt saying "always call this"; a function that is not offered cannot be called.

### Contexts and names

#### Resolving names

The model fills a redirect's parameters from what the user wrote, and where the set of possible values is small, it is shown the whole set: the positions and qualities a club uses are listed as the only allowed values. Strict mode, in which the provider checks every tool call against its schema, stops the model inventing values outside such a list. Players, teams and matches are far too many to list, so the model gives a name as text and the name is resolved afterwards, in four steps (@fig-resolve). A full-text search over names, which also favours players with higher market values, returns up to 20 candidates; if it finds none it tries again without the team, then without the competition. The candidates are written out as sentences — the player, the team, the competition — and a second model call, given the user's own words, picks one. It is told: "If you cannot confidently determine a match, do not guess." If nothing is picked, the redirect fails, and the model is told to ask the user for the missing or incorrect information.

::: figure {#fig-resolve src="Code/outputs/figures/diagram_resolve_names.svg" width=wide alt="Four boxes in sequence: the model gives the name as text; full-text search returns up to 20 candidates; the model picks one, or none if unsure; the context is set, or the user is asked."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_resolve_names.svg]]
Resolving a name. The tool call gives the name as text, a database search finds candidates, and a second model call chooses one, or none, in which case the user is asked.
:::

#### Context objects

A resolved context is stored with its chat, written into the analyst's system message, and shown to the user in a side pane, so they know what the analyst is working on before they ask anything (@fig-contexts). Every function of the analyst reads its identifiers to fetch data; the model never writes a database query.

::: figure {#fig-contexts src="Code/outputs/figures/diagram_contexts.svg" width=wide alt="Three rows: we're talking about a player, a match, a team; each points to a context object with its identifiers."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_contexts.svg]]
Contexts for a player, a match and a team, as Earpiece stores them (abbreviated). The identifiers are the examples given in Earpiece's own schemas.
:::

A context can be richer than identifiers. The parameters of a redirect are described to the model in words, and the descriptions double as instructions. Part of the context of the Search analyst, which finds players with given qualities in one league, is:

::: prompt {source="Attachments/earpiece-code/player_search_context.py"}
> gender: GenderType = Field(description="The gender of the players to search for.")
> position: str = Field(
>     description=(
>         "The position of the players to search for. "
>         "This should be the position that the user is interested in. "
>         "If the user does not specify a position, ask them to do so."
>         "Never assume a position, always ask the user to clarify. "
>         "If the user asks for Goalkeepers, answer that you do not include analysis on goalkeepers. "
>     ),
> )
> competition: CompetitionSeason = Field(
>     description="The competition in which to search for players. If the user specifies more than one competition, ask them to clarify which one they want to use."
> )
:::

A context is a footballing question made explicit. The Opposition Analyst's context has two teams, an opponent and a "hero team", so that it can answer a question such as how Arsenal attack against teams that defend like Liverpool.

### Functions

Besides the redirects, the twelve analysts offer 54 distinct functions between them (@tab-functions). Every analyst has the same three general functions, and some functions are shared, such as `find_similar_players`, which four player analysts offer. Function calling chooses the function in every case. What differs is how the reply is written, and by that we divide the functions into four types: structured wordalisations, which are chat completion from a text the code writes; search then answer, which adds embedding search; answers in several stages, which pass the reply of one model call to a second; and other functions.

::: table {#tab-functions width=wide}
The functions of each analyst, by type, apart from the redirects. The general functions are offered by every analyst, the receptionist included. The Complex Player Questions analyst, which has no functions of its own, is left out.
| Analyst | Structured wordalisation | Search, then answer | Several stages | Other |
| --- | --- | --- | --- | --- |
| General |  | `explain_data_analysis` |  | `get_data_coverage`, `get_team_fixtures` |
| Scout | `short_description`, `short_summary`, `short_strengths`, `short_weaknesses`, `player_summary_description`, `player_quality_description`, `player_pitch_description`, `switch_position` | `player_answer_skills_question`, `strengths_and_weaknesses`, `get_complete_player_data` |  | `find_similar_players`, `short_visualization`, `save_scout_report` |
| Comparison | `comparison_summary_description` | `answer_comparison_question` |  | `find_similar_players` |
| Transfer | `transfer_summary_description` | `answer_transfer_question` |  | `find_similar_players` |
| Team Fit | `describe_team_fit`, `describe_squad_comparison` | `answer_team_fit_question`, `answer_comparison_question` |  | `find_similar_players` |
| Search | `player_search` | `player_search_query` |  |  |
| Talent Discovery |  |  |  | `talent_discovery` |
| Match Analyst | `get_match_stats`, `get_match_lineups` |  | `describe_match`, `describe_match_quality`, `describe_match_time`, `describe_match_momentum`, `describe_match_pitch`, `answer_match_questions`, `get_team_strengths_weaknesses` | `save_match_report` |
| Match Scout | `describe_match_player` | `answer_match_player_question` |  |  |
| Opposition Analyst | `describe_opposition_strategy`, `describe_opposition_pitch`, `describe_opposition_pitch_secondary`, `describe_opposition_lineup` | `answer_opposition_question` |  | `save_opposition_report` |
| Season Analyst | `describe_season_stats` |  | `describe_season`, `describe_season_quality`, `describe_season_style`, `describe_season_style_quality`, `describe_season_quality_trend`, `answer_season_questions`, `get_season_strengths_weaknesses` | `save_season_report` |
:::

#### Structured wordalisations

Twenty-one functions answer questions that can be anticipated from the context alone: a summary of a player, one quality, where on the pitch the player acts, the statistics of a match. The code fetches the data for the context and writes a synthetic text from it, with fixed rules turning values into words, as in the wordalisation method of @caut2025. The function then makes a chat-completion call of its own, outside the conversation. Its prompt opens with question–answer pairs that explain the data and few-shot examples of good replies, both read from Twelve's knowledge store as user and assistant turns, and ends with the synthetic text. The reply is streamed straight to the user, usually beside a chart. The analyst's model chooses the function and its arguments, such as a quality from a listed set, but does not write the reply.

#### Search, then answer

Ten functions answer open questions, such as "Do you think they would struggle playing out from the back?". The model passes the user's question to the function word for word. An embedding search over example questions, each labelled with a quality, picks the qualities the question is about. The data for each quality is fetched and written as a synthetic text, and passages found by a second embedding search are added to it: what the quality measures, how it relates to the others, and how live scouts' observations relate to it. Each search returns only passages within a set distance of the question. The document ends with the question and the instruction to answer in no more than three sentences from the information given, and one model call answers it as for a wordalisation. Three variants depart from this. The Scout's `strengths_and_weaknesses` builds its search query from the data ("What can we say about a player who is …") rather than from the user's words. `explain_data_analysis` returns the passages it finds to the analyst's own model, which answers in the conversation. The Opposition Analyst's question function uses no search, and answers from the synthetic text of its strategy function.

#### Answers in several stages

Fourteen functions of the Match and Season analysts write their reply in two model calls. The first is a structured wordalisation or, for four of them, a search then answer, as above. When the team analysed is the user's own club and the club has entered its style of play, that reply is not shown. A second call adjusts its wording to the club's style, and to its objectives where they are given, keeping "all of the original information in the same order and same number of sentences". For any other team, the first reply is streamed to the user and there is no second call.

#### Other functions

Nine functions are none of these. Three are lookups whose result goes back to the analyst's own model, which writes the reply in the conversation: which competitions are covered, a team's next fixtures, and the three players most similar to the one in the context, after which the model offers a search for more. `talent_discovery` sends the user's filters to an endpoint whose ranked table is shown directly, and a model call writes up to three sentences describing the selection. `short_visualization` draws a radar chart and writes nothing. The four save functions store a request for a report on the current context, and reply from a template that suggests two follow-up questions. The report itself is a set of pages, each a chart and a structured wordalisation.

## Results

### Analysts and redirects

Earpiece is tested every night against 81 queries in nine suites, each case stating the function the model should call and the arguments it should give, and in name-resolution cases the identifiers the name should resolve to. Forty-one cases test routing: the receptionist's redirects, the Scout's choice of function, follow-up questions within a context, and refusals to users without access. Forty test resolution, of a player alone or with a competition, a team or a season. One model call is a sample, not a verdict, so each case is run three times and counts as failed only when most attempts fail; a suite passes when its pass rate meets its threshold, between 93% and 100%. Cases known to fail are run and reported but not counted. @tab-evals gives the most recent results.

::: table {#tab-evals}
The nightly test on 13 October 2026, with each case run three times. The one known failure, excluded from the count, was a lower-league player whose lookup was refused by a check meant for the transfer model.
| Suite | Cases | Threshold | Pass rate |
| --- | ---: | ---: | ---: |
| Receptionist redirects | 16 | 93% | 100% |
| Receptionist refusals without access | 3 | 95% | 100% |
| Scout function choice | 19 | 94% | 100% |
| Follow-ups within a context | 3 | 95% | 100% |
| Player and competition | 17 | 94% | 100% |
| Player and season | 6 | 95% | 100% |
| Player and team | 7 | 95% | 100% |
| Player only | 7 | 95% | 100% |
| Unsupported positions | 2 | 100% | 100% |
:::

### Contexts and names

Over the ten nights from 4 to 13 October 2026, every suite met its threshold on nine nights. On 10 October, "How did Moussa dembele play in 2022/23?" resolved to the right player but to the 2026 season, so the player-and-season suite scored five cases out of six. The test shows that routing and resolution work for the questions it contains. It says nothing about questions outside it, and it does not judge whether the replies themselves are right.

### Functions

For Internazionale's 4–0 win over Atalanta on 30 August 2024 (@fig-match), the synthetic text of the match summary began with the result, the date and the competition, and continued:

::: box {label="Synthetic text:" source="Attachments/context-engineering/6. Conversational context.md"}
Here is some background context:
We look at the game from the perspective of Internazionale.
Compared to their other matches, Internazionale can be satisfied with the outcome of the match.
Internazionale did not concede any goals. Internazionale scored 3 goals: at 56 minutes, 47 minutes and 10 minutes.
Internazionale had the upper hand during the opening 15 minutes of the first half.
Atalanta had the upper hand during the middle of the first half.
Atalanta completely dominated during the last part of the first half.
Internazionale completely dominated during the opening 15 minutes of the second half.
Atalanta dominated during the middle of the second half.
Internazionale dominated during the last part of the second half.
:::

The text lists three goals for a 4–0 win. The score comes from the table of results and the goals from the match's shot events, and nothing checks that the two agree, so a goal missing from the events disappears from the text while the score stays right.

::: figure {#fig-match src="Attachments/context-engineering/Images/Screenshot_2025-07-30_at_12.36.55.png" width=wide alt="Earpiece showing Internazionale's overall performance against Atalanta: a distribution plot of seven phases of play against the team's other matches, a wordalisation below it, and a side pane with the context, win probability and match statistics."}
![[papers/0002-twelve-earpiece/Attachments/context-engineering/Images/Screenshot_2025-07-30_at_12.36.55.png]]
The Match Analyst's summary of Internazionale 4–0 Atalanta (July 2025). Left: Internazionale's performance in seven phases of play, as a dot against their other matches, and the wordalisation below. Right: the context (date, time and competition), the pre-match win probability and match statistics.
:::

## Discussion

### Analysts and redirects

Most of what keeps Earpiece reliable is done in code rather than in prompts. Small sets of values are listed for the model and large ones looked up afterwards; access and the end of a chain are enforced by not offering functions; a name is resolved once per chat. Prompts are still where the boundaries between analysts are drawn, and those boundaries grow with the number of analysts.

### Contexts and names

The two places where the model is least controlled are the choice of candidate when resolving a name and the answers to open questions, which depend on what the embedding search retrieves. The night the test failed, the choice of season went wrong. The course example in the background shows a merging step adding a fact. [CHECK: the background is now part of the Introduction.] This is where we would expect most errors, and where the evaluation should be extended next.

### Functions

The design gives the language model two jobs: converting insight into language, and managing the conversation. The analysis is done elsewhere, by statistical models and databases, and reaches the model as text. This is what keeps each function general enough that a few of them cover a subject, and what lets a function's reply be traced back to its synthetic text and so to the data.

The Complex Player Questions analyst, to which the Scout redirects questions about trends, seasons, single matches or a career, answers in three model calls. The first annotates the question with one of eight labels, such as `stats`, `form` or `season_comparison`. The second is a tool-use loop over the tools of a separate server, which give it data, explanations of the metrics and Earpiece's own descriptions, guided by instructions written for the label: for `stats`, which tools to call in which order, and which are cheap. It ends with a research summary in a fixed format, which the user does not see. The third call writes the reply from the question, the research summary, a writing prompt for the label and question–answer pairs found by embedding search.

### Limitations

The architecture is described from Earpiece's code as of 9 October 2026. The test covers routing and name resolution for 81 fixed queries; it does not measure how often real users' questions are routed or resolved correctly, nor whether the replies are accurate. Earpiece logs each player search as attempted, succeeded or failed, which could give a success rate on real traffic, but we have not analysed those logs here. The limit of about twenty functions is a provider's suggestion, and the benchmarks we cite tested tool selection in general rather than our analysts; the Scout exceeds it for users with access to everything. The background examples use Guardian articles, not Earpiece's data.

### Looking ahead

[TO WRITE: one paragraph on what should be done next, by whom, and what it would settle.]

## Data and code availability

Earpiece's code is proprietary. The course notebooks used in the background are public in the [Context-Engineering-Course](https://github.com/Twelve-Educational/Context-Engineering-Course) repository, and the code of the wordalisation applications in the [wordalisations](https://github.com/BeimnetGirma/wordalisations) repository.

## Disclaimer

This report was written with the help of agentic AI at every stage: gathering the material, describing the method, producing the figures, videos and interactive figures, checking the references and drafting the text. Each step was directed and reviewed by the authors, every quoted output comes from a saved file, and every number comes from code that can be re-run. Before publication the report was reviewed by the Vivid Insights team.

## References
