# Literature review: similar work and approaches to building chatbots

A working document for paper 0002 (Twelve Earpiece), written 18 October 2026, not published. It gathers work related to the paper's three points and its evaluation, and suggests what to read further. It was put together from four literature searches run by agents.

**How far to trust it.** Every source listed was opened, but almost all were read at the level of the abstract or the documentation page; no full papers were read. Before a source is cited in `Report.md` it has to be opened in full and its details checked (`References and Citation` in `instructions.md`). Venues marked *check* could not be confirmed from the page. Works the paper already cites are marked **(cited)** and not repeated in the lists.

---

## Where the paper sits: the four things to dig into first

1. **Earpiece is a task-oriented dialogue system with an LLM in the slots.** The receptionist is domain and intent classification, the context object is a frame with filled slots, and the analysts and redirects are a hand-crafted dialogue manager. That literature goes back to GUS (1977) and is the strongest scholarly frame for the architecture, and recent agent papers rarely cite it. Read Jurafsky & Martin's chapter, Young et al. (2013) and Hudeček & Dušek (2023) (section 1).
2. **The industry has converged on the same pattern under the name "handoffs".** The OpenAI Agents SDK, LangGraph and Rasa CALM each describe something close to analysts and redirects. Anthropic's "Building effective agents" calls it a *routing workflow* and argues for it over autonomous agents. None of them evaluates the pattern, and the search found no academic paper that does. That gap is the paper's opening (section 1).
3. **Guessing rather than asking is a known LLM failure.** The name test's finding, that the resolution settled on a plausible wrong player more often than it asked, matches CLAM, CLAMBER and NoisyToolBench. Chen et al. (2021) offer a mechanism: retrievers prefer the more popular of two entities with the same name (section 2).
4. **The evaluation's main result is predicted by the LLM-as-a-judge literature.** The judge preferred long, number-dense answers under undefined criteria, the order reversed when a person defined the criteria after reading the answers, and scores moved with the judging format. These match verbosity bias, self-preference, sensitivity to rubrics and "criteria drift" (Shankar et al. 2024). This could make the Discussion's argument for the detailed instructions much stronger, and it also names a confound the paper does not yet mention: Claude judged a Claude agent (section 4).

---

## 1. Architecture: analysts, redirects and context (point A)

### Task-oriented dialogue: the ancestor

- **Jurafsky & Martin, *Frame-Based Dialogue Systems*** (SLP3 Appendix K, draft 19 August 2026). https://web.stanford.edu/~jurafsky/slp3/K.pdf. Task dialogue since GUS (1977) is built on frames of slots. Each turn goes through domain classification, intent determination and slot filling. *For Earpiece:* the receptionist is the domain and intent step, and the context object (player, season) is a frame.
- **Young, Gašić, Thomson & Williams (2013), *POMDP-based Statistical Spoken Dialogue Systems: a Review*.** *Proc. IEEE* 101(5):1160–1179. https://doi.org/10.1109/JPROC.2012.2225812. Conventional dialogue managers are flow charts written by hand, and statistical methods were developed to avoid writing them. *For Earpiece:* the twelve analysts and their redirects are a hand-written flow chart, with an LLM doing understanding and generation. The review gives the old argument for and against writing it by hand.
- **Hudeček & Dušek (2023), *Are LLMs All You Need for Task-Oriented Dialogue?*** SIGDial 2023. https://arxiv.org/abs/2304.06556. LLMs track dialogue state worse than specialised models, but given the right slot values they complete dialogues. *For Earpiece:* supports keeping the state in a context object outside the model.

### Handoffs and routing in industry frameworks

