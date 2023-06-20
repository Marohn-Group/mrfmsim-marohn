from mrfmsim_marohn.component import SphereMagnet, Grid, Sample, Cantilever
from mrfmsim_marohn.experiment import cermitesr
import numpy as np
import pytest


class TestCERMITESR:
    """Test cermitesr experiment."""

    @pytest.fixture
    def sample(self):
        """Return the sample object."""

        return Sample(
            spin_type="electron",
            temperature=11.0,
            T1=1.3e-3,
            T2=0.45e-6,
            spin_density=0.0241,
        )

    @pytest.fixture
    def cantilever(self):
        """Return the cantilever object."""

        return Cantilever(
            k_c=2e4,
            f_c=3e6,
        )

    def test_cermitesr_SPAM(self, sample, cantilever):
        """Test the result in SPAM geometry, Moore parameters, local peak."""

        magnet = SphereMagnet(radius=1850.0, mu0_Ms=440.0, origin=[0, 1850, 0])
        grid = Grid(shape=[501, 21, 251], step=[8, 10, 8], origin=[0, -100, 0])

        cantilever = Cantilever(k_c=2e4, f_c=3e6)

        B1 = 3.9e-4
        mw_x_0p = 330
        B0 = 700
        f_rf = 17.7e9
        h = [0, 50, 0]  # tip sample separation [nm]

        df_spin = cermitesr(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)

        assert np.isclose(df_spin, cantilever.dk_to_df_ac_cermit(-0.940), rtol=5e-1)

    def test_cermitesr_hangdown(self, sample, cantilever):
        """Test the result in SPAM geometry, Issac parameters."""

        magnet = SphereMagnet(radius=3300.0, mu0_Ms=440.0, origin=[0, 0, 3300])
        grid = Grid(shape=[400, 1200, 8], step=[25, 25, 25], origin=[0, 0, -100])

        B1 = 1.3e-3
        mw_x_0p = 100
        B0 = 570
        f_rf = 18.5e9
        h = [0, 0, 1450]  # tip sample separation [nm]

        df_spin = cermitesr(B0, B1, cantilever, f_rf, grid, h, magnet, mw_x_0p, sample)

        assert np.isclose(df_spin, cantilever.dk_to_df_ac_cermit(-25.086), rtol=5e-1)
