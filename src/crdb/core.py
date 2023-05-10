"""Core library functions."""
from __future__ import annotations

import csv
from datetime import datetime, timedelta
import re
import ssl
import tempfile
import urllib.request as rq
from pathlib import Path
from typing import Dict
from typing import List
from typing import Sequence
from typing import Tuple
from typing import Union

import cachier
import numpy as np
from numpy.typing import NDArray

# generated from np.unqiue(crdb.all().quantity)
VALID_NAMES = (
    '10B/11B',
    '10B/9Be',
    '10B/B',
    '10Be/9Be',
    '10Be/Be',
    '11B/10B',
    '11B/B',
    '12C/C',
    '13C/12C',
    '13C/C',
    '14N/16O',
    '14N/N',
    '15N/16O',
    '15N/N',
    '16O/O',
    '17O/16O',
    '17O/O',
    '18O/16O',
    '18O/O',
    '19F/20Ne',
    '1H',
    '1H-bar',
    '1H-bar/1H',
    '1H-bar/H',
    '1H-bar/e+',
    '1H-bar/e-',
    '1H/He',
    '1H/e+',
    '1H/e-',
    '20Ne/Ne',
    '21Ne/20Ne',
    '21Ne/Ne',
    '22Ne/20Ne',
    '22Ne/Ne',
    '23Na/Na',
    '24Mg/Mg',
    '25Mg/24Mg',
    '25Mg/Mg',
    '26Al/27Al',
    '26Al/Al',
    '26Mg/24Mg',
    '26Mg/Mg',
    '27Al/Al',
    '28Si/Si',
    '29Si/28Si',
    '29Si/Si',
    '2H',
    '2H-bar',
    '2H/1H',
    '2H/3He',
    '2H/4He',
    '2H/H',
    '2H/He',
    '30Si/28Si',
    '30Si/Si',
    '31P/32S',
    '31P/P',
    '32S/S',
    '33S/32S',
    '33S/S',
    '34S/32S',
    '34S/S',
    '35Cl/Cl',
    '36Ar/Ar',
    '36Cl/Cl',
    '36S/32S',
    '37Ar/36Ar',
    '37Ar/Ar',
    '37Cl/35Cl',
    '37Cl/Cl',
    '38Ar/36Ar',
    '38Ar/Ar',
    '39K/K',
    '3He',
    '3He/4He',
    '3He/He',
    '40Ar/36Ar',
    '40Ar/Ar',
    '40Ca/Ca',
    '40Ca/Fe',
    '40K/K',
    '41Ca/40Ca',
    '41Ca/Ca',
    '41K/K',
    '42Ca/40Ca',
    '42Ca/Ca',
    '43Ca/40Ca',
    '43Ca/Ca',
    '44Ca/40Ca',
    '44Ca/Ca',
    '44Ti/48Ti',
    '44Ti/Ti',
    '46Ca/Ca',
    '46Ti/48Ti',
    '46Ti/Ti',
    '47Ti/48Ti',
    '47Ti/Ti',
    '48Ti/Ti',
    '49Ti/Ti',
    '49V/49Ti',
    '49V/50V',
    '49V/51V',
    '49V/V',
    '4He',
    '50Cr/52Cr',
    '50Cr/Cr',
    '50Ti/48Ti',
    '50Ti/Ti',
    '50V/V',
    '51Cr/51V',
    '51Cr/52Cr',
    '51Cr/Cr',
    '51V/50V',
    '51V/V',
    '52Cr/Cr',
    '53Cr/52Cr',
    '53Cr/Cr',
    '53Mn/Mn',
    '54Cr/Cr',
    '54Fe/56Fe',
    '54Fe/Fe',
    '54Mn/53Mn',
    '54Mn/Mn',
    '55Fe/56Fe',
    '55Fe/Fe',
    '55Mn/53Mn',
    '55Mn/Mn',
    '56Fe/Fe',
    '56Ni/Ni',
    '57Co/59Co',
    '57Co/60Ni',
    '57Co/Co',
    '57Fe/56Fe',
    '57Fe/Fe',
    '58Fe/56Fe',
    '58Fe/Fe',
    '58Ni/Ni',
    '59Co/57Co',
    '59Co/60Ni',
    '59Co/Co',
    '59Ni/58Ni',
    '60Ni/58Ni',
    '60Ni/Ni',
    '61Ni/58Ni',
    '62Ni/58Ni',
    '62Ni/Ni',
    '63Cu/Cu',
    '64Ni/58Ni',
    '64Zn/Zn',
    '65Cu/Cu',
    '66Zn/Zn',
    '67Ga/Ga',
    '67Zn/Zn',
    '68Zn/Zn',
    '69Ga/Ga',
    '6Li/7Li',
    '6Li/Li',
    '70Ge/Ge',
    '70Zn/Zn',
    '71Ga/Ga',
    '71Ge/Ge',
    '72Ge/Ge',
    '73As/As',
    '73Ge/Ge',
    '74+75+76+77+78Se/Se',
    '74Ge/Ge',
    '75As/As',
    '76Ge/Ge',
    '78+80+81+82Kr/Kr',
    '79Br/Br',
    '7Be/9Be',
    '7Be/9Be+10Be',
    '7Be/Be',
    '7Li/6Li',
    '7Li/9Be',
    '7Li/Li',
    '80+82Se/Se',
    '81Br/Br',
    '83+84+86Kr/Kr',
    '84+85+86Sr/Sr',
    '87+88Sr/Sr',
    '9Be/7Be',
    '9Be/Be',
    'Ac/Zgeq55',
    'Ac/Zgeq70',
    'Al',
    'Al/F',
    'Al/Mg',
    'Al/O',
    'Al/Si',
    'AllParticles',
    'Am/Zgeq70',
    'Ar',
    'Ar/Fe',
    'Ar/O',
    'Ar/Si',
    'As/Fe',
    'At/Zgeq70',
    'Au/Zgeq55',
    'Au/Zgeq70',
    'B',
    'B/C',
    'B/O',
    'B/Si',
    'Ba/Fe',
    'Ba/Te',
    'Ba/Zgeq55',
    'Be',
    'Be/B',
    'Be/C',
    'Be/O',
    'Be/Si',
    'Bi/Zgeq55',
    'Bi/Zgeq70',
    'Bk/Zgeq70',
    'Br/Fe',
    'C',
    'C-Fe-group',
    'C-bar/C',
    'C/O',
    'C/Si',
    'Ca',
    'Ca/Fe',
    'Ca/O',
    'Ca/Si',
    'Cd/Fe',
    'Ce/Fe',
    'Ce/Te',
    'Ce/Zgeq55',
    'Cl',
    'Cl/Ar',
    'Cl/Fe',
    'Cl/O',
    'Cl/Si',
    'Cm/Zgeq70',
    'Co',
    'Co/Fe',
    'Co/O',
    'Co/Si',
    'Cr',
    'Cr/Fe',
    'Cr/O',
    'Cr/Si',
    'Cs/Zgeq55',
    'Cu/Fe',
    'DipoleAmplitude',
    'DipolePhase',
    'Dy/Fe',
    'Dy/Zgeq55',
    'Er/Fe',
    'Er/Zgeq55',
    'Eu/Zgeq55',
    'F',
    'F/B',
    'F/Ne',
    'F/O',
    'F/Si',
    'Fe',
    'Fe-group/AllParticles',
    'Fe/He',
    'Fe/O',
    'Fe/Si',
    'Fe/Te',
    'Fr/Zgeq70',
    'Ga/Fe',
    'Gd/Fe',
    'Gd/Zgeq55',
    'Ge/Fe',
    'H',
    'H-He-group',
    'H/AllParticles',
    'H/He',
    'He',
    'He-bar/He',
    'He/AllParticles',
    'He/H',
    'He/O',
    'Hf/Fe',
    'Hf/Z_74-80',
    'Hf/Zgeq70',
    'Hg/Fe',
    'Hg/Z_74-80',
    'Hg/Zgeq55',
    'Hg/Zgeq70',
    'Ho/Zgeq55',
    'Ir/Z_74-80',
    'Ir/Zgeq55',
    'Ir/Zgeq70',
    'K',
    'K/Fe',
    'K/O',
    'K/Si',
    'Kr/Fe',
    'La/Zgeq55',
    'Li',
    'Li/B',
    'Li/Be',
    'Li/C',
    'Li/O',
    'Lu/Zgeq55',
    'Lu/Zgeq70',
    'Mg',
    'Mg/O',
    'Mg/Si',
    'Mn',
    'Mn/Fe',
    'Mn/O',
    'Mn/Si',
    'Mo/Fe',
    'N',
    'N-group/AllParticles',
    'N/B',
    'N/O',
    'N/Si',
    'Na',
    'Na/F',
    'Na/Mg',
    'Na/O',
    'Na/Si',
    'Nb/Fe',
    'Nd/Fe',
    'Nd/Zgeq55',
    'Ne',
    'Ne/Mg',
    'Ne/O',
    'Ne/Si',
    'Ni',
    'Ni/Fe',
    'Ni/O',
    'Ni/Si',
    'Np/Zgeq70',
    'O',
    'O-group/AllParticles',
    'O/Si',
    'Os/Fe',
    'Os/Z_74-80',
    'Os/Zgeq55',
    'Os/Zgeq70',
    'P',
    'P/Fe',
    'P/He',
    'P/O',
    'P/S',
    'P/Si',
    'Pa/Zgeq70',
    'Pb/Fe',
    'Pb/Z_74-80',
    'Pb/Zgeq55',
    'Pb/Zgeq70',
    'Pm/Zgeq55',
    'Po/Zgeq70',
    'Pr/Zgeq55',
    'Pt/Fe',
    'Pt/Z_74-80',
    'Pt/Zgeq55',
    'Pt/Zgeq70',
    'Pu/Zgeq70',
    'Ra/Zgeq55',
    'Ra/Zgeq70',
    'Rb/Fe',
    'Re/Zgeq70',
    'Rn/Zgeq70',
    'Ru/Fe',
    'S',
    'S/Fe',
    'S/O',
    'S/Si',
    'Sc',
    'Sc/Fe',
    'Sc/O',
    'Sc/Si',
    'Se/Fe',
    'Si',
    'Si/Fe',
    'Si/Mg',
    'Si/O',
    'Sm/Fe',
    'Sm/Zgeq55',
    'Sn/Fe',
    'Sn/Te',
    'Sr/Fe',
    'SubFe',
    'SubFe/Fe',
    'Ta/Zgeq55',
    'Ta/Zgeq70',
    'Tb/Zgeq55',
    'Te/Fe',
    'Th/Zgeq70',
    'Ti',
    'Ti/Fe',
    'Ti/O',
    'Ti/Si',
    'Ti/Zgeq55',
    'Ti/Zgeq70',
    'Tl/Zgeq70',
    'Tm/Zgeq55',
    'U/Zgeq70',
    'V',
    'V/Fe',
    'V/O',
    'V/Si',
    'W/Fe',
    'W/Z_74-80',
    'W/Zgeq55',
    'W/Zgeq70',
    'Xe/Fe',
    'Xe/Te',
    'Y/Fe',
    'Yb/Fe',
    'Yb/Zgeq55',
    'Yb/Zgeq70',
    'Z_33-34/Fe',
    'Z_35-36/Fe',
    'Z_37-38/Fe',
    'Z_39-40/Fe',
    'Z_41-42/Fe',
    'Z_43-44/Fe',
    'Z_45-46/Fe',
    'Z_47-48/Fe',
    'Z_49-50/Fe',
    'Z_51-52/Fe',
    'Z_53-54/Fe',
    'Z_55-56/Fe',
    'Z_57-58/Fe',
    'Z_59-60/Fe',
    'Z_62-69/Fe',
    'Z_62-69/Z_74-87',
    'Z_70-73/Fe',
    'Z_70-73/Z_74-87',
    'Z_74-80/Fe',
    'Z_74-87/Sn',
    'Z_74-87/Zgeq65',
    'Z_81-87/Fe',
    'Z_81-87/Z_74-80',
    'Zgeq110/Z_74-87',
    'Zgeq2-bar/Zgeq2',
    'Zgeq3-bar/Zgeq3',
    'Zgeq6-bar/Zgeq6',
    'Zgeq65',
    'Zgeq88/Fe',
    'Zgeq88/Z_74-80',
    'Zgeq88/Z_74-87',
    'Zgeq94/Z_74-87',
    'Zn/Fe',
    'Zr/Fe',
    'e+',
    'e+/e-',
    'e+/e-+e+',
    'e-',
    'e-+e+',
)

