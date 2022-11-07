from mrfmsim_marohn.formulas.math import (
    hex_mul_sum,
    slice_matrix,
    as_strided_x,
    min_abs_x,
    ogrid_sub,
    ogrid_method,
    xtrapz_integral,
)
import numpy as np


def test_hex_mul_sum():
    """Test the chained multiplication sum works for both matrix and scalar"""

    matrices = {i: np.random.rand(2, 3, 4) for i in ["b", "c", "d"]}
    sum_value = hex_mul_sum(a=2, e=3, **matrices)

    assert np.isclose(
        sum_value, np.sum(2 * 3 * matrices["b"] * matrices["c"] * matrices["d"])
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


def test_min_abs_x():
    """Test min_abs_x"""
    matrix_a = np.random.rand(30, 20, 10) - 0.3  # lower 0 crossing chance
    grid_ext = 2  # follow the behavior of extend x_0p both sides
    window = grid_ext * 2 + 1
    offset_min_calc = min_abs_x(matrix_a, window)

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


def test_min_abs_x_symmetry():
    """Test if min_abs_x result is symmetric
    If a matrix is flipped, the result should also be flipped
    """

    matrix_a = np.random.rand(20, 10, 5) - 0.3
    matrix_b = np.flip(matrix_a, axis=0)
    window = 5
    offset_min_a = min_abs_x(matrix_a, window)
    offset_min_b = min_abs_x(matrix_b, window)

    assert np.array_equal(offset_min_a, np.flip(offset_min_b, axis=0))


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


def test_xtrapz_integral_multi_dimension():
    """Test trapz integral when there are multiple grid points and dimension"""

    y = np.array([1, 2, 3, 4, 5, 6, 7]).reshape(7, 1, 1)
    step = 2

    xtrpaz = xtrapz_integral(y, [step, 0, 0], 1, 1)
    assert xtrpaz.shape == (2, 1, 1)
    assert np.array_equal(xtrpaz.flatten(), [12, 20])


def test_xtrapz_integral_linear():
    """Test trapz integral against 1D functions

    We test against a linear function y = 2.5x. Let the original grid size be 1,
    with ext_pts = 3, and xdiv_pts = 3. This gives the a fine grid
    of 25 pts, and final grid of 1 pt. The result should be the value at the
    mid point.
    """

    x = np.linspace(0, 24, 25)
    y = 2.5 * x

    assert xtrapz_integral(y, [4, 0, 0], 3, 3) == 2.5 * 24 * 24 / 2


def test_xtrapz_integral_nonlinear():
    """Test trapz integral against 1D functions

    We test against a linear function y = cosx. Let the original grid size be 1,
    with ext_pts = 3, and xdiv_pts = 3. This gives the a fine grid
    of 25 pts, and final grid of 1 pt. The result should be the value at the
    mid point.
    """

    x = np.linspace(-np.pi / 2, np.pi / 2, 25)
    y = np.cos(x)
    step = np.pi / (25 - 1) * 4

    assert np.isclose(xtrapz_integral(y, [step, 0, 0], 3, 3), 2, atol=5e-3)


def test_xtrapz_integral_against_theta():
    """Test trapz integral against 1D functions

    The original trapz integral is used to approximate function with equal
    theta steps of a position. Here we test that on different functions.

    y = 2.5x
    """

    theta = np.linspace(0, np.pi, 25)
    x = np.cos(theta)
    y = 2.5 * x
    trapz_theta = np.trapz(y, x)

    x = np.linspace(-1, 1, 25)
    y = 2.5 * x
    step = 2 / (25 - 1) * 4
    trapz_x = xtrapz_integral(y, [step, 0, 0], 3, 3)
    assert np.isclose(trapz_theta, trapz_x)
