import os
import re
from datetime import date


def bump(file_name: str) -> None:
    """function that bumps version in a file to today's date
    (using calver). should work with any text file
    as long as there is a line with the word version in it
    """

    today = date.today()
    version = f"{str(today.year)[-2:]}.{today.month}.{today.day}"

    with open(file_name, "r") as file:
        lines = file.readlines()

    outfile = file_name + ".temp"
    with open(outfile, "w") as file:
        for line in lines:
            try:
                if "version" in line:
                    match = re.search(r"\d+\.\d+.\d+", line)
                    old_version = match.group(0)
                    file.write(line.replace(old_version, version))
                else:
                    file.write(line)
            except Exception:
                file.write(line)

    # delete the old file
    os.remove(file_name)

    # rename the new file to the old file
    os.rename(file_name + ".temp", file_name)