ELEMENTS = {k: i + 1 for (i, k) in enumerate(VALID_NAMES[:99])}

COMBINE = (
    "AESOP",
    "AMS01",
    "ATIC",
    "BESS",
    "BETS",
    "Balloon",
    "CAPRICE",
    "CREAM",
    "Fermi-LAT",
    "Gemini",
    "H.E.S.S.",
    "HEAO3",
    "HEAT",
    "IMAX",
    "IMP",
    "ISEE3",
    "IceCube",
    "KASCADE-Grande",
    "MASS",
    "NUCLEON",
    "OGO",
    "PAMELA",
    "PierreAugerObservatory",
    "Pioneer",
    "SMILI",
    "TRACER",
    "TUNKA",
    "TelescopeArray",
    "Tibet",
    "Trek",
    "UHECR-LDEF",
    "Ulysses",
    "Voyager",
)

_CSV_FIELDS = (
    ("quantity", "U32"),  # DATA-QTY
    ("sub_exp", "U100"),  # SUBEXP-NAME
    ("e_type", "U4"),  # DATA-EAXIS
    ("e", "f8"),  # DATA-E_MEAN
    ("e_bin", "f8", (2,)),  # EBIN_LOW, EBIN_HIGH
    ("value", "f8"),  # QUANTITY VALUE
    ("err_sta", "f8", (2,)),  # ERR_STAT-,  ERR_STAT+
    ("err_sys", "f8", (2,)),  # ERR_SYST-, ERR_SYST+
    ("ads", "U32"),  # ADS URL FOR PAPER REF
    ("phi", "f8"),  # phi [MV]
    ("distance", "f8"),  # DISTANCE [AU]
    ("datetime", "U256"),  # DATIMES
    ("is_upper_limit", "?"),  # IS UPPER LIMIT
)

