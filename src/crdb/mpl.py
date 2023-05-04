from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt
from numpy.typing import NDArray


def draw_table(table, factor=1.0, label=None, sys_lw=5, **kwargs):
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


def draw_references(
    table: NDArray,
    color: str = "0.5",
    fontsize: str = "xx-small",
    **kwargs,
):
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


def draw_logo(x, y, height=0.1, zorder=None):
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
