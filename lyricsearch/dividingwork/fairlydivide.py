#!/usr/bin/env python3.7
"""Divide the lyrics text files (fairly) evenly into directories."""
# stand lib
from collections import deque
import sys
from time import time

# custom
from constants import (
    LYRICSDIR,
    RESULTSDIR,
    )
from fairlydivideutil import (
    valid_bins,
    fairly_divide,
    )
from filesanddirs import (
    block_dir,
    count_files,
    get_files,
    )
from systemcheck import ismac, ispi


if __name__ == "__main__":
    if ismac():
        try:
            bins = int(input("How many bins do you want to sort into? "))
        except ValueError:
            print("Please choose a number. Quitting...")
            quit()

        if valid_bins(bins):
            print("Counting files...")
            file_amt = count_files(LYRICSDIR)
            print("File count:", str(file_amt))

            fs: Deque = deque()
            print("Collecting files...")
            for f in get_files(LYRICSDIR):
                fs.append(str(f.resolve()).strip())
            print("Finished collecting files.")

            print("Dividing files...")
            groups = fairly_divide(fs, bins)
            print("Finished dividing files.")
        else:
            print("Please choose a factor of 2  between 2 and 16.")
            quit()

        print("Copying files...")
        start = time()
        count = 0
        for group in groups:
            count += 1
            if not Path(RESULTSDIR).exists():
                Path(RESULTSDIR).mkdir(mode=0o755)
            block = Path(RESULTSDIR+block_dir(count)).resolve()
            if not block.exists():
                block.mkdir(mode=0o755)
            copy_deque_files(group, str(block.resolve()))
        print("Finished copying.")
        finish = time()
        print("Time taken:", str(round(finish-start, 2)))
    elif ispi():
        print("This script is made for the mac. Quitting...")
