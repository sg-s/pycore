"""
This module contains core functionality that is present in MATLAB
but isn't in python, so acts as a shorthand for commonly used functions
and types 
"""
import hashlib
import inspect
import os

import matplotlib.pyplot as plt
import numpy as np


def format_p_value(pvalue: float) -> str:
    """
    pretty formats a given p-value

    if your p-values are very small, follows
    good statistical practice and reports it
    as < .01 instead of some meaningless ~0
    value

    Args:
        pvalue (float): p-value

    Returns:
        str: nicely formatted string
    """
    if pvalue < 0.01:
        txt = "p < .01 "
    else:
        txt = "p = " + "{:.2f}".format(pvalue)

    return txt


def hash_dict(dictionary):
    """
    hashes a dictionary, by directly hashing values
    numpy.ndarrays are converted to bytes and then hashed
    all hashes are combined to return a single hash

    Args:
        dictionary (dict): some dictionary with string keys

    Returns:
        hash: hex-encoded string
    """
    check_type(dictionary, dict)
    keys = dictionary.keys()
    m = hashlib.md5()

    for key in keys:
        temp = dictionary[key]

        if isinstance(temp, list):
            t = tuple(temp)
            for thing in t:
                m.update(thing.encode())
        elif isinstance(temp, np.ndarray):
            m.update(temp)
        else:
            m.update(temp.to_bytes(8, "big"))

    return m.hexdigest()


def check_all_arrays_same_shape(arrays):
    """Checks that all arrays have the same shape

    Args:
        arrays (tuple): tuple of np.ndarrays

    No Longer Returned:
        nothing
    """
    for i in range(len(arrays)):
        check_type(arrays[i], np.ndarray)
        assert arrays[0].shape == arrays[i].shape, "All arrays should be the same size"


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
    ), "Argument is not a numpy.vector, instead, it has shape: " + str(thing.shape)


def dict_to_array(d):
    """converts d to an np.array, ignoring keys

    Args:
        d (dictionary): some dictionary

    Returns:
        TYPE: Description
    """

    temp = np.array(list(d.items()))
    return temp[:, -1]


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
