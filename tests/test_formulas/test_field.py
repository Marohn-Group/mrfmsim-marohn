"""Test un-categorized formulas under __init__.py"""
from mrfmsim_marohn.formulas import (
    B_offset,
    xtrapz_fxdtheta,
    xtrapz_field_gradient,
    min_abs_offset,
)
import numpy as np


def test_B_offset():
    """Test B_offset
    Test the hydrogen atom
    """

    Gamma = 267.5222005  # rad MHz/T
    B_tot = 4.6973188  # T
    f_rf = 200  # MHz

    assert np.isclose(B_offset(B_tot, f_rf, Gamma), 0)


def test_min_abs_offset():
    """Test min_abs_x"""
    matrix_a = np.random.rand(30, 20, 10) - 0.3  # lower 0 crossing chance
    grid_ext = 2  # follow the behavior of extend x_0p both sides
    window = grid_ext * 2 + 1
    offset_min_calc = min_abs_offset(matrix_a, grid_ext)

    #  a python loop for the logic
    new_shape = (matrix_a.shape[0] - window + 1,) + matrix_a.shape[1:]

    offset_min_exp = np.zeros(new_shape)
    for i in range(new_shape[0]):

        matrix_offset_max = np.amax(matrix_a[i : i + window, :, :], axis=0)
        matrix_offset_min = np.amin(matrix_a[i : i + window, :, :], axis=0)
        minabs_pos = np.argmin(abs(matrix_a[i : i + window, :, :]), axis=0)

        for j in range(new_shape[1]):
            for k in range(new_shape[2]):
                if not ((matrix_offset_max[j, k] > 0) & (matrix_offset_min[j, k] < 0)):
                    offset_min_exp[i, j, k] = abs(matrix_a[i : i + window, :, :])[
                        minabs_pos[j, k], j, k
                    ]

    assert np.array_equal(offset_min_calc, offset_min_exp)


def test_min_abs_offset_symmetry():
    """Test if min_abs_x result is symmetric
    If a matrix is flipped, the result should also be flipped
    """

    matrix_a = np.random.rand(20, 10, 5) - 0.3
    matrix_b = np.flip(matrix_a, axis=0)
    ext_pts = 2
    offset_min_a = min_abs_offset(matrix_a, ext_pts)
    offset_min_b = min_abs_offset(matrix_b, ext_pts)

    assert np.array_equal(offset_min_a, np.flip(offset_min_b, axis=0))