# fields set to None here are skipped during parsing
_CSV_ASIMPORT_FIELDS = (
    ("exp", "U64"),  # EXP-NAME
    ("exp_type", "U16"),  # EXP-TYPE
    None,  # EXP-HTML
    None,  # EXP-STARTYEAR
    ("sub_exp", "U100"),  # SUBEXP-NAME
    None,  # SUBEXP-DESCRIPTION
    ("e_relerr", "f8"),  # SUBEXP-ESCALE_RELERR
    None,  # SUBEXP-INFO
    ("distance", "f8"),  # SUBEXP-DISTANCE
    ("datetime", "U256"),  # SUBEXP-DATES
    ("ads", "U32"),  # PUBLI-HTML
    None,  # PUBLI-DATAORIGIN
    ("quantity", "U32"),  # DATA-QTY
    ("e_type", "U4"),  # DATA-EAXIS
    ("e", "f8"),  # DATA-E_MEAN
    ("e_bin", "f8", (2,)),  # DATA-E_BIN_L, DATA-E_BIN_U
    ("value", "f8"),  # DATA-VAL
    ("err_sta", "f8", (2,)),  # DATA-VAL_ERRSTAT_L, DATA-VAL_ERRSTAT_U
    ("err_sys", "f8", (2,)),  # DATA-VAL_ERRSYST_L, DATA-VAL_ERRSYST_U
    ("is_upper_limit", "?"),  # DATA-ISUPPERLIM
    ("phi", "f8"),  # phi [MV]
)


