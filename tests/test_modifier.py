from mrfmsim_marohn.modifier import numba_jit


def test_numba_jit():
    """Test the numba_jit decorator."""

    mod = numba_jit(nopython=True, parallel=True)

    def func(x):
        return x

    assert mod.metadata == "numba_jit(nopython=True, parallel=True)"
    assert mod(func)(1) == 1
