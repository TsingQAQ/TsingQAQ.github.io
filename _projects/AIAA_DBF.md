---

title: Design Optimization of an aircraft for AIAA Deisgn·Build·Fly Competition
collection: projects
layout: archive
date: 2017-9-13
author_profile: True
excerpt: An aircraft design optimnization was performed for [AIAA DBF](https://www.aiaadbf.org/General-Info/ "AIAA DBF") . The [score model](https://www.aiaadbf.org/Scoring/ "score model") of the competition draw special concern as that both geometry paramters and mission performance were involved in, and the contradiction of these parameters speified that a design optimization must be performed.  An aircraft preliminary design coupled with mission planning framework was built based on [PyADAO](https://tsingqaq.github.io/projects/PyADAO_construction/ "PyADAO") to find a design that could get the highest score. A tandem wing configuration was found for the final design.
permalink: /projects/AIAA_DBF/
---
![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/gitmap.png?raw=true)

## Backgrounds
An aircraft design optimnization was performed for [AIAA DBF](https://www.aiaadbf.org/General-Info/ "AIAA DBF") . The [score model](https://www.aiaadbf.org/Scoring/ "score model") of the competition draw special concern as that both geometry paramters and mission performance were involved in, and the contradiction of these parameters speified that a design optimization must be performed. An aircraft preliminary design coupled with mission planning framework was built based on [PyADAO](https://tsingqaq.github.io/projects/PyADAO_construction/ "PyADAO") to find a design that could get the highest score. A tandem wing configuration was found for the final design.

## Role&Responsibility
As the cheif engineer, I was responsible for the whole design process of the aircrafts, which include:
* Mission and score formula analysis 
* Choose the configuration [Initial design]
* Aerodynamic design ,structure design [preliminary stage]
* Complete the design part of final report

## Difficulties and Approaches

### Score Formula

$$Score=\frac{Writen ReportScore *  ToltalMissionScore}{RAC} $$

$$ToltalMissionScore=1 + M_2 + M_3$$

$$RAC=EWmax * Wingspan$$

Notes:                 
1 $$EWmax$$: Aircraft Empty weight
2 $$M_2$$: Mission 2 score
3 $$M_3$$: Mission 3 score

### Analysis
The main different of DBF match and other aeronatical contest is the rules. Unlike many other competitions that the design goal is clearly specified, a series of score formula is provided for teams, and you have to analysis these formula to make out **what kind of aircraft have the highest possibilty to get a highest score**, thus optimizations and sensitivity analysis are usuallt involved.

The crucial part of the match is to analysis the core formula. A large aircrafts can carry more payload and ,more likely to get a higher score for Mission 3, while it will have a large $$EWmax$$ henc large $$RAC$$. By contrast, a lighter aircraft may be able to fly faster to get a better score at Mission 2, but it will not tend to behave will in mission 3. 

In conclusion, differnt type of aircrafts will get different scores in missions, and there's no obvious one that can get the highest score in multiple missions, a design optimization is expected to be carried out.


## Approaches: How could PyADAO be helpful for the design
In the initial design stage, a low fidelity solver is chosen as it can provide an result that is fast enough and with not too bad accuracy. Thus the AVL was used as the flow solver, different configurations were provided as candidates and analysised by a score model, which has a sub optimization process in it (Mixed Integer Nonlinear Optimization), the whole process was driven by a parallel partical swarm method to find a better one.

As illustrated bellow, the whole optimization process was built as a case in PyADAO and thanks to that the solver and optimizer was all implemented in the framework, the total code lines is within 1k.
![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/AIAA_DBF/framework.png?raw=true)
Also, the formulation of geometry paramters are rubost enough so that all the two wings confirguation, such as tandem wing and carnard wing, are included in the design space.
A glance of optimization candidates is shown below:


## Projects Outcome&Highlights
Test Fly:

![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/AIAA_DBF/P1.png?raw=true)

