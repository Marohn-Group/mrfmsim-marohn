from mrfmsim import Experiment
from textwrap import dedent
import importlib


def test_show(capsys):
    """Test the show function to list all experiments."""
    experiment_module = importlib.import_module("mrfmsim_marohn.experiment")

    experiment_module.show()
    captured = capsys.readouterr()
    assert captured.out == dedent(
        """\
    The list of available experiments:
    cermitarp
    cermitarp_smalltip
    cermitesr
    cermitesr_periodirrad_stationarytip
    cermitesr_smalltip
    cermitesr_stationarytip
    cermitnut
    cermitnut_multipulse
    cermitesr_singlespin
    cermitesr_singlespin_approx
    cermittd
    cermittd_singlepulse
    cermittd_smalltip
    ibmcyclic
    """
    )


def test_import_experiment():
    """Test the experiments are imported."""

    experiment_module = importlib.import_module("mrfmsim_marohn.experiment")

    assert isinstance(experiment_module.ibmcyclic, Experiment)
