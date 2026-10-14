---
title: "A specimen of the Vivid Insights report format"
slug: specimen
folder: papers/0000-specimen
report-number: VI-2026-000
authors:
  - name: David Sumpter
    affiliation: [1, 2]
    email: info@vividinsights.se
    corresponding: true
affiliations:
  1: Vivid Insights
  2: Department of Information Technology, Uppsala University, Sweden
date: 2026-10-09
version: "0.1"
keywords: [report format, structure, three points]
licence: CC BY 4.0
references: references.yaml
---

## Abstract

Here we state the field in one sentence and the specific problem in the next. We then state the three points of the paper, in the order they are taken throughout, with what was done for each and what was found. The main limitation is attached to the finding it limits, and the last sentence says what the reader should take away. The abstract is one paragraph of short sentences, with no method plumbing and nothing that is not in the report. It is drafted early, before the other sections, and used as their template; it is revised once they are written. This specimen makes no empirical claim. Its blocks show the format with real files from a small example, a normative model that turns a z-score into one of seven phrases.

## What We Have Built

Here, optionally, we describe the app, converser or tool the report is about, in a short paragraph for a reader who wants to see the thing before the argument: what it does, who uses it and where to find it. This section is unnumbered. It does not replace any part of the Methods, and a report without something built leaves it out.

## Introduction

Here we introduce the area in general terms: the problem the report is about, why it matters and to whom, and the main lines of work on it. The Introduction is a review of what is happening in the area, in four to six paragraphs, citing at least 20 papers. It builds from the general to the specific, and it never anticipates what the report found.

Here we give the background for the first point in the context of the literature: what is known, who showed it, and what remains open. A citation in the sentence reads as @caut2025, and one at its end reads as [@caut2025]. Every work cited has been opened, and its entry in `references.yaml` carries a link.

Here we give the background for the second point, in a paragraph of its own. Where earlier work disagrees, both sides are cited.

Here we give the background for the third point, narrowing to the specific question the report takes up.

Here, if it is needed, we close by saying what this report does about the three points, without saying what it found. @tab-structure shows where each point appears in the rest of the report.

