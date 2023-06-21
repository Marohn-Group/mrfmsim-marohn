Units
=====

To avoid roundoff error, we work in units that are natural to the problem at hand:

* position :math:`(x,y,z)`: :math:`\mathrm{nm}`

* time :math:`t`: :math:`\mathrm{s}` 

* fields :math:`B_z` and :math:`B_1`: :math:`\mathrm{mT} = 1 \times 10^{-3} \: \mathrm{T}`

* force: :math:`F`: :math:`\mathrm{aN} = 1 \times 10^{-18} \: \mathrm{N}`

* temperature :math:`T`: :math:`\mathrm{K}`

Units which follow from these choices include:

* volume element :math:`dV`: :math:`\mathrm{nm}^{-3}`

* frequency :math:`f`: :math:`\mathrm{Hz}`

* gyromagnetic ratio :math:`\gamma_{\mathrm{p}}` and :math:`\gamma_{\mathrm{e}}`: :math:`\mathrm{s}^{-1} \: \mathrm{mT}^{-1}`

* field derivative :math:`\partial B_z / \partial x`: :math:`\mathrm{mT} \: \mathrm{nm}^{-1}`

* field second derivative :math:`\partial^2 B_z / \partial x^2`: :math:`\mathrm{mT} \: \mathrm{nm}^{-2}`

* spin density :math:`\rho`: :math:`\mathrm{nm}^{-3}`

* magnetic moment :math:`\mu_{\text{p}}` and :math:`\mu_{\text{e}}`: :math:`\mathrm{aN} \: \mathrm{nm} \: \mathrm{mT}^{-1}` 

In these units, the electron gyromagnetic ratio [#NISTgammae]_ is 

.. math::

    \gamma_e & = 1.760 859 708 \times 10^{11} \: \mathrm{s}^{-1} \: \mathrm{T}^{-1} \\
             & = 1.760 859 708 \times 10^{8} \: \mathrm{s}^{-1} \: \mathrm{mT}^{-1},

the electron magnetic moment [#NISTmue]_ is 

.. math::

    \mu_e & = -928.476 430 \times 10^{-26} \: \mathrm{J} \: \mathrm{T}^{-1} \\
          & = -9.28 \: \mathrm{aN} \: \mathrm{nm} \: \mathrm{mT}^{-1},
    
the proton gyromagnetic ratio [#NISTgammap]_ is

.. math::

    \gamma_p & = 2.675 222 005 \times 10^{8} \: \mathrm{s}^{-1} \: \mathrm{T}^{-1} \\
             & = 2.675 222 005 \times 10^{5} \: \mathrm{s}^{-1} \: \mathrm{mT}^{-1},

and the proton magnetic moment is

.. math::

    \mu_p &= 1.410 606 743 \times 10^{-26} \: \mathrm{J} \: \mathrm{T}^{-1} \\
          &= 0.0141 \: \mathrm{aN} \: \mathrm{nm} \: \mathrm{mT}^{-1}.

The gyromagnetic ratios were taken from the NIST database and do not account for any chemical shift corrections.  It is pleasing to find that in our units system the electron and proton magnetic moments come out to be numbers of order one!

In the calculations below, we will need the following two physical constants.  In terms of our practical units,  
        
.. math::
            
    \hbar &= \text{Planck's constant divided by } 2 \pi \\
          &= 1.054571628 \times 10^{-34} \: \mathrm{J} \: \mathrm{s} \\
          &= 1.054571628 \times 10^{-7} \: \mathrm{aN} \: \mathrm{nm} \: \mathrm{s} \\
    k_b &= \text{Boltzmann's constant} \\
        &= 1.3806504 \times 10^{-23} \: \mathrm{J} \: \mathrm{K}^{-1} \\
        &= 1.3806504 \times 10^{4} \: \mathrm{aN} \: \mathrm{nm} \: \mathrm{K}^{-1}

**References**

.. [#NISTgammae] http://physics.nist.gov/cgi-bin/cuu/Value?gammae
.. [#NISTgammap] http://physics.nist.gov/cgi-bin/cuu/Value?gammap
.. [#NISTmue] http://physics.nist.gov/cgi-bin/cuu/Value?muem
.. [#NISTmup] http://physics.nist.gov/cgi-bin/cuu/Value?mup