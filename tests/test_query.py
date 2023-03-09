import pytest

from crdb import query


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


def test_recarray():
    tab = query("Li")
    assert len(tab.sub_exp) > 1
