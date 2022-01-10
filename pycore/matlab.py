"""
This module contains functions that mimic some of MATLAB's builtins
for easier transition to python land
"""

import multiprocessing

import numpy as np

from pycore.core import (
    check_all_arrays_same_shape,
    check_axis,
    check_first_dimension_size,
    check_type,
)


def first_nonzero(arr, axis=0, invalid_val=-1):
    """
    find the index of the first non-zero element in an array

    Args:
        arr (np.array): some array
        axis (TYPE): axis to operate on
        invalid_val (-1): if there are no nonzero values, then use this to indicate

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
        invalid_val (-1): if there are no nonzero values, then use this to indicate

    Returns:
        array of integers of positions in array
    """
    mask = arr != 0
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)


def parfor(func, args, operate_on_columns=True):
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


def methods(thing, spacing=None, ignore_internal=True):
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


def properties(thing, ignore_internal=True, spacing=20):
    """show properties of object

    Args:
        thing (TYPE): object
        ignore_internal (True, optional): should we ignore attrs that start with _?
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


def imshow(X, axis=None):
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


def Vector(N, dtype="float64", fill=None):
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


def StringArray(N, value=""):
    """make a 1D string array

    I can't see any built-in which makes an array of strings
    Lists don't work because they don't enforce type and will
    therefore be inefficient.
    This is the equivalent of repmat("",N,1) in MATLAB

    Args:
        N (integer): length of array
        value (optional): fill array with this value
    """
    array = np.array([value for _ in range(N)], dtype="<U5")
    return array


def NaN(dims):
    """makes a NaN array. like NaN in MATLAB

    Args:
        dims (TYPE): tuple specifying shape

    Returns:
        TYPE: array filled with NaNs
    """
    array = np.empty(dims)
    array.fill(np.nan)
    return array


def splitapply(data, groups, func=np.nanmean, flatten=False):
    """equivalent to MATLAB's splitapply

    Args:
        data (np.ndarray): 2D or 1D matrix
        groups (np.ndarray): vector as long as data

    Returns:
        result: np.ndarray the same size as unique(groups)
        unique_values: unique values in groups
    """

    check_type(data, np.ndarray)
    check_type(groups, np.ndarray)
    check_first_dimension_size((data, groups))

    data = np.copy(data)

    unique_values = np.unique(groups)

    if flatten or len(data.shape) == 1:
        result = np.full_like(unique_values, np.nan)
    else:
        result = np.zeros((unique_values.shape[0], data.shape[1]))

    for i, value in enumerate(unique_values):
        this = data[groups == value]

        if flatten:
            result[i] = func(data[groups == value].flatten())
        else:
            result[i] = func(data[groups == value])

    return result, unique_values
