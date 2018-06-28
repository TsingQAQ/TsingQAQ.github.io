---
title: 'Construction of an aircraft design, analysis and optimization framework: PyADAO'
layout: archive
collection: projects
date: 2016-12-11
permalink: /projects/PyADAO_construction/
excerption: The fast improvement of aerodynamic shape optimization methedologies(i.e geometric parametrization, Adjoint method, surrogate models) has introduced the change that state-of-the-art methods can be used at the very beginning of an aircraft design, even in conceptual design processes. While many opensource tools like OpenMDAO, SUAVE, and SU2 are widely used, a framework must be consturcted to properly wrap these tools and offer a flexible enviroments for design and optimization problem formulation. Thus a Python based aircraft design, analysis, optimization framework was consturcted. A flying wing configuration drag(induced drag) reduce optimization was carried out to validate the code and a superior one was found.
author_profile: True
tags:
  - cool posts
  - category1
  - category2
---
![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/gitmap.png?raw=true)

The PyADAO 
{: .notice--success}
## Motivation&Backgrounds
Besides the introduction in [projects page](https://tsingqaq.github.io/projects/), the construction of PyADAO could also be help of :
* Providing a platform for aircraft design optimizations
* Learning and implementing aircraft optimization ralated theories
* Learning and practice Python programming language

## Survey of related codes/software 
A survey was conducted to find the exist aircraft design optimization frameworks, some of them are listed in the following tables:

|| ![](http://suave.stanford.edu/images/logo.svg)  | ![](https://www.parapy.nl/wp-content/uploads/2016/08/parapy_logo_small@2x.png) |![](http://occ-airconics.readthedocs.io/en/latest/_images/cover.png) |<img src="http://www.aircraftdesign.ca/_images/software_pyacdt.png" alt="drawing" width="500px" height="70px"/> | 
| :------------: |:---------------:| :-----:|:-----:| :-----:| 
| Name | SUAVE| ParaPy |AirConics/occ-airconics| PyACDT | 
| Developer| [Stanford](http://suave.stanford.edu/) | [ParaPy Inc](https://www.parapy.nl/) | [Andra Sobester](https://aircraftgeometrycodes.wordpress.com/airconics/); [Paul Chamber](https://github.com/p-chambers/occ_airconics), etc| [AAD Lab](http://www.aircraftdesign.ca/software/pyacdt/pyacdt.html) & [MDO lab](http://mdolab.engin.umich.edu/tags/pyacdt)| 
| Focuses| inital design|  framework   |model generator| not known |
 |Code info |Python 2 <br> Heavy develop| Python | Python 3<br> Develop stopped| Python|
|Notes |opensource on github |Commercial |opensource on github |Lab use |

## Why Python
* Python is a programming language that lets you work quickly
and integrate systems more effectively
<p align="right">Python.org</p>
* Python excels at interfacing with other languages, making it particularly useful to wrap numerically intensive disciplinary computations which are usually implemented in C/C++ or Fortran
<p align="right">PyACDT [paper](https://arc.aiaa.org/doi/10.2514/6.2008-5955)</p>
*  Python’s combination of object oriented programming, duck typing, concise language, portability in open source, and community standard as glueware has driven our decision.
<p align="right">SUAVE [paper](https://arc.aiaa.org/doi/10.2514/6.2015-3087)</p>

* "Lif is Short, you need Python"
<p align="right">Bruce Eckel</p>

## Challenges & Proposed Solutions

## Projects Outcome

## Projects Highlights
<img src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/LF%20DLR%20F4.png?raw=true" alt="drawing" width="300px" height="250px"/> <img src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/HF%20DLR%20F4.png?raw=true" alt="drawing" width="300px" height="250px"/> 
src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/HF%20DLR%20F4.png?raw=true" alt="drawing" width="300px" height="250px"/> 
## Future of PyADAO

