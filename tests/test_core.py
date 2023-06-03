import pytest
from crdb import ELEMENTS
from crdb import valid_quantities
from crdb import all
from crdb import query
from crdb import solar_system_composition


@pytest.mark.parametrize("quantity", ("B/C", "H", "Li"))
def test_all(quantity):
    tab = all()
    mask = tab["quantity"] == quantity
    assert len(tab[mask]) > 1


@pytest.mark.parametrize("elem,z", [("H", 1), ("He", 2), ("Fe", 26), ("Es", 99)])
def test_elements(elem, z):
    assert ELEMENTS[elem] == z


def test_last_element():
    assert list(ELEMENTS)[-1] == "Es"


@pytest.mark.parametrize(
    "quantity",
    (
        "Li",
        "e+",
        "B/C",
    ),
)
def test_query(quantity):
    tab = query(quantity)
    assert len(tab) > 1


def test_bad_query():
    with pytest.raises(ValueError):
        query("Foobar")

    with pytest.raises(ValueError):
        query("H", energy_type="Foobar")


def test_recarray_1():
    tab = query("Li")
    assert len(tab.sub_exp) > 1


def test_recarray_2():
    tab = query(("Li", "e+"))
    assert len(tab.sub_exp) > 1


def test_solar_system_composition():
    d = solar_system_composition()
    assert "H-bar" not in d
    assert d["H"] == [(1, 2.431e10), (2, 4.716e5)]
    assert d["Li"] == [(6, 4.21), (7, 51.26)]
    assert d["U"] == [(235, 0.000067), (238, 0.009238)]


def test_valid_quantities():
    q = valid_quantities()

    assert "H" in q
    assert "Li" in q
    assert "1H-bar" in q
