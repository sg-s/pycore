"""
This module contains core functionality that is present in MATLAB
but isn't in python, so acts as a shorthand for commonly used functions
and types 
"""
import matplotlib.pyplot as plt
import numpy as np
import inspect
import os


def check_all_arrays_same_shape(arrays):
    """Checks that all arrays have the same shape

    Args:
        arrays (tuple): tuple of np.ndarrays

    Returns:
        nothing
    """
    for i in range(len(arrays)):
        check_type(arrays[i], np.ndarray)
        assert arrays[0].shape == arrays[i].shape, "All arrays should be the same size"


def check_element_type(things, typename):
    """checks if a numpy array has elements of a certain type

    Args:
        things (np.ndarray): array that should contain typename
    """

    check_type(things, np.ndarray)
    for thing in things:
        check_type(thing, typename)


def check_vector(thing):
    """checks if argument is a numpy vector

    Args:
        thing (anything): any thing

    Returns:
        nothing
    """

    check_type(thing, np.ndarray)

    assert (
        len(thing.shape) == 1
    ), "Argument is not a numpy.vector, instead, it has shape: " + str(thing.shape)


def dict_to_array(d):
    """converts d to an np.array, ignoring keys

    Args:
        d (dictionary): some dictionary
    """

    temp = np.array(list(d.items()))
    return temp[:, -1]


def check_first_dimension_size(things):
    """checks if all the things passed in here have the same
    size in the first dimension

    Args:
        things (tuple): tuple of anything
    """

    if hasattr(things[0], 'shape'):
        first_dim_size = things[0].shape[0]
    else:
        first_dim_size = len(things[0])

    for thing in things:
        if hasattr(thing, 'shape'):
            this_size = thing.shape[0]
        else:
            this_size = len(thing)

        assert (
            first_dim_size == this_size
        ), "Not all things have the same first dimension size"


def check_type(thing, typename):
    """
    checks if thing is of type typename, if not, throws an error

    Arguments:
    ----------
    thing: any object
    typename: valid python type of type type
    """

    assert isinstance(thing, typename), (
        "Expected argument to be of: "
        + str(typename)
        + ". Instead, it was of: "
        + str(type(thing))
    )
