"""Helper functions to draw plots from tables with matplotlib."""

import warnings
from pathlib import Path
import numpy as np
from typing import Any, Optional
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from crdb._lib import get_mean_datetime


def draw_table(
    table: np.recarray,
    factor: float = 1.0,
    label: Optional[str] = None,
    sys_lw: float = 5,
    **kwargs: Any,
) -> Line2D:
    """
    Draw table with statistical and systematic error bars.

    Parameters
    ----------
    table : array
        CRDB table.
    factor : array-like, optional
        Optional scaling factor for the y-coordinates. Default is 1.
    label : str, optional
        Optional label for the plot.
    sys_lw : float, optional
        Line width for the error bar that represents systematic uncertainties.
    """
    x = table.e
    y = table.value * factor
    ye1 = np.transpose(table.err_sta) * factor
    ye2 = np.transpose(table.err_sys) * factor
    lines = plt.errorbar(x, y, ye1, ls="none", label=label, **kwargs)[0]
    for key in ("color", "alpha", "lw", "marker"):
        if key in kwargs:
            del kwargs[key]
    plt.errorbar(
        x,
        y,
        ye2,
        marker="none",
        ls="none",
        lw=sys_lw,
        color=lines.get_color(),
        alpha=0.5,
        **kwargs,
    )
    return lines


def draw_timeseries(
    table: np.recarray,
    factor: float = 1.0,
    label: Optional[str] = None,
    sys_lw: float = 5,
    **kwargs: Any,
) -> Line2D:
    """
    Draw table as a time series with statistical and systematic error bars.

    Parameters
    ----------
    table : array
        CRDB table.
    factor : array-like, optional
        Optional scaling factor for the y-coordinates. Default is 1.
    label : str, optional
        Optional label for the plot.
    sys_lw : float, optional
        Line width for the error bar that represents systematic uncertainties.
    """
    mask = []
    x = []
    xrange = []
    for dt in table.datetime:
        if ";" in dt:
            mask.append(False)
        else:
            mask.append(True)
            x1, x2 = get_mean_datetime(dt)
            x.append(x1)
            xrange.append(x2)
    mask = np.array(mask)
    n_invalid = np.sum(~mask)
    if n_invalid:
        msg = (
            f"input contains {n_invalid} points with multiple time ranges, "
            "which are ignored"
        )
        warnings.warn(msg, RuntimeWarning)
        table = table[mask]
    y = table.value * factor
    ye1 = np.transpose(table.err_sta) * factor
    ye2 = np.transpose(table.err_sys) * factor
    lines = plt.errorbar(x, y, ye1, xerr=xrange, ls="none", label=label, **kwargs)[0]
    for key in ("color", "alpha", "lw", "marker"):
        if key in kwargs:
            del kwargs[key]
    plt.errorbar(
        x,
        y,
        ye2,
        marker="none",
        ls="none",
        lw=sys_lw,
        color=lines.get_color(),
        alpha=0.5,
        **kwargs,
    )
    return lines


def draw_references(
    table: np.recarray,
    color: str = "0.5",
    fontsize: str = "xx-small",
    **kwargs: Any,
) -> None:
    """
    List references for table in columns using a modified Legend artist.

    The references are drawn using a legend artist, but the normal legend is
    not overridden.

    Parameters
    ----------
    table : array
        CRDB table.
    color : str, optional
        Color of the text, default is '0.5'.
    kwargs :
        Other keyword arguments are forwarded to matplotlib.legend.Legend.
    """
    import matplotlib.legend as mlegend
    from matplotlib.patches import Patch

    refs = np.sort(np.unique(table.ads))

    ax = plt.gca()
    leg = mlegend.Legend(
        ax,
        handles=[Patch(color="none") for ref in refs],
        labels=refs,
        frameon=False,
        handlelength=0,
        handletextpad=0,
        labelcolor=color,
        fontsize=fontsize,
        shadow=False,
        title_fontproperties={"size": fontsize},
        **kwargs,
    )
    leg.get_title().set_color(color)
    plt.gcf().add_artist(leg)


def draw_logo(
    x: float, y: float, height: float = 0.1, zorder: Optional[int] = None
) -> None:
    """
    Draw the CRDB logo.

    Parameters
    ----------
    x : float
        Left edge of image box in axes coordinates.
    y : float
        Upper edge of image box in axes coordinates.
    height : float, optional
        Height of image box in axes coordinates.
    zorder : int, optional
        Plotting order for the image.
    """
    from PIL import Image

    img = np.asarray(Image.open(Path(__file__).parent / "crdb_logo.png"))
    borderaxespad = 0.01
    iax = plt.gca().inset_axes(
        (x + borderaxespad, y - height, 2 * height, height), zorder=zorder
    )
    iax.set(xticks=[], yticks=[])
    iax.spines[:].set_visible(False)
    iax.imshow(img)
