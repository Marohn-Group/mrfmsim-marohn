Experiment
==========

**single spin:**

.. .. autosummary::

..     mrfmsim_marohn.experiment.cermitesr_singlespin

See how experiments are tested:
:ref:`experiment tests <tests_experimental_section>`

Experiment Protocol: Spin Noise
-------------------------------

In this package we implement in Python the protocol outlined in the supporting 
information of Longenecker [#Longenecker2012oct]_ for determining the
small-ensemble force variance signal in a cyclic modulation NMR-MRFM 
experiment.

.. .. autosummary::
    
..     mrfmsim_marohn.experiment.ibmcyclic
..     mrfmsim_marohn.formula.polarization.rel_dpol_arp_ibm




.. .. autosummary::
    
..     mrfmsim_marohn.experiment.cermitarp_smalltip
..     mrfmsim_marohn.formula.field.xtrapz_field_gradient

The single-slice simulation is quite 
slow because, essentially, a full magnetic field and field gradient simulation 
must be done for each :math:`\theta`.  If you approximate the :math:`\theta` 
integral using (only!) 32 points, then the simulation will take 32 times 
longer to run than single simulation.  Since the :math:`x(\theta)` values are 
*not* equally spaced, you cannot simplify the integral by translating the 
:math:`x` coordinates.


.. John's :ref:`intermittent irradiation <theory_irradation_section>` experiments 
.. also implemented:

**Intermittent irradiation**

.. .. autosummary::
    
..     mrfmsim_marohn.experiment.cermitesr_periodirrad_stationarytip


**Cornell-style frequency-shift** [#Garner2004jun]_

.. .. autosummary::
    
..     mrfmsim_marohn.experiment.cermitarp
..     mrfmsim_marohn.experiment.cermitnut


**IBM-style cyclic-inversion** [#Degen2009jan]_ [#Longenecker2012oct]_

.. .. autosummary::
    
..     mrfmsim_marohn.experiment.ibmcyclic

**Cornell-style cyclic saturation ESR** [#Moore2009dec]_ [#Issac2016feb]_
[#Lee2012apr]_

There are two different versions of this experiment to simulate:

1. an experiment employing a large spherical magnetic tip (radius :math:`r
   \sim 2 \: \mu \mathrm{m}`).
2. an experiment employing a small spherical magnetic tip (radius :math:`r =
   100 \; \mathrm{nm}`).

The cyclic-saturation experiment has a few important differences from the
NMR experiments previously described include:

- the cantilever motion cannot be neglected and actually (partially)
  determines the volume of spins in resonance as the cantilever motion sweeps
  out the resonant slice
- the magnetization is determined by the Bloch equations

**Large tip approximation**

.. .. autosummary::
    
..     mrfmsim_marohn.experiment.cermitesr

- In practice, spins are saturated with a microwave pulse every n cantilever
  cycles. This saturation is modulated with a time of no microwave pulses
  to generate a modulated cantilever frequency shift detected via lock-in
  detection.
- For this simulation, we can calculate the spin-dependent frequency shift 
  experiments by the cantilever using

.. math::

    \Delta f = - \frac{f_c}{2 k} \sum_j \mu_z(\vec{r}_j) \frac{\partial^2
    B_z^{\mathrm{tip}}( \vec{r}_j )}{\partial x^2}

  which is valid when the tip radius is much smaller than the zero-to-peak
  the amplitude of the cantilever oscillation. Where :math:`f_c` is the cantilever resonance

- At a fixed cantilever position in this ESR-CERMIT experiment, the
  magnetization distribution :math:`\mu_z( \vec{r} )` depends on the frequency
  :math:`f_{\mathrm{rf}}` and strength :math:`B_1` of the microwave field, the
  sample relaxation times (:math:`T_1` and :math:`T_2`), the sample spin
  density, the applied magnetic field :math:`B_0`, and the tip magnetic field
  :math:`B_z^{\mathrm{tip}}`.
- As the cantilever moves it sweeps over a region of saturated spins that we 
  must sum over to obtain the signal. We must include these cantilever motion 
  effects in our simulations.

**Small tip approximation**

In the small tip experiment, the cantilever amplitude may not be assumed small 
when compared to the tip radius. We therefore must evaluate the full integral 
given by Lee, *et al.*.

.. .. autosummary::
    
..     mrfmsim_marohn.experiment.cermitarp_smalltip
..     mrfmsim_marohn.experiment.cermitesr_smalltip

**Cornell Single Spin ESR**

.. .. autosummary::
    
..     mrfmsim_marohn.experiment.cermitesr_singlespin

**Additional Experiments**

.. .. autosummary::
    
..     mrfmsim_marohn.experiment.cermitesr_stationarytip
..     mrfmsim_marohn.experiment.cermitesr_periodirrad_stationarytip

Reference
----------


.. [#Garner2004jun] Garner, S. R.; Kuehn, S.; Dawlaty, J. M.; Jenkins, N. E. &
    Marohn, J. A.  "Force-Gradient Detected Nuclear Magnetic Resonance" *Appl. 
    Phys. Lett.*, **2004**, *84*, 5091 - 5093
    [`10.1063/1.1762700 <http://dx.doi.org/10.1063/1.1762700>`__].

.. [#Moore2009dec] Moore, E. W.; Lee, S.-G.; Hickman, S. A.; Wright, S. J.; 
    Harrell, L. E.; Borbat, P. P.; Freed, J. H. & Marohn, J. A. "Scanned-Probe 
    Detection of Electron Spin Resonance from a Nitroxide Spin Probe", *Proc. 
    Natl. Acad. Sci. U.S.A.*, **2009**, *106*, 22251 - 22256 
    [`10.1073/pnas.0908120106 <http://doi.org/10.1073/pnas.0908120106>`__].

.. [#Moore2009] Moore, E. W. & Marohn, J. A. *Unpublished calculation*, 
    **2009**.

.. [#Lee2012apra] Lee, S.-G.; Moore, E. W. & Marohn, J. A. "A Unified Picture 
    of Cantilever Frequency-Shift Measurements of Magnetic Resonance", 
    *Phys. Rev. B*, **2012**, *85*, 165447 
    [`10.1103/PhysRevB.85.165447 <http://doi.org/10.1103/PhysRevB.85.165447>`__].  

.. [#Lee2012note] Equation 20 in Lee *et al.* **2012** is off by a factor of 
    :math:`-1`.  We give the correct equation above.

.. [#Rugar2004jul] Rugar, D.; Budakian, R.; Mamin, H. J. & Chui, B. W. "Single 
    Spin Detection by Magnetic Resonance Force Microscopy", *Nature*, **2004**
    , *430*, 329 - 332 
    [`10.1038/nature02658 <http://dx.doi.org/10.1038/nature02658>`__].

.. [#Wago1998jan] Wago, K.; Botkin, D.; Yannoni, C. & Rugar, D. 
    "Force-detected Electron-spin Resonance: Adiabatic Inversion, Nutation, 
    and Spin Echo", *Phys. Rev. B*, **1998**, *57*, 1108 - 1114 
    [`10.1103/PhysRevB.57.1108 <http://doi.org/10.1103/PhysRevB.57.1108>`__].

.. [#Klein2000aug] Klein, O.; Naletov, V. & Alloul, H. "Mechanical Detection 
    of Nuclear Spin Relaxation in a Micron-size Crystal", *Eur. Phys. J. B*, 
    **2000**, *17*, 57 - 68 
    [`10.1007/s100510070160 <http://dx.doi.org/10.1007/s100510070160>`__].

.. [#Baum1985dec] Baum, J.; Tycko, R. & Pines, A. "Broadband and Adiabatic 
    Inversion of a Two-level System by Phase-modulated Pulses", *Phys. Rev. A*
    , **1985**, *32*, 3435 - 3447 
    [`10.1103/PhysRevA.32.3435 
    <http://dx.doi.org/10.1103/PhysRevA.32.3435>`__].

.. [#Kupce1996feb] Kupce, E. & Freeman, R. "Optimized Adiabatic Pulses for 
    Wideband Spin Inversion", *Journal of Magnetic Resonance, Series A*, 
    **1996**, *118*, 299 - 303
    [`10.1006/jmra.1996.0042 <http://dx.doi.org/10.1006/jmra.1996.0042>`__].

.. [#Degen2009jan] Degen, C. L.; Poggio, M.; Mamin, H. J.; Rettner, C. T. & 
     Rugar, D. "Nanoscale Magnetic Resonance Imaging", *Proc. Natl. Acad. 
     Sci. U.S.A.*, **2009**, *106*, 1313 - 1317 
     [`10.1073/pnas.0812068106 <http://dx.doi.org/10.1073/pnas.0812068106>`__].

.. [#Longenecker2012oct] Longenecker, J. G.; Mamin, H. J.; Senko, A. W.; Chen, 
    L.; Rettner, C. T.; Rugar, D. & Marohn, J. A. "High-Gradient
    Nanomagnets on Cantilevers for Sensitive Detection of Nuclear
    Magnetic Resonance", *ACS Nano*, **2012**, *6*, 9637 - 9645
    [`10.1021/nn3030628 <http://dx.doi.org/10.1021/nn3030628>`__].

.. [#Issac2016feb] Isaac, C. E.; Gleave, C. M.; Nasr, P. T.; Nguyen, H.L.; 
    Curley, E. A.; Yoder, J.L.; Moore, E. W.; Chen, L & Marohn, J. A.
    "Dynamic nuclear polarization in a magnetic resonance force microscope 
    experiment", *Phys. Chem. Chem. Phys.*, **2016**, *18*, 8806
    [`10.1039/c6cp00084c <http://dx.doi.org/10.1039/c6cp00084c>`__].

.. [#Lee2012apr] Lee, S. G.; Moore, E. W.; & Marohn, J. A. "Unified picture of 
    cantilever frequency shift measurements of magnetic
    resonance", *Phys. Rev. B*, **2012**, *85*, 165447
    [`10.1103/PhysRevB.85.165447 <doi.org/10.1103/PhysRevB.85.165447>`__].


:py:mod:`experiment` module
---------------------------

.. automodule:: mrfmsim_marohn.experiment
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:

.. autofunction:: mrfmsim_marohn.experiment.IBMCyclic
.. experiment:: mrfmsim_marohn.experiment.IBMCyclic

.. autodata:: mrfmsim_marohn.experiment.CermitTDCollection
.. collection:: mrfmsim_marohn.experiment.CermitTDCollection

.. autodata:: mrfmsim_marohn.experiment.CermitESRCollection
.. collection:: mrfmsim_marohn.experiment.CermitESRCollection

.. autodata:: mrfmsim_marohn.experiment.CermitESRSingleSpinCollection
.. collection:: mrfmsim_marohn.experiment.CermitESRSingleSpinCollection

