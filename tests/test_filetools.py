from pycore.filetools import format_bytes, get_folder_size


def test_get_folder_size():

    assert (
        get_folder_size("/Users/srinivas/code/pycore/.github/") == 890
    ), "folder size estimation failed"


def test_format_bytes():

    assert (
        format_bytes(100_000_000_000_000) == "90.95 TB"
    ), "Format bytes failed"

    assert format_bytes(900_000_000) == "858.31 MB", "format_bytes failed"
