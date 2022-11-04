"""Cacluations related to field"""
import numpy as np
import numba as nb

@nb.jit(nopython=True, parallel=True)
def B_offset(B_tot, f_rf, Gamma):
    """Calculate the resonance offset"""
    return B_tot - 2 * np.pi * f_rf/Gamma