- **OpenAI Cookbook, *Orchestrating Agents: Routines and Handoffs*** (archived, companion to Swarm). https://developers.openai.com/cookbook/examples/orchestrating_agents. A routine is a system prompt plus its tools; a handoff is a tool that returns another agent. *For Earpiece:* the closest published match to analysts and redirects. The differences are that the receiving agent sees the whole history rather than a context object, and nothing ends a chain.
- **OpenAI Agents SDK, *Handoffs*** (documentation). https://openai.github.io/openai-agents-python/handoffs/. Handoffs are presented as tools. `input_filter` changes the history the next agent sees, `is_enabled` switches a handoff off at runtime, and authorisation belongs in code rather than in instructions. *For Earpiece:* the industry form of "withhold the function rather than instruct".
- **LangChain/LangGraph, *Multi-agent*** (documentation). https://docs.langchain.com/oss/python/langchain/multi-agent. Three patterns: subagents as tools, handoffs (a state variable switches the active agent's prompt and tools), and routers. It calls context engineering "the center of multi-agent design". *For Earpiece:* the handoff pattern is Earpiece's design.
- **Bocklisch, Werkmeister, Varshneya & Nichol (2024), *Task-Oriented Dialogue with In-Context Learning* (Rasa CALM).** Preprint. https://arxiv.org/abs/2402.12234. The LLM turns messages into commands, and predefined flows with a deterministic manager decide what happens next. *For Earpiece:* the same division of labour, with heavier structure.
- **Rebedea et al. (2023), *NeMo Guardrails*.** EMNLP 2023 Demos. https://arxiv.org/abs/2310.10501. Rails defined at runtime keep a conversation on set paths. *For Earpiece:* another way of constraining the model from outside it.
- **Wu et al. (2024), *StateFlow*.** Preprint. https://arxiv.org/abs/2403.11322. Tasks modelled as state machines beat ReAct and cost less. *For Earpiece:* the closest academic formalisation, with analysts as states and redirects as transitions, though built for solving tasks rather than for conversation.

### Workflows against agents, and context engineering

