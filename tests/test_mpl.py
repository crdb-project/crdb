import numpy as np
import pytest

from crdb import all
from crdb import mpl

# These tests are dumb, they check whether functions run,
# but not the output. Still better than nothing.


@pytest.fixture
def table():
    tab = all()
    return tab[tab.quantity == "Li"]


def test_draw_references(table):
    mpl.draw_references(table)


def test_draw_table(table):
    assert set(np.unique(table.e_type)) == {"EKN", "R"}

    with pytest.raises(ValueError):
        # table contains incompatible e_types
        mpl.draw_table(table)

    table2 = table[table.e_type == "EKN"]
    mpl.draw_table(table2)


def test_draw_logo():
    mpl.draw_logo(1, 1)


def test_draw_timeseries(table):
    with pytest.warns(RuntimeWarning, match="input contains"):
        mpl.draw_timeseries(table)

    mask = []
    for dt in table.datetime:
        mask.append(";" not in dt)
    mask = np.array(mask)
    tab = table[mask]

    # no warning now
    mpl.draw_timeseries(tab)


def test_draw_timeseries_2(table):
    with pytest.warns(RuntimeWarning, match="input contains"):
        mpl.draw_timeseries(table, show_bin=True)
