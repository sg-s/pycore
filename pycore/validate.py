"""This module provides shortcuts for simple input validation"""

import os

import matplotlib.pyplot as plt
import numpy as np


def ext_is(txt: str, ext: str):
    """input should have an extention that is of a certain type"""
    this_ext = os.path.splitext(txt)[1]
    assert (
        this_ext == ext
    ), f"txt should have an extension {ext}, instead it was {this_ext}"


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
        except Exception:
            _, axis = plt.subplots()
            plt.sca(axis)

    else:
        plt.sca(axis)

    return axis