def query(
    quantity: Union[str, Sequence[str]],
    *,
    energy_type: str = "R",
    combo_level: int = 1,
    energy_convert_level: int = 1,
    flux_rescaling: float = 0.0,
    exp_dates: str = "",
    energy_start: float = 0.0,
    energy_stop: float = 0.0,
    time_start: str = "",
    time_stop: str = "",
    time_series: str = "",
    modulation: str = "",
    timeout: int = 120,
    server_url: str = "http://lpsc.in2p3.fr/crdb",
) -> np.recarray:
    """
    Query CRDB and return table as a numpy array.

    See http://lpsc.in2p3.fr/crdb for documentation which parameters are accepted.

    Parameters
    ----------
    quantity: str or sequence of str
        Element, isotope, particle, or mass group, or ratio of those, e.g. 'H', 'B/C'.
        For valid names, see the constant crdb.VALID_NAMES. Multiple quantities can be
        bundled in a sequence for convenience, but this is not more efficient than
        running multiple queries by hand.
    energy_type: str, optional
        Energy unit for the requested quantity. Default is R.
        Valid values: EKN, EK, R, ETOT, ETOTN.
    combo_level: int, optional
        One of 0, 1, 2. Default is 1. Add combinations (ratio, products) of native data
        (from the same sub-exp at the same energy) that match quantities in list (e.g.
        compute B/C from native B and C). Three levels of combos are enabled: 0 (native
        data only, no combo), 1 (exact combos), or 2 (exact and approximate combos): in
        level 1, the mean energy (or energy bin) of the two quantities must be within
        5%, whereas for level 2, it must be within 20%.
    energy_convert_level: int, optional
        One of 0, 1, 2. Default is 1. Add data obtained from an exact or approximate
        energy_type conversion (from native to queried). Three levels of conversion are
        enabled: 0 (native data only, no conversion), 1 (exact conversion only, which
        applies to isotopic and leptonic fluxes), and 2 (exact and approximate
        conversions, the later applying to flux of elements and of groups of elements).
    flux_rescaling: float, optional
        Flux is multiplied by E^flux_rescaling.
    exp_dates: str, optional
        Comma-separated list (optional time intervals) of sub-experiment names.
    energy_start: float, optional
        Lower limit for energy_type.
    energy_stop: float, optional
        Upper limit for energy_type.
    time_start: str, optional
        Lower limit for interval selection. Format: YYYY[/MM] (2014, 2010/06).
    time_stop: str, optional
        Upper limit for interval selection. Format: YYYY[/MM] (2020, 2019/06).
    time_series: str, optional
        Whether to discard, select only, or keep time series data in query CRDB keywords
        ('no', 'only', 'all'). Default is 'no'.
    modulation: str, optional
        Source of Solar modulation values; one of 'USO05', 'USO17', 'GHE17'. Default is
        'GHE17'.
    timeout: int, optional
        Timeout for server response in seconds. Default is 60.
    server_url: str, optional
        URL to send the request to. Default is http://lpsc.in2p3.fr/crdb). This is an
        expert option, users do not need to change this.

    Returns
    -------
    numpy record array with the database content

    Energies are in GeV or GV. Solar modulation values are in MV. Distances are in
    AU. Fluxes are in sr s m2 energy_unit.

    Raises
    ------
    ValueError
        An invalid parameter value triggers a ValueError.

    TimeoutError
        If the server does not respond within the timeout time.

    Notes
    -----
    This function caches identical queries for 30 days. If you need to reset the cache,
    do::

        from crdb import clear_cache

        clear_cache()
    """
    if not isinstance(quantity, str):
        results = [
            query(
                quantity=q,
                energy_type=energy_type,
                combo_level=combo_level,
                energy_convert_level=energy_convert_level,
                flux_rescaling=flux_rescaling,
                exp_dates=exp_dates,
                energy_start=energy_start,
                energy_stop=energy_stop,
                time_start=time_start,
                time_stop=time_stop,
                time_series=time_series,
                modulation=modulation,
                server_url=server_url,
                timeout=timeout,
            )
            for q in quantity
        ]
        return np.concatenate(results).view(np.recarray)  # type:ignore

    url = _url(
        quantity=quantity,
        energy_type=energy_type,
        combo_level=combo_level,
        energy_convert_level=energy_convert_level,
        flux_rescaling=flux_rescaling,
        exp_dates=exp_dates,
        energy_start=energy_start,
        energy_stop=energy_stop,
        time_start=time_start,
        time_stop=time_stop,
        time_series=time_series,
        format="csv-asimport",
        modulation=modulation,
        server_url=server_url,
    )

    data = _server_request(url, timeout)

    # check for errors and display them
    if len(data) == 1:
        raise ValueError(data[0])

    table = _convert_csv(data, _CSV_ASIMPORT_FIELDS)

    return table


