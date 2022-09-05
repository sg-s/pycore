"""
This module tests functions in isxcore.core 
"""
import numpy as np
from pycore.core import hash_dict


def test_hash_dict():
    """tests hash dict"""
    data = {}
    data["foo"] = 10
    data["bar"] = "wow"
    data["baz"] = np.zeros(10)
    data["list"] = ["wow", "so", "list"]

    hash = hash_dict(data)

    assert hash == "10f15aecea001568b0fb5fabfa14e14b", "unexpected hash"
