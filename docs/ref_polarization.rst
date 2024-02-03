Polarization
=============

Steady-state solution
^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::

    mrfmsim_marohn.formula.polarization.rel_dpol_sat_steadystate



Intermittent Irradiation
^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::

    mrfmsim_marohn.formula.polarization.rel_dpol_periodic_irrad

In our magnetic resonance experiment, we alternate microwave-on and 
microwave-off periods. With the microwaves on, magnetization evolves towards 
a saturated, steady-state value at a rate :math:`r0`. With the microwaves 
off, magnetization evolved towards equilibrium at a rate :math:`r1 = 1/T1`. 
The irradiation scheme and resulting magnetization dynamics are summarized 
in the following table

Nutation
^^^^^^^^^^^^^^^^^^^^^^^^

.. autosummary::

    mrfmsim_marohn.formula.polarization.rel_dpol_nut


If the rf is turned on suddenly at :math:`t =0`, the magnetization will nutate 
around the effective field.  Neglecting relaxation, the magnetization vector a 
time :math:`t_{\mathrm{p}}` after the start of the rf pulse is

.. math::

    \begin{align}
    \frac{\vec{M}(t_p)}{M_{z}(0)} = 
        & \left(  
            \frac{\Omega}{\Omega^2+1} - \frac{\Omega}{\Omega^2+1} 
            \cos{(\Omega_1 t_p \sqrt{\Omega^2+1} \: )} 
        \right) \hat{x}_{\mathrm{R}} \\
        & - \left(
            \frac{1}{\Omega^2+1} \sin{(\Omega_1 t_p \sqrt{\Omega^2+1} \: )}
        \right) \hat{y}_{\mathrm{R}} \\
        & + \left(
            \frac{\Omega^2}{\Omega^2+1} 
            + \frac{1}{\Omega^2+1} \cos{(\Omega_1 t_p \sqrt{\Omega^2+1} \: )} 
        \right) \hat{z}
    \end{align}
        
with :math:`\Omega`, the unitless resonance offset, given by Eq. :eq:`Eq:Omega`
.  Since we observe the :math:`z` component of magnetization, we are 
interested in:

.. math::

    \rho_{\mathrm{rel}}
        = \frac{M_z}{M_z(0)}
        = \frac{\Omega^2}{\Omega^2+1} 
            + \frac{1}{\Omega^2+1} \cos{(\Omega_1 t_p \sqrt{\Omega^2+1} \: )}

The change in the :math:`z` component of the magnetization due to the pulse 
is, after some simplification, 

.. math::
    :label: Eq:deltaMz-pulse

    \delta M_{z}(\theta, \Omega) = M_{z}(t_{\mathrm{p}}) - M_{z}(0) 
    =  - 2 \, M_{z}(0) \frac{1}{\Omega^2+1} 
        \sin^2{\left( \frac{\theta_p}{2} \sqrt{\Omega^2 + 1} \: \right)}
    
where :math:`\theta_p \equiv \omega_1 t_p` is the pulse angle. Plotting this 
function, we see that the biggest change in magnetization, :math:`\delta 
M_{z}(\theta_p,\Omega)/M_{z}(0) = -2`, occurs on resonance (:math:`\Omega = 0`
) when the pulse angle is set to :math:`\theta_p = \pi`.  When :math:`\theta_p 
= \pi`, the full width at half max (FWHM) of the :math:`\delta M_
{z}(\pi,\Omega)/M_{z}(0)` function is approximately :math:`1.597 \Omega`. In 
other words, a :math:`\pi` pulse will invert magnetization over a resonant 
slice of whose width, in field units, is approximately :math:`1.597 \: B_1`.  


:py:mod:`formula.polarization` module
----------------------------------------------------

.. automodule:: mrfmsim_marohn.formula.polarization
    :members:
    :undoc-members:
    :show-inheritance:

