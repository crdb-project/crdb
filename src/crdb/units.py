"""
Units for the CRDB table data.

These are the base units in which the CRDB table data is given.
Use these instead of plain numbers to make code more readable,
e.g.::

    import crdb
    from crdb.mpl import draw_table
    from crdb.unit import TeV

    tab = crdb.query("e-")

    draw_table(tab, xunit=TeV)
"""

# units
GeV = 1
TeV = 1e3 * GeV
PeV = 1e3 * TeV
EeV = 1e3 * PeV
MeV = 1e-3 * GeV
keV = 1e-3 * MeV

GV = 1
TV = 1e3 * GV
PV = 1e3 * TV
EV = 1e3 * PV
MV = 1e-3 * GV
kV = 1e-3 * MV
