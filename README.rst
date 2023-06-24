MrfmSim-Marohn
==============

|GitHub version| |Unit tests| |DOI|

The MrfmSim-Marohn package can be used as a standalone or used as a plugin for
the `MrfmSim package <https://github.com/Marohn-Group/mrfmsim>`__ and the
`documentation <https://github.com/Marohn-Group/mrfmsim-docs>`__.

This package contains tools to simulate signals in a Magnetic Resonance Force 
Microscope [#Sidles1995jan]_ [#Kuehn2008feb]_ [#Poggio2010aug]_ experiment.
The code in the package simulates signal from **electron spins**, 
particularly the **nitroxide spin radical** ``TEMPO`` to **selected nuclear 
spins (1H, 19F, and 71Ga)**.

It can simulate signals from both **Curie-law spin magnetization** and **spin 
fluctuations** (in the small polarization limit); and can simulate **force 
experiments** and **force-gradient experiments** (in the 
small-cantilever-amplitude limit and without the small amplitude approximation 
--- in the large amplitude limit). 

It can simulate signal with the cantilever and field-aligned in both the 
**hangdown** [#Mamin2003nov]_ and **SPAM** [#Marohn1998dec]_ [#Garner2004jun]_ 
experimental geometries.


Installation 
-------------

To install the MrfmSim-Marohn package, *under root directory*::

    python -m pip install .

To run the unit tests::
    
    python -m pytest

To run test the package in different environments::

    python -m pip install .[test]
    tox

Contribute
----------

Peter Sun (hs859@cornell.edu) and John Marohn (jam99@cornell.edu)
maintain the package. 
Collaborating on code development is encouraged, 
using the `fork & pull` model 
[`link <https://help.github.com/articles/using-pull-requests/>`__].

References
----------

.. [#Sidles1995jan] Sidles, J. A.; Garbini, J. J.; Bruland, K. J.; Rugar, D.; 
    Züger, O.; Hoen, S. & Yannoni, C. S. "Magnetic Resonance Force Microscopy",
    *Rev. Mod. Phys.*, **1995**, *67*, 249 - 265
    [`10.1103/RevModPhys.67.249\
    <http://doi.org/10.1103/RevModPhys.67.249>`__].

.. [#Kuehn2008feb] Kuehn, S.; Hickman, S. A. & Marohn, J. A. "Advances in 
    Mechanical Detection of Magnetic Resonance", *J. Chem. Phys.*, **2008**, 
    *128*, 052208 
    [`10.1063/1.2834737 <http://dx.doi.org/10.1063/1.2834737>`__].
    **OPEN ACCESS**.

.. [#Poggio2010aug] Poggio, M. & Degen, C. L. "Force-Detected Nuclear Magnetic
    Resonance: Recent Advances and Future Challenges", 
    *Nanotechnology*, **2010**, *21*, 342001 
    [`10.1088/0957-4484/21/34/342001\
    <http://doi.org/10.1088/0957-4484/21/34/342001>`__].

.. [#Mamin2003nov] Mamin, H. J.; Budakian, R.; Chui, B. W. & Rugar, D.
     "Detection and Manipulation of Statistical Polarization in Small 
     Spin Ensembles", *Phys. Rev. Lett.*, **2003**, *91*, 207604 
     [`10.1103/PhysRevLett.91.207604\
     <http://doi.org/10.1103/PhysRevLett.91.207604>`__].

.. [#Marohn1998dec] Marohn, J. A.; Fainchtein, R. & Smith, D. D. 
    "An Optimal Magnetic Tip Configuration for Magnetic-Resonance Force 
    Microscopy of Microscale Buried Features", *Appl. Phys. Lett.*, **1998**,
    *73*, 3778 - 3780 
    [`10.1063/1.122892 <http://dx.doi.org/10.1063/1.122892>`__].
    SPAM stands for Springiness Preservation by Aligning Magnetization.

.. [#Garner2004jun] Garner, S. R.; Kuehn, S.; Dawlaty, J. M.; Jenkins, N. E. 
    & Marohn, J. A. "Force-Gradient Detected Nuclear Magnetic Resonance", 
    *Appl. Phys. Lett.*, **2004**, *84*, 5091 - 5093 
    [`10.1063/1.1762700 <http://dx.doi.org/10.1063/1.1762700>`__]. 

.. |GitHub version| image:: https://badge.fury.io/gh/Marohn-Group%2Fmrfmsim-marohn.svg
   :target: https://github.com/Marohn-Group/mrfmsim-marohn

.. |Unit tests| image:: https://github.com/Marohn-Group/mrfmsim/actions/workflows/tox.yml/badge.svg
    :target: https://github.com/Marohn-Group/mrfmsim-marohn/actions

.. |DOI| image:: https://zenodo.org/badge/553750575.svg
   :target: https://zenodo.org/badge/latestdoi/553750575
