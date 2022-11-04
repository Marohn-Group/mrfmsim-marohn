"""Test un-categorized formulas under __init__.py"""
from mrfmsim_marohn.formulas import B_offset
import numpy as np

def test_B_offset():
    """Test B_offset
    Test the hydrogen atom
    """

    Gamma = 267.5222005 # rad MHz/T
    B_tot = 4.6973188 #T
    f_rf = 200 #MHz

    assert np.isclose(B_offset(B_tot, f_rf, Gamma), 0)
