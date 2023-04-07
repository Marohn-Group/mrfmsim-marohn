"""Cacluations related to field"""
import numpy as np
import numba as nb
from .math import as_strided_x
import scipy


@nb.jit(nopython=True, parallel=True)
def B_offset(B_tot, f_rf, Gamma):
    """Calculate the resonance offset"""
    return B_tot - 2 * np.pi * f_rf / Gamma


def min_abs_offset(ext_B_offset, ext_pts):
    """Minimum absolute value of a matrix in x direction based on the window.

    The function is used to calculate the minimum B_offset during a saturation
    experiment.
    For each x-data point in the sample, calculate the resonance offset over
    the expanded grid. The points to the left and right of each grid point
    give the resonance offset as the cantilever moves. Find the minimum
    resonance offset over the range of array values corresponding to the
    cantilever motion, and compute the saturation polarization using that
    minimum offset and the given B1.

    To calculate the spin polarization profile resulting from the cantilever
    moving while spin-saturating irradiation is applied we use the following
    algorithm:
        If the resonance offset changed sign during the sweep, then the spin
        must have experienced a zero resonance offset during the sweep, so set
        the resonance offset to zero manually.
    This procedure mitigates the problem of previous algorithms not finding
    the true minimum resonance offset (and polarization) due to the finite grid
    size. While this new procedure will still not capture the shape of the
    polarization at the edge of the sensitive slice, it should produce a
    polarization which is properly saturated inside the sensitive slice.
    :param float b_offset: resonance offset of extended grid [mT]
    :param int window: number of grid point used to determine the minimum offset
    """
    window = 2 * ext_pts + 1
    b_offset_strided = as_strided_x(ext_B_offset, window)
    b_offset_abs_strided = as_strided_x(abs(ext_B_offset), window)

    return b_offset_abs_strided.min(axis=1) * np.logical_or(
        np.all(b_offset_strided > 0, axis=1),
        np.all(b_offset_strided < 0, axis=1),
    )


def xtrapz_fxdtheta(method, ogrid, n_pts, xrange, x0):
    r"""Calculate the integral of a function over a range of theta.

    .. math::
        \int_{xmin}^{xmax} f(x - x_0cos\theta)x_0cos\theta d\theta
    """

    theta = np.linspace(xrange[0], xrange[1], n_pts)
    grid_shape = tuple(np.prod(list(map(np.shape, ogrid)), axis=0))
    grid_shape_x = grid_shape[0]
    grid_dim = len(grid_shape)

    # calculate the new grid
    new_ogrid_shape = np.ones(grid_dim)
    new_ogrid_shape[0] = n_pts * grid_shape_x
    new_ogrid_shape = new_ogrid_shape.astype(int)

    # expand the dimension to (pts, 1, 1, 1)
    # expand the x grid dimension to (1, x_shape, 1, 1)
    # The result of addition is (pts, x_shape, 1, 1)
    # the final (x, y, z) is (pts * x_shape, 1, 1)
    grid_x = np.expand_dims(ogrid[0], axis=0)
    # dx = x0 * cos(theta)
    x = x0 * np.cos(theta)
    dx = np.expand_dims(x, axis=list(range(1, grid_dim + 1)))
    new_ogrid = [(grid_x - dx).reshape(new_ogrid_shape)] + ogrid[1:]

    # calculate the integral
    # new grid shape is (trapz_pts, x_shape, y_shape, z_shape)
    # dx has the shape of (trapz_pts, 1, 1, 1)
    # The multiplication is also an optimization here
    new_grid_shape = (n_pts,) + grid_shape
    integrand = method(*new_ogrid).reshape(new_grid_shape) * dx
    return np.trapz(integrand, x=theta, axis=0)


def xtrapz_field_gradient(Bzx_method, sample_ogrid, trapz_pts, x_0p):
    """Calculate CERMIT integral using Trapezoidal summation.

    The integrand is an odd function, therefore we can approximate the
    integral from -pi to pi, -pi to 0. Here we make an important
    assumption that the magnet is symmetric in the x direction. Therefore
    we approximate the integral from -np/2 to 0 and time the final result by 4.

    :param list sample_ogrid: ogrid generated by a numpy ogrid
        For one dimensional grid, the ogrid should be encapsulated in a list
    :param int trapz_pts: points to integrate across 2 pi.
        In this particular implementation, the number is divided by 4 for
        [-pi/2, 0 ] integration.
    """
    n_pts = int(trapz_pts / 4)
    integral = xtrapz_fxdtheta(Bzx_method, sample_ogrid, n_pts, [-np.pi / 2, 0], x_0p)
    return (4 / x_0p**2 / np.pi) * integral


