from mrfmsim_marohn.formulas.math import (
    create_func,
    numba_sum,
    numba_sum_of_multiplication,
    sum_of_multiplication,
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


def test_create_func():
    """Test create_func."""

    func = create_func("add", 'def add(a, b): """Add a and b."""; return a + b')
    assert func(1, 2) == 3
    assert func.__name__ == "add"
    assert func.__doc__ == "Add a and b."


def test_nb_summation():
    """Test numba summation function creation."""

    func = numba_sum(["a", "b"])

    assert func.__name__ == "numba_sum"
    assert func.__doc__ == "Sum of a, b."
    assert func(1, 2) == 3


def test_numba_sum_of_multiplication():
    """Test numba sum of multiplication function creation."""

    func = numba_sum_of_multiplication(["a", "b", "c"])

    assert func.__name__ == "numba_sum_of_multiplication"
    assert func.__doc__ == "Sum of the product of a, b, c."
    assert func(1, 2, np.array([1, 2, 3])) == 12


def test_sum_of_multiplication():
    """Test the chained multiplication sum works for both matrix and scalar."""

    matrices = {i: np.random.rand(2, 3, 4) for i in ["b", "c", "d"]}
    matrices["f"] = -1
    sum_value = sum_of_multiplication(a=2, e=3, **matrices)

    assert np.isclose(
        sum_value, -np.sum(2 * 3 * matrices["b"] * matrices["c"] * matrices["d"])
    )
