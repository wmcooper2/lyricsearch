# stand lib
from pathlib import Path
from collections import deque
from typing import Deque
from typing import List
from typing import Text

no_remainder = lambda x, y: x % y == 0
valid_bins = lambda num: 2 <= num and num <= 16


def block_dir(num: int) -> Text:
    """Formats dir name. Returns String."""
    return "block"+str(num)


def block_set(num: int) -> Text:
    """Formats block set name. Returns String."""
    return "blockset"+str(num)


def count_files(dir_: str) -> int:
    """Counts the files that end in '.txt' in 'path_'. Returns Integer."""
    return sum([1 for x in Path(dir_).glob("**/*.txt")])


def copy_deque_files(group: Deque, dest: Text) -> None:
    """Copies files in group to 'dest/'. Returns None."""
    for file_ in group:
        shutil.copy(file_, dest)
    return None


def divide_bulk(files: Deque, sub: Deque, num: int) -> None:
    """Appends num elements from files to sub. Returns None."""
    for x in range(num):
        sub.append(files.pop())
    return None


def divide_remainder(files: Deque, groups: List) -> None:
    """Try to put an element into QueueA from QueueB. Returns None."""
    if len(files) > 0:
        for group in groups:
            try:
                group.append(files.pop())
            except IndexError: # empty deque
                pass
    return None


def get_files(dir_: str) -> list:
    """Gets text files from dir_, recursively. Returns List."""
    return [file_ for file_ in Path(dir_).glob("**/*.txt")]


def fairly_divide(files: Deque, bins: int) -> List:
    """Fairly divides files into different directories.
        Returns List of Deque Objects."""
    group_size = len(files)//bins
    groups: List = [deque() for x in range(bins)]

    for group in groups:
        divide_bulk(files, group, group_size)
    if no_remainder(len(files), bins):
        pass
    else:
        divide_remainder(files, groups)
    return groups


