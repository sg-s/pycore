from pycore.filetools import format_bytes


def test_format_bytes():
    assert (
        format_bytes(100_000_000_000_000) == "90.95 TB"
    ), "Format bytes failed"

    assert format_bytes(900_000_000) == "858.31 MB", "format_bytes failed"
