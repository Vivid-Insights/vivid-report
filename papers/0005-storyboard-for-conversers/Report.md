---
title: "[TO WRITE: suggested in step 7, once the argument is settled]"
slug: "storyboard-for-conversers"
folder: "papers/0005-storyboard-for-conversers"
report-number: "0005"
authors:
  - name: "[TO WRITE: author]"
    affiliation: [1]
affiliations:
  1: Vivid Insights
date: 2026-10-09
version: "0.1"
keywords: []
references: references.yaml
---

## Abstract

Developing chatbots using agents is much like developing software using agents as it requires the developer to gather requirements of what it should contain or look like and give it to the agent as context. But it is tricky to use regular methods of requirement elicitation and documentation as its requirements cover the states and flow of the conversation as well as its contents [@silva2022; @goncalves2024]. One of the tricky and tedious point a builder has to work on when building a chatbot is changing their requirements for what the bot should contain and how it should work like into a format that can easily provide context for the agent. Plus if any context is missing, the agent tries to fill it in on its own which might not give the result the builder wants [@yang2025]. In this paper we describe an intermediate representation of a builder's high-level requirements, called a “Storyboard”. A storyboard holds the software features of a chatbot, such as its pages and buttons, as well as its conversational requirements. This paper covers the conversational requirements. The builder lists the conversations the chatbot should have, gathers them into areas and functions, and draws the flow of each function: when it is triggered and what happens next. We then show the structure of the prompt that gives the chatbot its context when it answers, what the prompt contains and where each part came from. Last, we describe the data each function uses and where that data comes from.

*Step 7 revises it against the finished report. Keep this note below the working abstract until then.*

## Introduction

*Plan for the five paragraphs, one line each. Edit it here; each drafted paragraph replaces its line.*

1. The area: building chatbots with agents, and how the context an agent is given decides what it builds.
2. Background to A: how the conversations a chatbot handles are listed, grouped into areas and functions, and drawn as flows.
3. Background to B: the structure of the prompt a chatbot is given, what goes into it and where each part comes from.
4. Background to C: the data a function uses to answer, its kinds and its sources.
5. Roughly what this report does, in the order A, B, C.

## Methods

*Step 4: written from the code and repository, thoroughly, with one sub-heading per point in the order of the Introduction, and every normative choice named.*

### The storyboard and Ask-Afya

Ask-Afya is a cardiovascular health chatbot for the general public. Users give basic health measurements (blood pressure, cholesterol, blood sugar, body-mass index and, if they wish, smoking, drinking and activity) in a form or in chat. Ask-Afya explains where they stand against American Heart Association (AHA) thresholds, answers questions about any one factor and gives general lifestyle advice based on their own results. It also computes a personalised risk age from a logistic-regression model. Before it runs an assessment it checks for three cases its model is not built for: a blood pressure in the hypertensive-emergency range, an age outside 35 to 65, and pregnancy. It is a demonstration project and not a medical device.

The storyboard is a web page with one tab for each part of the chatbot. We cover five of them for Ask-Afya: the Overview, the Function Flows, the Areas, the Prompts and the Data Sources. A router built on OpenAI function calling chooses which function answers each message. [CHECK: the model and version used for the router and for the generation calls, the provider, and the main software and versions.]

### Conversations, areas and functions

#### What the Overview fixes: audience, states, scope

The Overview starts by fixing the domain: a person's own cardiovascular risk, read against AHA thresholds, with a logistic-regression risk age beside it. Anything else is outside it.

It then names the audience, the general public, through four personas. Ken wants honest answers without a lecture, Amara is motivated by her family, Kwame wants his priorities in order and Zainab wants reassurance. Each persona has a tone (direct, plain-spoken, pragmatic, and informative without alarm), a risk tier (high, high, middle and low) and two variables to ask about.

The Overview also fixes two conversation states. Before a report exists, a user can ask what Ask-Afya is or give measurements, and a question about results is answered by asking for data first. Once a report exists, the functions that explain it open up, and a new assessment overwrites it.

Its scope lists five things Ask-Afya answers: what it is and how to use it, running a risk assessment, what the overall and per-factor results mean, general definitions of the tracked factors, and practical advice based on the person's own results. Each comes with an example question. The Overview also says how a message is matched: new measurements go to GetRiskAssessment, a question about the result to ExplainRisk, a named factor to ExplainVariable, a request for next steps to GiveAdvice, a greeting or a question about the tool to HowAfyaWorks, and anything unclear to OutOfScope.

Six things are out of scope: diagnosing conditions, recommending medications, naming a doctor or hospital, assessing pregnant users, assessing anyone outside 35 to 65, and anything unrelated to the person's own assessment. A fixed message handles them. It lists what Ask-Afya can do and says it cannot give medical advice.

The disclaimer says Ask-Afya is a demonstration project, not a certified medical device, and has not been clinically validated. It adds that a reading of 180/120 mmHg or higher gets an urgent-care message, and that this does not replace calling emergency services.

#### Functions and their types

#### Function flows

#### Areas

### The structure of the prompt

#### What a prompt contains

#### Where each part comes from

### Data for each function

## Results

*Step 5: the examples and evidence, under the same sub-headings as the Methods.*

## Discussion

*Step 6: where the three points are answered. Ideally five paragraphs and no sub-headings: one per point in the order of the Methods, then the limitations, then looking ahead, linking back to the literature in the Introduction.*

## Data and code availability

*Step 10 states where the code, prompts and saved outputs behind the report can be found, and under what terms.*

## Disclaimer

This report was written with the help of agentic AI at every stage: gathering the material, describing the method, producing the figures, videos and interactive figures, checking the references and drafting the text. Each step was directed and reviewed by the authors, every quoted output comes from a saved file, and every number comes from code that can be re-run. Before publication the report was reviewed by the Vivid Insights team.

## References