def _url(
    quantity: str,
    energy_type: str = "R",
    combo_level: int = 1,
    energy_convert_level: int = 1,
    flux_rescaling: float = 0.0,
    exp_dates: str = "",
    energy_start: float = 0.0,
    energy_stop: float = 0.0,
    time_start: str = "",
    time_stop: str = "",
    time_series: str = "",
    format: str = "",
    modulation: str = "",
    server_url: str = "http://lpsc.in2p3.fr/crdb",
) -> str:
    """Build a query URL for the CRDB server."""
    num, *rest = quantity.split("/")
    if len(rest) > 1:
        raise ValueError("ratio contains more than one / operator")

    num = num.strip()
    den = rest[0].strip() if rest else ""

    if num not in VALID_NAMES or (den and den not in VALID_NAMES):
        raise ValueError(f"quantity {quantity} is not valid, see crdb.VALID_NAMES")

    # "+" must be escaped in URL, see
    # https://en.wikipedia.org/wiki/Percent-encoding
    num = num.replace("+", "%2B")
    den = den.replace("+", "%2B")

    # workaround for empty error message from CRDB
    valid_energy_types = ("EKN", "EK", "R", "ETOT", "ETOTN")
    if energy_type.upper() not in valid_energy_types:
        raise ValueError("energy_type must be one of " + ",".join(valid_energy_types))

    if combo_level not in (0, 1, 2):
        raise ValueError(f"invalid combo_level {combo_level}")

    if energy_convert_level not in (0, 1, 2):
        raise ValueError(f"invalid energy_convert_level {energy_convert_level}")

    if flux_rescaling < 0 or flux_rescaling > 2.5:
        raise ValueError(f"invalid flux_rescaling {flux_rescaling}")

    if time_series and time_series not in ("no", "only", "all"):
        raise ValueError(f"invalid time_series {time_series}")

    if format and format not in ("usine", "galprop", "csv", "csv-asimport"):
        raise ValueError(f"invalid format {format}")

    if modulation and modulation not in ("USO05", "USO17", "GHE17"):
        raise ValueError(f"invalid modulation {modulation}")

    # do the query
    kwargs: Dict[str, Union[str, float, int]] = {
        "num": num,
        "energy_type": energy_type.upper(),
    }
    if den:
        kwargs["den"] = den
    if combo_level != 1:
        kwargs["combo_level"] = combo_level
    if energy_convert_level != 1:
        kwargs["energy_convert_level"] = energy_convert_level
    if flux_rescaling:
        kwargs["flux_rescaling"] = flux_rescaling
    if exp_dates:
        kwargs["exp_dates"] = exp_dates
    if energy_start:
        kwargs["energy_start"] = energy_start
    if energy_stop:
        kwargs["energy_stop"] = energy_stop
    if time_start:
        kwargs["time_start"] = time_start
    if time_stop:
        kwargs["time_stop"] = time_stop
    if time_series:
        kwargs["time_series"] = time_series
    if format:
        kwargs["format"] = format
    if modulation:
        kwargs["modulation"] = modulation

    return f"{server_url}/rest.php?" + "&".join(
        ["{0}={1}".format(k, v) for (k, v) in kwargs.items()]
    )


