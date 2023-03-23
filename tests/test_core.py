"""
This module tests functions in isxcore.core 
"""
import numpy as np
import pandas as pd

from pycore.core import hash_dict, md5hash, struct


def test_md5hash():
    """tests the universal hashing function"""

    # int
    assert (
        md5hash(0) == "7dea362b3fac8e00956a4952a3d4f474"
    ), "Failure in hashing int"

    assert (
        md5hash(0.0) == "30565a8911a6bb487e3745c0ea3c8224"
    ), "Failure in hashing floats"

    assert (
        md5hash([1.0]) == "3147e474b9c2a5b484473aaebccd5213"
    ), "Failure in hashing lists"

    assert (
        md5hash("wow") == "bcedc450f8481e89b1445069acdc3dd9"
    ), "Failure in hashing a string"

    assert (
        md5hash(["wow"]) == "96cabca7a92e0ebe17f802ad6e592cb2"
    ), "Failure in hashing a string in a list"

    assert (
        md5hash(["wow", "foo"]) == "74e12dc5917c5035cdb1ae6c692cac34"
    ), "Failure in hashing a list of strings"

    df = pd.DataFrame(dict(a=[1, 2, 4], b=["a", "b", "c"]))

    assert (
        md5hash(df) == "3f49ae9563974257fac2e582ae4084df"
    ), "Failure in hashing pandas dataframe"

    assert (
        md5hash(np.zeros(10)) == "bbf7c6077962a7c28114dbd10be947cd"
    ), "Failure in hashing a numpy array"

    assert (
        md5hash((1, 2, "a")) == "8de6e804d698fc88d230c169a509cc20"
    ), "Failure in hashing a tuple"


def test_struct():
    """tests the struct class"""
    a = struct()
    assert isinstance(a, dict), "struct is not a dictionary"

    # check fast construction
    a = struct(foo=1, bar="wow")
    assert a.foo == 1, "Something went wrong in getting members"
    assert a.bar == "wow", "Something went wrong in getting members"


def test_hash_dict():
    """tests hash dict"""

    data = {}
    data["foo"] = 10
    data["bar"] = "wow"
    data["baz"] = np.zeros(10)
    data["list"] = ["wow", "so", "list"]
    data["float"] = 3.14

    correct_hash = "ab57ae69616db0669f32dd8ad9c3d9f8"

    hash = hash_dict(data)

    assert hash == correct_hash, "unexpected hash"

    # now the same thing, but keys in a different order

    data = {}
    data["float"] = 3.14
    data["bar"] = "wow"
    data["foo"] = 10
    data["baz"] = np.zeros(10)
    data["list"] = ["wow", "so", "list"]

    hash = hash_dict(data)

    assert hash == correct_hash, "unexpected hash when reordering dictionary"

    # now add a key and ignore it
    data["ignored1"] = "wow"
    data["ignored2"] = "goo"

    hash = hash_dict(data, ignore_keys=["ignored1", "ignored2"])

    assert hash == correct_hash, "unexpected hash with ignored keys"
