__all__ = ["numba_jit"]

import numba as nb


def numba_jit(**kwargs):
    """Numba jit modifier with keyword arguments.

    Add metadata to numba.jit. The numba decorator outputs
    all the parameters makes it hard to read.
    Use the decorator the same way as numba.jit().
    """

    def decorator(func):
        func = nb.jit(**kwargs)(func)
        return func

    meta = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    decorator.metadata = f"numba_jit({meta})"
    return decorator