@cachier.cachier(stale_after=timedelta(days=30))
def _server_request(url: str, timeout: int) -> List[str]:
    # if there is a timeout error, we hide original long traceback from the internal
    # libs and instead show a simple traceback
    try:
        context = ssl._create_unverified_context()
        with rq.urlopen(url, timeout=timeout, context=context) as u:
            data: List[str] = u.read().decode("utf-8").split("\n")
        timeout_error = False
    except TimeoutError:
        timeout_error = True

    if timeout_error:
        raise TimeoutError(
            f"server did not respond within timeout={timeout} to url={url}"
        )

    if not data:
        raise ValueError("empty server response")

    return data


def _convert_csv(
    data: List[str],
    fields: Sequence[Union[None, Tuple[str, str], Tuple[str, str, Tuple[int]]]],
) -> np.recarray:
    # convert text to numpy record array
    mapping: List[Union[None, str, Tuple[str, int]]] = []
    for f in fields:
        if f is None:
            mapping.append(None)
        elif len(f) == 3:
            (n,) = f[2]  # type:ignore
            for k in range(n):
                mapping.append((f[0], k))
        else:
            mapping.append(f[0])
    fields = [x for x in fields if x is not None]

    for start, line in enumerate(data):
        if not line.startswith("#"):
            break

    table = np.recarray(len(data) - start - 1, fields)
    for idx, row in enumerate(csv.reader(data[start:-1])):
        val: Union[str, int]
        for val, key in zip(row, mapping):
            if key is None:
                continue
            if isinstance(key, tuple):
                key, pos = key
                table[idx][key][pos] = val
            else:
                if key == "is_upper_limit":
                    val = int(val)
                table[idx][key] = val

    # workaround: replace &amp; in sub_exp strings
    sub_exps = np.unique(table["sub_exp"])
    code = "&amp;"
    for sub_exp in sub_exps:
        if code not in sub_exp:
            continue
        mask = table["sub_exp"] == sub_exp
        table["sub_exp"][mask] = sub_exp.replace(code, "&")

    # workaround: err_stat_minus or err_sys_minus may be negative
    for x in ("sta", "sys"):
        field = f"err_{x}"
        table[field] = np.abs(table[field])

    return table


