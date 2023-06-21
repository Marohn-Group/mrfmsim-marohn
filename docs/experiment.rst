Experiment
==========

.. Summary of experiments implemented in this package

.. **ensemble:**

.. .. autosummary::
    
..     mrfmsim_marohn.experiment.ibmcyclic
..     mrfmsim_marohn.experiment.cermitesr
..     mrfmsim_marohn.experiment.cermitesr_stationarytip
..     mrfmsim_marohn.experiment.cermitesr_periodirrad_stationarytip
..     mrfmsim_marohn.experiment.cermitnut
..     mrfmsim_marohn.experiment.cermitarp
..     mrfmsim_marohn.experiment.cermitarp_smalltip
..     mrfmsim_marohn.experiment.cermitesr_smalltip
..     mrfmsim_marohn.experiment.cermitesr_singlespin
..     mrfmsim_marohn.experiment.cermitesr_singlespin_approx
..     mrfmsim_marohn.experiment.cermittd
..     mrfmsim_marohn.experiment.cermittd_smalltip
..     mrfmsim_marohn.experiment.cermittd_singlepulse

**single spin:**

.. autosummary::

    mrfmsim_marohn.experiment.cermitesr_singlespin

See how experiments are tested:
:ref:`experiment tests <tests_experimental_section>`

Experiment Protocol: Spin Noise
-------------------------------

