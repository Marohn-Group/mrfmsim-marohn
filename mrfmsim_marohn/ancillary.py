"""General function to support function definition"""

import numpy as np
import numba as nb


def run_method(method, **kwargs):
    """Execute given method

    Keyword arguments only. The use case is when the method is a user
    input instead of built in the graph.
    """
    return method(**kwargs)


@nb.jit(nopython=True, parallel=True)
def hex_mul_sum(a, b, c, d, e):
    """Summation of 5 matrices or scalar

    To use numba jit, the compromise is to explicitly define the parameters,
    meaning we cannot define a function with arbitrary number of parameters.
    The method is faster than reduce or other numpy tricks.

    """
    return np.sum(a * b * c * d * e)


def slice_matrix(matrix, shape):
    """Slice numpy matrix

    The function only slice the matrix in the middle based on the shape.
    The resulting array should be a view of the original array,
    which provides memory and speed improvement.

    :param ndarray matrix: a numpy array.
    :param tuple shape: sliced shape, has the same dimension as the matrix.
        The shape along the sliced axis should be the same oddity as the matrix
    """

    oshape = np.array(matrix.shape)
    shape = np.array(shape)

    index_i = ((oshape - shape) / 2).astype(int)
    index_f = index_i + shape

    slice_index = []
    for i in range(shape.size):
        slice_index.append(slice(index_i[i], index_f[i]))

    return matrix[tuple(slice_index)]


def as_strided_x(dataset, window):
    """This is the function for adjusting the stride size in x direction
    The operation is very fast and does not require extra memory because it
    only defines the stride size rather than creating a new array
    For a dataset with a shape of (6, 5, 4) with a window of 3 in x direction,
    the resulting array shape is (4, 5, 4). The two parameters new is
    (4, 6, 5, 4), stride is (160, 160, 32, 8), if each element is 2 bytes
    For example to determine the max value of an 3 dimensional array for every
    3 elements in x direction::
        dataset_strided = strided_axis0(dataset, 3)
        dataset_strided.max(axis = 1)
    For more information see:
        https://docs.scipy.org/doc/numpy/reference/generated/
        numpy.lib.stride_tricks.as_strided.html#numpy.lib.stride_tricks.as_strided
        https://www.jessicayung.com/numpy-arrays-memory-and-strides/
    :param array dataset: the dataset target to determine max and min
                        (or other running operations)
    :param int window: the size of a sliding window for the dataset
    :return: strided dataset
    :rtype: ndarray
    """

    new = (dataset.shape[0] - window + 1, window) + dataset.shape[1:]
    strides = (dataset.strides[0],) + dataset.strides

    return np.lib.stride_tricks.as_strided(
        dataset, shape=new, strides=strides, writeable=False
    )


def min_abs_x(matrix, window):
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

    b_offset_strided = as_strided_x(matrix, window)
    b_offset_abs_strided = as_strided_x(abs(matrix), window)

    return b_offset_abs_strided.min(axis=1) * np.logical_or(
        np.all(b_offset_strided > 0, axis=1),
        np.all(b_offset_strided < 0, axis=1),
    )
