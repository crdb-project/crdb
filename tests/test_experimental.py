from numpy.testing import assert_allclose
from numpy.testing import assert_equal

from crdb import all
from crdb.experimental import convert_energy
from crdb.experimental import energy_conversion_numbers


def test_energy_conversion_numbers():
    ecn = energy_conversion_numbers()
    assert_allclose(ecn["H"], (1, 1.000019), atol=1e-6)
    assert_allclose(ecn["He"], (2, 3.999834), atol=1e-6)


def test_convert_energy():
    tab = all()
    tab1 = tab[tab.e_type == "R"]
    tab2 = convert_energy(tab1, "R")
    assert_equal(tab2, tab1)
    tab2 = convert_energy(tab1, "EK")
    assert len(tab2) > 0
    assert len(tab2) < len(tab1)
