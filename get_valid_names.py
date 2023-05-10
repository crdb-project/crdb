"""Compute valid names."""
import crdb
import numpy as np

tab = crdb.all()

names = set()
for q in np.unique(tab.quantity):
    num, *rest = q.split("/")
    names.add(num)
    if rest:
        (den,) = rest
        names.add(den)

print(repr(tuple(sorted(names))))
