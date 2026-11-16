---
title: "What is a Vivid Report"
slug: "what-is-a-vivid-report"
folder: "papers/0001-what-is-a-vivid-report"
report-number: "0001"
authors:
  - name: David J. T. Sumpter
    affiliation: [1, 2]
    email: david.sumpter@it.uu.se
affiliations:
  1: Department of Information Technology, Uppsala University, Box 524, 751 20 Uppsala, Sweden
  2: Vivid Insights
date: 2026-11-02
version: "0.1"
keywords: []
references: references.yaml
---

## Abstract

Vivid Reports is a forum for developing ways of exploiting the capabilities of agentic AI in data science and research. We publish three types of report:

1. Applications which combine models and words to produce insight.
2. Methodological and theoretical contributions where models and words are combined.
3. Description of Agentic AI solutions, where human decision-making is placed at the centre.

The Vivid Reports series is itself an AI agent. Submissions are written together with an agent, reviews are semi-automated and the repository itself can provide help and support to application builders and researchers.

## What is a Vivid Report?

A profound change brought about by Agentic AI lies in the way it changes relationships between words and statistical or mathematical models. Until recently, a model reached the people who used it through a statistician or data scientist, who knew which set of equations answered which question, what was assumed and when the model should not be trusted. Language models can now do part (although not all) of that work themselves [@majumder2025; @chen2025; @gu2024blade]. We can ask an AI agent a question in plain language, it can code a solution and provide an answer, blurring the lines about what is a "data science" question and what is just a question. 

Vivid Insights publishes reports which recognise these changes and looks to shape future approaches to modelling and data science on the basis of them.

We publish three types of report. The first type of report applies models and words to give people insight to act on. In the past year, applications that join language and statistical models have started to appear. For example, a multi-agent system has provided suggestions of how existing drugs might be used for new treatments [@ghareeb2026]  and studies have shown how research tasks can be carried out by agents throughout biomedicine [@huang2026]. Social systems have their own examples. An AI mediator that wrote group statements from participants' own opinions helped people on opposing sides of political issues find common ground [@tessler2024]. Personalised, evidence-based conversations with a language model reduced belief in conspiracy theories [@costello2024]. In the second Vivid Report, a conversational analyst is developed which chooses which model answers a footballing question and explains what the answer means [@sumpter2026earpiece]. Among the other initial reports in this series, report 0007 describes an agentic mentor that supports African women entering technology careers, report 0009 a workshop on how generative AI might help caseworkers assess asylum claims, and report 0011 an explainable model of electrocardiograms.

The second kind of report is methodological or theoretical, focusing on relating models and words. Broadly speaking, there are at least three ways of getting from a model to words: build a model that can be read directly, a so called interpretable model [@rudin2019]; narrate the output of an explanation of a machine learning model [@zytek2024]; or reverse-engineer the computations inside a neural network into human concepts [@bereska2024]. We welcome all three approaches. The first report in this series gives an example of the first of these: showing how to turn a statistical model of the data into an engaging text [@caut2025]. Report 0005 sets out a method for writing storyboards that explain how a chatbot will behave before it is built, and report 0010 a framework for communicating an individual's health risk from population models in words.

A third kind of report describes methods for building agentic AI systems that work with humans. @schluntz2024 distinguish workflows, in which language models and tools follow predefined code paths, from agents, in which the model directs its own process and use of tools. Built well, such systems help the people who make the decisions. For example, using an agent that drew on treatment guidelines, junior doctors came closer to the treatment choices of senior specialists [@zoller2026]; a language model fine-tuned on psychology experiments predicted the choices of new participants better than existing cognitive models [@binz2025]; and Co-Scientist generates and refines hypotheses from a scientist's own research goals [@gottweis2026]. Indeed, Vivid Reports are built on that approach: the report repository is itself an agent that can explain the concepts written about in the reports themselves. Report 0004 describes building a football application coding agent for non-coders, report 0006 a course in which statisticians and data scientists stay in control of an agent doing their analysis, and report 0008 specialised agents that guide a user through choosing a machine learning model one step at a time.

