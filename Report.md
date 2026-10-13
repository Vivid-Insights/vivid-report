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

Four of the most important uses of large language models are: chat completion, embedding search, annotation and function calling (or tool use). In chat completion, the application sends a conversation history to the model and receives a reply. The history starts with system messages, which set the model's role and behaviour, followed by pairs of user questions and assistant answers. These can be earlier turns of the conversation or few-shot examples of the questions and answers the application expects [@brown2020].

Embedding search turns a piece of text into a vector chosen so that texts with similar meaning lie close together [@reimers2019]. We split the 50 articles into 3 101 sentences and embedded each one with OpenAI's text-embedding-3-large model, which gives a vector of 3 072 numbers per sentence. A question is embedded the same way and compared with every sentence by cosine similarity. For the question "Why is there so much fuss about Manchester City?", the closest sentence (similarity 0.51) was "Unlike United, a club that 13 years later still has shaky foundations, City are a slickly-run organisation."

Annotation uses an LLM to label text. LLMs have been found to match or exceed crowd workers on several annotation tasks [@gilardi2023], although agreement with human labels varies a great deal between labels and tasks [@zhu2023]. We asked gpt-4o-mini to list every player and every club or national team in each article, using full team names, and to return them as JSON. Across the 50 articles this gave 519 player names and 175 team names, and each paragraph was then tagged with the players and teams it mentions.

Function calling gives the model a list of functions, each with a description and parameters, and the model returns the function the user most likely wants together with the values of its parameters [@wang2026]. Extracting those values is annotation of the user's message. Our news assistant has five functions: how many articles mention a name, a summary of a team, a summary of a player, and an answer to a question about a team or about a player. Its system prompt sets rules for choosing between them and ends "Always call tools — never answer from your own knowledge." A second call merges the results of the functions into one reply.

We illustrate each on the same small dataset, the 50 most recent football articles from The Guardian's API, using the example notebooks of our course on context engineering.


The merging step shows how these pipelines go wrong. Asked "What are the main problems Arsenal are facing?", the team summary returned, among other things:

::: output {source="Attachments/LLMMethods/GuardianFootballFunctions.ipynb" model="gpt-4o-mini"}
> Arsenal's next match is at home against Newcastle, with further fixtures against Fulham, West Ham, Burnley and Crystal Palace.
:::

and the merged reply ended:

::: output {source="Attachments/LLMMethods/GuardianFootballFunctions.ipynb" model="gpt-4o-mini"}
> Their remaining fixtures include home to Newcastle, and trips to Fulham, West Ham, Burnley, and Crystal Palace.
:::

The merge prompt says "do not expand or add new facts", but the reply states that the last four matches are away from home, which the function's result did not say.

A user of Earpiece types "Tell me about Jude Bellingham". The assistant does not answer. It calls a function, `redirect_to_scout`, with the player's name as its argument, and the user is handed to the Scout, an analyst whose context holds the player, a competition and a season as database identifiers (@fig-redirect). Everything the Scout says from then on is about that player in that season.

