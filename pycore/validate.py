"""This module provides shortcuts for simple input validation"""

import os

import matplotlib.pyplot as plt
import numpy as np

from beartype import beartype


@beartype
def ext_is(txt: str, ext: str) -> None:
    """input should have an extention that is of a certain type"""
    this_ext = os.path.splitext(txt)[1]
    assert (
        this_ext == ext
    ), f"txt should have an extension {ext}, instead it was {this_ext}"


def check_first_dimension_size(things):
    """checks if all the things passed in here have the same
    size in the first dimension

    Args:
        things (tuple): tuple of anything
    """

    if hasattr(things[0], "shape"):
        first_dim_size = things[0].shape[0]
    else:
        first_dim_size = len(things[0])

    for thing in things:
        if hasattr(thing, "shape"):
            this_size = thing.shape[0]
        else:
            this_size = len(thing)

        assert (
            first_dim_size == this_size
        ), "Not all things have the same first dimension size"


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


def check_all_arrays_same_shape(arrays):
    """Checks that all arrays have the same shape

    Args:
        arrays (tuple): tuple of np.ndarrays

    No Longer Returned:
        nothing
    """
    for i in range(len(arrays)):
        check_type(arrays[i], np.ndarray)
        assert (
            arrays[0].shape == arrays[i].shape
        ), "All arrays should be the same size"


def check_element_type(things, typename):
    """checks if a numpy array has elements of a certain type

    Args:
        things (np.ndarray): array that should contain typename
        typename (TYPE): Description
    """

    check_type(things, np.ndarray)
    for thing in things:
        check_type(thing, typename)


def check_vector(thing):
    """checks if argument is a numpy vector

    Args:
        thing (anything): any thing

    No Longer Returned:
        nothing
    """

    check_type(thing, np.ndarray)

    assert (
        len(thing.shape) == 1
    ), "Argument is not a numpy.vector, instead, it has shape: " + str(
        thing.shape
    )


def check_type(thing, typename):
    """
    checks if thing is of type typename, if not, throws an error

    Arguments:
        thing: any object
        typename: valid python type of type type
        ----------
    """

    assert isinstance(thing, typename), (
        "Expected argument to be of: "
        + str(typename)
        + ". Instead, it was of: "
        + str(type(thing))
    )