Language models already take part in coding, as well as writing and reviewing science. By the end of 2024, an estimated 29% of the Python functions contributed to open-source projects in the United States were generated by AI [@daniotti2025]. Programmers who used AI more often tried new libraries and new combinations of them, which the authors read as a move into areas of programming new to them. An estimated 6.5 to 16.9 percent of peer-review text at four AI conferences in 2023 and 2024 was substantially modified by a language model, and the share of model-modified text in published papers is rising steadily, mostly in computer science [@liang2024mapping]. In a study of 7.3 million articles from four publishers, an estimated 57% of those published in 2025 showed signs of LLM influence in their wording, up from 12% in 2023 [@siler2026]. 

A big challenge in the agentic approach is keeping the human in the loop. @mitchell2026 argue that current agent designs make oversight hard, and that relying on agents erodes the skills that oversight depends on. Among knowledge workers, higher confidence in generative AI was associated with less critical thinking [@lee2025], and in a small study of essay writing, people who used a language model had the lowest sense of ownership of their essays and struggled to quote from them [@kosmyna2025]. Vivid Insights encourages a way of working with agents that addresses these issues, in which the author makes the decisions, do the thinking first, and read everything the agent writes. 

We encourage incremental contributions. Given the agentic nature of the series, we do not gatekeep based on some preconceived notion of novelty. The idea is to build up a reference work on how models can be used to understand the world and how new agentic applications are constructed. 

## Writing a report

Each Vivid Report is written in a shared repository, in one folder that holds the report, its references, its code and the material it rests on. The author works with an AI coding agent, and the report is a single Markdown file that both of them edit and that is built into the published page. Every change is committed, so the history of the report, including which sentences the agent wrote and which the author changed, can be read back.

Writing follows six phases: sketch the idea, draft the abstract, revise, write the start and end together, revise the abstract, and simplify and revise. At the first step, the agent gathers the material the report will rest on, such as code, saved model outputs, earlier papers and notes, and records where each came from. In the second step, author and agent agree the three points the report makes and put them into a working abstract. The abstract is then the template that each later section is checked against: the Introduction gives one paragraph of background to each point, the Methods and Results take them in the same order, and the Discussion answers them.

::: figure {#fig-writing src="Code/outputs/figures/writing_process.png" width=wide alt="A timeline of the six phases of writing a report, numbered 01 to 06 with their steps, steps 3 to 7 drawn as separate boxes, above two rows of cards: what the author does in each phase and what the agent does"}
![[papers/0001-what-is-a-vivid-report/Code/outputs/figures/writing_process.png]]
The six phases of writing a report, numbered from left to right, with the steps carried out in each. The upper row of cards says what the author does in each phase, the lower row what the agent does. In the third phase the Methods and Results are written one point at a time, A in step 3, B in step 4 and C in step 5, and each point is redrafted in rounds. In the fourth phase the Introduction (step 6) and then the Discussion (step 7) are written. The arrow joins the phase in which the abstract is drafted to the phase in which it is revised against the finished report. Review and publication come after step 9 and are not shown.
:::

The agent is instructed to keep the author's judgement at the centre. The author decides what the report says, and is asked to go first: to name the point of a paragraph before it is drafted, the papers they know before a search, and what they expected before a result is written up. The agent writes its drafts directly into the report, where the author edits them, and reads the author's edits before its next change. It works one step at a time and stops, so that each step can be read before the next begins.

The agent checks the writing as it goes. Every quoted model output is taken from its saved file, and the build checks it word for word. Every cited work is one the agent has opened, and when a paper cannot be opened the author is asked to download it. Every number comes from a saved output. When the author corrects how the agent writes or works, the correction is added, with the sentence that prompted it, to a set of writing rules that every later report follows. This report was written that way, and its history is in its repository.

## How reports are reviewed

To be completed.

## Disclaimer

This report was written with the help of agentic AI at every stage: gathering the material, describing the method, producing the figures, videos and interactive figures, checking the references and drafting the text. Each step was directed and reviewed by the authors, every quoted output comes from a saved file, and every number comes from code that can be re-run. Before publication the report was reviewed by the Vivid Insights team.

## References