- **Schluntz & Zhang (Anthropic, 19 December 2024), *Building Effective Agents*.** https://www.anthropic.com/research/building-effective-agents. Distinguishes workflows (LLMs on predefined code paths) from agents, names routing as a workflow, and advises "the simplest solution possible". *For Earpiece:* the natural citation for the contrast with Claude Code; Earpiece is a routing workflow.
- **Rajasekaran, Dixon, Ryan & Hadfield (Anthropic, 29 September 2025), *Effective Context Engineering for AI Agents*.** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents. Names "bloated tool sets" as a failure, and describes subagents that return condensed summaries. *For Earpiece:* fits the short function lists, and functions whose reply is written by a separate call.
- Mei et al. (2025), *A Survey of Context Engineering* **(cited)**. It does not single out routing or handoff designs.
- **Cemri et al. (2025), *Why Do Multi-Agent LLM Systems Fail?*** Preprint. https://arxiv.org/abs/2503.13657. 14 failure modes from over 1,600 traces of multi-agent frameworks. *For Earpiece:* Earpiece avoids agents talking to each other, but its redirect chains could show the failures of system design.
- **Wu et al. (2023), *AutoGen*.** Preprint. https://arxiv.org/abs/2308.08155. Agents converse freely with each other. *For Earpiece:* the contrasting design, in which the user drives every turn.
- **Ong et al. (2024), *RouteLLM*** (https://arxiv.org/abs/2406.18665) and **Wang et al. (2024), *Mixture-of-Agents*** (https://arxiv.org/abs/2406.04692). Both preprints. Here "routing" means choosing a model by cost, or combining models. Worth a sentence to separate that meaning from Earpiece's routing.

### Many tools

- **Gan & Sun (2025), *RAG-MCP*.** Preprint. https://arxiv.org/abs/2505.03275. Retrieving only the relevant tool descriptions raised tool-selection accuracy from 13.62% to 43.13%. *For Earpiece:* direct evidence that fewer tools on offer helps; Earpiece gets the same effect by structure.
- **Paramanayakam et al. (2024), *Less is More*.** DATE 2025. https://arxiv.org/abs/2411.15399. Fewer tools gave better success, faster.
- **Qin et al. (2023), *ToolLLM*** (https://arxiv.org/abs/2307.16789) and **Patil et al. (2023), *Gorilla*** (https://arxiv.org/abs/2305.15334). Both preprints. The opposite answer: retrieve from thousands of APIs, or fine-tune. Gorilla documents GPT-4 inventing API arguments.
- No source found gives a threshold such as "twenty functions" from evidence. The paper's figure rests on OpenAI's advice **(cited)**, which is the honest way to put it.

**Dig into:**
- Read Jurafsky & Martin and Young et al., and decide whether the Introduction's background to point A should name Earpiece as a frame-based dialogue system. This could fill the "LATER ADD MORE REFERENCES HERE FOR SIMILAR APPROACHS" placeholder.
- Compare Earpiece's redirects with the OpenAI handoff and its `is_enabled`/`input_filter` in a sentence or two. The differences (context object rather than history, withholding functions to end chains) are what Earpiece adds.
- Use Anthropic's workflow/agent distinction in the Discussion's first paragraph.

## 2. Resolving names (point B)

### Entity linking

- **Wu et al. (2020), *Scalable Zero-shot Entity Linking with Dense Entity Retrieval* (BLINK).** EMNLP 2020. https://arxiv.org/abs/1911.03814. Retrieve candidates with a bi-encoder, then re-rank them with a cross-encoder. *For Earpiece:* the same two stages as a database search followed by a second model call.
- **Logeswaran et al. (2019), *Zero-Shot Entity Linking by Reading Entity Descriptions*.** ACL 2019. https://arxiv.org/abs/1906.07348. Linking to entities never seen in training. *For Earpiece:* tens of thousands of players, most of them rare.
- **Ayoola et al. (2022), *ReFinED*.** NAACL 2022 Industry. https://arxiv.org/abs/2207.04108. Uses entity types to disambiguate. *For Earpiece:* the team plays that role.
- **Ding, Zeng & Weninger (2024), *ChatEL*.** Preprint. https://arxiv.org/abs/2402.14858. An LLM chooses among candidates, and many of the gold labels turned out to be wrong.
- **Chen et al. (2021), *AmbER*.** https://arxiv.org/abs/2106.06830. Retrievers were about twice as likely to fail on the less popular of two entities with the same name. *For Earpiece:* a likely mechanism for settling on the plausible wrong player.
- **Joko, Hasibi, Balog & de Vries (2021), *Conversational Entity Linking*.** SIGIR 2021 (*check*). https://arxiv.org/abs/2105.04903. Entity linking inside conversations, where earlier turns give context.
- **Cohen, Ravikumar & Fienberg (2003), *A Comparison of String Distance Metrics for Name-Matching Tasks*.** IJCAI-03 workshop. https://www.cs.cmu.edu/~wcohen/postscript/ijcai-ws-2003.pdf. The best metric combined TF-IDF tokens with Jaro-Winkler distance. A baseline for the fuzzy search step, alongside Christen (2006) **(cited)**.

### Asking rather than guessing

- **Kuhn, Gal & Farquhar (2022), *CLAM*.** Preprint. https://arxiv.org/abs/2212.07769. "Current language models rarely ask users to clarify ambiguous questions and instead provide incorrect answers."
- **Zhang et al. (2024), *CLAMBER*.** ACL 2024. https://arxiv.org/abs/2405.12063. LLMs are poor at spotting ambiguity; chain-of-thought and few-shot examples add little and may raise overconfidence. *For Earpiece:* prompting the second call harder may not fix it.
- **Wang et al. (2024), *Learning to Ask: When LLM Agents Meet Unclear Instruction*.** EMNLP 2025 (*check*). https://arxiv.org/abs/2409.00557. LLMs invent missing tool arguments. *For Earpiece:* an unresolved player is a missing argument.
- **Zhang & Choi (2023), *Clarify When Necessary*.** Preprint. https://arxiv.org/abs/2311.09469. Uses entropy over possible intents to decide when to ask. *For Earpiece:* a stated rule, where Earpiece now leaves the decision to the model.
- **Aliannejadi et al. (2019), *Qulac*** (SIGIR 2019, https://arxiv.org/abs/1907.06554) and **Rao & Daumé (2018)** (ACL 2018, https://aclanthology.org/P18-1255/). One good clarifying question removes most of the ambiguity; a question is worth asking when its answer is informative.
- **Vijayvargiya et al. (2025), *Ambig-SWE*.** ICLR 2026 (*check*). https://arxiv.org/abs/2502.13069. Agents don't notice underspecification, and gain up to 74% when they ask.
- **Kadavath et al. (2022), *Language Models (Mostly) Know What They Know*.** Preprint. https://arxiv.org/abs/2207.05221. Self-assessed confidence is calibrated on familiar tasks and less so on new ones.
- **Bhaskar et al. (2023), *AmbiQT*.** EMNLP 2023. https://arxiv.org/abs/2310.13659. Text-to-SQL systems collapse onto one reading of an ambiguous question. Dong et al. (2024), PRACTIQ **(cited)**, and Li et al. (2026) **(cited)** are already in the paper.

**Dig into:**
- Chen et al. (AmbER) on popularity bias. Could the name test check whether the wrong players resolved to were better known, by minutes played or league level, than the players asked about? That would test the mechanism with data already saved.
- Zhang & Choi, and Kuhn et al., for the Discussion's point that the resolution guessed rather than asked. Together with Li et al. (cited) they make it a known failure rather than a quirk of Earpiece.
- The searches found nothing on single-name players or on entity linking in sports. The Robinho finding may be new.

## 3. Wordalisation, data-to-text and answers from data (point C)

### Classic data-to-text, and sports

- **Reiter & Dale (1997), *Building applied natural language generation systems*.** *Natural Language Engineering* 3(1):57–87. https://doi.org/10.1017/S1351324997001502. The pipeline: content determination, discourse planning, aggregation, lexicalisation, referring expressions, realisation. *For Earpiece:* the synthetic text does the first stages by rule and the LLM does realisation. This is a clean way to describe wordalisation in standard terms.
- **Wiseman, Shieber & Rush (2017), *Challenges in Data-to-Document Generation*** (RotoWire). EMNLP 2017. https://arxiv.org/abs/1707.08052. The founding sports data-to-text benchmark. Neural models were fluent but worse than humans, and templates sometimes beat them.
- **Puduppully, Dong & Lapata (2019), *Data-to-Text Generation with Content Selection and Planning*.** AAAI 2019 (*check*). https://arxiv.org/abs/1809.00582. Plan first, then write. *For Earpiece:* the plan is written by rules over z-scores.
- **Castro Ferreira et al. (2019), *Neural data-to-text generation: A comparison between pipeline and end-to-end architectures*.** EMNLP 2019. https://arxiv.org/abs/1908.09022. Pipelines with explicit intermediate steps gave better texts and generalised better. **Kale & Rastogi (2020)** (INLG 2020, https://arxiv.org/abs/2005.10433) found the opposite with T5 pre-training. Cite both for balance.
- **Thomson, Reiter & Sripada (2020), *SportSett:Basketball*.** IntelLanG 2020. https://aclanthology.org/2020.intellang-1.4/. Abstract not readable. A structured statistics database as the base for sports NLG.
- **Parikh et al. (2020), *ToTTo*.** EMNLP 2020. https://arxiv.org/abs/2004.14373. Highlighting which cells to describe controls hallucination. *For Earpiece:* the synthetic text does the same job by choosing the statistics.
- **Zhao et al. (2023), *Investigating Table-to-Text Generation Capabilities of LLMs*.** EMNLP 2023 Industry. https://arxiv.org/abs/2305.14987. How well LLMs narrate tables directly, which is the Claude agent's route.

### LLMs explaining numbers and models

- **Zytek et al. (2024), *Explingo*.** IEEE BigData 2024. https://arxiv.org/abs/2412.05145. An LLM turns feature importances into narratives, guided by few-shot examples, and the narratives are graded by an LLM. *For Earpiece:* very close to wordalisation. Worth reading in full for how they grade narratives.
- **Martens et al. (2025), *Tell Me a Story! Narrative-Driven XAI with LLMs*.** *Decision Support Systems* 191. https://arxiv.org/abs/2309.17057. Lay readers understood SHAP stories better than SHAP values. *For Earpiece:* human evidence that narrated numbers beat raw ones, which bears on the detailed-instructions argument.
- **Slack et al. (2022), *TalkToModel*.** *Nature Machine Intelligence* 2023 (*check*). https://arxiv.org/abs/2207.04154. Conversation routed to fixed explanation operations; healthcare workers preferred it to clicking through tools. The same pattern as routing to wordalisation functions.

### Chat with your data, and football

- **Hong et al. (2024), *A Survey of LLM-based Text-to-SQL*.** IEEE TKDE 2025. https://arxiv.org/abs/2406.08426. The main alternative way of answering open data questions.
- **Zhang et al. (2023), *Data-Copilot*.** Preprint. https://arxiv.org/abs/2306.07209. Builds validated, reusable interfaces in advance rather than writing code at runtime. *For Earpiece:* the same trade-off as Earpiece against the Claude agent, and close to the Discussion's "next step" of automating construction.
- **Strand et al. (2024), *SoccerRAG*.** CBMI 2024. https://arxiv.org/abs/2406.01273. Retrieval over a football database. The closest football precedent for answering open questions from documents.
- **Xia et al. (2024), *SportQA*.** NAACL 2024. https://arxiv.org/abs/2402.15862. LLMs know basic sports facts but reason poorly about scenarios. A reason to ground answers in data.
- **Rao et al. (2024), *MatchTime*** (EMNLP 2024, https://arxiv.org/abs/2406.18530) and **Mkhallati et al. (2023), *SoccerNet-Caption*** (CVPRW 2023, https://arxiv.org/abs/2304.04565). Football commentary generated from video; a different input.
- No peer-reviewed LLM chat assistant built on football player statistics was found, other than SoccerRAG. Caut et al. and Rahimian et al. **(cited)** may be the main precedents.

**Dig into:**
- Reiter & Dale, plus Castro Ferreira et al., to place wordalisation as a pipeline in which code plans and the LLM realises. This would strengthen the Introduction's background to point C and the Discussion's explanation of why Earpiece's answers had fewer unsupported claims.
- Martens et al., for human evidence behind the claim that comparisons in words serve a reader better than raw figures.
- Data-Copilot, for the "next step" paragraph on automating construction.

## 4. Evaluation: LLM judges and their biases

### Foundations

- **Zheng et al. (2023), *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*.** NeurIPS 2023 D&B. https://arxiv.org/abs/2306.05685. GPT-4 agrees with humans over 80% of the time, and the paper names position, verbosity and self-enhancement biases.
- **Liu et al. (2023), *G-Eval*.** Preprint. https://arxiv.org/abs/2303.16634. Scoring by criterion with chain of thought, with an early warning that LLM judges may favour text written by LLMs.
- **Gu et al. (2024), *A Survey on LLM-as-a-Judge*.** Preprint. https://arxiv.org/abs/2411.15594.

### Biases that bear directly on the result

- **Saito et al. (2023), *Verbosity Bias in Preference Labeling by LLMs*.** Preprint. https://arxiv.org/abs/2310.10076. GPT-4 prefers longer answers more than humans do.
- **Dubois et al. (2024), *Length-Controlled AlpacaEval*.** COLM 2024. https://arxiv.org/abs/2404.04475. Regressing out the difference in length debiases the judge. *For Earpiece:* a method that could be applied to the saved scores; the agent's answers were longer than Earpiece's.
- **Panickssery, Bowman & Feng (2024), *LLM Evaluators Recognize and Favor Their Own Generations*.** Preprint. https://arxiv.org/abs/2404.13076. Self-recognition correlates with self-preference and seems to cause it. *For Earpiece:* Claude judged a Claude agent. This is a confound the report should name, and it also helps explain the basic-instructions result.
- **Wang et al. (2023), *Large Language Models are not Fair Evaluators*.** Preprint. https://arxiv.org/abs/2305.17926. The order of presentation changes rankings. The nearest evidence on why judging in batches shifted scores.
- **Hosking, Blunsom & Bartolo (2023), *Human Feedback is not Gold Standard*.** ICLR 2024. https://arxiv.org/abs/2309.16349. Assertive answers hide factual errors from human raters.

### Defining the criteria

- **Shankar et al. (2024), *Who Validates the Validators?*** Preprint. https://arxiv.org/abs/2404.12272. "Criteria drift": people need criteria to grade outputs, but grading outputs changes the criteria, and some criteria only appear after the outputs are seen. *For Earpiece:* the detailed instructions were written after reading the answers. This is the paper that turns that from a weakness into a described phenomenon, and the strongest support for the Discussion's argument. Read it first.
- **Bagaria et al. (2026), *Judging LLM-as-a-Judge: Concerning Rubric Artifacts*.** EMNLP 2026 (*check*). https://arxiv.org/abs/2609.02942. The rubric text alone partly predicts the judge's scores, and judges often fail to change their verdict when the criterion is reversed. Very recent.
- **Lee et al. (2024), *CheckEval*** (EMNLP 2025, https://arxiv.org/abs/2403.18771) and **Cook et al. (2024), *TICK*** (preprint, https://arxiv.org/abs/2410.03608). Yes/no checklists give more stable judges than Likert scores on subjective criteria. *For Earpiece:* the detailed instructions could be turned into a checklist: does it compare with similar players? does it explain each number?
- **Hashemi et al. (2024), *LLM-Rubric*.** ACL 2024. https://arxiv.org/abs/2501.00274. Calibrating the judge's rubric answers against people halves the error in predicting dialogue satisfaction.

### Faithfulness

- **Min et al. (2023), *FActScore*.** EMNLP 2023. https://arxiv.org/abs/2305.14251. Split the text into atomic facts and score the share supported. *For Earpiece:* an alternative to one overall faithfulness score; each claim checked against the player's data.
- **Rashkin et al. (2021), *Measuring Attribution in NLG* (AIS).** Preprint. https://arxiv.org/abs/2112.12870. Faithfulness is defined relative to an identified source. *For Earpiece:* the concept behind the finding that faithfulness depends on what the judge is given.
- **Thomson & Reiter (2020), *A Gold Standard Methodology for Evaluating Accuracy in Data-To-Text Systems*.** INLG 2020. https://arxiv.org/abs/2011.03992. Human annotation of errors in sports summaries. A model for checking the judge's faithfulness scores by hand.
- **Laban et al. (2021), *SummaC*.** TACL (*check*). https://arxiv.org/abs/2111.09525. NLI-based inconsistency detection.
- **Ji et al. (2022), *Survey of Hallucination in NLG*.** *ACM Computing Surveys*. https://doi.org/10.1145/3571730.

### Judges against people

- **Bavaresco et al. (2024), *LLMs instead of Human Judges?*** ACL 2025. https://arxiv.org/abs/2406.18403. Agreement with humans varies by model, property and source of the text; judges "should be carefully validated against human judgments". **Chiang & Lee (2023)** (ACL 2023, https://arxiv.org/abs/2305.01937) is the earlier, more optimistic view.
- **Deriu et al. (2020), *Survey on Evaluation Methods for Dialogue Systems*.** *Artificial Intelligence Review*. https://doi.org/10.1007/s10462-020-09866-x.
- **Følstad & Brandtzaeg (2020), *Users' experiences with chatbots*.** *Quality and User Experience* 5:3. https://doi.org/10.1007/s41233-020-00033-2. Users value efficient, relevant help. This bears on whether scouts would want the agent's number-dense answers.

**Dig into:**
- Shankar et al. first, then Panickssery et al. and Saito et al. Together they explain the basic-instructions result (a Claude judge rewarding a Claude agent's long answers) and justify the detailed instructions. These could go straight into the Discussion's fourth paragraph.
- **A confound the report doesn't mention yet:** the judge and the agent are both Claude. Either name it as a limitation, or rerun a sample with a judge from another provider. Every judgement so far is saved, so a sample of a few hundred would be cheap.
- **Length:** apply Dubois et al.'s length control to the saved scores, as a check that needs no new judging.
- **People:** no source tests whether users, rather than judges, prefer answers with more information. A small rating by scouts of the three example pairs, or of a sample, would answer the question the evaluation can't.

---

## Gaps the searches found

- No paper evaluates the pattern of one function call per turn, at discrete points, with access enforced by withholding functions, in a chatbot that faces users.
- Nothing on entity linking in sports, or on players known by a single name.
- No paper compares judging in batches with judging one answer per call.
- No evidence-based threshold for the number of tools.
- No peer-reviewed LLM assistant built on football player statistics, other than Twelve's own work and SoccerRAG.
