# Modelling Philosophy

The following principles underly all the models we use at Twelve. 

1, They are explainable in football terms. (”**understandable”**)

2, They should be relate to measurements of goals scored and conceded. (”**help teams win”**)

3, We use the best motivated approach to each problem we solve (**”advanced AI”**) 

## Always provide insight

**The golden rule for [building an analyst](Building%20a%20Twelve%20Analyst%2022cfdb4493c58092a87cc234093aabb3.md) is that it provides insight which is valuable to the people working in or watching football.**

There are certain activities you will need to carry out when building an analyst. The first and most important is to define what questions it will answer. At Twelve, we are *always* providing insight in to a footballing question. “How will Arsenal play against Liverpool?”, “How can Liverpool best defend against Arsenal?”, “Will Wirtz fit into the Liverpool squad?”, “Where are Liverpool most dangerous?”, “Has Mbuemo just had a lucky season or is he a natural goal scorer?”, etc. 

To help both formulate questions and to think about how to answer them we work with coaching staff, scouts and stakeholders working in football: the individuals who will benefit from the insight. For example, when Dimitris built the opposition analyst he talked to the analysts at ??? and . Dom gave feedback on his work with Burton. Similarly, when Ida built the match analyst she used her experience from Manchester United and IFK Göteborg. The original scout analyst was built by Agust after working with Hammarby. The idea is to build a tool that will help these and similar stakeholders.

The primary way we provide insight is to build a **mathematical** **model** of the data. This model can be relatively straightforward, like ranking [qualities and metrics](https://app.notion.com/p/225fdb4493c580bd9ebde12ab8f0a383?pvs=21) used in scouting. It can use theoretical statistical method, like the [transfer model](Transfer%20model%20225fdb4493c580108f53f1e390d473df.md) or the [attack and defence strength](Team%20strength%20model%20225fdb4493c5803b90b0d2f21281e3d1.md) model. It can use a machine learning approach, like the [total football](Total%20Football%20225fdb4493c58003931af465afedfe11.md) model. We pay careful attention to building models that explain football and the results of which can be interpreted by a human. 

We also have a **normative** model of football, which describes what our model says in words. This is done in the question answer pairs in the *describe files* and the examples files. The describe files relates the measurements we make in data to footballing insight. The *example files* tell us specifically how to deliver short reports about data. These pairs tie together the insight we got from the stakeholders to our models. We use the word normative as defined as [“setting a standard for evaluating or making judgments about behaviour or outcomes.”](https://en.wikipedia.org/wiki/Normativity) Our stakeholders define the norms and we build models that reflect their (subjective) judgements. At Twelve, we respect subjective judgements of our stakeholders and we try to make our models so they align with footballing norms. Models should be **understandable**.

While our models do build on subjective opinions of experts in football, they make predictions in two objective criteria: transfer value and goals. This is because we **help teams win** (and/or make money).

We avoid methods (such as clustering, auto-encoders, and even deep learning) that are purely black box representations of data. The philosophy of this approach is best described by Cynthia Rudin’s article “[Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead](https://pmc.ncbi.nlm.nih.gov/articles/PMC9122117/pdf/nihms-1058031.pdf)”. We are helping teams make high stake decisions. Rudin makes an important distinction between interpretable models and explainable models. We build interpretative models: we describe what our model assumes, fit it to data and then interpret the results using our normative model. Black box models might be explained post-hoc, but as Rudin points out, *“trying to explain black box models, rather than creating models that are interpretable in the first place, is likely to perpetuate bad practices and can potentially cause catastrophic harm to society.”* (or in our case football teams)*.* There is a tight connection between putting a premium on subjectivity (i.e. the importance of listening to stakeholders),  the use of language models to explain results, interpretability and Rudin’s point about models for high stake decisions. Although machine learning has a veneer of objectivity (since no “biased” stakeholder is consulted) this ultimately means it cannot be explained  to a stakeholder afterwards and is thus flawed in a decision-making setting.

## Also see

The interpretable-over-black-box principle here is the Twelve applied version of [[First Principles Method|David’s First Principles Method]] (understanding > prediction; mathematical models > ML for understanding). The practitioner-experience argument — that coaches and scouts evolve reliable judgment under fierce selection — is the same argument as [[Soccermatics Uncut/Chapter07_BirdBrain_Uncut|Soccermatics Ch.7 Bird Brain]] (football managers as evolved strategists). The broader vault discussion of interpretable vs ML models is [[Mathematical Bridges#11. Understanding vs prediction — interpretable models against machine learning|Mathematical Bridges — Bridge 11]], and the academic framing is in [[Models and AI/Building models in the age of machine learning and AI|Building models in the age of machine learning and AI]]. The triangulation-and-coherence view of statistical modelling is developed in [[Models and AI/Coherence, charity and triangulation in statistical modelling|Coherence, charity and triangulation in statistical modelling]].

- Twelve model index: [[Twelve Models (do not share externally)/Algorithms and Models 16ffdb4493c58088af16dc5b0e67a4bf|Algorithms and Models]]

## In the Soccermatics Course

The public teaching version of this model is taught, with runnable Python, in the course:

- [[Soccermatics Course/lesson5/Philosophy|L5 — Modelling philosophy (course)]]