def get_mean_datetime(timerange: str) -> Tuple[datetime, timedelta]:
    """
    Return the average time for a given time range.

    Parameters
    ----------
    timerange : string
        CRDB time range in "YYYY/MM/DD-HHMMSS:YYYY/MM/DD-HHMMSS" format.

    Returns
    -------
    Datetime
        Center of the time range.

    Raises
    ------
    ValueError
        Raised if the argument contains multiple time ranges.
    """
    if ";" in timerange:
        raise ValueError("argument contains multiple time ranges")

    s1, s2 = timerange.split(":")
    dt1 = datetime.strptime(s1, "%Y/%m/%d-%H%M%S")
    dt2 = datetime.strptime(s2, "%Y/%m/%d-%H%M%S")
    return dt1 + (dt2 - dt1) / 2, (dt2 - dt1) / 2


def experiment_masks(
    table: np.recarray, combine: Sequence[str] = COMBINE
) -> Dict[str, NDArray]:
    """
    Generate masks which select all points from each experiment.

    Different data taking campains are joined. Optionally, one can also
    join different experiments with the same name, e.g. AEASOP00, AESOP02, ...

    Parameters
    ----------
    table : array
        CRDB database table.
    combine : sequence of str, optional
        Further combine all experiments which these common prefixes.
        The default is to combine all experiments listed in crdb.COMBINE.

    Returns
    -------
    Dict[str, NDArray]
        Dictionary which maps the experiment name to its table mask.
    """
    d = {}
    for key in np.unique(table.sub_exp):
        for c in combine:
            if key.startswith(c):
                d[key] = c
                break
        else:
            c = key[: key.index("(")]
            d[key] = c

    result = {}
    for i, t in enumerate(table):
        c = d[t.sub_exp]
        if c not in result:
            result[c] = np.zeros(len(table), dtype=bool)
        result[c][i] = True
    return result