::: figure {#fig-redirect src="Code/outputs/figures/diagram_context_switch.svg" width=wide alt="Three boxes: the user names a player; the model calls a redirect function; a new chat with the Scout in a resolved player context. Below each, the messages, the tool call and the resulting context."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_context_switch.svg]]
A context switch. Left: the system message tells the model to call `redirect_to_scout` when the user names a player, and the user does. Middle: the model's tool call, with the player's name among its arguments (abbreviated). Right: the context the Scout then works in, with identifiers in place of names. The identifiers are the examples given in Earpiece's own schemas.
:::

The redirect deals with two problems that every application built on LLM services has. The first is that the services are stateless. Each request is treated as new, so a conversation exists only because the application stores every message and sends the whole chat again on every turn (@fig-stateless). Current models handle a single call well, but memory and decisions over many steps remain open problems [@patil2025]. The second is that a model knows nothing beyond its training data, which has a cut-off date and none of a club's data. The application has to bring the right information into the conversation, at the right moment, in a form the model can use.

::: figure {#fig-stateless src="Code/outputs/figures/diagram_stateless.svg" width=wide alt="The client sends a chat id and a new message to the Earpiece API, which reads the stored chat from its database and sends the whole chat to the LLM API, which returns the next message."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_stateless.svg]]
Where the state lives. The client sends only the chat's identifier and the new message. The Earpiece API reads the stored chat from its database and sends all of it to the LLM API, which returns the next message.
:::

The naive solution is a function for every question. If the user asks "How many goals has Messi scored this season?", the model calls a function `get_goals` with the player and the season, and so on for passes, cards and every other statistic. This fails on the number of functions. OpenAI advises to "aim for fewer than 20 functions available at the start of a turn at any one time" [@openai2026], and benchmarks of tool selection find that most models still struggle to choose the right one [@huang2023] and that both choosing functions and filling in their parameters get harder as tasks get more complex [@song2025]. Asking the model to write a database query instead does not help with many of the questions people actually ask, such as "Do you think Messi will perform well now he is playing in the USA?".

Our earlier work on wordalisation suggests a looser design [@caut2025; @rahimian2025]. A wordalisation turns statistics into a synthetic text in code, and a language model, given few-shot examples [@schulhoff2024], writes the reply from it. Functions built this way answer general questions — how a player performs, how he would do in another league — instead of fetching single numbers, so a handful of them covers most of what a user asks about one subject. We combine this with what chat completion does well, writing plain language from text it is given; with what function calling does well, working out roughly what the user wants; and with embedding search, finding background information relevant to the question.

We describe how this works in Earpiece. The contributions are four:

1. An architecture of specialised analysts, each with its own context and a short list of functions, coordinated by a receptionist and moving between one another through redirect functions.
2. A way of filling a context with the right player or team, by searching the database for candidates and letting the model choose among them.
3. Functions that write their replies as wordalisations, and answer open questions from documents assembled with embedding search.
4. The rules that keep this reliable, and an automated test of routing and name resolution.

## Methods {#sec-architecture}

### Analysts and redirects

#### Analysts

An analyst is the part of Earpiece the user talks to. It has a system prompt, a context and a list of functions, and these map directly onto a chat-completion request: the prompt and a description of the context become the system message, and the functions become the tools the model may call. The Scout's context is a player in a competition and season; the Match Analyst's is one team in one match. There are twelve analysts, among them the Scout, a comparison of two players, a prediction of a player's performance in another league or team, a search for players, and analysts of a match, a season and an opponent. Most offer the model between 8 and 16 functions, depending on what the user has access to; the Scout, for a user with access to everything, offers 24.

#### The receptionist and redirect functions

A user always starts with the receptionist (@fig-receptionist). Its functions are three general ones — explaining how the platform works, which leagues are covered, and a team's fixtures — and one redirect function for each analyst the user may use, at most twelve in all. A redirect function is generated from its target analyst: its name is `redirect_to_` and the analyst's name, its description is the analyst's own description of what it does, and its parameters ask for the names the analyst needs, such as a player, a team, a competition and a season. When the model calls it, the names are resolved to identifiers and a new chat is opened with that analyst in that context.

::: figure {#fig-receptionist src="Code/outputs/figures/diagram_receptionist.svg" width=wide alt="The receptionist in the centre, connected by two-way arrows to the player analysts, the match analysts, Talent Discovery or Search, the Season Analyst and the Opposition Analyst. A dashed arrow joins the player analysts and Talent Discovery directly."}
![[papers/0002-twelve-earpiece/Code/outputs/figures/diagram_receptionist.svg]]
How the analysts are connected. Each solid arrow is a pair of redirects: from the receptionist into an analyst's context, and back to the receptionist when the user changes subject. Analysts in the same box hand over to each other directly, as do the player analysts and the player search (dashed).
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

#### Keeping it finite

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

With the context set, an analyst's functions are the questions it can answer, and they are of three kinds.

The first is a summary, which the analyst's prompt tells it to give when the user has only named the subject: for the Scout, a short description of the player. The second describes one quality, one area of the pitch or one development over time, with a chart. Both are wordalisations [@caut2025]. The code turns the data into a synthetic text, and the function makes its own model call, outside the conversation, with question–answer pairs that explain the data, few-shot examples of good replies, and the synthetic text; the reply is streamed straight to the user.

The third kind answers a question directly. Its synthetic text is a document assembled for the question: an embedding search over example questions picks the qualities the question is about, the data for those qualities is fetched, and explanatory passages found by embedding search are added to each before the model is asked to answer.

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

### Limitations

The architecture is described from Earpiece's code as of 9 October 2026. The test covers routing and name resolution for 81 fixed queries; it does not measure how often real users' questions are routed or resolved correctly, nor whether the replies are accurate. Earpiece logs each player search as attempted, succeeded or failed, which could give a success rate on real traffic, but we have not analysed those logs here. The limit of about twenty functions is a provider's suggestion, and the benchmarks we cite tested tool selection in general rather than our analysts; the Scout exceeds it for users with access to everything. The background examples use Guardian articles, not Earpiece's data.

### Looking ahead

[TO WRITE: one paragraph on what should be done next, by whom, and what it would settle.]

## Data and code availability

Earpiece's code is proprietary. The course notebooks used in the background are public in the [Context-Engineering-Course](https://github.com/Twelve-Educational/Context-Engineering-Course) repository, and the code of the wordalisation applications in the [wordalisations](https://github.com/BeimnetGirma/wordalisations) repository.

## Disclaimer

This report was written with the help of agentic AI at every stage: gathering the material, describing the method, producing the figures, videos and interactive figures, checking the references and drafting the text. Each step was directed and reviewed by the authors, every quoted output comes from a saved file, and every number comes from code that can be re-run. Before publication the report was reviewed by the Vivid Insights team.

## References
