"""
contains useful maths-related functions
"""


import numpy as np
import pandas as pd
import scipy
import scipy.cluster.hierarchy as sch
from pycore.matlab import chunk_index
from scipy import stats


def cluster_corr(corr_array, inplace=False):
    """
    Rearranges the correlation matrix, corr_array, so that groups of highly
    correlated variables are next to eachother

    Parameters
    ----------
    corr_array : pandas.DataFrame or numpy.ndarray
        a NxN correlation matrix

    Returns
    -------
    pandas.DataFrame or numpy.ndarray
        a NxN correlation matrix with the columns and rows rearranged
    """
    pairwise_distances = sch.distance.pdist(corr_array)
    linkage = sch.linkage(pairwise_distances, method="complete")
    cluster_distance_threshold = pairwise_distances.max() / 2
    idx_to_cluster_array = sch.fcluster(
        linkage, cluster_distance_threshold, criterion="distance"
    )
    idx = np.argsort(idx_to_cluster_array)

    if not inplace:
        corr_array = corr_array.copy()

    if isinstance(corr_array, pd.DataFrame):
        return corr_array.iloc[idx, :].T.iloc[idx, :]
    return corr_array[idx, :][:, idx]


def cross_correlation(x: np.array, y: np.array, *, chunk_size: int = 1000):
    """computes the cross correlation between two vectors

    a wrapper around scipy.correlate, with the following tricks:

    - sane defaults
    - auto zscoring
    - splits signals into smaller chunks and computes in each chunk


    """

    x = x.flatten()
    y = y.flatten()

    idx = chunk_index(x, chunk_size=chunk_size)

    groups = np.unique(idx)

    a = stats.zscore(x[idx == groups[0]])
    c = np.full((len(a), len(groups)), np.nan)

    for i, group in enumerate(groups):
        a = stats.zscore(x[idx == group])
        b = stats.zscore(y[idx == group])

        try:
            c[:, i] = scipy.signal.correlate(a, b, mode="same")
            c[:, i] /= len(a)
        except Exception:
            pass
    return c