class TestXTrapzFxDtheta:
    """Test xtrapz_fxdtheta"""

    def test_xtrapz_fxdtheta_cos(self):
        r"""Test xtrapz_fxdtheta against cosxdx

        Let's consider the field method returns 1, the trapz integral
        should return the value of

        .. math::

            \int{x_0 cos\theta d\theta}

        The results:
        (-pi/2 -> 0): x0
        (-pi -> 0): 0
        """

        def method(x):
            """A function that is independent from x"""
            return np.ones(x.size)

        ogrid = [np.linspace(0, 3, 3)]
        x0 = 3
        trapz_pts = 20

        # range from -pi, 0
        integral = xtrapz_fxdtheta(method, ogrid, trapz_pts, [-np.pi, 0], x0)
        assert integral.shape == (3,)
        assert np.allclose(integral, (0, 0, 0), rtol=1e-3)

        # range from -pi/2, 0
        integral = xtrapz_fxdtheta(method, ogrid, trapz_pts, [-np.pi / 2, 0], x0)
        assert np.allclose(integral, (3, 3, 3), rtol=1e-3)

    def test_xtrapz_xtrapz_fxdtheta_xcos(self):
        r"""Test xtrapz_fxdtheta against xcos

        Let's consider a case where the field f(x) = x

        .. math::

            \int{(x-x_0 cos\theta)x_0 cos\theta d\theta}}

        The results:
        (-pi/2 -> 0): x*x0 - x0^2*pi/4
        (-pi -> 0): - x0^2 * pi/2
        """

        def method(x):
            """A function that is independent from x"""
            return x

        ogrid = [np.linspace(0, 2, 3)]
        trapz_pts = 20
        x0 = 3

        # range from -pi/2, 0
        integral = xtrapz_fxdtheta(method, ogrid, trapz_pts, [-np.pi / 2, 0], x0)
        assert integral.shape == (3,)
        assert np.allclose(
            integral, (-9 * np.pi / 4, 3 - 9 * np.pi / 4, 6 - 9 * np.pi / 4), rtol=5e-3
        )

        # range from -pi, 0
        integral = xtrapz_fxdtheta(method, ogrid, trapz_pts, [-np.pi, 0], x0)
        assert integral.shape == (3,)
        assert np.allclose(
            integral, (-9 / 2 * np.pi, -9 / 2 * np.pi, -9 / 2 * np.pi), rtol=5e-3
        )

    def test_xtrapz_xtrapz_fxdtheta_x2cos(self):
        r"""Test xtrapz_fxdtheta against x2cos

        Let's consider a case where the field f(x) = x

        .. math::

            \int{(x-x_0 cos\theta)x_0 cos\theta d\theta}}
         The results:
        (-pi/2 -> 0): x^2*x0 - pi/2*x*x0^2 + 2/3 * x0^3
        (-pi -> 0): - pi*x*x0^2
        """

        def method(x):
            """A function that is independent from x"""
            return x**2

        ogrid = [np.linspace(0, 2, 3)]
        trapz_pts = 20
        x0 = 3

        # range from -pi/2, 0
        integral = xtrapz_fxdtheta(method, ogrid, trapz_pts, [-np.pi / 2, 0], x0)
        assert integral.shape == (3,)
        assert np.allclose(
            integral, (18, 21 - 9 / 2 * np.pi, 30 - 9 * np.pi), rtol=5e-3
        )

        # range from -pi, 0
        integral = xtrapz_fxdtheta(method, ogrid, trapz_pts, [-np.pi, 0], x0)
        assert integral.shape == (3,)
        assert np.allclose(integral, (0, -9 * np.pi, -18 * np.pi), rtol=5e-3)

    def test_xtrapz_fxdtheta_multidim(self):
        """Test xtrapz_fxdtheta against xcos for multi-dimensions"""

        def method(x, y):
            """A function that is independent from x"""
            return x + 0.5 * y

        ogrid = np.ogrid[0:2:3j, 0:1:2j]
        trapz_pts = 20
        x0 = 1

        # range from -pi/2, 0
        integral = xtrapz_fxdtheta(method, ogrid, trapz_pts, [-np.pi / 2, 0], x0)
        assert integral.shape == (3, 2)
        assert np.allclose(
            integral,
            [
                [-np.pi / 4, 0.5 - np.pi / 4],
                [1 - np.pi / 4, 1.5 - np.pi / 4],
                [2 - np.pi / 4, 2.5 - np.pi / 4],
            ],
            rtol=5e-3,
        )


class TestXTrapzFieldGradient:
    """Test trapz field gradient"""

    def test_xtrapz_field_gradient_smallamp(self):
        """Test gradient against a small x0p

        When the 0 to peak is very small, the integrand is independent of
        costheta. Here we "fake" a small grid step for x direction, because
        grid step here is only used to calculate x_0p. The cantilever is 150 nm
        away from the sample and 10 nm off center (avoid 0 in rtol)
        """

        from mrfmsim_marohn.components import RectangularMagnet, Grid

        magnet = RectangularMagnet(
            length=[40.0, 60.0, 100.0], mu0_Ms=1800.0, origin=[10.0, 0.0, 200.0]
        )
        grid = Grid(shape=[3, 2, 1], step=[50, 50, 50])

        trapz_pts = 32
        x_0p = 0.01

        gradient = xtrapz_field_gradient(
            magnet.Bzx_method, grid.grid_array, trapz_pts, 0.01
        )

        real = magnet.Bzx_method(*grid.grid_array) * 4 / x_0p / np.pi

        assert gradient.shape == (3, 2, 1)
        assert np.allclose(gradient, real, rtol=1e-2)

    def test_xtrapz_field_gradient_large_distance(self):
        """Test gradient against a large tip sample separation

        When the distance is very large, the change of Bzx in between grid points
        are small.
        """

        from mrfmsim_marohn.components import RectangularMagnet, Grid

        magnet = RectangularMagnet(
            length=[40.0, 60.0, 100.0], mu0_Ms=1800.0, origin=[10.0, 0.0, 3000.0]
        )
        grid = Grid(shape=[3, 2, 1], step=[50, 50, 50])

        trapz_pts = 32
        x_0p = 50

        gradient = xtrapz_field_gradient(
            magnet.Bzx_method, grid.grid_array, trapz_pts, x_0p=50
        )

        real = magnet.Bzx_method(*grid.grid_array) * 4 / x_0p / np.pi

        assert np.allclose(gradient, real, rtol=1e-2)
