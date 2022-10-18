#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test magnet module in mrfmsim.components

SphereMagnet
------------

All sphere magnet are tested using parameter:
r = 50.0 nm
mu0_Ms = 1800.0 mT
o = [0, 0, 0] nm

bz_method
^^^^^^^^^^

1. Test bz at poles (0.0, 0.0, 50.0) and (0.0, 0.0, -50.0) both result
  in Bz value of 1200.0 mT
2. Test bz at equator (50.0, 0.0, 0.0), (0.0, 5.0, 0.0), 
  and (-1.0*50.0/sqrt(2),  -1.0*50.0/sqrt(2), 0.0), all result in Bz
  value of -600.0 mT

"""

import pytest
import numpy as np
from mrfmsim_marohn.components import SphereMagnet, RectangularMagnet
from textwrap import dedent

SPHERE_STR = """SphereMagnet(
  magnet_origin=[0.0 0.0 0.0] [nm] # magnet origin
  magnet_radius=50.0 [nm] # magnet radius
  mu0_Ms=1800.0 [mT] # tip magnetization, oriented along z
)"""


class MagnetTester:

    magnet_str = ""

    def test_str(self, magnet):
        """Test magnet repr"""

        assert str(magnet) == dedent(self.magnet_str)

    def check_bz(self, magnet, x, y, z, theory):
        """Test Bz calculation against theory"""
        assert np.allclose(magnet.Bz(x, y, z), theory, rtol=1e-12)

    def check_bzx(self, magnet, x, y, z):
        """test Bzx at selected points against estimation from Bz calculation"""

        dx = 0.001

        Bzx_est = (magnet.Bz(x + 0.5 * dx, y, z) - magnet.Bz(x - 0.5 * dx, y, z)) / dx
        Bzx_sim = magnet.Bzx(x, y, z)

        assert np.allclose(Bzx_est, Bzx_sim, rtol=1e-9)

    def check_bzxx(self, magnet, x, y, z):
        """test Bzxx at selected points against estimation from Bzx calculation"""

        dx = 0.001

        Bzxx_est = (
            magnet.Bzx(x + 0.5 * dx, y, z) - magnet.Bzx(x - 0.5 * dx, y, z)
        ) / dx
        Bzxx_sim = magnet.Bzxx(x, y, z)

        assert np.allclose(Bzxx_est, Bzxx_sim, rtol=1e-9)


class TestSphereMagnet(MagnetTester):
    """Test SphereManget class"""

    magnet_str = """\
    SphereMagnet(
      magnet_origin=[0.0 0.0 0.0] [nm] # magnet origin
      magnet_radius=50.0 [nm] # magnet radius
      mu0_Ms=1800.0 [mT] # tip magnetization, oriented along z
    )"""

    @pytest.fixture
    def magnet(self):
        """Instantiate a SphereManget instance"""
        return SphereMagnet(radius=50.0, mu0_Ms=1800.0, origin=[0.0, 0.0, 0.0])

    @pytest.mark.parametrize(
        "x, y, z, theory",
        [
            # at poles
            (0.0, 0.0, 50.0, 1200.0),
            (0.0, 0.0, -50.0, 1200.0),
            # at equators
            (50.0, 0.0, 0.0, -600.0),
            (0.0, 50.0, 0.0, -600.0),
            (-1.0 * 50.0 / np.sqrt(2), -1.0 * 50.0 / np.sqrt(2), 0.0, -600.0),
        ],
    )
    def test_bz(self, magnet, x, y, z, theory):
        """Test Bz calculation at poles and equators"""

        self.check_bz(magnet, x, y, z, theory)

    @pytest.mark.parametrize(
        "x, y, z",
        [
            (57.29, 0.0, 0.0),  # at equator
            (10.91, 13.16, 53.18),  # near north pole
        ],
    )
    def test_bzx(self, magnet, x, y, z):
        """test Bzx at selected points against estimation from Bz calculation"""

        self.check_bzx(magnet, x, y, z)

    @pytest.mark.parametrize(
        "x, y, z",
        [
            (57.29, 0.0, 0.0),  # at equator
            (10.91, 13.16, 53.18),  # near north pole
        ],
    )
    def test_bzxx(self, magnet, x, y, z):
        """test Bzxx at selected points against estimation from Bzx calculation"""

        self.check_bzxx(magnet, x, y, z)


class TestRectangularMagnet(MagnetTester):
    """Tests RectangularMagnet

    TODO
        Test absolute magnet bz calculation
    """

    magnet_str = """\
    RectangularMagnet(
      magnet_length=[40.0 60.0 100.0] [nm] # magnet length in x, y, z direction
      magnet_origin=[0.0 0.0 0.0] [nm] # magnet origin
      mu0_Ms=1800.0 [mT] # tip magnetization, oriented along z
    )"""

    @pytest.fixture
    def magnet(self):
        """Instantiate a RectangularManget instance"""

        return RectangularMagnet(
            length=[40.0, 60.0, 100.0], mu0_Ms=1800.0, origin=[0.0, 0.0, 0.0]
        )

    @pytest.mark.parametrize("x, y, z", [(np.arange(50, 100, 5), 100, 100)])
    def test_rectmagnet_x_symmetry(self, magnet, x, y, z):
        """Test x direction symmetry

        Bz - even function in x direction
        Bzx - odd function in x direction
        Bzxx - even function in x direction
        """

        np.allclose(magnet.Bz(x, y, z), magnet.Bz(-x, y, z), rtol=1e-10)
        np.allclose(magnet.Bzx(x, y, z), -magnet.Bzx(-x, y, z), rtol=1e-10)
        np.allclose(magnet.Bzxx(x, y, z), magnet.Bzxx(-x, y, z), rtol=1e-10)

    @pytest.mark.parametrize("x, y, z", [(0.0, 0.0, np.arange(50, 100, 5))])
    def test_rectmagnet_Bz_symmetry_z(self, magnet, x, y, z):
        """Test bz_func of RectMagnet symmetry in z direction"""

        np.allclose(magnet.Bz(x, y, z), magnet.Bz(x, y, -z), rtol=1e-10)

    @pytest.mark.parametrize("x, y, z", [(np.arange(100, 150, 5), -100, 100)])
    def test_rectmagnet_Bzx(self, magnet, x, y, z):
        """Test bzx_func by using against gradient of bz"""

        self.check_bzx(magnet, x, y, z)

    @pytest.mark.parametrize("x, y, z", [(np.arange(100, 150, 5), -100, 100)])
    def test_rectmagnet_Bzxx(self, magnet, x, y, z):
        """Test the bzxx_func of RectMagnet against the derivative bzx_func"""

        self.check_bzxx(magnet, x, y, z)
