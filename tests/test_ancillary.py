import mrfmsim_marohn.ancillary as anc
import numpy as np


def test_run_method():
    """Test if run method works with numpy functions"""

    result = anc.run_method(np.dot, a=np.array([1, 2]), b=np.array([3, 4]))

    assert result == 11


def test_hex_mul_sum():
    """Test the chained multiplication sum works for both matrix and scalar"""

    matrices = {i: np.random.rand(2, 3, 4) for i in ["b", "c", "d"]}
    sum_value = anc.hex_mul_sum(a=2, e=3, **matrices)

    assert np.isclose(
        sum_value, np.sum(2 * 3 * matrices["b"] * matrices["c"] * matrices["d"])
    )

def test_slice_matrix():
    """Test slice matrix cuts the matrix in the center"""


    matrix = np.array([[1, 2, 3, 4, 5], [11, 22, 33, 44, 55], [111, 222, 333, 444, 555]])

    assert np.array_equal(anc.slice_matrix(matrix, (3, 3)), np.array([[2, 3, 4], [22, 33, 44], [222, 333, 444]]))
    assert np.array_equal(anc.slice_matrix(matrix, (1, 3)), np.array([[22, 33, 44]]))

    # check that the slice matrix is a view of the original
    assert np.shares_memory(anc.slice_matrix(matrix, (1, 3)), matrix)

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
    strided_result = anc.as_strided_x(matrix_a, window).max(axis=1)

    assert np.array_equal(result, strided_result)

def test_min_abs_x():
    """Test min_abs_x"""
    matrix_a = np.random.rand(30, 20, 10) - 0.3  # lower 0 crossing chance
    grid_ext = 2  # follow the behavior of extend x_0p both sides
    window = grid_ext * 2 + 1
    offset_min_calc = anc.min_abs_x(matrix_a, window)

    #  a python loop for the logic
    new_shape = (matrix_a.shape[0] - window + 1,) + matrix_a.shape[1:]

    offset_min_exp = np.zeros(new_shape)
    for i in range(new_shape[0]):

        matrix_offset_max = np.amax(matrix_a[i : i + window, :, :], axis=0)
        matrix_offset_min = np.amin(matrix_a[i : i + window, :, :], axis=0)
        minabs_pos = np.argmin(abs(matrix_a[i : i + window, :, :]), axis=0)

        for j in range(new_shape[1]):
            for k in range(new_shape[2]):
                if not (
                    (matrix_offset_max[j, k] > 0)
                    & (matrix_offset_min[j, k] < 0)
                ):
                    offset_min_exp[i, j, k] = abs(
                        matrix_a[i : i + window, :, :]
                    )[minabs_pos[j, k], j, k]

    assert np.array_equal(offset_min_calc, offset_min_exp)

def test_min_abs_x_symmetry():
    """Test if min_abs_x result is symmetric
    If a matrix is flipped, the result should also be flipped
    """

    matrix_a = np.random.rand(20, 10, 5) - 0.3
    matrix_b = np.flip(matrix_a, axis=0)
    window = 5
    offset_min_a = anc.min_abs_x(matrix_a, window)
    offset_min_b = anc.min_abs_x(matrix_b, window)

    assert np.array_equal(
        offset_min_a, np.flip(offset_min_b, axis=0)
    )
