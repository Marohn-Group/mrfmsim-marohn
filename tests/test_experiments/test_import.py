import sys
import glob
import os


def test_import():
    """Test the experiments have been imported"""
    # __init__.py is not executed if experiments are not imported
    import mrfmsim_marohn.experiments

    filelist = glob.glob("./mrfmsim_marohn/experiments/**.yaml")

    exp_name = []
    for fname in filelist:
        exp_name.append(
            f"mrfmsim_marohn.experiments.{os.path.basename(os.path.splitext(fname)[0])}"
        )

    for exp in exp_name:
        assert exp in sys.modules
