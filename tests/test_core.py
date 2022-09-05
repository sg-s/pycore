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

    assert hash == "bbba5ab5117f57bf9c186955806e4556", "unexpected hash"

    # now the same thing, but keys in a different order

    data = {}
    data["float"] = 3.14
    data["bar"] = "wow"
    data["foo"] = 10
    data["baz"] = np.zeros(10)
    data["list"] = ["wow", "so", "list"]

    hash = hash_dict(data)

    assert hash == "bbba5ab5117f57bf9c186955806e4556", "unexpected hash"

    # now add a key and ignore it
    data["ignored1"] = "wow"
    data["ignored2"] = "goo"

    hash = hash_dict(data, ignore_keys=["ignored1", "ignored2"])

    assert hash == "bbba5ab5117f57bf9c186955806e4556", "unexpected hash"