def single_spin_field_gradient(
    magnet_origin, magnet_radius, mu0_Ms, mu_z, tip_sample_distance, geometry, x_0p
):
    """The analytical calculation for a single spin.

    The analytical solution to the exact equations for the delta k
    without any approximations as derived below:
    :math:`\Delta f = - \frac{f}{k x_{pk}^2} \langle F_{ts} x \rangle`
    where :math:`x_{pk}` is the zero-to-peak amplitude of the cantilever.
    This equation can be expressed as an integral over an angle
    :math:`\theta`
    For the *hangdown* geometry,

    .. math::
        F_{ts} = \mu_z \mu_0 M r^3 \dfrac{x^3 - 4z^2x}{(z^2 + x^2)^{7/2}}
    For the *SPAM* geometry,
    :math:`F_{ts} = \dfrac{\mu_z \mu_0 M r^3 x}{(x^2 + y^2)^{5/2}}`
    where :math:`\mu_z` is the spin magnetic moment, :math:`\mu_0 M` is
    the saturation magnetization of the tip, and r is the tip radius.

    .. math::
        \Delta f =  \frac{f}{2 \pi k x_{pk}^2} \int_{-\pi}^{\pi}
        \mu(x,y,z,\theta) \times \frac{\partial B_{z}^{\mathrm{tip}}
        (x-x_{pk}\cos \theta, y, z)}{\partial x} x_{pk}\cos \theta d\theta
    Substituting into the integral and introducing a unitless variable
    :math:`\hat{z} = z/x_{peak}` for the hangdown geometry and
    :math:`\hat{y}/x_{peak}` for the SPAM geometry,
    we obtain the following integrals:
    For the *hangdown* geometry,

    .. math::
        \Delta f = \frac{f}{2 k x_{pk}}\frac{\mu_z \mu_0 M}{a}
        (\frac{a}{z})^4 \times \frac{\bar{z}^4}{\pi}
        \int_0^{2\pi} \frac{\cos^4 \theta - 4\hat{z}^2\cos^2\theta}
        {(\hat{z}^2 + \cos^2\theta)^{7/2}} d\theta
    This integral (along with the :math:`\frac{\hat{z}^4}{\pi}` prefactor)
    can be solved exactly in Mathematica to give a solution in terms of
    Elliptic Integrals

    .. math::
        \frac{\hat{z}^3}{3\pi(\hat{z}^2 +1)}(4(2\hat{z}^4 -
        7\hat{z}^2 -1)E(-1/\hat{z}^2) -8(\hat{z}^4 - 1)K(-1/\hat{z}^2))
    where :math:`K(m)` and :math:`E(m)` are, respectively,
    the complete elliptic integrals of the first and second kind.
    For the *SPAM* geometry,

    .. math::
        \Delta f = \frac{f}{2 k x_{pk}} \frac{\mu_z \mu_0 M}
        {z} \left(\frac{a}{y}\right)^4 \times \frac{\hat{z}^4}{\pi}
        \int_0^{2\pi}\frac{\cos^2 \theta}{(\cos^2 \theta +
        \hat{y}^2)^{5/2}}d\theta
    This integral (along with the :math:`\frac{\hat{y}^4}{\pi}` prefactor
    can be solved exactly in terms of Elliptic integrals:

    .. math::
        \frac{4\hat{y}^3}{3\pi(1+\hat{y}^2)^2}[(1+\hat{y}^2)E(-1/\hat{y}^2)
        - (\hat{y}^2 -1)K(-1/\hat{y}^2)
    """

    if geometry == "SPAM":
        origin_sample_distance = magnet_origin[1] + tip_sample_distance
        Y = origin_sample_distance / x_0p
        val = -1.0 / Y**2
        ek = scipy.special.ellipk(val)
        ee = scipy.special.ellipe(val)

        I_term = (
            4.0
            * Y**3
            / (3.0 * np.pi * (1.0 + Y**2) ** 2)
            * ((1.0 + Y**2) * ek - (Y**2 - 1.0) * ee)
        )

    elif geometry == "hangdown":
        origin_sample_distance = magnet_origin[2] + tip_sample_distance
        Z = origin_sample_distance / x_0p
        val = -1.0 / Z**2
        ek = scipy.special.ellipk(val)
        ee = scipy.special.ellipe(val)

        I_term = (
            Z**3
            / (3.0 * np.pi * (1 + Z**2) ** 3)
            * (
                4.0 * (2.0 * Z**4 - 7.0 * Z**2 - 1.0) * ee
                - 8.0 * (Z**4 - 1.0) * ek
            )
        )

    const_term = (
        mu0_Ms * mu_z / magnet_radius * (magnet_radius / origin_sample_distance) ** 4
    )

    # Assuming the spin is completely saturated, from 1 to 0
    # polarization change is -1, hence the negative sign.
    dF_spin = const_term * I_term

    return dF_spin
