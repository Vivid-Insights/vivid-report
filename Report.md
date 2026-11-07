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

Articles in Models and Words are about understanding social, biological, medical, sporting and technological systems, about the models we build of them, and about how those models relate to the words we use to describe them. We are looking for three types of contributions:

1. Applications which combine models and words to produce insight for stakeholders.
2. Methodological and theoretical contributions where models and words are combined.
3. Description of Agentic AI solutions, where human decision-making is placed in the centre.

Models and Words is itself an AI agent. Submissions are written together with an agent, reviews will be semi-automated and the repository itself can provide help and support to application builders and researchers.

*Step 7 revises it against the finished report. Keep this note below the working abstract until then.*

## Introduction

New models change how we see the world. Kermack and McKendrick's model of epidemics showed that an outbreak can end before everyone has been infected [@kermack1927]. Turing proposed that two chemicals reacting and diffusing could produce the spots and stripes on animals [@turing1952], and Vicsek and Couzin showed that animals following simple rules about their neighbours' positions and directions produce the ordered motion of flocks and schools [@vicsek1995; @couzin2002]. In social science, Schelling showed that people with only mild preferences about their neighbours can produce strongly segregated cities [@schelling1971], an idea that grew into agent-based simulations of whole economies [@farmer2009; @axtell2025]. In sport, models of which space a football team controls [@spearman2018] and of the expected value of a basketball possession [@cervone2016] changed how games are analysed. @kasirzadeh2026 argues, using linear programming as an example, that encounters between the real world and models are where new mathematics often starts. Similarly, @gyllingberg2023 argue that this art of formulating new models has (until recently) been neglected in favour of analysing the ones already written down. Agentic AI opens up new possibilities to both find new models and build a rich new form of applications based on combinations between models and words. These possibilities arise because large language models can now write code and analyse equations quickly, while also saying in words what a model shows. The aim of this 

The first kind of article we want applies models and words to give people insight they act on. Twelve Earpiece, a conversational analyst for football data, is one example [@sumpter2026earpiece]. When a scout asks about a player, code decides which specialised analyst answers and which data it sees, and most replies are written by a language model from a text the code generates from those data. Judged blind against a general coding agent given the same data, its answers made fewer unsupported claims. In the past year, applications that join language models to models and data have appeared in the largest journals. Two multi-agent systems proposed drug-repurposing hypotheses that were then confirmed in the laboratory, one for acute myeloid leukaemia [@gottweis2026] and one for dry age-related macular degeneration [@ghareeb2026], and a third carried out research tasks across 25 areas of biomedicine [@huang2026]. In the clinic, an agent grounded in treatment guidelines and in more than 2,000 earlier tumour-board cases agreed with tumour-board decisions in about four cases out of five [@zoller2026], and an agent that checked how consistent its own diagnoses were could pass the uncertain cases to clinicians and be right almost every time on the rest [@zhang2026]. The same tools can mislead. Physicians trained in AI literacy who were shown deliberately wrong suggestions from a language model diagnosed less accurately than those who were not [@qazi2026], and the training that made conversational AI more persuasive in political conversations also made its claims less accurate [@hackenburg2025]. What people take away from these systems depends on how the model and the words are joined.

The second kind of article is methodological or theoretical, focusing in particular on relating models and words. There are at least three ways of getting from a model to words: build a model that can be read directly [@rudin2019], narrate the output of an explanation method afterwards [@zytek2024], or reverse-engineer the computations inside a neural network into human concepts [@bereska2024]. Language models are also being used to generate scientific hypotheses from data [@zhou2024]. @messeri2024 warn that tools of this kind can give scientists an illusion of understanding, so that science "produces more but understands less". Methods for checking what a text says against the model it describes are needed as much as methods for producing the text. The first article in this report series gives a straightforward example of how to  turn a statistical model of the data into a rule-based description, deciding what is said and in what order, and a language model then writes only that description out as fluent text [@caut2025]. Similarly, @rahimian2025 turned the coefficients of an expected goals model into sentences, which a language model then wrote up as a description of each shot. In both, the link between model and words is a set of written rules that a reader can inspect and change.

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
