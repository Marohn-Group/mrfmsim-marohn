Overview
==========

A number of methods have been devised for detecting spin magnetic resonance 
using a cantilever. The methods are different enough that numerically 
calculating the effect of the spins on the cantilever requires a distinct 
approach for each method. We are most interested in simulating the signal from 
Degen *et al.* [#Degen2009jan]_ and Longenecker *et al.* [#Longenecker2012oct]_
experiments.

In these experiments, adiabatic rapid passages were used to repeatedly invert 
the sample's spin magnetization in time with the natural oscillation period of 
the cantilever. The modulated spin magnetization interacted with a magnetic 
field gradient to produce a resonant force that excited the cantilever. The 
cantilever position was observed with a lock-in detector; spin resonance was 
registered as a change in the *amplitude* of the cantilever oscillation. In 
the experiments cited above, the number of spins in resonance was so small 
that the spin fluctuations exceeded the average thermal spin polarization. In 
this small-ensemble limit, nuclear magnetic resonance (NMR) was detected as a 
change in the *variance* of the cantilever position fluctuations observed in 
the in-phase channel of the lock-in detector.

- :doc:`experiment <experiment>`: summarizes all the experimental method
- :doc:`polarization <theory>`: summarizes polarization and magnetization calculations
- :doc:`Trapezoid Integration <simulation>`: summarizes using Trapezoid integration
  to calculate the field change during cantilever motion.


**Reference**

.. [#Degen2009jan] Degen, C. L.; Poggio, M.; Mamin, H. J.; Rettner, C. T. & 
    Rugar, D. "Nanoscale Magnetic Resonance Imaging", *Proc. Natl. Acad. Sci. 
    U.S.A.*, **2009**, *106*, 1313 - 1317
    [`10.1073/pnas.0812068106 <http://dx.doi.org/10.1073/pnas.0812068106>`__].

.. [#Longenecker2012oct] Longenecker, J. G.; Mamin, H. J.; Senko, A. W.; Chen, 
    L.; Rettner, C. T.; Rugar, D. & Marohn, J. A. "High-Gradient Nanomagnets 
    on Cantilevers for Sensitive Detection of Nuclear Magnetic Resonance", 
    *ACS Nano*, **2012**, *6*, 9637 - 9645 
    [`10.1021/nn3030628 <http://dx.doi.org/10.1021/nn3030628>`__].









