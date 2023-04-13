from mrfmsim_marohn.formulas.math import (
    slice_matrix,
    as_strided_x,
    ogrid_sub,
)
import numpy as np


def test_slice_matrix():
    """Test slice matrix cuts the matrix in the center."""

    matrix = np.array(
        [[1, 2, 3, 4, 5], [11, 22, 33, 44, 55], [111, 222, 333, 444, 555]]
    )

    assert np.array_equal(
        slice_matrix(matrix, (3, 3)),
        np.array([[2, 3, 4], [22, 33, 44], [222, 333, 444]]),
    )
    assert np.array_equal(slice_matrix(matrix, (1, 3)), np.array([[22, 33, 44]]))

    # check that the slice matrix is a view of the original
    assert np.shares_memory(slice_matrix(matrix, (1, 3)), matrix)


def test_as_strided_x():
    """Testing if as_strided_x maximum matches running max."""

    matrix_a = np.random.rand(30, 20, 10)
    window = 10

    new_shape = (
        matrix_a.shape[0] - window + 1,
        matrix_a.shape[1],
        matrix_a.shape[2],
    )
    # running maximum with a python loop
    result = np.zeros(new_shape)
    for i in range(result.shape[0]):
        result[i, ...] = np.amax(matrix_a[i : i + window, ...], axis=0)

    # running maximum calculated with strided_axis0
    strided_result = as_strided_x(matrix_a, window).max(axis=1)

    assert np.array_equal(result, strided_result)


def test_ogrid_sub():
    """Test ogrid_sub.

    The sub results in a iterable mapping. Here tests if the
    dimension and values are correct.
    """

    array2d = list(ogrid_sub(np.ogrid[-1:1:3j, -1:1:3j], [1, 2]))
    result0 = [[-2], [-1], [0]]  # (3, 1)
    result1 = [[-3, -2, -1]]  # (1, 3)

    assert np.array_equal(array2d[0], result0)
    assert np.array_equal(array2d[1], result1)

    array3d = list(ogrid_sub(np.ogrid[-1:1:2j, -1:1:2j, -1:1:2j], [1, 2, 3]))
    result0 = [[[-2.0]], [[0.0]]]  # (2, 1, 1)
    result1 = [[[-3.0], [-1.0]]]  # (1, 2, 1)
    result2 = [[[-4.0, -2.0]]]  # (1, 1, 2)

    assert np.array_equal(array3d[0], result0)
    assert np.array_equal(array3d[1], result1)
    assert np.array_equal(array3d[2], result2)