In this package we implement in Python the protocol outlined in the supporting 
information of Longenecker [#Longenecker2012oct]_ for determining the
small-ensemble force variance signal in a cyclic modulation NMR-MRFM 
experiment.

.. autosummary::
    
    mrfmsim_marohn.experiment.ibmcyclic
    mrfmsim_marohn.formula.polarization.rel_dpol_arp_ibm

Experiment Protocol: Frequency shift
------------------------------------

In Garner *et al.* [#Garner2004jun]_ and Moore *et al.* [#Moore2009dec]_ 
experiments, spin magnetization interacted with the second derivative of a 
magnetic field to produce a change in the cantilever's *frequency* of 
oscillation. This approach to detecting magnetic resonance was termed the 
CERMIT protocol, which stands for Cantilever-Enabled Readout of Magnetization 
Inversion Transients. 

In the Garner experiment [#Garner2004jun]_, nuclear spin magnetization was 
inverted once using a swept-frequency adiabatic rapid passage, and the 
resulting step-change in the cantilever frequency indicated nuclear spin 
resonance (NMR). In the Moore experiment [#Moore2009dec]_, electron spin 
magnetization was modulated slowly, by switching the spin-saturating 
microwaves on and off periodically. The cantilever oscillation was digitized 
and sent to a (software) frequency demodulator. The resulting 
frequency-versus-time data was fed to a (software) lock-in detector, operated 
with the microwave modulation trigger as the reference signal. A change in the 
lock-in output indicated electron spin resonance (ESR).  

To observe a change in the cantilever frequency, the cantilever in these 
experiments were driven into self-oscillation. In the presence of the tip field 
gradient, the motion of the cantilever led to a dithering of the resonance 
frequency of the spins in the sample. In the Moore experiment [#Moore2009dec]_,
microwave irradiation was applied at a fixed frequency and this dithering was 
used to sweep out a region of saturated electron spins below the tip. In the 
Garner experiment [#Garner2004jun]_, in contrast, the region of inverted 
magnetization swept out by the dithering of the tip was much smaller than the 
region of inverted spin magnetization created by sweeping the frequency of the 
applied radio frequency field.

In experiments like these involving a driven cantilever, the observed 
frequency shift depends on the amplitude of the cantilever oscillation and 
different equations are needed to calculate the spin signal in small-amplitude 
and large-amplitude limits. A unified set of equations describing 
frequency-shift experiments were derived from first principles [#Lee2012apra]_; 
those results are summarized below.

In this package we implement in Python the protocol for calculating the 
dc-NMR-CERMIT signal outlined in the Garner *et al.* manuscript
[#Garner2004jun]_ and the protocol for calculating the ac-ESR-CERMIT signal 
outlined in the supporting information of the Moore *et al.* manuscript 
[#Moore2009dec]_. 

Small amplitude limit (large tip)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the small-amplitude limit, we can calculate the spin-dependent frequency 
shift experienced by the cantilever using

.. math::
    :label: Eq:LargeTipDf

    \Delta f = - \frac{f}{2 k} \sum_j \mu_z(\vec{r}_j) 
        \frac{\partial^{\, 2} B_z^{\mathrm{tip}}( \vec{r}_j )}{\partial x^2}

where :math:`f \: [\mathrm{Hz}]` is the cantilever resonance frequency and 
:math:`k \: [\mathrm{N} \: \mathrm{m}^{-1}]` is the cantilever spring 
constant. The direction of the applied magnetic field is the :math:`z` and the 
direction of the cantilever motion is :math:`x`. In equation :eq:`Eq:LargeTipDf`, 
:math:`\mu_z \: [\mathrm{N} \: \mathrm{m} \: \mathrm{T}^{-1}]` is the :math:`z`
component of the spin magnetic moment, and :math:`B_z^{\mathrm{tip}} \:
[\mathrm{T}]` is the :math:`z` component of the magnetic field produced by the 
cantilever's magnetic tip. The sum represents a sum over all spins in 
resonance (discussed below). The frequency shift arises from a spring constant 
shift of

.. math::
    :label: Eq:LargeTipDk

    \Delta k = - \sum_j \mu_z(\vec{r}_j) 
        \frac{\partial^{\, 2} B_z^{\mathrm{tip}}( \vec{r}_j )}{\partial x^2}

Equations :eq:`Eq:LargeTipDf` and :eq:`Eq:LargeTipDk` are valid when the 
zero-to-peak amplitude of the cantilever oscillation is much smaller than the 
distance between the center of the (spherical) magnet and the sample spins
[#Lee2012apra]_.

In the ESR-CERMIT experiment of Moore *et al.*, the magnetization distribution 
:math:`\mu_z (\vec{r})` depends, according to the steady-state Bloch 
equations, on the frequency :math:`f_{\mathrm{rf}}` and strength :math:`B_1` 
of the microwave field, the sample relaxation times :math:`T_1` and :math:`T_2`
, the sample spin density, the applied magnetic field :math:`B_0`, the tip 
magnetic field :math:`B_z^{\mathrm{tip}}`, and cantilever position.  In the 
Moore experiment, the cantilever sweeps out a region of saturated 
magnetization as it moves.

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitesr
    mrfmsim_marohn.formula.polarization.rel_dpol_sat_steadystate

Assuming a stationary tip, an approximation can be made for the ESR experiment (Michael Boucher):

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitesr_stationarytip
    mrfmsim_marohn.formula.polarization.rel_dpol_sat_steadystate

In the NMR-CERMIT experiment of Garner *et al.*, 
the frequency of the applied radio frequency field :math:`f_{\mathrm{rf}}` is 
swept. The initial magnetization follows the effective field at each location 
in the sample, resulting in a region of inverted magnetization below the tip.

:ref:`Adiabatic Rapid Passage <theory_arp_section>` experiment:

.. autosummary::

    mrfmsim_marohn.experiment.cermitarp
    mrfmsim_marohn.formula.polarization.rel_dpol_sat_steadystate

:ref:`Nutation <theory_nutation_section>` experiments also implemented:

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitnut
    mrfmsim_marohn.formula.polarization.rel_dpol_nut

Large amplitude limit (small tip)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The small-amplitude approximation used to derive the above equations may not 
be valid in a small-tip ESR-CERMIT experiment [#Lee2012apra]_. In this case we 
must calculate the signal using Equation 20 [#Lee2012apra]_ [#Lee2012note]_:

.. math::
    :label: Eq:SmallTipDf

    \Delta f = \frac{f}{2 \pi k x_{\mathrm{pk}}^2} 
        \sum_j \int_{-\pi}^{\pi} \mu_z(\vec{r}_j,\theta)
            \frac{\partial B_z^{\mathrm{tip}}(x - x_{\mathrm{pk}} 
            \cos{\theta},y,z)}{\partial x}
            x_{\mathrm{pk}} \cos{\theta} d\theta 

where :math:`x_{\mathrm{pk}}` is the zero-to-peak amplitude of the cantilever 
oscillation. We write :math:`\mu_z(\vec{r}_j,\theta)` to indicate that, if the 
microwaves are left on during cantilever motion, then the magnetization may 
vary in syncrony with the cantilever oscillation. In the i-OSCAR experiment of 
Rugar and coworkers [#Rugar2004jul]_, the resulting position-dependent change 
in magnetization led to a measurable freqency shift.

Equation :eq:`Eq:SmallTipDf` is exact.  To understand the nature of the 
large-tip approximation, Eq. :eq:`Eq:LargeTipDf`, let us expand the Eq. 
:eq:`Eq:SmallTipDf` gradient in the :math:`x` variable:

.. math::
    :label: Eq:expansion
    
    \frac{\partial B_z^{\mathrm{tip}}(x - x_{\mathrm{pk}} \cos{\theta},y,z)}
    {\partial x} \approx \frac{\partial B_z^{\mathrm{tip}}(x,y,z)}{\partial x}
    - x_{\mathrm{pk}} \cos{\theta} \frac{\partial^2 B_z^{\mathrm{tip}}(x,y,z)}
    {\partial x^2} + {\cal O}(x_{\mathrm{pk}}^2)

In calculating the signal from our ESR-CERMIT experiment we will assume for 
simplicity that the spin distribution :math:`\mu_z(\vec{r}_j)` has reached 
steady-state; we neglect any change in the magnetization during the cantilever 
motion. In this approximation

.. math::
    :label: Eq:SmallTipDf2

    \Delta f = \frac{f}{2 \pi k x_{\mathrm{pk}}^2} \sum_j
    \int_{-\pi}^{\pi} 
        \mu_z(\vec{r}_j)
            \left( 
                \frac{\partial B_z^{\mathrm{tip}}(x,y,z)}{\partial x}
                - x_{\mathrm{pk}}                         
                \cos{\theta} \: \frac{\partial^2 
                B_z^{\mathrm{tip}}(x,y,z)}{\partial x^2}         
            \right)
        \: x_{\mathrm{pk}} \cos{\theta}
    \: d\theta

There are two terms. The first term is

.. math::
    \Delta f^{(1)} = \frac{f}{2 \pi k x_{\mathrm{pk}}} \sum_j \mu_z(\vec{r}_j) 
    \frac{\partial B_z^{\mathrm{tip}}(x,y,z)}{\partial x}
    \int_{-\pi}^{\pi} \cos{\theta} \: d\theta 

We are interested in experiments carried out in the SPAM geometry and the 
hangdown  geometry. In both of these cases the first term vanishes: the sum 
over sample spins is zero since the gradient is both positive and negative 
over the sensitive slice. Moreover, the integral over :math:`\theta` is zero. 
The second term in Eq. :eq:`Eq:SmallTipDf2` is

.. math::
    \Delta f^{(2)} = - \frac{f}{2 k} \sum_j \mu_z(\vec{r}_j)
    \frac{\partial^2 B_z^{\mathrm{tip}}(x,y,z)}{\partial x^2}
    \underbrace{\frac{1}{\pi} \int_{-\pi}^{\pi} \cos^2{\theta} \:
    d\theta}_{= 1}  

which simplifies to the large-tip result, Eq. :eq:`Eq:LargeTipDf`, 

.. math::
    \Delta f^{(2)} = - \frac{f}{2 k}
    \sum_j \mu_z(\vec{r}_j) \frac{\partial^2 
    B_z^{\mathrm{tip}}(x,y,z)}{\partial x^2}

We see from this derivation that the validity of Eq. :eq:`Eq:LargeTipDf` rests 
on the validity of the approximation in Eq. :eq:`Eq:expansion`.  According to 
Eq. :eq:`Eq:expansion`, for Eq. :eq:`Eq:LargeTipDf` to be valid, the change in 
the gradient experienced by any spin in the sample should be strictly linear 
in the cantilever amplitude.  This will not be true for a large-amplitude 
motion of the cantilever.

Let us rewrite Eq. :eq:`Eq:SmallTipDf` by 

1. assuming that the magnetization distribution is in steady-state, 
2. writing the frequency shift in terms of an eqivalent spring constant shift,
3. expressing the result in terms of an equivalent force.  

We showed in Reference [#Lee2012apra]_ that maximizing this equivalent force 
will maximize the signal-to-noise ratio in a frequency-shift experiment. In 
terms of a force, the ESR-CERMIT signal is

.. math::
    :label: Eq:SmallTipD_F
    
    \Delta F = \Delta k \: x_{\mathrm{pk}} = \frac{2}{\pi} \sum_j
    \int_{0}^{\pi} 
        \mu_z(\vec{r}_j)
        \: \frac{\partial B_z^{\mathrm{tip}}(x - x_{\mathrm{pk}}
             \cos{\theta},y,z)}{\partial x}
        \: \cos{\theta}
    \: d\theta

In writing Eq. :eq:`Eq:SmallTipD_F` we have condensed the integral to a half 
cycle of the cantilever oscillation. In the integrand, the position variable 
:math:`x(\theta) = x - x_{\mathrm{pk}} \cos{\theta}` runs from :math:`x - 
x_{\mathrm{pk}}` to :math:`x + x_{\mathrm{pk}}` as :math:`\theta` runs from 
:math:`0` to :math:`\pi`.  In the steady-state approximation, the spin 
distribution :math:`\mu_z(\vec{r}_j)` in Eq. :eq:`Eq:SmallTipD_F` is 
determined in the same way as in the large-tip experiment.


.. autosummary::
    
    mrfmsim_marohn.experiment.cermitesr_smalltip
    mrfmsim_marohn.formula.polarization.rel_dpol_sat_steadystate
    mrfmsim_marohn.formula.field.xtrapz_field_gradient

Eric Moore and co-workers previously implemented Eqs. :eq:`Eq:SmallTipDf` and 
:eq:`Eq:SmallTipD_F` to calculate the ESR-MRFM signal from a single spin 
[#Lee2012apra]_ [#Moore2009]_

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitesr_singlespin
    mrfmsim_marohn.experiment.cermitesr_singlespin_approx
    mrfmsim_marohn.formula.field.xtrapz_field_gradient

And to simulate the amplitude dependence of the 
signal from a single slice whose magnetization has been inverted *via* an 
adiabatic rapid passage [#Moore2009dec]_. 


.. autosummary::
    
    mrfmsim_marohn.experiment.cermitarp_smalltip
    mrfmsim_marohn.formula.field.xtrapz_field_gradient

The single-slice simulation is quite 
slow because, essentially, a full magnetic field and field gradient simulation 
must be done for each :math:`\theta`.  If you approximate the :math:`\theta` 
integral using (only!) 32 points, then the simulation will take 32 times 
longer to run than single simulation.  Since the :math:`x(\theta)` values are 
*not* equally spaced, you cannot simplify the integral by translating the 
:math:`x` coordinates.


John's :ref:`intermittent irradiation <theory_irradation_section>` experiments 
also implemented:

**Intermittent irradiation**

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitesr_periodirrad_stationarytip


**Cornell-style frequency-shift** [#Garner2004jun]_

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitarp
    mrfmsim_marohn.experiment.cermitnut


**IBM-style cyclic-inversion** [#Degen2009jan]_ [#Longenecker2012oct]_

.. autosummary::
    
    mrfmsim_marohn.experiment.ibmcyclic

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

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitesr

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

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitarp_smalltip
    mrfmsim_marohn.experiment.cermitesr_smalltip

**Cornell Single Spin ESR**

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitesr_singlespin

**Additional Experiments**

.. autosummary::
    
    mrfmsim_marohn.experiment.cermitesr_stationarytip
    mrfmsim_marohn.experiment.cermitesr_periodirrad_stationarytip

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
