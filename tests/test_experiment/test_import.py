from textwrap import dedent
import importlib


def test_show(capsys):
    """Test the show function to list all experiments."""
    experiment_module = importlib.import_module("mrfmsim_marohn.experiment")

    experiment_module.show()
    captured = capsys.readouterr()
    assert captured.out == dedent(
    """\
    The list of available collections/experiments:
    CermitARPCollection
    CermitESRCollection
    CermitESRSingleSpinCollection
    CermitTDCollection
    IBMCyclic
    """
    )
