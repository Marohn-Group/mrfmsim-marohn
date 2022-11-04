
import sys

def test_import():
    """Test the experiments have been imported"""
    # __init__.py is not executed if experiments are not imported
    import mrfmsim_marohn.experiments 

    assert 'mrfmsim_marohn.experiments.cornellesr' in sys.modules
