---
title: 'Direct Lift Control (DLC) of a Box-wing aircraft'
collection: projects
layout: archive
date: 2016-05-11
author_profile: True
excerpt: Box wing aircraft have several appealing advanteages like siginicantlty reduced wingspan and more compact wing structures. Besides, the existence of the two wings have also introduces the capability of direct lift control(DLC). To explore the potential value of this and gain knowledges about box wing design. a team was built and a <a href="https://baike.baidu.com/item/%E5%9B%BD%E5%AE%B6%E5%A4%A7%E5%AD%A6%E7%94%9F%E5%88%9B%E6%96%B0%E6%80%A7%E5%AE%9E%E9%AA%8C%E8%AE%A1%E5%88%92 ">National University Student Innovation Program</a> was applied to fund the research. Several box wing aircrafts was design and built. A DFC control Law was also designed by parametric identifications based on flight tests. DFC flight tests were performed and the data was analyzed. It was shown that the DFC for box wing aircraft has potential values for overload controls like gust alleviation, while it has limited capablity to change the trajectory of the aircraft as the control force will soon be cancelled out by the change of aircraft angle of attack. **[read more](/projects/DLC_boxwing/)**
permalink: /projects/DLC_boxwing/
---


## Blingbling: This page is under construction:)

![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/DLC/DLC.jpg?raw=true)

## Motivations
* Figure out how much benifits a box wing aircraft can acquire from DLC
* Learn how to design an aircraft(Including aerodynamic design and structure design processes)
* Learn how the aircraft can be controlled by flight control systems
* Get some usage experience on relative softwares
* Learn how to work as a team to solve a problem


## Role&Responsibility

* Aerodynamic design of the box wing aircraft
* Structure design of the wings
* Deesign the control law of direct lift control and vallidate it through simulation
* Design the dirct lift Control experiments
* Analyze flight data and conclude the experiment. 

## Challenges & Proposed Solutions
### Challenges: Large computational consumptions

While providing a relative accurate results, a cruicial deficiency of CFD is the large computational consumption, i.e, long time to run. The expense of computation is directly related to the grids number: a typical calculation will last hours to days on workstation or cluster. Which means that traditional global optimization methods like GA, PSO are imposible to handle this questions for the large number of function calls.

### Proposed Solutions:
#### Momentum Source Concept

As stated before, one way to reduce the computational cost is to reduce the grids number, while still provied accurate methods. Thus we have chosen the momentum source concept (MSC) to model the propellers, in which the propeller is treated as source terms added in the governing equations so that no complex 3D propeller body grids are needed. MSC give a good prediction at relative low cost, and thanks to the periodic flow condition in hovering condition, the total grids number can be reduced one step further. 
PS. The constructing of MSC was not my work, further talks about this is beyond the scope to this short introduction,  

#### Gradient Based (Adjoint) Methods

Gradient optimizers can significantly reduce the number of function calls as they search for local optimums. In addition, the proposition of adjoint method in CFD has dramatically enhanced the usage of gradient base methods as the gradient can be calculated with no more CFD calls. The gradient based methods provide fast optimizations, while a local optimum was more likely to be found instead of a global one. 

#### Surrogate Based Optimization

Another perfect way to treat expensive black box optimization is to use <a href="https://en.wikipedia.org/wiki/Bayesian_optimization"><font color="blue">Baysian Optimization</font></a>, or surrogate based optimization (SBO). The <a href="https://en.wikipedia.org/wiki/Surrogate_model"><font color="blue">surrogate model</font></a> can be built with modern design of experiment methods which require limited number of function calls, and an optimization can then be performed with some sequential design strategies, i.e, Expected Improvement infill criteria, to find an optimum. Many SBO methods like <a href="https://en.wikipedia.org/wiki/Kriging"><font color="blue">Kriging</font></a> have been widely used in aerodynamic optimization and these methods give promising results.


## Optimization Framework

An optimization framework was constructed as follows, the initial samples were provided by <a href="https://en.wikipedia.org/wiki/Latin_hypercube_sampling"><font color="blue">Latin Hypercube Sampling (LHS)</font></a> method, and the expected improvement (EI) and minimum surrogate prediction (MSP) infill criteria were used in sequential design process. A max iteration number and minimum EI were set as the convergence check methods.

&ensp;&ensp;<img  src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/ducted%20fan%20optimization%20framework.png?raw=true"/>

### optimization problems



## Projects Outcome&Highlights
Optimal propeller on our third generation double ducted fan
![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/3nd%20propeller.png?raw=true)

We're in the experiments
![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/inexp2.JPG?raw=true)

## Final thoughts


