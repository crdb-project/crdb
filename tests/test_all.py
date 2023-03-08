from crdb import all
import pytest


@pytest.mark.parametrize("quantity", ("B/C", "H", "Li"))
def test_all(quantity):
    tab = all()
    mask = tab["quantity"] == quantity
    assert len(tab[mask]) > 1
