"""
This module contains helper graphics functions for making figures, subplots
and modifying plots
"""

import inspect
import os
import typing

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import scipy.stats
from matplotlib import cm

from pycore.core import *


def plot_pairwise(x: np.ndarray, y: np.ndarray, ax=None) -> None:
    """makes a pairwise scatter plot

    Args:
        x (numpy vector): some vector
        y (numpy vector): some other vector
        ax (None, optional): Description
    """
    ax = check_axis(ax)

    check_vector(x)
    check_vector(y)

    check_all_arrays_same_shape((x, y))

    m = np.nanmin(np.concatenate((x, y)))
    M = np.nanmax(np.concatenate((x, y)))

    plt.sca(ax)
    plt.xlim(m, M)
    plt.ylim(m, M)

    plt.plot([m, M], [m, M], "k:")

    plt.gca().set_aspect("equal", adjustable="box")
    h = plt.scatter(x, y)

    # t-test
    t, p = scipy.stats.ttest_rel(x, y, nan_policy="omit")
    p = format_p_value(p)
    h.set_label(p)
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

    plt.sca(axis)
    return axis
