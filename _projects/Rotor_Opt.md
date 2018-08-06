---
layout: archive
collection: projects
title: Propeller Optimization of ducted fan VTOL Aircrafts 
excerpt: A design optimization was carried out on ducted fan propellers, chord and twist distribution was parametrized by quadratic spline method. An optimization problem was formulated to find a better hovering efficiency configuration subjecting to a thrust constraint. The analysis was carried out by Computational Fluild Dynamics(CFD) with the help of Kirging surrogate based optimization method. The output propeller and newly designed energy system can carry the UAV to fly above 4000 meters altitude **[read more](/projects/Rotor_Optimization/)**
date: 2018-01-15
permalink: /projects/Rotor_Optimization/
author_profile: True
---


![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/bo.png?raw=true)

## Backgrounds

Ducted fan is the kind of configuration that a propeller is mounted in a duct so that a thrust augmentation can be obtained. Besides, the existence of the duct brings with extra advantages like improved safety and reduced noise. This configuration has been proposed and developed for more than half a century and still shows growing concern on many appilacations, like <a href="https://en.wikipedia.org/wiki/Micro_air_vehicle"><font color="blue">MAV</font></a>, <a href="https://en.wikipedia.org/wiki/Flying_car"><font color="blue">flying cars</font></a> and fan in wing configurations.
  
Our lab's second generation double ducted aircrafts are able to fly smoothly in the air, while the main drawback of this aircraft comes from the two blade commercial propeller which was originally used for fixed wing aircrafts, this less efficienct propeller significantly reduces the endurance time of the aircraft. In order to prolong the time in air and make the UAV flies above an elevation of 4000 meters, a design optimization of propellers was carried out.

![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/double%20ducted%20fan.png?raw=true)

## Role&Responsibility

* Design and conduct a force&moment test experiment to validate the computational fluid dynamics (CFD) methods
* Implement an optimization processes and validate the code through <a href="https://en.wikipedia.org/wiki/Test_functions_for_optimization"><font color="blue">numerical benchmark functions</font></a>
* Construct the main optimization framework
* Conduct sensitivity analysis of the optimal output

## Challenges & Proposed Solutions
### Challenges: Large computational consumptions

While providing a relative accurate results, a cruicial deficiency of CFD is the large computational consumption, i.e, long time to run. The expense of computation is directly related to the grids number: a typical calculation will last for hours to days on workstation or cluster. Thus traditional global optimization methods like GA, PSO are impossible to handle these questions for the large number of function calls.

### Proposed Solutions:
#### Momentum Source Concept

As stated before, one way to reduce the computational cost is to reduce the grids number, while still maintain an accaptable accuracy. Thus we have chosen the momentum source concept (MSC) to model the propellers, in which the propeller is treated as source terms added in the governing equations so that no complex 3D propeller body grids are needed. MSC give a good prediction at relative low cost, and thanks to the periodic flow condition in hovering condition, the total grids number can be reduced one step further. 
PS. The constructing of MSC was not my work, so further talks about this is beyond the scope to this short introduction,  

#### Gradient Based (Adjoint) Methods

Gradient optimizers can significantly reduce the number of function calls as they search for local optimums. In addition, the proposed adjoint method in CFD has dramatically enhanced the usage of gradient base methods as the gradient can be calculated with no more CFD calls. The gradient based methods provide fast optimizations, nevertheless, a local optimum was more likely to be found instead of a global one. 

#### Surrogate Based Optimization

Another perfect way to treat expensive black box optimization is to use <a href="https://en.wikipedia.org/wiki/Bayesian_optimization"><font color="blue">Baysian Optimization</font></a>, or surrogate based optimization (SBO). The <a href="https://en.wikipedia.org/wiki/Surrogate_model"><font color="blue">surrogate model</font></a> can be built with modern design of experiment(DOE) methods which require limited number of function calls, and an optimization can then be performed with some sequential design strategies, e.g, Expected Improvement infill criteria, to find an optimum. Many SBO methods like <a href="https://en.wikipedia.org/wiki/Kriging"><font color="blue">Kriging</font></a> have been widely used in aerodynamic optimization and these methods give promising results.


## Optimization Framework

An optimization framework was constructed as follows, the initial samples were provided by <a href="https://en.wikipedia.org/wiki/Latin_hypercube_sampling"><font color="blue">Latin Hypercube Sampling (LHS)</font></a> method, and the expected improvement (EI) and minimum surrogate prediction (MSP) infill criteria were used in sequential design process. A max iteration number and minimum EI were set as the convergence check methods.

&ensp;&ensp;<img  src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/ducted%20fan%20optimization%20framework.png?raw=true"/>

### optimization problems




$$Minimize -FM $$

$$s.t  \: X$$

$$w.r.t \: T_{opt}>=T_{baseline}$$

Notes  

1 FM: figure of merit (denote the hover efficiency of ducted fan)

2 X: propeller geometry design variables

3 T_opt: optimized propeller thrust

4 T_baseline: baseline propeller thrust


## Projects Outcome&Highlights
Optimal propeller on our third generation double ducted fan
![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/3nd%20propeller.png?raw=true)

In experiments
![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/inexp2.JPG?raw=true)


