"""
This module contains core functionality that is present in MATLAB
but isn't in python, so acts as a shorthand for commonly used functions
and types 
"""

import hashlib
from typing import Optional

import numpy as np


class struct(dict):
    """structs are simply dictionaries that you
    can access using dot notation
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def format_p_value(pvalue: float) -> str:
    """
    utility function to prettify printing of p-values


    Args:
        pvalue (float): p-value ∈ [0,1]

    Returns:
        str: "p = .81" or "p < .01"
    """
    if pvalue < 0.001:
        return "p < .001"
    else:
        return "p = " + "{:.3f}".format(pvalue)


def md5hash(obj):
    """
    hash almost anything

    Args:
        thing (TYPE): Description
    """

    m = hashlib.md5()

    if obj is None:
        return "none"

    elif isinstance(obj, float):
        # hashing floats is basically impossible in python,
        # see: https://stackoverflow.com/questions/58212573/
        # how-to-use-hashlib-to-md5-hash-a-number
        # so we're going to use a dirty hack to cast into a string
        m.update(str(obj).encode())
    elif isinstance(obj, list):
        t = tuple(obj)
        list_m = ""
        for thing in t:
            list_m += md5hash(thing)
        m.update(list_m.encode())
    elif isinstance(obj, np.ndarray):
        m.update(np.ascontiguousarray(obj))
    elif isinstance(obj, str):
        m.update(obj.encode())
    else:
        m.update(obj.to_bytes(8, "big"))
    return m.hexdigest()


def hash_dict(dictionary: dict, *, ignore_keys: Optional[list] = None) -> str:
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
    keys = list(dictionary.keys())
    m = hashlib.md5()

    # sort keys to make this reproducible
    keys.sort()

    for key in keys:
        if ignore_keys is not None and key in ignore_keys:
            continue

        value = dictionary[key]

        if isinstance(value, list):
            t = tuple(value)
            for thing in t:
                m.update(thing.encode())
        elif isinstance(value, float):
            m.update(str(value).encode())
        elif isinstance(value, np.ndarray):
            m.update(value)
        elif isinstance(value, str):
            m.update(value.encode())
        else:
            m.update(value.to_bytes(8, "big"))

    return m.hexdigest()


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
