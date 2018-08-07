---
title: 'Construction of an aircraft design, analysis and optimization framework: PyADAO'
layout: archive
collection: projects
date: 2016-12-11
permalink: /projects/PyADAO_construction/
excerpt: The fast improvement of aerodynamic shape optimization methedologies (e.g geometric parametrization, Adjoint method, surrogate models) has introduced the change that many "state-of-the-art" methods can be used at the very beginning of an aircraft design, even in conceptual design process. While many opensource tools like [OpenMDAO](http://openmdao.org/), [SU2](https://su2code.github.io/) are widely used, a framework must be consturcted to properly wrap these tools and offer a flexible enviroments for design and optimization problem formulation. Thus a Python based aircraft design, analysis, optimization framework was consturcted. **[read more](/projects/PyADAO_construction/)**
author_profile: True
tags:
  - cool posts
  - category1
  - category2
---
![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/gitmap.png?raw=true)

The development of PyADAO has moved to concentrate on optimization methods as I am currently working on this. While there're many interesting TODO list in model builder, low fidelity solver and APIs, to name a few. PyADAO is planned to be opensource in the near future, there are some issues like installation and docs that are not fully prepared for the release of its 0.1 Version yet. If this projects could fulfil some needs for you or you are also interested in building a similar project, feel free to contact me:)
{: .notice--success}
## Motivation&Backgrounds
Besides the introduction in <a href="https://tsingqaq.github.io/projects/" target="_blank"><font color="blue">projects page</font></a>
, the construction of PyADAO could also be help of :
* Providing a platform for aircraft design optimizations
* Learning and implementing aircraft optimization ralated theories
* Learning and practice Python programming language

## Role&Responsibility
As the main (only) developer, currently I am responsible for the whole program. 

## Survey of related codes/software 
A survey was conducted to find the exist aircraft design optimization frameworks, some of them are listed in the following tables:

|| ![](http://suave.stanford.edu/images/logo.svg)  | ![](https://www.parapy.nl/wp-content/uploads/2016/08/parapy_logo_small@2x.png) |![](http://occ-airconics.readthedocs.io/en/latest/_images/cover.png) |<img src="http://www.aircraftdesign.ca/_images/software_pyacdt.png" alt="drawing" width="500px" height="70px"/> | 
| :------------: |:---------------:| :-----:|:-----:| :-----:| 
| Name | SUAVE| ParaPy |AirConics/occ-airconics| PyACDT | 
| Developer| <a href="http://suave.stanford.edu/" target="_blank"><font color="blue">Stanford</font></a> | <a href="https://www.parapy.nl/" target="_blank"><font color="blue">ParaPy Inc</font></a> | <a href="https://aircraftgeometrycodes.wordpress.com/airconics/" target="_blank"><font color="blue">Andra Sobester</font></a>; <a href="https://github.com/p-chambers/occ_airconics" target="_blank"><font color="blue">Paul Chamber</font></a>, etc| <a href="http://www.aircraftdesign.ca/software/pyacdt/pyacdt.html" target="_blank"><font color="blue">AAD Lab</font></a> & <a href="http://mdolab.engin.umich.edu/tags/pyacdt" target="_blank"><font color="blue">MDO lab</font></a>| 
| Focuses| inital design|  framework   |model generator| not known |
 |Code info |Python 2 <br> Heavy develop| Python | Python 3<br> Develop stopped| Python|
|Notes |opensource on github |Commercial |opensource on github |Lab use |

## Why Python
* Python is a programming language that lets you work quickly
and integrate systems more effectively
<p align="right">Python.org</p>

* Python excels at interfacing with other languages, making it particularly useful to wrap numerically intensive disciplinary computations which are usually implemented in C/C++ or Fortran
<p align="right">PyACDT <a href="https://arc.aiaa.org/doi/10.2514/6.2008-5955" target="_blank"><font color="blue">paper</font></a></p>
  
* Python’s combination of object oriented programming, duck typing, concise language, portability in open source, and community standard as glueware has driven our decision.
<p align="right">SUAVE <a href="https://arc.aiaa.org/doi/10.2514/6.2015-3087" target="_blank"><font color="blue">paper</font></a></p>

* "Lif is Short, you need Python"
<p align="right">Bruce Eckel</p>

Meanwile, many famous machine learning frameworks like <a href="https://github.com/keras-team/keras"><font color="blue">Keras</font></a>, <a href="https://github.com/tensorflow/tensorflow"><font color="blue">tensorflow</font></a>, <a href="http://scikit-learn.org/stable/index.html"><font color="blue">scikit-learn</font></a> are written (or at least the top level codes are written) in Python, which offers appleaing chances for implementing related machine learning algorithms in PyADAO

## PyADAO capabilities
### Moldel Builder
* Low fidelity data 
* CAD Model (PythonOCC)
* CATIA(Plan to do)

### Solver 
* <a href="http://web.mit.edu/drela/Public/web/avl/"><font color="blue">Athena Vortex Lattice (AVL)</font></a>
* <a href="http://web.mit.edu/drela/Public/web/xfoil/"><font color="blue">Xfoil</font></a>
* SU2(Plann to do)

### Numerical Optimization
* Some benchmark test functions
* Scipy provided optimizers (gradient base, etc)
* Genetic Alogorthms (Supported by <a href="https://github.com/aarongarrett/inspyred"><font color="blue">Inspyred</font></a>)
* Partical Swarm (several variants are included)
* ACO (<a href="http://www.midaco-solver.com/"><font color="blue">MIDACO</font></a> (limited version))

A benchmark optimization of <a href="https://en.wikipedia.org/wiki/Rosenbrock_function"><font color="blue">Rosenbrock</font></a> function (dimension: 10, variable range: [-10, 10] for each dimension) can be shown:

![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/opt.png?raw=true)

### Capability demonstration: 
Instead of giving a lengthy, abstract description about the framwork's function, here's a case provided to see how PyADAO's able to construct the wing geometry of <a href="https://www.google.com/search?rlz=1C2SQJL_zh-CNUS786US786&source=hp&ei=qU04W9q9D8v7vgSL_JHYCA&q=DLR+F4&oq=DLR+F4&gs_l=psy-ab.3..0i203k1l10.210.1171.0.1295.7.6.0.0.0.0.171.326.0j2.2.0....0...1c.1.64.psy-ab..5.2.324.0..0j35i39k1j0i131k1j0i67k1.0.JUtz8IP57Y4"><font color="blue">DLR F4</font></a> aircraft in an object orientive and robust way:


<pre style="height: 400px; overflow: scroll;">
import sys
from os.path import abspath, join, dirname, pardir

import numpy as np

from Aerodynamics.Aero_Solver import builtin_solvers_lib
from Builtins.Units import Unit
from Flight_Dynamics.Flight_Condition import phase
from Model_Builder.Aircraft_geo import Aircraft_geometry
from Model_Builder.Airfoil.Airfoils import Airfoil
from Model_Builder.Fuselage import Fuselage_Geometry
from Model_Builder.Main import Wing

sys.path.insert(0, abspath(join(dirname(__file__), pardir)))


'''
DLR F4 wing modeling
references:
[1] A Selection of Experimental Test Cases for the Validation of CFD Codes
[2] Drag Predictionfor the DLR-F4Wing/Body usingOVERFLOWandCFL3D on an Overset Mesh
[3] A comparison of Experimental Results for the Transonic Flow around the DFVLR-F-4 Wing Body Configuration: Final Report
'''
# some parameters:
Span = 0.5857 * 2 * Unit['m']   # source: [1]
Ref_area = 0.1454 * Unit['m^2']  # suorce: [1]
MAC = 0.1412  # source: [1]

# define wing geometric parameters:

def Sweep_Func(Epsilon):
    """
    27.1 deg source: [1]
    :param Epsilon:
    :return:
    """
    return 27.1


def Dihedral_Func(Epsilon):
    """
    unit: deg source: [1].Fig 1
    :param Epsilon:
    :return:
    """
    return 4.8


def Airfoil_Func(Epsilon):
    """
    airfoil datas at each loctaion
    source: [1]
    :param Epsilon:
    :return:
    """
    if Epsilon == 0.126:
        return Airfoil(Selig_Airfoil='DLR F4 DEF1')
    if Epsilon == 0.4:
        return Airfoil(Selig_Airfoil='DLR F4 DEF2')
    if Epsilon == 0.7:
        return Airfoil(Selig_Airfoil='DLR F4 DEF3')
    if Epsilon == 1.0:
        return Airfoil(Selig_Airfoil='DLR F4 DEF4')


def Chord_Func(Epsilon):
    """
    chord datas at each soan location
    :param Epsilon:
    :return:
    """
    if Epsilon == 0.126:
        return 202.13777 * Unit['mm']
    if Epsilon == 0.4:
        return 119.81715 * Unit['mm']
    if Epsilon == 0.7:
        return 90.23006 * Unit['mm']
    if Epsilon == 1.0:
        return 60.64112 * Unit['mm']


def Incidence_Angle(Epsilon):
    """
    source [3] Fig. 3
    :param Epsilon:
    :return:
    """
    if Epsilon == 0.126:
        return 4.4
    if Epsilon == 0.4:
        return 1.8
    if Epsilon == 0.7:
        return 0.98
    if Epsilon == 1.0:
        return -0.55


# ===========wing modeling==============
DLR_F4_Wing = Wing(name='DLR_F4_Wing')

# Yahudi break: 0.37
DLR_F4_Wing.Kinks_Position_list = [0.4]

DLR_F4_Wing.Build_Sections_location = np.array([0.126, 0.4, 0.7, 1])
DLR_F4_Wing.dihedral_angle = Dihedral_Func
DLR_F4_Wing.sweep_angle = Sweep_Func
DLR_F4_Wing.Airfoils = Airfoil_Func
DLR_F4_Wing.twist_angle = Incidence_Angle
DLR_F4_Wing.chord_length = Chord_Func
DLR_F4_Wing.Resolve_Wing(span_scale=0.5857, chord_scale=1)
DLR_F4_Wing.Build_Surface()
DLR_F4_Wing.show_surface(high_fidelity=True, duplicate=True)


# ===put the wing in to an aircraft instance===============
DLR_F4 = Aircraft_geometry('Flyxiang')
DLR_F4.add_surface(DLR_F4_Wing, apex=np.array([347, 0, 0]) * Unit['mm']) 
DLR_F4.add_fuselage(DLR_F4_Fuse)
DLR_F4.show_aircraft(high_fidelity=False)
</pre>

The code:

`DLR_F4.show_aircraft(high_fidelity=False)` 

will provide a low fidelity DLR F4 wing illustrated in the following picture.  

<img src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/LF%20DLR%20F4.png?raw=true" alt="drawing" width="300px" height="250px" style="width:50%;"/>   

If a high fidelity model is needed, just chang the defualt key word to True:

`DLR_F4.show_aircraft(high_fidelity=True)`

and you will get a CAD model by PythonOCC:

<img src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/HF%20DLR%20F4.png?raw=true" alt="drawing" width="300px" height="250px" style="width:50%;"/> 

After the construction of aircraft model, it can be simply used to calculate the aerodynamic coefficients:

<pre style="height: 300px; overflow: scroll;">
# ===========================Define flight condition(for CFD analysis)=================
DLR_F4_Test_Phase = phase()
DLR_F4_Test_Phase.flight_altitude = 8000 * Unit['m'] 
DLR_F4_Test_Phase.air_speed_kph = 918 * Unit['Km/h']
# =====================================================================================


# ===============================Low fidelity CFD========================================
# =====================AVL========================
solver = builtin_solvers_lib.low_fidelity_solver(DLR_F4, 'AVL')  
solver.set_params2solve(['CL', 'e'])
solver.set_reference_param(Sref=0.1454 * Unit['m^2'], Cref=0.1412 * Unit['m'])
solver.set_flight_condition(DLR_F4_Test_Phase)
solver.init(write_fuselage=True)
solver.run()
CL = solver.post_process('CL')
e = solver.post_process('e')
print('DLR_F4 CL: {}, e: {}'.format(CL, e))
solver.end()

# ==================== A more compact way to do similar work can be written as follows ===================
print('\nThe AVL method is can also be called by the followeing function:\n')
from Aerodynamics.Aero_Solver.solvers import Aircraft_coefficients_solver

CL_, e_ = Aircraft_coefficients_solver(DLR_F4, ['CL', 'e'], Sref=0.1454 * Unit['m^2'], Cref=0.1412 * Unit['m'],
                                       phase=DLR_F4_Test_Phase, write_fuselage=True)
print('DLR_F4 CL: {}, e: {}\n'.format(CL, e))

# ================== PyADAO have also implemented a Static Margin solver using AVL ======================
from Flight_Dynamics.FC_Solver import Get_Trimmed_SM
print('Static Margin is: {}'.format(Get_Trimmed_SM(DLR_F4, DLR_F4_Test_Phase, MAC=0.1412 * Unit['m'])))
</pre>

Some other images of PyADAO are illustrated here:

<img
src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/CSM.png?raw=true" alt="drawing" width="300px" height="200px" align="middle"/> 
<img
src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/tinny%20yellow.jpg?raw=true" alt="drawing" width="300px" height="200px" align="middle"/>
<img
src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/RAE2822.png?raw=true" alt="drawing" align="middle"/> 
## Projects Outcome
* The PyADAO has succesfully offered a platform for aircraft preliminary design and optimizations, and it has played a huge role in the [AIAA DBF](https://tsingqaq.github.io/projects/AIAA_DBF/) project. 
* The projects has also been awarded as a good conclusion in the final project measurement:
<img src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/jj.png?raw=true" alt="drawing" width="300px" height="450px"/> 

## Future of PyADAO
* Connect to high fidelity Solvers
* Fully Support the capability to build a fuselage (require some researches on relative parameterization methods)
* support <a href="https://en.wikipedia.org/wiki/CATIA"><font color="blue">CATIA CAD</font></a>
* Wrap latest optimization methos
![](https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/PyADAO_framwork.png?raw=true)

Notes: A detailed roadmap of PyADAO has been included in readme on bitbucket. The framework has changed its name to PyADASO, with the hope that Simulation capability is also included (plan to use <a href="http://jsbsim.sourceforge.net/"><font color="blue">JSBsim</font></a>), albiet that this is a long map. Feel free to contact me to get more details if you like this project.

