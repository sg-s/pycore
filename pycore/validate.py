"""This module provides shortcuts for simple input validation"""

import os


def ext_is(txt: str, ext: str):
    """input should have an extention that is of a certain type"""
    this_ext = os.path.splitext(txt)[1]
    assert (
        this_ext == ext
    ), f"txt should have an extension {ext}, instead it was {this_ext}"
