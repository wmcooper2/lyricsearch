#!/usr/bin/env python3.7
"""Utility module for dividefiles.py"""
# stand lib
import os
from pathlib import Path
from collections import deque
import shutil
from typing import (
        Any,
        Deque,
        List,
        Text,
        )


def block_set(num: int) -> Text:
    """Formats block set name. Returns String."""
    return "blockset"+str(num)


def move_deque_files(group: Deque, dest: Text) -> None:
    """Moves files in group to 'dest/'. Returns None."""
    file_amt = len(group)
    moved = 0
    for file_ in group:
        shutil.move(str(file_), dest, copy_function=shutil.copy)
        moved += 1
        progress_bar(moved, file_amt, prefix=str(moved)+"/"+str(file_amt)
                     newline=False)
    return None

def copy_deque_files(group: Deque, dest: Text) -> None:
    """Copies files in group to 'dest/'. Returns None."""
    file_amt = len(group)
    copied_files = 0
    for file_ in group:
        shutil.copy(file_, dest)
        copied_files += 1
        progress_bar(copied_files, file_amt, prefix="Copied:")
    return None


def divide_bulk(files: Deque, sub: Deque, num: int) -> None:
    """Appends num elements from files to sub. Returns None."""
    divided = 0
    for x in range(num):
        sub.append(files.pop())
        divided += 1
    return None


def divide_remainder(files: Deque, groups: List) -> None:
    """Try to put an element into QueueA from QueueB. Returns None."""
    if len(files) > 0:
        for group in groups:
            try:
                group.append(files.pop())
            except IndexError:  # empty deque
                pass
    return None


def fairly_divide(deques: Deque, bins: int) -> List[Deque]:
    """Fairly divides files. Returns List of Deque Objects."""
    group_size = len(deques)//bins
    groups: List[Deque] = [deque() for x in range(bins)]
    finished = 0
    for group in groups:
        divide_bulk(deques, group, group_size)
        finished += 1
    if no_remainder(len(deques), bins):
        pass
    else:
        divide_remainder(deques, groups)
    return groups


def no_remainder(x: int, y: int) -> bool:
    return x % y == 0


# taken from StackOverflow
def progress_bar(iteration, total, prefix='Progress:',
                 suffix='Complete:', decimals=1, length=50, fill='█',
                 newline=True) -> None:
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals
                                  in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    try:
        percent = ("{0:." + str(decimals) +
                   "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix),
              end='\r')
        # Print New Line on Complete
    except ZeroDivisionError:
        print("Zero division error in:", os.path.abspath(__file__),
              ":: "+progress_bar.__name__+"()")
    if iteration == total and newline:
        print()
    return None


def valid_bins(num: int) -> bool:
    """Checks valid bin amount. Returns Boolean."""
    return 2 <= num and num <= 1000
