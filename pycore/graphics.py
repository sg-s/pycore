"""
This module contains helper graphics functions for making figures, subplots
and modifying plots
"""

from typing import List, Optional, Tuple

import bokeh
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import pandas as pd
import scipy.stats
from bokeh.plotting import figure, output_notebook
from matplotlib import cm

from pycore.core import (
    check_all_arrays_same_shape,
    check_vector,
    dict_to_array,
    format_p_value,
)

output_notebook()


def scatter_groups(
    data: pd.DataFrame,
    x: str,
    y: str,
    group_by: str,
    width: int = 333,
    height: int = 333,
    size: int = 10,
    legend_location: str = "bottom_right",
    x_axis_type="linear",
    y_axis_type="linear",
):
    """
    creates an interactive scatter plot using bokeh
    where clicking on legend shows/hides dots
    for that group
    """

    fig = figure(
        width=width,
        height=height,
        tools=[],
        toolbar_location=None,
        x_axis_label=x,
        y_axis_label=y,
        x_axis_type=x_axis_type,
        y_axis_type=y_axis_type,
    )

    groups = data[group_by].unique()

    if len(groups) < 9:
        colors = bokeh.palettes.Colorblind[8]
    else:
        colors = bokeh.palettes.Viridis256[256]

    for i, group in enumerate(groups):
        xx = list(data[x][data[group_by] == group])
        yy = list(data[y][data[group_by] == group])
        fig.circle(
            xx,
            yy,
            alpha=0.5,
            legend_label=group,
            hover_alpha=1,
            fill_color=colors[i],
            line_color=colors[i],
            size=size,
        )

    fig.legend.click_policy = "hide"
    fig.legend.location = legend_location

    return fig


def subsample(x: np.ndarray, bin_size: int = 50) -> np.ndarray:
    """
    min-max resampler to make plots smaller
    and to prevent the heat death of your graphics card

    this destroys and alters data, and should only be used
    for plots!

    Args:
        x: a vector
        bin_size: max and min will be computed on this bin size (default 50)
    """

    check_vector(x)

    z = np.floor(x.shape[0] / bin_size).astype(int) * bin_size
    xx = x[0:z]
    nbins = int(len(xx) / bin_size)

    xx = np.reshape(xx, (nbins, bin_size))
    tops = xx.max(axis=1)
    bottoms = xx.min(axis=1)

    reduced_x = np.zeros(tops.shape[0] * 2)
    reduced_x[1::2] = tops
    reduced_x[0::2] = bottoms

    return reduced_x


def plot_pairwise(
    x: np.ndarray,
    y: np.ndarray,
    ax=None,
    color=None,
    label: Optional[str] = None,
    size: int = 2,
    annotations: Optional[list] = None,
) -> None:
    """
    makes a pairwise scatter plot and performs a
    paired t-test

    Args:
        x (numpy vector): some vector
        y (numpy vector): some other vector
        ax (None, optional): where to plot?
        color: the one color to color all points
        label: label for all points
        annotations: if you want annotations for each point, use this
    """
    ax = check_axis(ax)

    check_vector(x)
    check_vector(y)

    check_all_arrays_same_shape((x, y))

    m = np.nanmin(np.concatenate((x, y)))
    M = np.nanmax(np.concatenate((x, y)))

    plt.sca(ax)
    plt.plot([m, M], [m, M], "k:")

    ax.set_aspect("equal", adjustable="box")
    if color is None:
        color = "k"

    # t-test
    t, p = scipy.stats.ttest_rel(x, y, nan_policy="omit")
    p = format_p_value(p)

    if annotations is not None:
        h = plt.scatter(np.nan, np.nan, color=color, s=size)

        for idx, annotation in enumerate(annotations):
            ax.annotate(
                annotation,
                (x[idx], y[idx]),
                horizontalalignment="center",
                verticalalignment="center",
                color=color,
                fontweight="bold",
            )

    else:
        h = plt.scatter(x, y, color=color, s=size)

    if label is None:
        h.set_label(p)
    else:
        h.set_label(label + " " + p)
    plt.legend()


def reorder_colormap(cmap="plasma", reorder_by=None):
    """
    reorder a colormap by some vector

    Args:
        cmap (str, optional): name of built-in colormap
        reorder_by (np.array): some vector

    Returns:
        TYPE: sorted colormap
    """
    cmap = cm.get_cmap(cmap)

    order = np.argsort(reorder_by)
    ranks = order.argsort()
    N = len(reorder_by)
    colors = [cmap(r / N) for r in ranks]

    return colors


def labelled_subplots(mosaic, label=True, **optionals):
    """wrapper to subplot_mosaic that makes subplots

    Args:
        mosaic (list of lists): or other mosaic compatible arg.
        **optionals: key value arguments that are passed onto subplot_mosaic

    Returns:
        fig: handle to figure
        axes: numpy array of axes
    """
    plt.close("all")
    fig, axes = plt.subplot_mosaic(mosaic, constrained_layout=True, **optionals)
    if label:
        label_axes(fig, axes)

    axes = dict_to_array(axes)

    return fig, axes


def label_axes(fig, axs, fontsize=15):
    """label axes generated by subplot_mosaic

    given a dictionary of axes objects, each axes object is labelled
    with the key of that dictionary item

    Args:
        fig (matplotlib.figure.Figure):
        axs (dictionary of axes):
        fontsize (str, optional): specify font size using valid syntax
    """
    for label, ax in axs.items():
        # label physical distance to the left and up:
        trans = mtransforms.ScaledTranslation(-20 / 72, 7 / 72, fig.dpi_scale_trans)
        ax.text(
            -0.02,
            1.0,
            label,
            transform=ax.transAxes + trans,
            fontsize=fontsize,
            va="bottom",
            fontfamily="sans-serif",
            fontweight="bold",
        )


def check_axis(axis):

    """
    Utility function that generates an axis if needed, and activates it

    Parameters:
    -----------
    axis: None or axis

    Returns:
    -----------
    handle to an axis

    """

    if axis is None:
        _, axis = plt.subplots()

    if isinstance(axis, np.ndarray):
        # probably fine, hope for the best
        try:
            plt.sca(axis[0])
        except:
            _, axis = plt.subplots()
            plt.sca(axis)

    else:
        plt.sca(axis)

    return axis
