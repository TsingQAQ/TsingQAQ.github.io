---
layout: archive
collection: projects
title: Propeller Optimization of ducted fan VTOL Aircrafts 
excerption: A design optimization was carried out on ducted fan propellers, chord and twist distribution was parametrized by quadratic spline method. An optimization problem was formulated to find a better hovering efficiency such that the thrust was constriant. The analysis was carried out by Computational Fluild Dynamics with the help of Kirging surrogate based optimization method. The output propeller and newly designed energy system could carry the UAV to fly above 4000 m elevation
collection: projects
date: 2018-05-15
permalink: /projects/Rotor_Optimization/
author_profile: True
tags:
  - cool posts
  - category1
  - category2
---


![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/gitmap.png?raw=true)

## Backgrounds

Ducted fan is a configurtaion propeller mounted in a duct so that a thrust augmentation can be obtained. Also, the existence of the duct brings with extra advantages like improved safety and low noise. These configurations have been propsed and developed for more than half a century and still shows growing concern on many appilacations, like <a href="https://en.wikipedia.org/wiki/Micro_air_vehicle"><font color="blue">MAV</font></a>, <a href="https://en.wikipedia.org/wiki/Flying_car"><font color="blue">flying cars</font></a> and fan in wing configurations.
  


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

### Surrogate Based Optimization
The main different of DBF match and other aeronatical contest is the rules. Unlike many other competitions that the design goal is clearly specified, a series of score formula is provided for teams, and you have to analysis these formula to make out **what kind of aircraft have the highest possibilty to get a highest score**, thus optimizations and sensitivity analysis are usuallt involved.

The crucial part of the match is to analysis the core formula. A large aircrafts can carry more payload and ,more likely to get a higher score for Mission 3, while it will have a large $$EWmax$$ henc large $$RAC$$. By contrast, a lighter aircraft may be able to fly faster to get a better score at Mission 2, but it will not tend to behave will in mission 3. 

In conclusion, differnt type of aircrafts will get different scores in missions, and there's no obvious one that can get the highest score in multiple missions, a design optimization is expected to be carried out.


## Optimization Framework



## Projects Outcome&Highlights
Test Fly:

![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/AIAA_DBF/P1.png?raw=true)
