#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Defines the grid objects. Performance wise it is faster to start a grid
based on a cuboid shape, the RectGrid can be used directly or inherited for
additional functions.
"""

from re import U
import numpy as np
from mrfmsim.component import ComponentBase
from mrfmsim_marohn import UNITS


class Grid(ComponentBase):
    """Instantiate a rectangular grid with length, step and origin
    The result grid has equal spacing in each dimension.
    """

    _units = UNITS

    def __init__(self, shape, step, origin=[0, 0, 0]):
        """Construct the grid object
        The grid's step sizes, lengths, and the number of points is fixed at
        instantiation time.  The grid's step sizes and lengths number are thus
        *not* updated if you manually reset the ``L`` or ``dL`` elements of
        the object manually later.
        If the lengths (``L``, etc) are not an integer multiple of the step
        sizes (``dL``, etc), then use for the lengths the closest multiple of
        the step sizes. This rounding is done silently and no error is flagged.
        .. Note::
            The grid shape are forced to be odd in x and y direction, to avoid
            artifact when convolve.
        :param np.array length: array of lengths along (x, y, z)
        :param np.array step: a list of step sizes
        :param np.array origin: the grid origin
        :ivar np.array grid_length: actual lengths of the grid. This is recalculated
            based on rounded value of grid shape and step size.
        :ivar np.array grid_origin: grid origin
        :ivar np.array grid_step: grid setup size in x, y, z direction
        :ivar float v_voxel: the volume of each grid voxel
        :ivar tuple grid_shape: grid dimension
            (number of points in x, y, z direction)
        :ivar np.array _range: range in (x, y, z direction), shape (3, 2)
        :ivar np.array grid_array: the grid coordinates in x, y, z direction
        """

        self.grid_origin = np.array(origin, dtype=np.float64)
        self.grid_step = np.array(step, dtype=np.float64)
        self.grid_voxel = self.grid_step.prod()
        self.grid_shape = np.array(shape)
        self.grid_range = (self.grid_shape - [1, 1, 1]) * self.grid_step
        self.grid_length = self.grid_shape * self.grid_step

    @staticmethod
    def grid_extents(length, origin):
        """Calculate grid extents based on the grid length and origin

        The result is column stacked into a dimension of (3, 2)
        """

        return np.column_stack((-length / 2 + origin, length / 2 + origin))

    @property
    def grid_array(self):
        """Generate a open mesh-grid of the given grid dimensions
        The benefit of the property is that it cannot be modified,
        therefore, it is not included when using ``vars()`` to obtain
        the object dictionary. It also generates at runtime.
        """

        extents = self.grid_extents(self.grid_range, self.grid_origin)

        return np.ogrid[
            extents[0][0] : extents[0][1] : self.grid_shape[0] * 1j,
            extents[1][0] : extents[1][1] : self.grid_shape[1] * 1j,
            extents[2][0] : extents[2][1] : self.grid_shape[2] * 1j,
        ]

    def extend_grid_method(self, ext_pts):
        """Extend grid by number of points in x, y, z direction (one side)"""

        ext_shape = self.grid_shape + np.array(ext_pts) * 2
        ext_range = (ext_shape - [1, 1, 1]) * self.grid_step
        extents = self.grid_extents(ext_range, self.grid_origin)

        return np.ogrid[
            extents[0][0] : extents[0][1] : ext_shape[0] * 1j,
            extents[1][0] : extents[1][1] : ext_shape[1] * 1j,
            extents[2][0] : extents[2][1] : ext_shape[2] * 1j,
        ]

    def extend_fine_grid_method(self, ext_pts, xdiv_pts):
        """Extend grid by number of points in x, y, z direction with fine grid

        :param list div_pts: points in between regular grid points
        """
        div_pts = [xdiv_pts + 1, 1, 1]

        ext_shape = (self.grid_shape + np.array(ext_pts) * 2 - 1) * div_pts + 1
        ext_range = (ext_shape - [1, 1, 1]) * self.grid_step / div_pts
        extents = self.grid_extents(ext_range, self.grid_origin)

        return np.ogrid[
            extents[0][0] : extents[0][1] : ext_shape[0] * 1j,
            extents[1][0] : extents[1][1] : ext_shape[1] * 1j,
            extents[2][0] : extents[2][1] : ext_shape[2] * 1j,
        ]
