"""small tools to help with files"""

import math
import os

from beartype import beartype


@beartype
def largest(files: list) -> str:
    """
    returns largest file in a list of files

    Args:
        files (list): list of file paths

    Returns:
        path pointing to largest file
    """
    sizes = [os.path.getsize(file) for file in files]
    return files[sizes.index(max(sizes))]


@beartype
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


@beartype
def get_folder_size(start_path: str = ".") -> int:
    """get total size of folder, including all sub directories"""
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


@beartype
def format_bytes(size_bytes: int) -> str:
    """converts bytes into MB, GB, etc. for a humans

    from here:

    https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