def clear_cache() -> None:
    """Delete the local CRDB cache."""
    _server_request.clear_cache()
    _all_request.clear_cache()
    all.clear_cache()


def reference_urls(table: np.recarray) -> List[str]:
    """Return list of URLs to entries in the ADSABS database for datasets in table."""
    result = []
    for key in sorted(np.unique(table.ads)):
        result.append(f"https://ui.adsabs.harvard.edu/abs/{key}")
    return result


def bibliography(table: np.recarray) -> Dict[str, str]:
    """
    Return dictionary that maps ADSABS keys in table to BibTex entries.

    This requires the external library `autobib`.
    """
    try:
        from autobib.util import get_entry_online
    except ModuleNotFoundError as e:
        e.msg += ". Install autobib (`pip install autobib`) to use this function."
        raise

    result = {}
    for adskey in sorted(np.unique(table.ads)):
        k, *r = get_entry_online(adskey)
        result[k] = "".join(r)

    return result


@cachier.cachier(stale_after=timedelta(days=30))
def _all_request() -> List[str]:
    # url = "https://lpsc.in2p3.fr/crdb/_export_all_data.php?format=csv-asimport"
    url = "https://lpsc.in2p3.fr/crdb/_export_all_data.php?format=csv"

    try:
        context = ssl._create_unverified_context()
        response = rq.urlopen(url, context=context)
        connection_error = False
    except Exception:
        import traceback

        traceback.print_exc()
        connection_error = True

    if connection_error:
        raise ConnectionError(
            "Please check if you can connect to https://lpsc.in2p3.fr/crdb with your "
            f"browser. If that works, something is wrong with url = '{url}', "
            "please report this as an issue at "
            "https://github.com/crdb-project/crdb/issues"
        )

    blocksize = 1024**2
    nbytes = 0
    with tempfile.TemporaryFile(mode="w+") as f:
        while True:
            chunk = response.read(blocksize)
            nbytes += len(chunk)
            print(f"\r{nbytes / blocksize:.0f} Mb downloaded", end="", flush=True)
            if not chunk:
                break
            f.write(chunk.decode())
        print()
        f.flush()
        f.seek(0)
        data = f.readlines()

    if not data:
        raise ValueError("empty server response")

    return data


@cachier.cachier(stale_after=timedelta(days=30))
def all() -> NDArray:
    """Return the full raw CRDB database as a table."""
    data = _all_request()
    return _convert_csv(data, _CSV_FIELDS)


def solar_system_composition() -> Dict[str, List[Tuple[int, float]]]:
    """
    Return a dict with the isotope composition in the solar system.

    Data are taken from:
    Lodders, ApJ 591, 1220 (2003)
    http://adsabs.harvard.edu/abs/2003ApJ...591.1220L

    Returns
    -------
    Dictionary that maps element names to lists of isotope abundances. Isotopes are
    described by the tuple (A, F), where A is the number of nucleons, and F is the
    abundance in arbitrary units.
    """
    result: Dict[str, List[Tuple[int, float]]] = {}
    with open(Path(__file__).parent / "solarsystem_abundances2003.dat") as f:
        for line in f:
            m = re.match(r"^ *([0-9]+)([A-Za-z]+)\s*[0-9\.]+\s*([0-9\.e]+)", line)
            if not m:
                continue
            a = int(m.group(1))
            elem = m.group(2)
            abundance = float(m.group(3))
            result.setdefault(elem, []).append((a, abundance))
    return result
