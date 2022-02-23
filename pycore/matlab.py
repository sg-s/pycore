"""
This module contains functions that mimic some of MATLAB's builtins
for easier transition to python land
"""

import multiprocessing
from typing import Callable

import numpy as np

from pycore.core import (
    check_all_arrays_same_shape,
    check_first_dimension_size,
    check_type,
    check_vector,
)
from pycore.graphics import check_axis


def downsample(
    x: np.array, *, bin_size: int = 10, func=lambda x: np.nanmean(x, axis=1)
) -> np.array:
    """
    fast, effective downsampler

    Args:
        x (np.array): Description
        bin_size (int, optional): Description
    """

    check_vector(x)

    # trim to closest multiple of bin size
    z = np.floor(x.shape[0] / bin_size).astype(int) * bin_size
    xx = x[0:z]
    nbins = int(len(xx) / bin_size)

    xx = np.reshape(xx, (nbins, bin_size))
    tops = func(axis=1)
    bottoms = xx.min(axis=1)


def chunk_index(x: np.array, chunk_size: int) -> np.array:
    """
    returns an array the same size of x that
    partitions it into chunks of size chunk_size
    going from left to right along the array

    Args:
        x (np.array): Description
        chunk_size (int): Description
    """

    return np.floor(np.arange(len(x)) / chunk_size).astype(int)


def first_nonzero(arr: np.array, axis: int = 0, invalid_val: float = -1):
    """
    find the index of the first non-zero element in an array

    Args:
        arr (np.array): some array
        axis (TYPE): axis to operate on
        invalid_val (-1): if there are no nonzero values, then use
        this to indicate

    Returns:
        array of integers of positions in array
    """

    mask = arr != 0
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)


def last_nonzero(arr, axis=0, invalid_val=-1):
    """
    find the index of the last non-zero element in an array

    Args:
        arr (np.array): some array
        axis (TYPE): axis to operate on
        invalid_val (-1): if there are no nonzero values, then use
        this to indicate

    Returns:
        array of integers of positions in array
    """
    mask = arr != 0
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)


def parfor(func: Callable, args, operate_on_columns: bool = True):
    """
    auto parallelization of numpy arrays

    Automatically apply function to columns/rows
    of numpy array using multiprocessing.Pool

    This is an attempt to replicate the simplicity of
    parfor in MATLAB. Basically this is to allow something
    like this in MATLAB:

    % X, Y are some arrays
    parfor i = 1:length(X)
        X(i,:) = func(Y(i,:));
    end

    Args:
        func (function): Description
        args (TYPE): Description
        operate_on_columns (bool, optional): Description

    Returns:
        TYPE: Description
    """

    assert callable(func), "Expected first argument to be a function"
    check_all_arrays_same_shape(args)

    n_procs = multiprocessing.cpu_count()

    if operate_on_columns:
        n_col = args[0].shape[1]
        n_args = len(args)
        func_data = [[args[i][:, col] for i in range(n_args)] for col in range(n_col)]

    else:
        n_rows = args[0].shape[0]
        n_args = len(args)
        func_data = [[args[i][row, :] for i in range(n_args)] for row in range(n_rows)]

    with multiprocessing.Pool(n_procs) as p:
        result = p.starmap(func, func_data)

    if operate_on_columns:
        result = np.array(result).transpose()
    else:
        result = np.array(res)

    return result


def _methods_and_properties(thing, ignore_internal=True):
    """returns methods and properties of an object

    Args:
        thing (object): some object

    Returns:
        methods: list of method names
        properties: list of property names

    """

    method_list = []
    prop_list = []
    for attr_name in dir(thing):

        if attr_name.startswith("_") and ignore_internal:
            continue

        try:
            if callable(getattr(thing, attr_name)):
                method_list.append(str(attr_name))
            else:
                prop_list.append(str(attr_name))
        except:
            pass

    return method_list, prop_list


def methods(thing, spacing=None, ignore_internal: bool = True):
    """show methods of object.

    Args:
        thing (some object): any object

    Ignores attributes starting with "__"

    modified from: https://stackoverflow.com/questions/34439/
    finding-what-methods-a-python-object-has

    """

    method_list, _ = _methods_and_properties(thing, ignore_internal=ignore_internal)

    process_func = (lambda s: " ".join(s.split())) or (lambda s: s)

    if spacing is None:
        spacing = 3 + max([len(method) for method in method_list])

    for method in method_list:

        try:
            print(
                str(method.ljust(spacing))
                + " "
                + process_func(str(getattr(thing, method).__doc__)[0:90])
            )
        except:
            print(method.ljust(spacing) + " " + " getattr() failed")


def properties(thing, ignore_internal: bool = True, spacing: int = 20):
    """show properties of object

    Args:
        thing (TYPE): object
        ignore_internal (True, optional): should we ignore
        attrs that start with _?
    """
    _, prop_list = _methods_and_properties(thing, ignore_internal=ignore_internal)

    process_func = (lambda s: " ".join(s.split())) or (lambda s: s)

    for method in prop_list:

        try:
            print(
                str(method.ljust(spacing))
                + " "
                + process_func(str(getattr(thing, method).__doc__)[0:90])
            )
        except:
            print(method.ljust(spacing) + " " + " getattr() failed")


def imshow(X: np.ndarray, axis=None):
    """behaves like MATLAB's imshow, just plots the matrix given to it

    If no axis is specified, returns a handle to the axis. If it is,
    then returns a handle to the image


    Arguments:
        X (np.ndarray): Description
        axis (None, optional): where to plot?

    Returns:
        axis: handle to an axis
        or
        image_handle: handle to image created on axis provided
    """

    check_type(X, np.ndarray)

    return_axis = False
    if axis is None:
        return_axis = True

    axis = check_axis(axis)
    axis.imshow(X, aspect="auto")

    image_handle = axis.get_images()

    if return_axis:
        return axis
    else:
        return image_handle


def Vector(N, *, dtype="float64", fill=None):
    """makes a vector, because this is fraught with danger

    Args:
        N (int): how long should it be?
        dtype (str, optional): type of thing in vector
        fill (None, optional): What should it be filled with?

    Returns:
        TYPE: Description
    """
    x = np.zeros(N, dtype=dtype)
    if fill is not None:
        x.fill(fill)
    else:
        x.fill(np.nan)

    return x


def splitapply(
    data: np.array, *, groups: np.array, func=np.nanmean, flatten: bool = False
) -> np.array:
    """equivalent to MATLAB's splitapply

    Args:
        data (np.ndarray): 2D or 1D matrix
        groups (np.ndarray): vector as long as data

    Returns:
        result: np.ndarray the same size as unique(groups)

    """

    check_type(data, np.ndarray)
    check_type(groups, np.ndarray)
    check_first_dimension_size((data, groups))

    data = np.copy(data)

    unique_values = np.unique(groups)

    if flatten or len(data.shape) == 1:
        result = np.full(unique_values.shape, np.nan)
    else:
        result = np.full((unique_values.shape[0], data.shape[1]))

    for i, value in enumerate(unique_values):

        if flatten:
            result[i] = func(data[groups == value].flatten())
        else:
            result[i] = func(data[groups == value])

    return result
