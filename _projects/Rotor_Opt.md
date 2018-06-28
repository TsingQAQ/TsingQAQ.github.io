---
layout: archive
collection: projects
title: Propeller Optimization of ducted fan VTOL Aircrafts 
excerption: A design optimization was carried out on ducted fan propellers, chord and twist distribution was parametrized by quadratic spline method. An optimization problem was formulated to find a better hovering efficiency such that the thrust was constriant. The analysis was carried out by Computational Fluild Dynamics with the help of Kirging surrogate based optimization method. The output propeller and newly designed energy system could carry the UAV to fly above 4000 m elevation
collection: projects
date: 2018-01-15
permalink: /projects/Rotor_Optimization/
author_profile: True
---


![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/gitmap.png?raw=true)

## Backgrounds

Ducted fan is a configurtaion propeller mounted in a duct so that a thrust augmentation can be obtained. Also, the existence of the duct brings with extra advantages like improved safety and low noise. These configurations have been propsed and developed for more than half a century and still shows growing concern on many appilacations, like <a href="https://en.wikipedia.org/wiki/Micro_air_vehicle"><font color="blue">MAV</font></a>, <a href="https://en.wikipedia.org/wiki/Flying_car"><font color="blue">flying cars</font></a> and fan in wing configurations.
  
Our lab's second generation double ducted aircrafts flies smoothly in the air, while the main drawback of this aircrafts is the two blade commercial propeller which was used for fixed wing aircrafts, this low efficienct propeller significantly affect the endurance time of the aircrafts. In order to prolong the time in air and fly above 4000 meters elevation, a design optimization of propellers was carried out.

![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/double%20ducted%20fan.png?raw=true)

## Role&Responsibility

* design and conduct an force&moment test to validate the computational fluid dynamics (CFD) methods
* build an optimization processes and validate the code through numerical benchmark functions
* construct the main optimization framework
* Sensitivity analysis of the optimize output

## Difficulties and Approaches
### Difficulties: Large computational consumptions

While providing a relative accurate results, a cruicial deficiency of CFD is the large computational consumption, i.e, long time to run. And the consumption are directly related to the grids number, a typical calculation will last hours to days, even on workstation or cluster. Which means that a traditional global optimization methods like GA, PSO is imposible for the large number of function calls.

### Approches:
#### Momentum Source Conecept

As stated before, one way to reduce the computational cost is to reduce the grids number, while still provied accurate methods. Thus we have chosen the momentum source concept (MSC) to model the propellers, in which the propeller is treated as source terms added in the governing equations so that no complex 3D propeller body grids are needed. MSC give a good prediction at relative low cost, and thanks to the periodic flow condition in hovering, the total grids number can be reduced step further. As the constructing of MSC was not my work, further talks about this is beyond the scope to this introduction,  
#### Surrogate Based Optimization



## Optimization Framework
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

![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/RO/3nd%20propeller.png?raw=true)
