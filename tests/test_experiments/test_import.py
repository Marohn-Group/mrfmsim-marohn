import sys
import glob
import os
from mrfmsim import Experiment
from textwrap import dedent

import pytest


def test_show(capsys):
    """Test the show function to list all experiments."""
    from mrfmsim_marohn import experiments

    experiments.show()
    captured = capsys.readouterr()
    assert captured.out == dedent(
        """\
    The list of available experiments:
    cermitarp
    cermitarp_smalltip
    cermitesr
    cermitesr_periodirrad_stationarytip
    cermitesr_singlespin
    cermitesr_smalltip
    cermitesr_stationarytip
    cermitnut
    cermitnut_multipulse
    cermittd
    cermittd_singlepulse
    cermittd_smalltip
    ibmcyclic
    """
    )


def test_import_syntax1():
    """Test the experiments are imported when called."""
    from mrfmsim_marohn.experiments import ibmcyclic

    assert isinstance(ibmcyclic, Experiment)


def test_import_syntax2():
    """Test the experiments are imported when called."""
    from mrfmsim_marohn import experiments

    assert isinstance(experiments.ibmcyclic, Experiment)
