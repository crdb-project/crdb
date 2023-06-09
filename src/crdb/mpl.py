"""Helper functions to draw plots from tables with matplotlib."""

import warnings
from pathlib import Path
import numpy as np
from typing import Any, Optional, Union
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from crdb.core import get_mean_datetime
from datetime import datetime


def draw_table(
    table: np.recarray,
    factor: float = 1.0,
    label: Optional[str] = None,
    show_bin: bool = False,
    xunit: float = 1.0,
    sys_lw: float = 5,
    **kwargs: Any,
) -> Line2D:
    """
    Draw table with statistical and systematic error bars.

    Supports drawing values and upper limits.

    Parameters
    ----------
    table : array
        CRDB table.
    factor : array-like, optional
        Optional scaling factor for the y-coordinates. Default is 1.
    label : str, optional
        Optional label for the plot.
    show_bin : bool, optional
        If true, show horizontal error bars to indicate the energy bin.
    xunit: float, optional
        Use this to change the default scale of the energy axis (GeV or GV). For
        example, setting xunit = 1e3 produces a plot in TeV or TV. Default is 1.
    sys_lw : float, optional
        Line width for the error bar that represents systematic uncertainties.
    kwargs :
        Other keyword arguments are forwarded to matplotlib.pyplot.errorbar.
    """
    e_types = np.unique(table.e_type)
    if len(e_types) > 1:
        et = set(e_types)
        is_warning = et == {"EK", "ETOT"}
        word = "potentially " if is_warning else ""
        msg = f"table contains {word}incompatbile e_types {et}"
        if is_warning:
            warnings.warn(msg, RuntimeWarning)
        else:
            raise ValueError(msg)

    x = table.e / xunit
    y = table.value * factor
    ysta = np.transpose(table.err_sta) * factor
    ysys = np.transpose(table.err_sys) * factor
    xerr = np.abs(np.transpose(table.e_bin / xunit) - x) if show_bin else None
    is_ul = table.is_upper_limit
    return _draw_with_errorbars(x, y, ysta, ysys, xerr, is_ul, label, sys_lw, **kwargs)


def draw_timeseries(
    table: np.recarray,
    factor: float = 1.0,
    label: Optional[str] = None,
    show_bin: bool = False,
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
    show_bin : bool, optional
        If true, show horizontal error bars to indicate the energy bin.
    sys_lw : float, optional
        Line width for the error bar that represents systematic uncertainties.
    kwargs :
        Other keyword arguments are forwarded to matplotlib.pyplot.errorbar.
    """
    multiple_ranges = 0
    x = []
    xerr = []
    for dt in table.datetime:
        if ";" in dt:
            multiple_ranges += 1
            x1: Optional[datetime] = None
            x2: Optional[datetime] = None
            for dti in dt.split(";"):
                cx, dx = get_mean_datetime(dti)
                if x1 is None or cx - dx < x1:
                    x1 = cx - dx
                if x2 is None or cx + dx > x2:
                    x2 = cx + dx
            dx = (x2 - x1) / 2  # type:ignore
            cx = x1 + 0.5 * dx  # type:ignore
        else:
            cx, dx = get_mean_datetime(dt)
        x.append(cx)
        xerr.append(dx)
    if multiple_ranges:
        msg = (
            f"input contains {multiple_ranges} points with multiple time ranges, "
            "we use minimum and maximum to construct an interval"
        )
        warnings.warn(msg, RuntimeWarning)
    x = np.array(x)
    y = table.value * factor
    ysta = np.transpose(table.err_sta) * factor
    ysys = np.transpose(table.err_sys) * factor
    xerr = np.transpose(xerr)  # type:ignore
    is_ul = table.is_upper_limit
    kwargs["marker"] = "."
    return _draw_with_errorbars(
        x, y, ysta, ysys, xerr if show_bin else None, is_ul, label, sys_lw, **kwargs
    )


def draw_references(
    table: np.recarray,
    color: str = "0.5",
    fontsize: Union[str, int] = "xx-small",
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
    fontsize: str or int, optional
        Font size in absolute units (int) or relative units (str).
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


def _draw_with_errorbars(
    x: np.ndarray,
    y: np.ndarray,
    ysta: np.ndarray,
    ysys: np.ndarray,
    xerr: Optional[np.ndarray],
    is_ul: np.ndarray,
    label: Optional[str],
    sys_lw: float,
    **kwargs: Any,
) -> Line2D:
    for key in ("ls", "linestyle"):
        if key in kwargs:
            del kwargs["ls"]
    if "fmt" in kwargs:
        raise ValueError("keyword 'fmt' is not allowed, use 'marker' instead")
    # taking abs here should not be necessary, but David reported issues
    ysta = np.abs(ysta)
    ysys = np.abs(ysys)
    if xerr is not None:
        xerr = np.abs(xerr)
    is_pt = ~is_ul
    lines = None
    for mask in (is_pt, is_ul):
        if not np.any(mask):
            continue
        xm = x[mask]
        ym = y[mask]
        ystam = ysta[:, mask]
        ysysm = ysys[:, mask]
        if xerr is None:
            xerrm = None
        else:
            xerrm = xerr[..., mask]
        if mask is is_ul:
            ystam = 0.2 * ym
        lines = plt.errorbar(
            xm,
            ym,
            ystam,
            xerrm,
            uplims=mask is is_ul,
            ls="none",
            label=label if lines is None else None,
            **kwargs,
        )[0]
        kwargs["color"] = lines.get_color()
        for key in ("alpha", "lw", "linewidth", "marker"):
            if key in kwargs:
                del kwargs[key]
        if mask is is_pt:
            plt.errorbar(
                xm,
                ym,
                ysysm,
                marker="none",
                ls="none",
                lw=sys_lw,
                alpha=0.5,
                **kwargs,
            )
    return lines
