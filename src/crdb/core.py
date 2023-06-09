"""Core library functions."""
from __future__ import annotations

import csv
from datetime import datetime, timedelta
import re
import ssl
import urllib.request as rq
from pathlib import Path
from typing import Dict
from typing import List
from typing import Sequence
from typing import Tuple
from typing import Union
from typing import Set

import cachier
import numpy as np
from numpy.typing import NDArray

ELEMENTS = {
    'H': 1,
    'He': 2,
    'Li': 3,
    'Be': 4,
    'B': 5,
    'C': 6,
    'N': 7,
    'O': 8,
    'F': 9,
    'Ne': 10,
    'Na': 11,
    'Mg': 12,
    'Al': 13,
    'Si': 14,
    'P': 15,
    'S': 16,
    'Cl': 17,
    'Ar': 18,
    'K': 19,
    'Ca': 20,
    'Sc': 21,
    'Ti': 22,
    'V': 23,
    'Cr': 24,
    'Mn': 25,
    'Fe': 26,
    'Co': 27,
    'Ni': 28,
    'Cu': 29,
    'Zn': 30,
    'Ga': 31,
    'Ge': 32,
    'As': 33,
    'Se': 34,
    'Br': 35,
    'Kr': 36,
    'Rb': 37,
    'Sr': 38,
    'Y': 39,
    'Zr': 40,
    'Nb': 41,
    'Mo': 42,
    'Tc': 43,
    'Ru': 44,
    'Rh': 45,
    'Pd': 46,
    'Ag': 47,
    'Cd': 48,
    'In': 49,
    'Sn': 50,
    'Sb': 51,
    'Te': 52,
    'I': 53,
    'Xe': 54,
    'Cs': 55,
    'Ba': 56,
    'La': 57,
    'Ce': 58,
    'Pr': 59,
    'Nd': 60,
    'Pm': 61,
    'Sm': 62,
    'Eu': 63,
    'Gd': 64,
    'Tb': 65,
    'Dy': 66,
    'Ho': 67,
    'Er': 68,
    'Tm': 69,
    'Yb': 70,
    'Lu': 71,
    'Hf': 72,
    'Ta': 73,
    'W': 74,
    'Re': 75,
    'Os': 76,
    'Ir': 77,
    'Pt': 78,
    'Au': 79,
    'Hg': 80,
    'Tl': 81,
    'Pb': 82,
    'Bi': 83,
    'Po': 84,
    'At': 85,
    'Rn': 86,
    'Fr': 87,
    'Ra': 88,
    'Ac': 89,
    'Th': 90,
    'Pa': 91,
    'U': 92,
    'Np': 93,
    'Pu': 94,
    'Am': 95,
    'Cm': 96,
    'Bk': 97,
    'Cf': 98,
    'Es': 99,
}

COMBINE = (
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


@cachier.cachier(stale_after=timedelta(days=30))
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
        For valid names, see the crdb.valid_quantities(). Multiple quantities can be
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
        Timeout for server response in seconds. Default is 120.
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

    ConnectionError
        If no connection to the server can be established.

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

    url = f"{server_url}/rest.php?" + "&".join(
        ["{0}={1}".format(k, v) for (k, v) in kwargs.items()]
    )
    return url


@cachier.cachier(stale_after=timedelta(days=30))
def _server_request(url: str, timeout: int) -> List[str]:
    # if there is a timeout error, we hide original long traceback from the internal
    # libs and instead show a simple traceback
    try:
        context = ssl._create_unverified_context()
        response = rq.urlopen(url, context=context, timeout=timeout)
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

    blocksize = 256**2
    Mb = 1024**2
    nbytes = 0
    chunks = []
    while True:
        timeout_error = False
        try:
            chunk = response.read(blocksize)
        except TimeoutError:
            timeout_error = True
        if timeout_error:
            raise TimeoutError(
                f"server did not respond within timeout={timeout} to url={url}"
            )
        nbytes += len(chunk)
        if not chunk:
            break
        chunks.append(chunk)
        if chunks:  # show progress if there is more than one chunk
            print(f"\r{nbytes / Mb:.2f} Mb downloaded", end="", flush=True)
    if len(chunks) > 1:
        print()

    if len(chunks) == 1 and (not chunks[0] or chunks[0].isspace()):
        raise ValueError("empty server response")

    s = b"".join(chunks).decode("utf-8")
    return s.split("\n")


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
            d[key] = c.strip()

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
    all.clear_cache()
    query.clear_cache()


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
def all(timeout: int = 120) -> NDArray:
    """Return the full raw CRDB database as a table.

    Parameters
    ----------
    timeout: int, optional
        Timeout for server response in seconds. Default is 120.

    Returns
    -------
    numpy record array with the database content

    Energies are in GeV or GV. Solar modulation values are in MV. Distances are in
    AU. Fluxes are in sr s m2 energy_unit.

    Raises
    ------
    ConnectionError
        If no connection to the server can be established.

    TimeoutError
        If the server does not respond within the timeout time.

    Notes
    -----
    This function caches identical queries for 30 days. If you need to reset the cache,
    do::

        from crdb import clear_cache

        clear_cache()
    """
    url = "https://lpsc.in2p3.fr/crdb/_export_all_data.php?format=csv-asimport"
    data = _server_request(url, timeout)
    return _convert_csv(data, _CSV_ASIMPORT_FIELDS)


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


def valid_quantities() -> Set[str]:
    """
    Return array with valid quantities that can be queried with crdb.query().

    Also ratios of these quantities can be queried. Calling this may be slow,
    since it downloads the full CRDB database to find all quantities.
    """
    tab = all()
    valid = set()
    for q in np.unique(tab.quantity):
        num, *rest = q.split("/")
        valid.add(num)
        if rest:
            valid.add(rest[0])
    return valid
