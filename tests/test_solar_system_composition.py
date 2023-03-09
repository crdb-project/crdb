from crdb import solar_system_composition


def test_solar_system_composition():
    d = solar_system_composition()
    assert "H-bar" not in d
    assert d["H"] == [(1, 2.431e10), (2, 4.716e5)]
    assert d["Li"] == [(6, 4.21), (7, 51.26)]
    assert d["U"] == [(235, 0.000067), (238, 0.009238)]
