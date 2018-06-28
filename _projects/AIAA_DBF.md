---

title: Design Optimization of an aircraft for AIAA Deisgn·Build·Fly Competition
collection: projects
layout: archive
date: 2018-05-11
author_profile: True
excerption: An aircraft design optimnization was performed for [AIAA DBF](https://www.aiaadbf.org/General-Info/ "AIAA DBF") . The [score model](https://www.aiaadbf.org/Scoring/ "score model") of the competition draw special concern as that both geometry paramters and mission performance were involved in, and the contradiction of these parameters speified that a design optimization must be performed.  An aircraft preliminary design coupled with mission planning framework was built based on [PyADAO](https://tsingqaq.github.io/projects/PyADAO_construction/ "PyADAO") to find a design that could get the highest score. A tandem wing configuration was found for the final design.
permalink: /projects/AIAA_DBF/
---

![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/gitmap.png?raw=true)

The development of PyADAO has moved to concentrate on optimization methods as I am currently working on this. While there're many interesting TODO list in model builder, low fidelity solver and APIs, to name a few. PyADAO is planned to be opensource in the near future, there are some issues like installation and docs that are not fully prepared for the release of its 0.1 Version. If this projects could fulfil some needs for you or you are also interested in building a similar project, feel free to contact me:)
{: .notice--success}

## Motivation&Backgrounds
Besides the introduction in <a href="https://tsingqaq.github.io/projects/" target="_blank"><font color="blue">projects page</font></a>
, the construction of PyADAO could also be help of :
* Providing a platform for aircraft design optimizations
* Learning and implementing aircraft optimization ralated theories
* Learning and practice Python programming language

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


## Competition Highlights

            
### 科学公式 TeX(KaTeX)
                    
$$E=mc^2$$

行内的公式$$E=mc^2$$行内的公式，行内的$$E=mc^2$$公式。

$$\(\sqrt{3x-1}+(1+x)^2\)$$
                    
$$\sin(\alpha)^{\theta}=\sum_{i=0}^{n}(x^i + \cos(f))$$

多行公式：

```math
\displaystyle
\left( \sum\_{k=1}^n a\_k b\_k \right)^2
\leq
\left( \sum\_{k=1}^n a\_k^2 \right)
\left( \sum\_{k=1}^n b\_k^2 \right)
```

```katex
\displaystyle 
    \frac{1}{
        \Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{
        \frac25 \pi}} = 1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {
        1+\frac{e^{-6\pi}}
        {1+\frac{e^{-8\pi}}
         {1+\cdots} }
        } 
    }
```

```latex
f(x) = \int_{-\infty}^\infty
    \hat f(\xi)\,e^{2 \pi i \xi x}
    \,d\xi
```
                
### 绘制流程图 Flowchart

```flow
st=>start: 用户登陆
op=>operation: 登陆操作
cond=>condition: 登陆成功 Yes or No?
e=>end: 进入后台

st->op->cond
cond(yes)->e
cond(no)->op
```
                    
### 绘制序列图 Sequence Diagram
                    
```seq
Andrew->China: Says Hello 
Note right of China: China thinks\nabout it 
China-->Andrew: How are you? 
Andrew->>China: I am good thanks!
```

### End
