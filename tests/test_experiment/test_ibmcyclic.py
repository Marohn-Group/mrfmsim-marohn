import pytest
from mrfmsim_marohn.experiment import ibmcyclic
from mrfmsim_marohn.component import Grid, Sample, SphereMagnet
import numpy as np


class TestIBMCyclic:
    """Test IBMCyclic Experimental method.

    See CornellCermitAPRTest for detailed implementations
    """

    def test_IBMCyclic_dF_spin(self):
        """Test IBM curie law signal."""
        B0 = 10000.000  # external field, 10 T
        B_tip = 284.032  # calculated field at the sample location
        B1 = 10.0
        B_tot = B0 + B_tip  # total field seen by spins right below the tip
        df_fm = 10.0 * B1 * 1.760859708e8 / (2 * np.pi)
        f_rf = B_tot * 1.760859708e8 / (2 * np.pi)
        h = [0, 0, 20.0]

        sample = Sample(
            spin_type="electron",  # an imaginary electron-spin sample
            temperature=10.0e-3,  # 10 mK so the spin is fully polarized
            T1=1,
            T2=0.45e-6,
            spin_density=1.0e9,
        )
        x_opt = 27.2507  # optimal lateral location [nm]
        magnet = SphereMagnet(radius=50.0, mu0_Ms=1800.0, origin=[x_opt, 0.0, 50.0])
        grid = Grid(
            shape=[2, 2, 2], step=[0.5e-3, 0.5e-3, 0.5e-3], origin=[0.0, 0.0, 0.0]
        )

        _, dF_spin = ibmcyclic(B0, df_fm, f_rf, grid, h, magnet, sample)

        assert np.isclose(dF_spin, -79.231, rtol=2e-2)

    def test_IBMCyclic_dF2_spin(self):
        """Test IBM cyclic force variance signal for nucleus.

        Values are taken from test-ibmexpt-1.ipynb simulation 1 #4- #9
        based on John's calculation.
        """

        grid = Grid(shape=[201, 201, 21], step=[2.0, 2.0, 2.0], origin=[0, 0, -20])

        magnet = SphereMagnet(radius=100.0, mu0_Ms=1800, origin=[0.0, 0.0, 100.0])

        sample = Sample(
            spin_type="1H", temperature=4.2, T1=10, T2=5e-6, spin_density=49.0
        )
        B0 = 2630.5
        f_rf = 112.0e6
        h = [0, 0, 64.1]
        df_fm = 2e6
        B1 = 2.0

        dF2_spin, dF_spin = ibmcyclic(B0, df_fm, f_rf, grid, h, magnet, sample)

        print(dF2_spin, dF_spin)

        assert np.isclose(dF2_spin, -477.032, rtol=5e-4)
