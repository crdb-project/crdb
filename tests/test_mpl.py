import pytest

from crdb import all
from crdb import mpl


@pytest.fixture
def table():
    tab = all()
    tab = tab[tab.quantity == "Li"]
    return tab


def test_draw_references(table):
    mpl.draw_references(table)


def test_draw_table(table):
    mpl.draw_table(table)


def test_draw_logo():
    mpl.draw_logo(1, 1)