::: table {#tab-structure}
Where the three points of the paper appear. Each row is a section; the points are taken in the same order in every section.
| Section | What it does for each point |
| --- | --- |
| Abstract | states it, with what was done and found |
| Introduction | gives its background in the literature, one paragraph each |
| Methods | describes how it was built or tested, under its own sub-heading |
| Results | shows the examples and evidence, under the same sub-heading |
| Discussion | answers it and links back to the Introduction, under the same sub-heading |
:::

## Methods {#sec-methods}

### What the three points share

Here we describe what all three points rest on, such as the data, the system as a whole or a model they all use, written from the code and repository. This sub-heading is optional. The equation, definition and figure below are real: they come from the specimen's small example, which turns a value into words by its z-score,

$$
z = \frac{x - \mu}{\sigma}
$$ {#eq-z}

where $\mu$ and $\sigma$ are the mean and standard deviation of the population the value is compared with. A term the report depends on is defined once, in a definition block, and used the same way throughout.

::: definition {#def-normative title="Normative model"}
The rules that turn the output of a statistical model into words: which thresholds separate one phrase from the next, what a value is compared with, and how the comparison is worded [@caut2025].
:::

A method figure is drawn by a script in `Code/`, so it can be regenerated. @fig-thresholds is made by `Code/fig_thresholds.py`, whose function `words()` is the specimen's normative model. Its cut points at $\pm 0.5$, $\pm 1$ and $\pm 2$ are a normative choice, and a report says so, with the alternatives.

::: figure {#fig-thresholds src="Code/outputs/figures/thresholds.png" alt="Standard normal density with six vertical threshold lines and the share of the population in each band"}
![[papers/0000-specimen/Code/outputs/figures/thresholds.png]]
A figure caption says what the figure shows and how to read it, not what it means. Here: a standard normal density, with vertical lines at the six thresholds of the normative model and, above each band, the percentage of a standard normal population that falls in it. The figure follows the reader's light or dark theme.
:::

### The first point

Here we describe the method behind the first point, thoroughly and from the code. Each fact about the method names the file that makes it true, and is recorded in the `Method Facts` table of the appendix with its commit. Every normative choice is named: what was chosen, by whom, and what the alternatives were. Where the method has published stages, it is described in its authors' terms and order.

### The second point

Here we describe the method behind the second point, under a sub-heading that the Results and Discussion will reuse.

### The third point

Here we describe the method behind the third point. Settings the app offers are either described or the report says why they are left out.

## Results

### The first point

Here we show the results for the first point, beginning with a concrete case. Generated text is quoted from the file it was saved in, and the build checks it word for word. The text below was generated by the app for the article by Zenebe and colleagues on communicating individual health risk, for a 42-year-old woman in a synthetic cardiovascular dataset, under the configuration that measures each contribution relative to the largest.

::: output {source="Attachments/figure2_configurations_excerpt.json" key="0.texts.0"}
> Your overall risk of heart and blood vessel problems is strongly reduced compared with other patients at the clinic. The strongest protective factor is your systolic blood pressure of 110, which strongly lowers your risk, and your age of 42 also reduces risk, though to a lesser extent. Your BMI 20.83, diastolic BP 70, normal cholesterol and active lifestyle do not significantly change your risk on their own. There are no measurements here that would raise your risk. To keep this favorable profile, continue your healthy habits and schedule periodic check-ups to monitor your blood pressure and other cardiovascular factors.
:::

A conversation with a converser is shown the same way, from its transcript file. The one below is hand-written, to show the layout, and the page labels it as such.

::: conversation {source="hand-written" assistant="Converser"}
> Reader: Is a z-score of 0.74 high?
> Converser: It is slightly above average. About 23% of people in a normally distributed population score higher.
:::

### The second point

Here we show the results for the second point. A video figure is used for something that happens in time, as in @fig-sweep, and it has a poster image for print.

::: video {#fig-sweep src="Code/outputs/videos/threshold-sweep.mp4" poster="Code/outputs/videos/threshold-sweep-poster.png" loop title="A value moving across the thresholds"}
![[papers/0000-specimen/Code/outputs/videos/threshold-sweep.mp4]]
A video caption says what happens and what is shown at each moment. Here: a value (dot) moving from $z = -2.8$ to $z = 2.8$ across the thresholds of @fig-thresholds, with the phrase the normative model gives it. The video loops without sound; in print, the frame at $z = +0.74$ is shown.
:::

### The third point

Here we show the results for the third point. An interactive figure is used when the reader learns by changing something, as in @fig-explorer; it calls no model from the page and has a still image for print. Where the report claims the method works, the evaluation goes here too: what it measured, on what sample, the estimate and its uncertainty.

::: interactive {#fig-explorer src="interactives/threshold-explorer/index.html" height=370 fallback="Code/outputs/figures/thresholds.png" title="Threshold explorer"}
![[papers/0000-specimen/Code/outputs/figures/thresholds.png]]
An interactive caption says what the controls do. Here: the upper slider sets the value and the lower one sets the inner cut point, which is $\pm 0.5$ in @fig-thresholds. The other four thresholds stay at $\pm 1$ and $\pm 2$.
:::

## Discussion

The Discussion has no sub-headings. It answers the three points in the order they were made, one paragraph each, and each paragraph's subject is clear from its first sentence. Here we answer the first point: what the results under its sub-heading in the Results support, and what they do not, kept distinguishable. We link the answer back to the literature of its Introduction paragraph, saying which work it agrees with, which it qualifies and which it contradicts, as with @caut2025. New literature can come in here when a result makes it relevant.

Here we answer the second point in one paragraph, in the same order as the Methods and Results.

Here we answer the third point in one paragraph, linking back to the Introduction.

Here, in one paragraph, we say what the method cannot do, what the examples cannot show, what was not evaluated, what depends on a particular model or provider, and what the normative choices assume about readers. A defect of one component stays beside that component in the Methods.

Here, in one paragraph, we say what should be done next, by whom, and what it would settle.

## Data and code availability

Here we say where the code, prompts and saved outputs behind the report can be found, at which commit, and under what terms. For this specimen they are in `papers/0000-specimen/` of the report workspace.

## Disclaimer

This report was written with the help of agentic AI at every stage: gathering the material, drafting the text, producing the figures and the interactive, and checking the references. Each step was directed and reviewed by the authors, and every quoted output and every number comes from a file or a script that can be re-run.

## References
