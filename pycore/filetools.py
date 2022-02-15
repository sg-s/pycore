"""small tools to help with files"""

import os


def largest(files: list):
    """
    returns largest file in a list of files

    Args:
        files (list): list of file paths

    Returns:
        path pointing to largest file
    """
    sizes = [os.path.getsize(file) for file in files]
    return files[sizes.index(max(sizes))]


def smallest(files: list) -> str:
    """
    returns smallest file in a list of files

    Args:
        files (list): list of file paths

    Returns:
        path pointing to smallest file
    """
    sizes = [os.path.getsize(file) for file in files]
    return files[sizes.index(min(sizes))]
