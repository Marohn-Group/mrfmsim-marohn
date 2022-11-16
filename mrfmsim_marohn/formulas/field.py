"""Cacluations related to field"""
import numpy as np
import numba as nb
from .math import as_strided_x


@nb.jit(nopython=True, parallel=True)
def B_offset(B_tot, f_rf, Gamma):
    """Calculate the resonance offset"""
    return B_tot - 2 * np.pi * f_rf / Gamma


def min_abs_offset(ext_B_offset, ext_pts):
    """Minimum absolute value of a matrix in x direction based on the window

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
    :param int window: number of grid point use to determine the minimum offset
    """
    window = 2 * ext_pts + 1
    b_offset_strided = as_strided_x(ext_B_offset, window)
    b_offset_abs_strided = as_strided_x(abs(ext_B_offset), window)

    return b_offset_abs_strided.min(axis=1) * np.logical_or(
        np.all(b_offset_strided > 0, axis=1),
        np.all(b_offset_strided < 0, axis=1),
    )


def xtrapz_fxdtheta(method, ogrid, trapz_pts, xrange, x0):
    r"""Trapz summation to calculate

    .. math::
        \int_{xmin}^{xmax} f(x - x_0cos\theta)x_0cos\theta d\theta
    """

    theta = np.linspace(xrange[0], xrange[1], trapz_pts)
    grid_shape = tuple(np.prod(list(map(np.shape, ogrid)), axis=0))
    grid_shape_x = grid_shape[0]
    grid_dim = len(grid_shape)

    # calculate the new grid
    new_ogrid_shape = np.ones(grid_dim)
    new_ogrid_shape[0] = trapz_pts * grid_shape_x
    new_ogrid_shape = new_ogrid_shape.astype(int)

    # expand the dimension to (pts, 1, 1, 1)
    # expand the x grid dimension to (1, x_shape, 1, 1)
    # the result of addition is (pts, x_shape, 1, 1)
    # the final (x, y, z) is (pts * x_shape, 1, 1)
    grid_x = np.expand_dims(ogrid[0], axis=0)
    # dx = x0 * cos(theta)
    x = x0 * np.cos(theta)
    dx = np.expand_dims(x, axis=list(range(1, grid_dim + 1)))
    new_ogrid = [(grid_x - dx).reshape(new_ogrid_shape)] + ogrid[1:]

    # calculate the integral
    # new grid shape is (trapz_pts, x_shape, y_shape, z_shape)
    # dx has the shape of (trapz_pts, 1, 1, 1)
    # the multiplication is also an optimization here
    new_grid_shape = (trapz_pts,) + grid_shape
    integrand = method(*new_ogrid).reshape(new_grid_shape) * dx
    return np.trapz(integrand, x=theta, axis=0)


def xtrapz_field_gradient(Bzx_method, sample_ogrid, trapz_pts, x_0p):
    """Calculate CERMIT integral using Trapezoidal summation

    The integrand is odd function, therefore we can approximate the
    integral from -pi to pi, to -pi to 0. Here we make an important
    assumption that the magnet is symmetric in x direction. Therefore
    we approximate the integral from -np/2 to 0 and time the final result by 4.

    :param list sample_ogrid: ogrid generated by numpy ogrid
        For one dimensional grid, the ogrid should be encapsulated in a list
    """

    integral = xtrapz_fxdtheta(
        Bzx_method, sample_ogrid, trapz_pts, [-np.pi / 2, 0], x_0p
    )
    return (4 / x_0p**2) * integral
