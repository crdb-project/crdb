"""
Experimental utilitites for the crdb Python package.

The functions in this module are not stable and their API can
change at any time. Use with caution.
"""
from typing import Dict, Tuple, Union

import numpy as np
from numpy.typing import NDArray

from crdb import ELEMENTS, valid_quantities
from crdb import solar_system_composition

NUCLEON_MASS = 0.9389187543299999  # GeV
ELECTRON_MASS = 0.51099895e-3  # GeV


def energy_conversion_numbers() -> Dict[str, Tuple[int, float]]:
    """
    Return dict with energy conversion numbers.

    Returns
    -------
    dict
        Maps the quantity name to a tuple (Z, A), where Z is the atomic number and A is
        the number of nucleons. Returns (1, NaN) for electrons and positrons.
    """
    comp = solar_system_composition()
    result = {k: (1, np.nan) for k in ("e-", "e+", "e-+e+")}
    for key, z in ELEMENTS.items():
        if key in comp:
            a, w = np.transpose(comp[key])
            a_mean = np.average(a, weights=w)
        else:
            a_mean = np.nan
        result[key] = (z, a_mean)

    for key in valid_quantities():
        if key.endswith("-bar") and key[:-4] in result:
            result[key] = result[key[:-4]]

    return result


def convert_energy(
    table: np.recarray, target: str = "EKN", approximate: bool = True
) -> np.recarray:
    """
    Convert e_type of all convertible quantities to target and removes the rest.

    Parameters
    ----------
    table : array
        CRDB table.
    target : str, optional
        What to convert the e_axis to.
    approximate : bool, optional
        Whether approximate conversion is allowed. An approximate conversion
        happens when an elemental flux with an unknown isotopic composition
        is converted and the effective number of nucleons is required.
        Default is true.

    Returns
    -------
    Converted table.
    """
    ecn = energy_conversion_numbers()

    result = table.copy()
    for i, t in enumerate(result):
        z, a = ecn.get(t.quantity, (np.nan, np.nan))
        if t.e_type == "R":
            if target == "R":
                pass
            elif target == "EK":
                _convert_energy(result, i, z)
                result[i].e_type = target
            elif target == "EKN":
                _convert_energy(result, i, z / a)
                result[i].e_type = target
            else:
                assert False
        elif t.e_type == "EK":
            if target == "R":
                _convert_energy(result, i, 1 / z)
                result[i].e_type = target
            elif target == "EK":
                pass
            elif target == "EKN":
                _convert_energy(result, i, 1 / a)
                result[i].e_type = target
            else:
                assert False
        elif t.e_type == "EKN":
            if target == "R":
                _convert_energy(result, i, a / z)
                result[i].e_type = target
            elif target == "EK":
                _convert_energy(result, i, a)
                result[i].e_type = target
            elif target == "EKN":
                pass
            else:
                assert False

    return result[~np.isnan(result.value) & (result.e_type == target)]


def _convert_energy(
    tab: np.recarray, mask: Union[int, NDArray], f: Union[float, NDArray]
) -> None:
    if np.ndim(f) > 0:
        f.shape = (len(f), 1)  # type:ignore
    tab[mask].e *= f
    tab[mask].e_bin *= f
    tab[mask].value /= f
    tab[mask].err_sta /= f
    tab[mask].err_sys /= f
