---
title: "What is Models and Words"
slug: "what-is-models-and-words"
folder: "papers/0001-what-is-models-and-words"
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

Articles in Models and Words are about understanding social, biological, sporting and technological systems, about the models we build of them, and about how those models relate to the words we use to describe them. We are looking for three types of contributions:

1. Applications which combine models and words to produce insight for stakeholders.
2. Methodological and theoretical contributions where models and words are combined.
3. Description of Agentic AI solutions, where human decision-making is placed in the centre.

Models and Words is itself an AI agent. Submissions are written together with an agent, reviews will be semi-automated and the repository itself can provide help and support to application builders and researchers.

*Step 7 revises it against the finished report. Keep this note below the working abstract until then.*

## Introduction

Artificial intelligence is changing how mathematics is done. @kasirzadeh2026 argues that it undermines a "checklist" view of mathematical progress, in which progress means solving problems set in advance, and favours a view in which mathematics grows out of open-ended encounters with the world. Her examples are Dantzig's linear programming and Wiener's cybernetics, both of which began with practical modelling problems. Modelling has been changing for longer. @breiman2001 described two cultures in statistics, one that builds a model of how the data were generated and one that treats the mechanism as unknown and predicts as well as it can. @rudin2019 argued that when the stakes are high, models should be interpretable by design, because explanations added to a black box afterwards can mislead. @gyllingberg2023 found that mathematical biologists spend most of their effort analysing models and too little formulating them, and called for many models of the same system in place of one. Large language models add a further step. They can write about what a model says, and in our own work they have been used to describe football players, personality tests and survey data from statistical models [@caut2025], and to explain machine learning models of actions in football [@rahimian2025]. The question of how models relate to the words we use about them is now a practical one.

The first kind of article we want applies models and words to give people insight they act on. This has a longer history than language models. The SUMTIME-MOUSAM system turned numerical weather predictions into forecast texts, after its authors found that human forecasters used the same words to mean different things, and forecast users preferred its texts to those written by people [@reiter2005]. In medicine, @gigerenzer2007 traced much of the confusion of doctors and patients about health statistics to how the numbers are framed, and showed that natural frequencies and absolute risks are understood better. @spiegelhalter2017 reviewed how numbers, verbal expressions and graphics communicate risk and uncertainty across health, weather and climate. Each of these settles on one way of putting a model into words. With language models, the words can be generated for each person and each question, which makes the choice of wording a decision taken every time a text is written.

The second kind of article is methodological or theoretical. @green2016 distinguish mechanistic explanations, which follow how the parts of a system produce an outcome, from constraint-based explanations, which rest on formal dependencies that hold whatever the parts are. The two kinds answer different questions, and both are put in words. There are at least three ways of getting from a model to words: build a model that can be read directly [@rudin2019], narrate the output of an explanation method afterwards [@zytek2024], or reverse-engineer the computations inside a neural network into human concepts [@bereska2024]. Language models are also being used to generate scientific hypotheses from data [@zhou2024]. @messeri2024 warn that tools of this kind can give scientists an illusion of understanding, so that science "produces more but understands less". Methods for checking what a text says against the model it describes are needed as much as methods for producing the text.

The third kind of article describes agentic AI systems built around a person's decision. @schluntz2024 distinguish workflows, in which language models and tools follow predefined code paths, from agents, in which the model directs its own process and use of tools. @shneiderman2020 argued that high automation and high human control can be designed together. The evidence on whether a human in the loop makes a difference is mixed. @bansal2021 found that AI explanations increased the chance that people accepted the AI's recommendation, whether it was right or wrong. In a randomised study of clinicians, a systematically biased model lowered diagnostic accuracy, and explanations did not help them recognise the bias [@jabbour2023]. In the United Kingdom, the Home Office trialled language-model tools that summarise asylum interviews and answer questions on country policy; the summaries saved caseworkers time, but some were removed as inaccurate or incomplete, and the government states that the tools do not replace any part of the decision [@homeoffice2025]. A legal Opinion later found that this use was at significant risk of being unlawful, in part because claimants were not told [@doughtystreet2026]. How the system is built decides what the person deciding actually sees.

Language models already take part in writing and reviewing science. An estimated 6.5 to 16.9 percent of peer-review text at four AI conferences in 2023 and 2024 was substantially modified by a language model [@liang2024monitoring], and the share of model-modified text in published papers has risen steadily, most in computer science [@liang2024mapping]. Comments from GPT-4 on research papers overlapped with human reviewers' about as much as two human reviewers overlapped with each other [@liang2024feedback]. Some go further: the AI Scientist writes, runs and reviews its own papers [@lu2024], and Agents4Science 2025 required AI authorship and used AI reviewers [@agents4science2025]. Writing with a model also changes the writer. A writing assistant set to argue one side shifted both what people wrote and what they later said they believed [@jakesch2023]. There is an older line of work on documents that carry their own computation, from literate programming [@knuth1984] to executable research articles [@maciocci2019]. Models and Words is built on that line: the journal is itself an agent, and each article is written with it, in a repository that holds the paper, its code and its review.

The difficulty is keeping the human in the loop. @mitchell2026 argue that current agent designs make oversight hard, and that relying on agents erodes the skills that oversight depends on. Among knowledge workers, higher confidence in generative AI was associated with less critical thinking [@lee2025], and in a small study of essay writing, people who used a language model had the lowest sense of ownership of their essays and struggled to quote from them [@kosmyna2025]. @bucinca2021 showed that cognitive forcing, in which people commit to their own judgement before seeing the AI's, reduces overreliance, though people liked those designs least. Our teaching on doing statistics with an agent is built on the same idea. The agent does one step and stops, and the person makes each choice along the way, which requires enough grounding in the methods to judge what the agent proposes. The way articles are written for Models and Words follows this approach.

## The articles we are looking for

*Step 4: the body of the editorial, one section per point, A, B and C, in the order of the Introduction, with the examples for each point in its section.*

## Writing your article with the agent

## How articles are reviewed

## Discussion

*Step 6: where the three points are answered. Ideally five paragraphs and no sub-headings: one per point in the order of the Methods, then the limitations, then looking ahead, linking back to the literature in the Introduction.*

## Data and code availability

*Step 10 states where the code, prompts and saved outputs behind the report can be found, and under what terms.*

## Disclaimer

This report was written with the help of agentic AI at every stage: gathering the material, describing the method, producing the figures, videos and interactive figures, checking the references and drafting the text. Each step was directed and reviewed by the authors, every quoted output comes from a saved file, and every number comes from code that can be re-run. Before publication the report was reviewed by the Vivid Insights team.

## References
