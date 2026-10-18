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

Some of our earlier work proposed a method, we called wordalisation, turns statistics into an engaging text [@caut2025; @rahimian2025]. These provide a special type of function, which is built to answer general questions — how a player performs, how he would do in another league — instead of fetching single number. In this work we build on that approach by looking at 
1. How context can be organised through a distinct system of analysts with redirects between them.
2. How we resolve names in databases consisting of tens of thousands of potential names. 
3. Managing multiple wordalisation functions and answering open questions from documents assembled with embedding search.
We report on testing of these features and discuss possible future developments of this approach.

## The Earpiece Application

[^2]: Earpiece is at [earpiece.twelve.football](https://earpiece.twelve.football). It is a product of Twelve Football and needs an account with access to the data a question asks about.

Twelve Earpiece answers questions about football data in conversation, for scouts, analysts and coaches at clubs.[^2] The user talks to a set of specialised analysts, and the application moves between them as the subject changes. A scout looking at a Hammarby midfielder asks four questions in a row, and is answered by three analysts without naming any of them (@fig-walk). The first question names the player, the competition and the season, and the receptionist redirects to the Scout, which reports what she did this season. "Could she play in WSL?" is a question about another league, which the Scout has no function for, so it hands over to the Transfer analyst; the player is already resolved, so the hand-over is direct rather than back through the receptionist, and "she" is never ambiguous because the player is in the context rather than in the conversation. "How would she fit in at Arsenal?" stays with the same analyst and adds a club to compare against, so the prediction is made against Arsenal's own midfielders rather than the league as a whole. The fourth question drops the player altogether and asks about Arsenal's season, which moves the conversation to the Season analyst and replaces a player context with a team one. The right-hand pane changes with it, from the player's profile to the league table.



::: figure {#fig-walk src="Code/outputs/figures/fig_conversation_walk.png" width=wide alt="Four screenshots of Earpiece in a two by two grid, each headed by the question asked and the analyst that answered it: the Scout on a player, the Transfer analyst on a move to the WSL, the Transfer analyst on Arsenal's midfielders, and the Season analyst on Arsenal's season."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/fig_conversation_walk.png]]
Four questions, three analysts. Each panel is one screen of the same conversation, headed by the question the user typed and the analyst that answered it. The player is resolved once, in the first question, and carried through the second and third without being named again. The fourth question names a team instead, and the context switches from the player to Arsenal in the Women's Super League.
:::

## Methods {#sec-architecture}

Earpiece is built around two constraints that every application on LLM services has. The first is that the services are stateless [@patil2025]. Each request is treated as new, so a conversation exists only because the application stores every message and sends the whole chat again on every turn (@fig-stateless).  The second is that a model knows nothing beyond its training data, which has a cut-off date and none of a club's data. The application has to bring the right information into the conversation, at the right moment, in a form the model can use. We now describe how we deal with these limitations in certain settings.

::: figure {#fig-stateless src="Code/outputs/figures/diagram_stateless.svg" width=wide alt="The client sends a chat id and a new message to the Earpiece API, which reads the stored chat from its database and sends the whole chat to the LLM API, which returns the next message."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_stateless.svg]]
Where the state lives. The client sends only the chat's identifier and the new message. The Earpiece API reads the stored chat from its database and sends all of it to the LLM API, which returns the next message.
:::

Earpiece is a web service written in Python with FastAPI. For the examples and tests in this report, the analysts ran on GPT-4o, and the functions' own model calls, including the choice among candidate names, on GPT-4o-mini, both served through Microsoft Azure. The knowledge store's question–answer pairs are searched by cosine distance between embeddings, also from Azure OpenAI, held in a PostgreSQL database with the pgvector extension.

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

### Resolving context

#### Identifying names

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

The majority of pre-defined functions answer questions that can be anticipated from the context alone. These include, for example, "Does she get involved in games?", "Where does he carry out most actions on the pitch?", "How would he perform playing as a full back?", "Could she play in WSL?", "How has Arsenal performed this season?" and "How did Arsenal play against Liverpool?". 

The structure of the answers is already tightly defined. Once the question is identified, the code fetches the data for the context and writes a synthetic text from it, with fixed rules turning values into words. The function then makes a chat-completion call of its own, outside the conversation, and builds its prompt in the four steps of @caut2025.  Figure @fig-prompt illustrates these steps: a system message tells the model who it is; it is told what it knows in the form of a long list of human expert-written question and answer pairs; a second system message and worked few-shot examples of a synthetic text and the reply we want tell it how to answer; and the synthetic text for the player in the context comes last, telling it what data to use.  The reply is streamed straight to the user, usually beside a chart. 

::: figure {#fig-prompt src="Code/outputs/figures/diagram_prompt_structure.svg" width=wide alt="Four rows, one per step. Each names the step and how many messages it contributes, and shows an excerpt of those messages: the system message, a question-answer pair about box threat, a worked example for another player, and the synthetic text for Vilma Koivisto."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_prompt_structure.svg]]
The prompt of the transfer function, in the four steps of @caut2025, as it was sent for the Hammarby player of @fig-walk. The excerpts are from the saved call; the counts of question–answer and worked pairs are read from the same call. The last step, highlighted, is the synthetic text for this player.
:::

#### Search, then answer

Ten functions answer open questions, such as "Do you think they would struggle playing out from the back?". The model passes the user's question to the function word for word. An embedding search over example questions, each labelled with a quality, picks the qualities the question is about. The data for each quality is fetched and written as a synthetic text, and passages found by a second embedding search are added to it: what the quality measures, how it relates to the others, and how live scouts' observations relate to it. Each search returns only passages within a set distance of the question. The document ends with the question and the instruction to answer in no more than three sentences from the information given, and one model call answers it as for a wordalisation. Three variants depart from this. The Scout's `strengths_and_weaknesses` builds its search query from the data ("What can we say about a player who is …") rather than from the user's words. `explain_data_analysis` returns the passages it finds to the analyst's own model, which answers in the conversation. The Opposition Analyst's question function uses no search, and answers from the synthetic text of its strategy function.

#### Answers in several stages

Fourteen functions of the Match and Season analysts write their reply in two model calls. The first is a structured wordalisation or, for four of them, a search then answer, as above. When the team analysed is the user's own club and the club has entered its style of play, that reply is not shown. A second call adjusts its wording to the club's style, and to its objectives where they are given, keeping "all of the original information in the same order and same number of sentences". For any other team, the first reply is streamed to the user and there is no second call.

#### Other functions

Nine functions are none of these. Three are lookups whose result goes back to the analyst's own model, which writes the reply in the conversation: which competitions are covered, a team's next fixtures, and the three players most similar to the one in the context, after which the model offers a search for more. `talent_discovery` sends the user's filters to an endpoint whose ranked table is shown directly, and a model call writes up to three sentences describing the selection. `short_visualization` draws a radar chart and writes nothing. The four save functions store a request for a report on the current context, and reply from a template that suggests two follow-up questions. The report itself is a set of pages, each a chart and a structured wordalisation.

### Answer Evaluation {#sec-evaluation}

To compare Earpiece's structured wordalisations with an agent that has the data but not the descriptions, we chose 20 of the 400 players of the name test, 10 women and 10 men, outfield players with at least 900 minutes in the season, spread over positions. We asked ten questions the Scout's functions are written for about each of them: a summary of the season; strengths and weaknesses; passing; dribbling; threat in the box; where on the pitch the player wins the ball back; whether they could play in another position; pressing; play in the air; and whether they get involved in games. Questions about transfers, team fit and comparisons were left out, because Earpiece answers them with prediction models an agent cannot reach. Earpiece answered in the player's context, as the app does. The Claude agent ran on Claude Opus 5.5 with the 35 data tools of Twelve's MCP server and none of Earpiece's descriptions or knowledge. Its whole system prompt was "You are a football analyst. Answer using the tools. Answer in exactly n sentences, in plain prose.", where n was the number of sentences in Earpiece's answer to the same question. A GPT-4o agent, served through Azure, was set up in the same way. Each system answered every question three times.

Claude Opus 5.5 then judged every answer on the criteria of the evaluation by @caut2025: faithfulness to the information given, engagement and usefulness, each from 1 to 5, and a list of every claim the information does not support. The judge worked in batches, one for each player, each holding up to 90 answers shuffled across questions and systems under identifiers that did not reveal which system wrote them, and was told to rate each answer on its own. The judge was given one of four sets of information about the player. Raw data: the player's quality and metric scores against players in the same position in the same competition, each quality's scores by zone of the pitch, and what a fixed set of the agent's data tools return about the player (biography, career by position, season metrics, defensive metrics and metrics by zone). Raw data and explanations: the raw data, and the question–answer pairs that explain the data in the prompt of the Earpiece function that answered. Raw data, explanations and synthetic text: these, and Earpiece's synthetic text for the question. Synthetic text only: Earpiece's synthetic text and nothing else, which is the information Caut and colleagues' judge had; here the judge rated faithfulness and unsupported claims alone. The explanations and synthetic text came from Earpiece's first answer, so all the answers to a question about a player were judged against the same information.

Engagement and usefulness were rated under two sets of instructions. The basic instructions asked how engaging the answer is to read, and how useful it is for understanding the player or making a decision about them. We wrote the detailed instructions after reading the Claude agent's answers, which were dense with numbers: "an engaging answer tells the scout about the player in footballing terms, without overwhelming them with numbers and statistics. If it gives a number, it does so in the context of comparing the player with other players", and "an answer is only useful if it compares the player with other, similar players. If it gives numbers, it explains what they mean." Faithfulness and unsupported claims were described in the same words in both, and the faithfulness we report was rated with the detailed instructions.

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

### Resolving context

Over the ten nights from 4 to 13 October 2026, every suite met its threshold on nine nights. On 10 October, "How did Moussa dembele play in 2022/23?" resolved to the right player but to the 2026 season, so the player-and-season suite scored five cases out of six. The test shows that routing and resolution work for the questions it contains. It says nothing about questions outside it, and it does not judge whether the replies themselves are right.

Asked "How has Robinho played this season?", meaning the Robinho who plays in the Portuguese Primeira Liga, the receptionist resolved the name to Robson Azevedo da Silva of Mohun Bagan. To see how often this happens, we asked about 400 players from less well-known leagues, 300 men and 100 women. They were drawn from Earpiece's own data, so that each came with the identifier a correct resolution must reach: domestic adult leagues outside the men's Big Five and the women's top divisions of England, the United States, Spain, Germany and France, at least 450 minutes in the 2025 or 2026 season, and at most three players from each of 136 competitions in 64 countries.

Each player was asked about twice, "How has {name} played this season?", once with the name as the data spells it and once misspelled. The misspellings followed a study of errors in patient names reported by @christen2006: 36% of errors were an added or missing name word, 39% a single wrong, missing, extra or swapped letter, 14% several letters changed, and 12% punctuation and spacing, and we used these shares. Names are often misspelled worse than this, and @udupa2010 found that misspellings in a real search log lay 2.33 edits from the name on average, so a quarter of ours were made hard, with three letter edits, or two for a name shorter than ten letters. We then asked the same questions with the player's team, "How has {name} played for {team} this season?", with the team given in an informal or misspelled form in the misspelled case. Three players whose team has no name in the data were left out. Each question was asked once and scored by whether the context the receptionist opened held the right player (@tab-names).

::: table {#tab-names}
Outcomes of the name test. Each column is one question per player: the name alone or with the team, spelled as in the data or misspelled. Right player: the receptionist opened a context with the player we asked about; asked the user: the resolution declined and asked for more; wrong player: it opened a context with another player; other: anything else, such as an error message.
| | Name only, correct | Name only, misspelled | With team, correct | With team, misspelled |
| --- | ---: | ---: | ---: | ---: |
| Right player | 371 (93%) | 250 (62%) | 396 (99.7%) | 334 (84%) |
| Asked the user | 3 (1%) | 39 (10%) | 0 | 29 (7%) |
| Wrong player | 26 (7%) | 108 (27%) | 0 | 29 (7%) |
| Other | 0 | 3 (1%) | 1 (0.3%) | 5 (1%) |
| Players | 400 | 400 | 397 | 397 |
:::

Spelled correctly but without a team, the names that led to another player each belonged to someone known by the same or a similar name. Players known by one name were most affected: 11 of 19, Robinho among them. With the team named, all but one led to the right player. Misspelled, a name alone often led to another player; with the team named, far fewer did. A missing or abbreviated name word gained most from the team, from 45% right to 79%, and single-letter errors went from 77% to 90%. The hard misspellings reached the right player in 42% of cases without the team and 61% with it; even with the team, 19 of these 100 led to another player, about as many as were asked to clarify. Each question was asked once, and the shares of error kinds come from hospital records, not from scouts typing names.

### Functions

Apart from the match summary of Internazionale, the examples in this section were made for this report, on the player and club of @fig-walk. We put five questions to an analyst in its context, as a user would type them after a redirect, through Earpiece's own code, and the analyst's model chose the function. Each question was run three times; we quote the first run and say where the other two differ.

#### Structured wordalisations



Asked "Does she get involved in games?", the Scout called `player_quality_description` for involvement, Vilma Koivisto's highest-rated quality. The function's synthetic text was:

::: box {label="Synthetic text:" source="Code/outputs/function-examples/quality-1.json" key="tool_results.0.content"}
Vilma Koivisto is outstanding at involvement compared to other midfielders. She is outstanding at expected goals buildup, touches and defensive actions won compared to other midfielders. She is average at aerials compared to other midfielders.
:::

and the reply:

::: output {source="Code/outputs/function-examples/quality-1.json" key="replies.0" model="GPT-4o-mini, 14 October 2026"}
> Vilma Koivisto is a dynamic midfielder who's heavily involved in both the build-up and defensive phases of the game. Her impressive ability to accumulate touches and consistently win defensive actions makes her a fundamental player for her team, while her aerial contributions remain average but do not detract from her overall influence.
:::

The reply keeps to the three sentences of the synthetic text and adds a judgement of its own, that she is "a fundamental player for her team". The other two runs say the same things in other words.

Asked "Could she play in WSL?", the Transfer analyst called `transfer_summary_description`, whose synthetic text predicts how she would perform in the WSL from how players of her age perform after the same move:

::: box {label="Synthetic text:" source="Code/outputs/function-examples/transfer-1.json" key="tool_results.0.content"}
Vilma Koivisto is a unknown footed 23-year-old midfielder (more specifically a defensive midfielder) playing for Hammarby in the Damallsvenskan. At 23 years old, she is still developing. Let's consider a move from the Swedish Damallsvenskan to the English Barclays Women's Super League. Typically a move of a player of this age from Swedish Damallsvenskan to English Barclays Women's Super League would lead her to perform a lot worse in intelligent defence, active defence, effectiveness, box threat, involvement, passing quality, progression and providing teammates over the next year. Overall, if Vilma Koivisto was playing in the Barclays Women's Super League she would be outstanding in involvement, intelligent defence and active defence. She would be excellent in passing quality. She would be average in progression, providing teammates and effectiveness. She would be poor in box threat.
:::

::: output {source="Code/outputs/function-examples/transfer-1.json" key="replies.0" model="GPT-4o-mini, 14 October 2026"}
> The young Koivisto, 23, could find her transition from the Damallsvenskan to the highly competitive Barclays Women's Super League challenging, particularly in aspects of her game that require high intensity. Despite the anticipated drop in her performance metrics like passing quality, effectiveness and how she provides for teammates, it's essential to note that her traits as a defensive midfielder will shine through. She is expected to stand out for her strong defensive capabilities, particularly in intelligent and active defence, which will be crucial in the high-pressure environment of the WSL. While she may struggle to threaten the opposition's box, her ability to get involved in the game could still make her a valuable asset to any team in England.  With an opportunity to develop further, Koivisto is a player to keep an eye on in the coming seasons.
:::

The reply keeps the predictions and adds what the synthetic text does not contain: that the WSL will test "aspects of her game that require high intensity", and that she is "a player to keep an eye on". The third run credits her with a "strong work ethic and tactical awareness", for which there is no data.

#### Search, then answer

Asked "What are the player's weaknesses?", the Scout called `strengths_and_weaknesses`. Its synthetic text names her three strongest and three weakest qualities, each followed by passages from the knowledge store on what the quality means. The part on her third weakness begins:

::: box {label="Synthetic text:" source="Code/outputs/function-examples/skills2-1.md"}
Vilma Koivisto third weakest quality lies in dribbling. She is average at dribbling compared to other midfielders.
:::

::: output {source="Code/outputs/function-examples/skills2-1.json" key="replies.0" model="GPT-4o-mini, 14 October 2026"}
> Vilma Koivisto's weaknesses lie in her run quality, box threat, and dribbling abilities, where she performs below average. This suggests she may struggle to create dangerous situations through her movement off the ball, has limited scoring potential within the opponent's penalty area, and may not effectively beat defenders, which could reduce her overall impact in attacking transitions and create fewer opportunities for her team.
:::

The reply says she is below average at dribbling, where the synthetic text says average; the other two runs say average.

#### Answers in several stages

No workspace we may publish has Arsenal as its club, so for this example we gave the Season Analyst a workspace of our own, named Arsenal, with the style of play "Control play." and the objectives "Win the league.". Everything else is Earpiece's code and data. Asked "How has Arsenal's season progressed?", the analyst called `describe_season_quality_trend` for outcome. The first call wrote:

::: output {source="Code/outputs/function-examples/rewrite-1.json" key="model_calls.1.output" model="GPT-4o-mini, 14 October 2026"}
> Over the longer term, Arsenal has struggled to find consistency, as evidenced by their average points tally, which reflects a lack of decisive performances throughout the season. In their last 10 matches, the team's outcome has shown significant decline, marked by fluctuations that suggest they are having difficulty maintaining a competitive edge in key moments. Overall, while Arsenal's performance is presently in a downward trend, the underlying variability indicates that they have the potential to turn things around if they can stabilize their game.
:::

This was not shown. The second call rewrote it as:

::: output {source="Code/outputs/function-examples/rewrite-1.json" key="replies.0" model="GPT-4o-mini, 14 October 2026"}
> Over the longer term, Arsenal has struggled to find consistency in their pursuit of winning the league, as evidenced by their average points tally, which reflects a lack of decisive performances throughout the season. In their last 10 matches, the team's outcome has shown significant decline, marked by fluctuations that suggest they are having difficulty maintaining control in key moments. Overall, while Arsenal's performance is presently in a downward trend, the underlying variability indicates that they have the potential to turn things around if they can stabilize their style of play and regain control of matches.
:::

The rewrite keeps the three sentences in their order and works in the club's terms: "maintaining a competitive edge" becomes "maintaining control", and "in their pursuit of winning the league" is added. All three runs bring in control and the league title.

#### Other functions

Asked "Can you find players similar to her?", the Scout called `find_similar_players`, which gave the Scout's own model her three highest-rated qualities and the instruction to name them and offer a search. The model replied:

::: output {source="Code/outputs/function-examples/similar-1.json" key="replies.0" model="GPT-4o, 14 October 2026"}
> Vilma Koivisto excels in her involvement in play, her passing quality, and her active defensive contributions. Specifically, her top qualities are Involvement, Passing Quality, and Active Defence.
>
> Would you like me to find similar players based on these qualities?
:::

All three runs end with the offer.

### Answer Evaluation

Earpiece's answers and the Claude agent's were judged as described in @sec-evaluation. The GPT-4o agent scored lowest on faithfulness, engagement and usefulness throughout. The 27 of Earpiece's 600 answers that were an error message or empty are left out.

#### Faithfulness

The judge rated faithfulness four times, each time given a different set of information about the player (@tab-faithfulness).

::: table {#tab-faithfulness width=wide}
Faithfulness of the answers, judged with four sets of information about the player. Faithfulness is the mean rating from 1 to 5; unsupported claims is the mean number per answer. Each is given ± the standard deviation over answers. Won: the share of the 573 questions, players and repeats on which Earpiece's answer was rated more faithful than the Claude agent's, and less; the rest were tied. Judged with the detailed instructions of @tab-engagement.
| Information | What the judge was given | Earpiece faithfulness | Claude agent faithfulness | Won, Earpiece / Claude agent | Earpiece unsupported claims | Claude agent unsupported claims |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Raw data | The player's quality and metric scores against players in the same position, the scores by zone of the pitch, and what a fixed set of the agent's data tools return about the player | 3.78 ± 0.72 | 4.21 ± 0.81 | 20% / 48% | 0.56 ± 0.67 | 0.75 ± 0.97 |
| Raw data and explanations | The raw data, and the explanations of the data in the prompt of the Earpiece function that answered | 3.82 ± 0.75 | 4.17 ± 0.81 | 24% / 45% | 0.70 ± 0.77 | 0.86 ± 1.08 |
| Raw data, explanations and synthetic text | The raw data and explanations, and Earpiece's synthetic text for the question | 4.03 ± 0.69 | 4.04 ± 0.83 | 34% / 35% | 0.55 ± 0.61 | 0.89 ± 0.99 |
| Synthetic text only | Earpiece's synthetic text for the question, and nothing else | 4.02 ± 0.69 | 1.58 ± 0.49 | 99% / 0% | 0.96 ± 0.83 | 5.87 ± 2.17 |
:::

Given the raw data, the judge rated the Claude agent's answers more faithful than Earpiece's. The more of Earpiece's own material the judge was given, the higher Earpiece scored and the lower the agent, until, given the synthetic text as well, the two were level. Earpiece's answers had fewer unsupported claims whatever the judge was given. Against the synthetic text alone, which is how Caut and colleagues' judge works, nearly every Earpiece answer was rated more faithful than the agent's, and the agent's answers had several times as many unsupported claims. Judging against the synthetic text alone favours Earpiece by its design: the synthetic text is what Earpiece wrote from, so a correct statement the agent took from other data counts as unsupported. The GPT-4o agent had the most unsupported claims whenever the judge had the raw data, and fewer than the Claude agent against the synthetic text alone.

#### Engagement and Usefulness

Engagement and usefulness were judged under the basic and the detailed instructions, with each of the three sets of information that include the raw data (@tab-engagement).

::: table {#tab-engagement width=wide}
Engagement and usefulness under basic and detailed instructions to the judge, with each of the three sets of information in @tab-faithfulness that include the raw data. Mean ratings from 1 to 5, ± the standard deviation over answers. Won: the share of the 573 questions, players and repeats on which Earpiece's answer was rated higher than the Claude agent's, and lower; the rest were tied.
| Instructions | Information | Earpiece engagement | Claude agent engagement | Engagement won, Earpiece / Claude agent | Earpiece usefulness | Claude agent usefulness | Usefulness won, Earpiece / Claude agent |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Basic | Raw data | 2.83 ± 0.40 | 3.92 ± 0.35 | 0% / 94% | 2.66 ± 0.57 | 4.38 ± 0.60 | <1% / 96% |
| Basic | Raw data and explanations | 2.92 ± 0.37 | 3.93 ± 0.29 | 0% / 93% | 2.91 ± 0.62 | 4.39 ± 0.63 | 1% / 90% |
| Basic | Raw data, explanations and synthetic text | 3.00 ± 0.39 | 3.94 ± 0.30 | <1% / 88% | 2.95 ± 0.59 | 4.16 ± 0.66 | 2% / 84% |
| Detailed | Raw data | 3.50 ± 0.57 | 3.34 ± 0.52 | 42% / 27% | 3.09 ± 0.71 | 2.30 ± 0.50 | 67% / 11% |
| Detailed | Raw data and explanations | 3.78 ± 0.47 | 3.27 ± 0.54 | 60% / 12% | 3.31 ± 0.67 | 2.38 ± 0.53 | 76% / 7% |
| Detailed | Raw data, explanations and synthetic text | 3.74 ± 0.51 | 3.15 ± 0.51 | 65% / 11% | 3.35 ± 0.67 | 2.26 ± 0.48 | 84% / 4% |
:::

With the basic instructions, the judge rated the Claude agent's answer more engaging and more useful than Earpiece's to nearly every question, whatever information it was given. With the detailed instructions the order reversed: Earpiece's answers were rated more engaging and more useful, and its lead on usefulness grew the more of Earpiece's material the judge had. In a sample of the answers, the agent's gave several figures in each sentence and Earpiece's almost none.

## Discussion

The choose-your-own-adventure architecture which we have described here relies as much on pre-coded staructure as prompting. We use no inline tool calls, deciding which functions to call at discrete points. At each turn the analyst's model chooses one function from a short list; the code runs it, and for most functions a separate LLM model call writes the reply from a text the code has prepared. This call is the final result, rather than an output used in a tool-use loop [@yao2023; @claudecode2026]. The language model is left two jobs: turning insight into language, and deciding which function is called. The analysis is done by statistical models and databases and reaches the model as text. This keeps each analyst near the twenty or so functions that providers advise [@openai2026], and gives the user the structure a bare text box lacks [@ma2023]: the analyst, its context and the functions on offer say what the system can do at that point of the conversation.

The method has the advantage is that each part can be tested in isolation. We found that routing and name resolution met their thresholds in the nightly test on nine nights of ten, and the one miss was a season resolved wrongly, not a player. A name with the player's team almost always reached the right player. Without the team, players who share a name with another player, and players known by a single name, were the most likely to be resolved wrongly, and a misspelled name alone often led to another player. In those cases the resolution more often settled on a plausible candidate than asked the user, the quiet failure @li2026underspec describe in agents given underspecified requests. Naming the team is the simplest remedy, and an interface that offers the team with the name would make it the default.

In many aspects, Earpiece descriptions outperform answers from Claude on the same data. Earpiece's answers had fewer unsupported claims whatever the judge was given, and under the detailed instructions they were rated more engaging and more useful. The reason lies in what each system writes from. Earpiece's synthetic text has already compared the player with others in the same position and put the comparison into words, so the model that writes the reply has a finding to convey and few figures to repeat [@caut2025]. The Claude agent had the raw values, and wrote them out. This result depends on the evaluation method however. Under the basic instructions the judge preferred the Claude agent's answer to nearly every question, and given only the raw data it rated the agent's answers more faithful as well.

::::: figure {#fig-examples cols=2 width=wide}
:::: panel {#fig-examples-a}
::: output {source="Code/outputs/wordalisation-test/examples.json" key="0.earpiece"}
Denis Krioutchenkov is a dynamic striker who can create dangerous opportunities through his dribbling, demonstrating strong ability at generating expected goals with his carries. While he's effective in the attacking third, he struggles slightly when facing pressure, which can limit his overall impact in tight situations.

Denis Krioutchenkov showcased his dribbling prowess in the attacking central midfield, where he stood out as a key playmaker. He also demonstrated good abilities in the attacking half-spaces and the opposition penalty area, effectively creating opportunities for himself and his teammates. However, his performances in defensive areas, particularly on both wings and half-spaces, were below average, which may limit his overall impact on his team's transitions.
:::

Earpiece, asked "How good is Denis Krioutchenkov at dribbling?" Basic instructions: engagement 3, usefulness 3. Detailed instructions: engagement 4, usefulness 3.
::::
:::: panel {#fig-examples-b}
::: output {source="Code/outputs/wordalisation-test/examples.json" key="0.claude"}
Denis Krioutchenkov is an efficient dribbler rather than a high-volume one, and his dribbles often lead to real chances. Across about 1,970 USL League 1 minutes in 2026 he tried 45 dribbles and completed 36, an 80% success rate, which is very high for a striker. That works out to only about 2 attempts per 90 minutes (about 1.6 successful), so he picks his moments instead of taking players on all the time. Most of it comes as a centre-forward (27 of 34 completed, 79%), where his dribbles added 1.25 expected threat (xT, a measure of how much an action raises the chance of scoring) and fed into 2.10 xG (expected goals) worth of shots. He also kept the ball 62.5% of the time when pressed, but I haven't compared any of this with other League 1 strikers, so how he ranks in the league is untested.
:::

The Claude agent, asked "How good is Denis Krioutchenkov at dribbling?" Basic instructions: engagement 4, usefulness 4. Detailed instructions: engagement 4, usefulness 2.
::::
:::: panel {#fig-examples-c}
::: output {source="Code/outputs/wordalisation-test/examples.json" key="1.earpiece"}
Daniela Maria Lopes Ortolan shows a commendable ability to defend effectively in her own penalty area for a striker. However, her contributions drop off significantly in other areas of the pitch, particularly in the attacking third and on the right side. Overall, while she excels in protecting her goal, her defensive effectiveness diminishes as she moves further up the field. 
:::

Earpiece, asked "Where on the pitch does Dani Ortolan win the ball back?" Basic instructions: engagement 3, usefulness 3. Detailed instructions: engagement 3, usefulness 3.
::::
:::: panel {#fig-examples-d}
::: output {source="Code/outputs/wordalisation-test/examples.json" key="1.claude"}
Dani Ortolan wins the ball back very rarely: in the zones I could see, she has only 2 recorded ball recoveries all season, one on the attacking-half left wing (as a second striker) and one on the attacking-half right wing (as a centre-forward). Most of her defensive work happens on the attacking-half left wing, with 6 defensive actions and 4 of 7 defensive duels won (as CF, LW and SS), plus 3 defensive actions in the attacking central zone and 5 in her own box, the box ones mostly aerial duels at defensive set pieces. The data output was cut off, so I couldn't check the penalty box or her own-half zones beyond her own box, but the visible numbers point to a forward who presses mainly down the left in the opposition half.
:::

The Claude agent, asked "Where on the pitch does Dani Ortolan win the ball back?" Basic instructions: engagement 4, usefulness 3. Detailed instructions: engagement 4, usefulness 2.
::::
:::: panel {#fig-examples-e}
::: output {source="Code/outputs/wordalisation-test/examples.json" key="2.earpiece"}
Dengler shines in passing quality, particularly noted for his ability to generate expected threat from passes and moving the ball effectively into the final third. While he is competent in crosses, his contributions in terms of chance-creating passes and passes in the final third suggest there's room for growth in those areas.

Dengler excels in central areas, particularly in defensive and attacking midfield roles, showcasing his ability to distribute the ball effectively from deep. However, his passing contribution wanes significantly in wider positions and the opposition's penalty area, indicating he is less influential outside the central zones.
:::

Earpiece, asked "How good is Jake Dengler at passing?" Basic instructions: engagement 3, usefulness 3. Detailed instructions: engagement 4, usefulness 4.
::::
:::: panel {#fig-examples-f}
::: output {source="Code/outputs/wordalisation-test/examples.json" key="2.claude"}
I'd rate Jake Dengler as a strong passing centre-back for USL League 1: he combines high volume, accuracy and progression better than any of the few other centre-backs I could compare him with. In 2026 he made 1,516 passes in about 2,341 minutes as a central defender (roughly 58 per 90) and completed 89.5% of them. He also played about 269 minutes on the left of a centre-back pair, where he hit 91% from 170 passes. Per 90 minutes he made about 6.8 progressive passes, 5.6 passes into the final third and 0.50 expected threat from his passes (a measure of how much his passes raise the chance of scoring), against roughly 1.4–3.2, 0.9–2.4 and 0.20–0.33 for the three regular centre-backs I could see. The league-wide data came back cut off, so I only saw a small sample of peers rather than a full ranking, and he creates very little in the final third (1 key pass, 0.15 expected assists); his value is in building play from deep, with 239 playmaking passes and 12.5 expected goals from build-up.
:::

The Claude agent, asked "How good is Jake Dengler at passing?" Basic instructions: engagement 4, usefulness 5. Detailed instructions: engagement 3, usefulness 4.
::::
Three pairs of answers from the evaluation: Earpiece's on the left, the Claude agent's to the same question about the same player on the right. The players and questions were drawn at random, one question per player, from Earpiece's first answers that were not an error message. Under each answer are its ratings from 1 to 5, judged with the raw data, explanations and synthetic text.
:::::

We think the detailed instructions are the right ones for the reader Earpiece is built for, and the three pairs of answers in @fig-examples show why. A scout who asks how good a striker is at dribbling wants to know whether he is good, and good compared with whom. The Claude agent's answer about Denis Krioutchenkov (@fig-examples-b) gives his completed dribbles, his attempts per 90 minutes, expected threat and expected goals, and ends by saying it has not compared any of this with other strikers in the league; under the basic instructions the judge rated it more useful than Earpiece's (@fig-examples-a), which tells the scout what he does well and where he struggles. A judge asked only whether an answer is useful rewards completeness and precision, which is what a language model with raw data produces. The agent's answer about Dani Ortolan (@fig-examples-d) counts her ball recoveries and defensive actions zone by zone, where Earpiece's (@fig-examples-c) says where she defends well for a striker and where she does not. The detailed instructions are not a rule against numbers. Where the agent did compare Jake Dengler with other centre-backs (@fig-examples-f), the detailed judge rated its answer as useful as Earpiece's (@fig-examples-e). What they ask for is the comparison, and the comparison is what the synthetic text supplies. Whether Earpiece's comparisons are right is a separate question, which the faithfulness ratings answer.

The next step would be to automate the construction of wordalisations and of choose-your-own-adventure applications: an agent that writes the synthetic text for a new statistical model, and the analysts, contexts and redirects for a new subject. We expect the hardest part of this to be deciding the evaluation criteria. In our evaluation the same answers came out in opposite orders under two reasonable sets of instructions, and the instructions that reversed the order were written by a person who had read the answers. An agent building a wordalisation can check its texts against the data, as the faithfulness ratings do. It cannot decide by itself what a scout, a clinician or a mentee needs from the text, and that decision, written down and checked with the people who will read the texts, is where we expect the work of building such applications to move.

## Data and code availability

Earpiece's code is proprietary. The course notebooks used in the background are public in the [Context-Engineering-Course](https://github.com/Twelve-Educational/Context-Engineering-Course) repository, and the code of the wordalisation applications in the [wordalisations](https://github.com/BeimnetGirma/wordalisations) repository.

## Disclaimer

This report was written with the help of agentic AI at every stage: gathering the material, describing the method, producing the figures, videos and interactive figures, checking the references and drafting the text. Each step was directed and reviewed by the authors, every quoted output comes from a saved file, and every number comes from code that can be re-run. Before publication the report was reviewed by the Vivid Insights team.

## References
