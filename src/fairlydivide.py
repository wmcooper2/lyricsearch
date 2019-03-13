"""Divide the lyrics text files (fairly) evenly."""
# stand lib
from collections import deque
import os
from pathlib import Path
import shutil
from time import time
# from typing import Queue
from typing import Any
from typing import Deque
from typing import List
from typing import Text

# custom
from constants import *
from searchutil import *


valid_bins = lambda num: 2 <= num and num <= 16
no_remainder = lambda x, y: x % y == 0


def count_files(dir_: str) -> int:
    """Counts the files that end in '.txt' in 'path_'. Returns Integer."""
    return sum([1 for x in Path(dir_).glob("**/*.txt")])


def get_files(dir_: str) -> list:
    """Gets text files from dir_, recursively. Returns List."""
    return [file_ for file_ in Path(dir_).glob("**/*.txt")]


def divide_bulk(main, sub, num):
    """Appends num elements from main to sub. Returns None."""
    [sub.append(main.pop()) for x in range(num)]


def divide_remainder(a: Any, b: Deque) -> None:
    """Try to put an element into QueueA from QueueB. Returns None."""
    try:
        a.append(b.pop())
    except IndexError:
        print("Can't pop from empty list.")


def fairly_divide(files: Deque, bins: int) -> List:
    """Fairly divides files into different directories.
        Returns List of Deque Objects."""
    group_size = len(files)//bins
    groups: List = [deque() for x in range(bins)]
    [divide_bulk(files, group, group_size) for group in groups]
    if not no_remainder(len(files), bins):
        for group in groups:
            if len(files) > 0:
                divide_remainder(group, files)
    return groups


def copy_files(dque: Deque, dest):
    """Copies files at paths in dque to dest. Returns None."""
    for src in dque:
        shutil.copyfile(src, dest)


def divided_dir_name(el: Deque, list_: List) -> Text:
    """Formats dir name. Returns String."""
    return RESULTDIR+"data"+str(list_.index(el)+1)


if __name__ == "__main__":
    if ismac():
        try:
            bins = int(input("How many bins do you want to sort into? "))
        except ValueError:
            print("Please choose a number. Quitting...")
            quit()

        if valid_bins(bins):
            print("Counting files...")
            file_amt = count_files(DATA_DIR+"test2/")
            print("File count:", str(file_amt))

            fs: Deque = deque()
            print("Collecting files...")
            for f in get_files(DATA_DIR+"test2/"):
                fs.append(str(f).strip())
            print("Finished collecting files.")

            print("Dividing files...")
            groups = fairly_divide(fs, bins)
            print("Finished dividing files.")
        else:
            print("Please choose a number between 2 and 16.")
            quit()

        print("Copying files...")
        start = time()
        [copy_files(group, divided_dir_name(group, groups))
            for group in groups]
        print("Finished copying.")
        finish = time()
        print("Time taken:", str(round(finish-start, 2)))
    else:
        print("This script is made for the mac. Quitting...")
