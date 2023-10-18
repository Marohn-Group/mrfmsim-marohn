Changelog
========= 
All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_

For previous versions of Marohn group mrfmsim, see `repository <https://github.com/peterhs73/MrfmSim-archived>`_.

[Unreleased]
------------

Changed
^^^^^^^

- Change the plugin system based on ``mrfmsim`` version 0.2.0.
    - Add the ``mrfmsim_plugin`` entry point in the pyproject.toml file.
- Moved the ``components`` submodule to ``mrfmsim`` main platform.
- Moved the units system to ``mrfmsim-unit`` library.



[0.1.0] - 2023-06-23
--------------------

Initial release.

Added
^^^^^^^
- Add components "Grid", "Sample", "Magnet" and "Cantilever".
- Add formulas with submodules: "math", "magnetization", "polarization" and "misc".
- Add cermitesr, cermitesr_singlespin, cermittd, cermitarp, cermitnut and ibmcyclic experiments.
- Add documentation.
