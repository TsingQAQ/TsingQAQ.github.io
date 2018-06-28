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

## PyADAO capabilities
### Moldel Builder
### Moldel Builder
PyADAO was capable of building different fidelity of aircraft geometries and airfoils, from low fidelity data to CAD models(supported by PythonOCC). And the code was specially designed for the easy construction.
### Solver 
PyADAO now wrapped AVL and Xfoil, and also has some zero fidelity(emprical) solvers for performance analysis. And I am going to connect it to some high fidelity solvers like Fluent and SU2.
### Capability demonstration: 
Instead of giving a lengthy abstract description about the function, here's a case provided to see how PyADAO's able to construct the wing geometry of DLR F4 aircraft:

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
# TODO: 对DLR_F4进行一个比较精确的建模，并将计算结果与DLR_F4的数据进行一个对比，也算是一个Validation

'''
DLR F4 机翼建模
程序引用附录:
[1] A Selection of Experimental Test Cases for the Validation of CFD Codes
[2] Drag Predictionfor the DLR-F4Wing/Body usingOVERFLOWandCFL3D on an Overset Mesh
[3] A comparison of Experimental Results for the Transonic Flow around the DFVLR-F-4 Wing Body Configuration: Final Report
'''
# 一些引用参数:
Span = 0.5857 * 2 * Unit['m']   # 来源: [1]
Ref_area = 0.1454 * Unit['m^2']  # 来源: [1]
MAC = 0.1412  # 来源: [1]


# 已设置
def Sweep_Func(Epsilon):
    """
    前缘后掠角函数； 27.1 deg 来源: [1]
    :param Epsilon:
    :return:
    """
    return 27.1


# 已设置
def Dihedral_Func(Epsilon):
    """
    上反角构建函数，注意是角度制 来源: [1].Fig 1
    :param Epsilon:
    :return:
    """
    return 4.8


def Airfoil_Func(Epsilon):
    """
    翼型构建函数
    展向站位数据 来源: [1]
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
    展向站位数据与翼型函数来源一致
    翼型及弦长数据来源:
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


# 说明: 由于翼型里面包含了位移，旋转，在消除位移后保持安装角为0即可
def Incidence_Angle(Epsilon):
    """
    数据来源:  目测自 [3] Fig. 3
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


from Model_Builder.Airfoil.Airfoils import Foil_Containers, Selig_Airfoil
DLR_F4_DEF_1 = Selig_Airfoil('DLR F4 DEF1')
DLR_F4_DEF_2 = Selig_Airfoil('DLR F4 DEF2')
DLR_F4_DEF_3 = Selig_Airfoil('DLR F4 DEF3')
DLR_F4_DEF_4 = Selig_Airfoil('DLR F4 DEF4')
DLR_F4_Foil_checker = Foil_Containers(DLR_F4_DEF_1, DLR_F4_DEF_2, DLR_F4_DEF_3, DLR_F4_DEF_4)
DLR_F4_Foil_checker.show_foils()

# ===========机翼建模==============
DLR_F4_Wing = Wing(name='DLR_F4_Wing')

# 下面这个表示在这几个位置会构建翼型
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


# ========== 机身建模  ================
'''
DLR_F4机身定义:
    从250 - 626 mm 都是直径为148.42 mm 的圆 来源:
'''
DLR_F4_Fuse = Fuselage_Geometry('DLR_F4_Fuse')
# TODO:  使用来源 [3] Fig. 5
lower_guide_curve = np.array([[0, -7.698], [35, -40], [200, -75], [250, -81.9], [626.76, -81.9], [800, -50],
                              [1000, -8], [1174, 38]]) * Unit['mm']
upper_guide_curve = np.array([[0, -7.698], [35, 20], [200, 66.512], [250, 66.512], [626.76, 66.512], [800, 66.512],
                              [1000, 66.512], [1174, 66.512]]) * Unit['mm']
DLR_F4_Fuse.add_lower_fuselage_guideCurve(lower_guide_curve)
DLR_F4_Fuse.add_upper_fuselage_guideCurve(upper_guide_curve)


# ===全机建模: 把机翼加入飞机===============
DLR_F4 = Aircraft_geometry('Flyxiang')
DLR_F4.add_surface(DLR_F4_Wing, apex=np.array([347, 0, 0]) * Unit['mm'])  # 该条代码运行正常
DLR_F4.add_fuselage(DLR_F4_Fuse)
DLR_F4.show_aircraft(high_fidelity=False)

# ===========================Define flight condition(for CFD analysis)=================
# 设置aero_solver运行飞行环境：
DLR_F4_Test_Phase = phase()
DLR_F4_Test_Phase.flight_altitude = 8000 * Unit['m']  # 高度参数必须在空速之前
DLR_F4_Test_Phase.air_speed_kph = 918 * Unit['Km/h']
# =====================================================================================


# ===============================Low fidelity CFD========================================
# =====================AVL========================
solver = builtin_solvers_lib.low_fidelity_solver(DLR_F4, 'AVL')  # 这条命令决定了如果Flyxiang发生更改，必须重新输入Flyxiang
solver.set_params2solve(['CL', 'e'])
solver.set_reference_param(Sref=0.1454 * Unit['m^2'], Cref=0.1412 * Unit['m'])
solver.set_flight_condition(DLR_F4_Test_Phase)
solver.init(write_fuselage=True)
solver.run()
CL = solver.post_process('CL')
e = solver.post_process('e')
print('DLR_F4 CL: {}, e: {}'.format(CL, e))
# 结束气动求解器运行: 一定要这句话!
solver.end()

# ==================== 封装的气动求解器函数 ===================
print('\nThe AVL method is can also be called by the followeing function:\n')
from Aerodynamics.Aero_Solver.solvers import Aircraft_coefficients_solver

CL_, e_ = Aircraft_coefficients_solver(DLR_F4, ['CL', 'e'], Sref=0.1454 * Unit['m^2'], Cref=0.1412 * Unit['m'],
                                       phase=DLR_F4_Test_Phase, write_fuselage=True)
print('DLR_F4 CL: {}, e: {}\n'.format(CL, e))

# ================== 计算纵向圈配平状态下: 0度攻角时候的静稳定裕度 ======================
from Flight_Dynamics.FC_Solver import Get_Trimmed_SM
print('Static Margin is: {}'.format(Get_Trimmed_SM(DLR_F4, DLR_F4_Test_Phase, MAC=0.1412 * Unit['m'])))
</pre>

<img src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/LF%20DLR%20F4.png?raw=true" alt="drawing" width="300px" height="250px"/> <img src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/HF%20DLR%20F4.png?raw=true" alt="drawing" width="300px" height="250px"/> 
<img
src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/CSM.png?raw=true" alt="drawing" width="300px" height="200px"/> 
<img
src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/tinny%20yellow.jpg?raw=true" alt="drawing" width="300px" height="200px"/>
<img
src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/RAE2822.png?raw=true" alt="drawing"/> 
## Projects Outcome
* The PyADAO has succesfully offered a platform for aircraft preliminary design and optimizations, and it has played a huge role in the [AIAA DBF](https://tsingqaq.github.io/projects/AIAA_DBF/) project. 
* The projects has also been awarded as a good conclusion in the final project measurement:
<img src="https://github.com/TsingQAQ/TsingQAQ.github.io/blob/master/images/PyADAO/jj.png?raw=true" alt="drawing" width="300px" height="450px"/> 

## Future of PyADAO
As 
