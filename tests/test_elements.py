from crdb import ELEMENTS
import pytest


@pytest.mark.parametrize("elem,z", [("H", 1), ("He", 2), ("Fe", 26), ("Es", 99)])
def test_elements(elem, z):
    assert ELEMENTS[elem] == z
