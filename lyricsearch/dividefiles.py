#!/usr/bin/env python3.7
"""Divide the lyrics text files (fairly) evenly into directories."""
# stand lib
from collections import deque
from pathlib import Path
import sys
from time import time
from typing import Any, Deque

# custom
from constants import (
    LYRICSDIR,
    RESULTSDIR,
    SOURCETEXT,
    )
from dividefilesutil import (
    move_deque_files,
    valid_bins,
    fairly_divide,
    progress_bar,
    )
from filesanddirs import (
    block_dir,
    count_files,
    get_files,
    )


def get_user_input() -> int:
    """Get user input from prompt. Returns Integer."""
    try:
        bins = int(input("How many bins do you want to sort into? "))
    except ValueError:
        print("Please choose a number. Quitting...")
        quit()
    return bins


def make_groups(bins: int) -> Any:
    """Divide the file paths into groups. Returns ???"""
    # count and sort file paths in memory
    if valid_bins(bins):
        print("Counting files...")
        file_amt = count_files(SOURCETEXT)
        print("File count:", str(file_amt))

        fs: Deque = deque()
        collected_files = 0
        print("Collecting files...")
        for f in get_files(SOURCETEXT):
            fs.append(str(f.resolve()).strip())
            collected_files += 1
            progress_bar(collected_files, file_amt, prefix="Collected:")

        print("Finished collecting files.")

        print("Dividing files...")
        groups = fairly_divide(fs, bins)
        print("Finished dividing files.")
    else:
        print("Please choose a factor of 2  between 2 and 16.")
        quit()
    return groups


def move_files(groups: Any) -> None:
    print("Moving files...")
    start = time()
    finished_groups = 0
    for group in groups:
        block = Path(LYRICSDIR+block_dir(finished_groups)).resolve()
        if not block.exists():
            block.mkdir(mode=0o755)
        move_deque_files(group, str(block.resolve()))
        finished_groups += 1
        print("Group {0} of {1}".format(finished_groups, len(groups)))
    print("Finished moving.")
    finish = time()
    print("Time taken:", str(round(finish-start, 2)))
    return None


def divide_all_files() -> None:
    bins = get_user_input()
    groups = make_groups(bins)
    if not Path(LYRICSDIR).exists():
        Path(LYRICSDIR).mkdir(mode=0o755)
    move_files(groups)
    return None


if __name__ == "__main__":
    divide_all_files()
