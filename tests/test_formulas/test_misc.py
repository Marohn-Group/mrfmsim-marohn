from mrfmsim_marohn.formulas.misc import convert_grid_pts


def test_convert_grid_pts():
    """Test convert_grid_pts.

    Make sure the final value is an int and is the floor value."""

    assert convert_grid_pts(2, [1.5, 1, 1]) == 1
    assert convert_grid_pts(1.1, [1.1, 1, 1]) == 1
