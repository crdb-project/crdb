from __future__ import annotations

import datetime
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

# from "Submit data" tab on CRDB website
VALID_NAMES = (
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Zgeq1",
    "Zgeq2",
    "Zgeq3",
    "Zgeq4",
    "Zgeq5",
    "Zgeq6",
    "Zgeq7",
    "Zgeq8",
    "H-bar",
    "He-bar",
    "Li-bar",
    "Be-bar",
    "B-bar",
    "C-bar",
    "N-bar",
    "O-bar",
    "Zgeq1-bar",
    "Zgeq2-bar",
    "Zgeq3-bar",
    "Zgeq4-bar",
    "Zgeq5-bar",
    "Zgeq6-bar",
    "Zgeq7-bar",
    "Zgeq8-bar",
    "1H-bar",
    "2H-bar",
    "3He-bar",
    "4He-bar",
    "6Li-bar",
    "9Be-bar",
    "11B-bar",
    "12C-bar",
    "14N-bar",
    "16O-bar",
    "e-",
    "e+",
    "NU_E",
    "NU_M",
    "NU_T",
    "GAMMA",
    "e-+e+",
    "SubFe",
    "1H",
    "2H",
    "3He",
    "4He",
    "6Li",
    "7Li",
    "7Be",
    "9Be",
    "10B",
    "10Be",
    "11B",
    "12C",
    "13C",
    "14N",
    "14C",
    "15N",
    "16O",
    "17O",
    "18O",
    "19F",
    "20Ne",
    "21Ne",
    "22Ne",
    "23Na",
    "24Mg",
    "25Mg",
    "26Mg",
    "26Al",
    "27Al",
    "28Si",
    "29Si",
    "30Si",
    "31P",
    "32S",
    "33S",
    "34S",
    "35Cl",
    "36S",
    "36Ar",
    "36Cl",
    "37Cl",
    "37Ar",
    "38Ar",
    "39K",
    "40Ar",
    "40Ca",
    "40K",
    "41K",
    "41Ca",
    "42Ca",
    "43Ca",
    "44Ca",
    "44Ti",
    "45Sc",
    "46Ti",
    "46Ca",
    "47Ti",
    "48Ti",
    "48Ca",
    "48Cr",
    "49Ti",
    "49V",
    "50Ti",
    "50Cr",
    "50V",
    "51V",
    "51Cr",
    "52Cr",
    "53Cr",
    "53Mn",
    "54Cr",
    "54Fe",
    "54Mn",
    "55Mn",
    "55Fe",
    "56Fe",
    "56Ni",
    "57Fe",
    "57Co",
    "58Fe",
    "58Ni",
    "59Co",
    "59Ni",
    "60Ni",
    "60Fe",
    "61Ni",
    "62Ni",
    "63Cu",
    "64Ni",
    "64Zn",
    "65Cu",
    "66Zn",
    "67Zn",
    "68Zn",
    "70Zn",
    "H-He-group",
    "N-group",
    "O-group",
    "Al-group",
    "Si-group",
    "Fe-group",
    "O-Fe-group",
    "C-Fe-group",
    "AllParticles",
    "<LnA>",
    "<X_max>",
    "X_mu_max",
    "<rho_mu_600>",
    "<rho_mu_800>",
    "<R_mu>",
    "LS-group",
    "HS-group",
    "Pt-group",
    "Pb-group",
    "Subactinides",
    "Actinides",
    "Z_33-34",
    "Z_35-36",
    "Z_37-38",
    "Z_39-40",
    "Z_41-42",
    "Z_43-44",
    "Z_45-46",
    "Z_47-48",
    "Z_49-50",
    "Z_51-52",
    "Z_53-54",
    "Z_55-56",
    "Z_57-58",
    "Z_59-60",
    "Zgeq70",
    "9Be+10Be",
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
):
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
        level 1, the mean energy (or energy bin) of the two quantities must be within 5%,
        whereas for level 2, it must be within 20%.
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
        return np.concatenate(results).view(np.recarray)

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
        format="csv",
        modulation=modulation,
        server_url=server_url,
    )

    data = _server_request(url, timeout)

    # check for errors and display them
    if len(data) == 1:
        raise ValueError(data[0])

    table = _convert(data)

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
):
    """
    Build a query URL for the CRDB server.
    """

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
    kwargs = {
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


@cachier.cachier(stale_after=datetime.timedelta(days=30))
def _server_request(url: str, timeout: int) -> List[str]:
    # if there is a timeout error, we hide original long traceback from the internal
    # libs and instead show a simple traceback
    try:
        context = ssl._create_unverified_context()
        with rq.urlopen(url, timeout=timeout, context=context) as u:
            data = u.read().decode("utf-8").split("\n")
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


def _convert(data: List[str]) -> NDArray:
    # convert text to numpy record array

    # Use this for csv-asimport or csv-extended when it becomes available
    # fields set to None here are skipped during parsing
    # fields = [
    #     ("exp", "U64"),  # EXP-NAME
    #     ("exp_type", "U16"),  # EXP-TYPE
    #     None,  # EXP-HTML
    #     None,  # EXP-STARTYEAR
    #     ("sub_exp", "U100"),  # SUBEXP-NAME
    #     None,  # SUBEXP-DESCRIPTION
    #     ("e_relerr", "f8"),  # SUBEXP-ESCALE_RELERR
    #     None,  # SUBEXP-INFO
    #     ("distance", "f8"),  # SUBEXP-DISTANCE
    #     ("datetime", "U64"),  # SUBEXP-DATES
    #     ("ads", "U32"),  # PUBLI-HTML
    #     None,  # PUBLI-DATAORIGIN
    #     ("quantity", "U32"),  # DATA-QTY
    #     ("e_axis", "U4"),  # DATA-EAXIS
    #     ("e_mean", "f8"),  # DATA-E_MEAN
    #     ("e_low", "f8"),  #  DATA-E_BIN_L
    #     ("e_high", "f8"),  # DATA-E_BIN_U
    #     ("value", "f8"),  # DATA-VAL
    #     ("err_stat_minus", "f8"),  # DATA-VAL_ERRSTAT_L
    #     ("err_stat_plus", "f8"),  # DATA-VAL_ERRSTAT_U
    #     ("err_sys_minus", "f8"),  # DATA-VAL_ERRSYST_L
    #     ("err_sys_plus", "f8"),  # DATA-VAL_ERRSYST_U
    #     ("is_upper_limit", "?"),  # DATA-ISUPPERLIM
    #     # ("phi", "f8"),
    # ]

    fields = [
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
    ]

    mapping = []
    for f in fields:
        if f is None:
            mapping.append(None)
        if len(f) == 3:
            for k in range(f[2][0]):
                mapping.append((f[0], k))
        else:
            mapping.append(f[0])
    fields = [x for x in fields if x is not None]

    # workaround for invalid CSV format,
    # to be replaced by standard parser
    data2 = []
    for iline, line in enumerate(data):
        try:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            items = []
            inquote = False
            start = 0
            for i, c in enumerate(line):
                if c == '"':
                    if inquote:
                        items.append(line[start + 1 : i])
                    else:
                        start = i
                    inquote = not inquote
            data2.append(items)
        except ValueError as e:
            msg = f"{e.args[0]}\nCould not parse line {iline} {line}"
            e.args = (msg,)
            raise

    table = np.recarray(len(data2), fields)
    for idx, row in enumerate(data2):
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


def experiment_masks(
    table: NDArray, combine: Sequence[str] = COMBINE
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
    """
    Delete the local CRDB cache.
    """
    _server_request.clear_cache()


def reference_urls(table: NDArray) -> List[str]:
    """
    Return list of URLs to entries in the ADSABS database for datasets in table.
    """
    result = []
    for key in sorted(np.unique(table.ads)):
        result.append(f"https://ui.adsabs.harvard.edu/abs/{key}")
    return result


def bibliography(table: NDArray) -> Dict[str, str]:
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


@cachier.cachier(stale_after=datetime.timedelta(days=30))
def all() -> NDArray:
    """
    Return the full raw CRDB database as a table.
    """
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

    return _convert(data)


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
    result = {}
    with open(Path(__file__).parent / "solarsystem_abundances2003.dat") as f:
        for line in f:
            m = re.match(r"^ *([0-9]+)([A-Za-z]+)\s*[0-9\.]+\s*([0-9\.e]+)", line)
            if not m:
                continue
            a = int(m.group(1))
            elem = m.group(2)
            f = float(m.group(3))
            result.setdefault(elem, []).append((a, f))
    return result
