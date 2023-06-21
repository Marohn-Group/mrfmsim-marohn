Trapezoid Integration
=====================

:py:func:`mrfmsim_marohn.formula.field.xtrapz_field_gradient`

For each x-data point in the sample, calculate the resonance offset over
the expanded grid. The points to the left and right of each grid point
give the resonance offset as the cantilever moves. Find the minimum
resonance offset over the range of array values corresponding to the
cantilever motion, and compute the saturation polarization using that
minimum offset and the given B_1.

To calculate the spin polarization profile resulting from the cantilever
moving while spin-saturating irradiation is applied we use the following
algorithm:

    If the resonance offset changed sign during the sweep, then the spin
    must have experienced a zero resonance offset during the sweep, so set
    the resonance offset to zero manually.

This procedure mitigates the problem of previous algorithms not finding
the true minimum resonance offset (and polarization) due to the finite grid
size. While this new procedure will still not capture the shape of the
polarization at the edge of the sensitive slice, it should produce a
polarization which is properly saturated inside the sensitive slice.

This is used for calculating :math:`\delta F` of the experiment
calculate the corresponding gradient based on the grid array
points and tip-sample separation (equation 3 in "Overview").
The integral is approximated with Trapezoid summation over
:math:`2 \pi` with n points.
The summation is over pi to increase the performance since it is
symmetry in [-pi, 0] to [0, pi] for the summation.

.. math::
    \Delta f = \frac{\sum_j \int_{-\pi}^{\pi} \mu_z(\vec{r}_j,\theta)
    \frac{\partial B_z^{\mathrm{tip}}(x - x_{\mathrm{pk}}
    \cos{\theta},y,z)}{\partial x}
    x_{\mathrm{pk}} \cos{\theta} d\theta}{\pi x_{\mathrm{pk}}^2}


.. Reference
.. ^^^^^^^^^

.. .. [#Bloch] `"Bloch Equations" <http://chemwiki.ucdavis.edu/Physical_Chemistry/
..     Spectroscopy/Magnetic_Resonance_Spectroscopies/
..     Nuclear_Magnetic_Resonance/NMR%3A_Theory/Bloch_Equations>`__.
.. .. [#Longenecker2012oct] Equation S3 in Longenecker, J. G.; Mamin, H. J.; 
..     Senko, A. W.; Chen, L.; Rettner, C. T.; Rugar, D. & Marohn, J. A.
..     "High-Gradient Nanomagnets on Cantilevers for Sensitive Detection of
..     Nuclear Magnetic Resonance", *ACS Nano*, **2012**, *6*, 9637 - 9645
..     [`10.1021/nn3030628 <http://dx.doi.org/10.1021/nn3030628>`__].
..     This equation was found to fit the simulated spin response to a
..     triangle-wave resonance-frequency modulation versus resonance offset
..     given by Equation S9 in [#Degen2009jan]_.
.. .. [#Degen2009jan] Degen, C. L.; Poggio, M.; Mamin, H. J.; Rettner, C. T. & 
..     Rugar, D. "Nanoscale Magnetic Resonance Imaging", *Proc. Natl. Acad. Sci. 
..     U.S.A.*, **2009**, *106*, 1313 - 1317
..     [`10.1073/pnas.0812068106 <http://dx.doi.org/10.1073/pnas.0812068106>`__].

.. .. [#Longenecker2012oct] Equation S3 in Longenecker, J. G.; Mamin, H. J.; 
..     Senko, A. W.; Chen, L.; Rettner, C. T.; Rugar, D. & Marohn, J. A.
..     "High-Gradient Nanomagnets on Cantilevers for Sensitive Detection of
..     Nuclear Magnetic Resonance", *ACS Nano*, **2012**, *6*, 9637 - 9645
..     [`10.1021/nn3030628 <http://dx.doi.org/10.1021/nn3030628>`__].
..     This equation was found to fit the simulated spin response to a
..     triangle-wave resonance-frequency modulation versus resonance offset
..     given by Equation S9 in [#Degen2009jan]_.
