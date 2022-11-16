from mrfmsim_marohn.formulas.math import (
    hex_mul_sum,
    slice_matrix,
    as_strided_x,
    ogrid_sub,
    ogrid_method
)
import numpy as np


def test_hex_mul_sum():
    """Test the chained multiplication sum works for both matrix and scalar"""

    matrices = {i: np.random.rand(2, 3, 4) for i in ["b", "c", "d"]}
    matrices['sign'] = -1
    sum_value = hex_mul_sum(a=2, e=3, **matrices)

    assert np.isclose(
        sum_value, - np.sum(2 * 3 * matrices["b"] * matrices["c"] * matrices["d"])
    )


def test_slice_matrix():
    """Test slice matrix cuts the matrix in the center"""

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
    """Testing if as_strided_x maximum matches running max"""

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
    """Test ogrid_sub

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


def test_ogrid_method():
    """Test ogrid_method

    Test if the value accepts ogrid, and mapping. The result should be the same
    as the mesh grid result. For a 2-D array [array([[0], [2]]), array([[1, 2]])]
    is equivalent to a 2x2 grid of (x, y): (0, 1), (0, 2), (2, 1), (2, 2)
    """

    def distance2d(x, y):
        return x**2 + y**2

    dis = ogrid_method(distance2d, np.ogrid[0:2:2j, 1:2:2j])
    assert np.array_equal(dis, [[1, 4], [5, 8]])

    def distance3d(x, y, z):
        return x**2 + y**2 + z**2

    dis = ogrid_method(distance3d, np.ogrid[0:1:2j, 1:2:2j, 2:3:2j])

    # in the order of x, y, z. The most inner is the z
    assert np.array_equal(dis, [[[5, 10], [8, 13]], [[6, 11], [9, 14]]])

    # test against full mesh

    dis_mesh = distance3d(*np.mgrid[0:1:2j, 1:2:2j, 2:3:2j])
    assert np.array_equal(dis, dis_mesh)
