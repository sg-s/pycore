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
    data["float"] = 3.14

    hash = hash_dict(data)

    assert hash == "ae03ed586028061d077ab0fbe69ef5a8", "unexpected hash"
