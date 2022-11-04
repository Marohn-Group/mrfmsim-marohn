import pytest
import numpy as np
from mrfmsim_marohn.formulas import mz_eq, HBAR, KB

@pytest.mark.parametrize(
    "Gamma, J,  temperature, mz_eq_true",
    [
        [1.760859708e8, 0.5, 0.001, 9.28476430],  # electron spin
        [2.0 * np.pi * 12.98e3, 1.5, 1e-6, 0.012901],  # 71Ga spin low field
    ],
)
def test_mz_eq_high_susceptibility(Gamma, J, temperature, mz_eq_true):
    """Test mz_eq function on different types of samples at low temperature
    The total field is set to 100 T
    """

    mz_eq_sim = mz_eq(100, Gamma, J, temperature)
    assert np.allclose(mz_eq_sim, mz_eq_true, rtol=1.0e-5)


@pytest.mark.parametrize("B_tot", np.linspace(100, 1000, 5))
def test_mz_eq_low_susceptibility(B_tot):
    """Test mz_eq on 71Ga at high temperature"""

    Gamma, J, temperature = 2.0 * np.pi * 12.98e3, 1.5, 300

    mz_eq_true = B_tot * (HBAR**2 * Gamma**2 * J * (J + 1)) / (3 * KB * temperature)
    mz_eq_sim = mz_eq(B_tot, Gamma, J, temperature)

    assert np.allclose(mz_eq_sim, mz_eq_true, rtol=2.0e-3, atol=0.0)
