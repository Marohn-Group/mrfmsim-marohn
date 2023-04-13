from mrfmsim_marohn import UNITS

def test_units():
    """Test if units are loaded correctly."""
    b1 = UNITS["B1"]
    assert b1["unit"] == "[mT]"
    assert b1["description"] == "transverse magnetic field"
    assert b1["latex_label"] == r"$B_1 \: [\mathrm{mT},]$"
    assert b1['format'] == ":.3f"
