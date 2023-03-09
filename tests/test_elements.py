import pytest

from crdb import ELEMENTS


@pytest.mark.parametrize("elem,z", [("H", 1), ("He", 2), ("Fe", 26), ("Es", 99)])
def test_elements(elem, z):
    assert ELEMENTS[elem] == z


def test_last_element():
    assert list(ELEMENTS)[-1] == "Es"
