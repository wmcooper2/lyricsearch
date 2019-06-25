#!/usr/bin/env python3.7
"""Utility module for dividefiles.py"""
# stand lib
from pathlib import Path
from collections import deque
from typing import (
        Any,
        Deque,
        List,
        Text,
        )


def block_set(num: int) -> Text:
    """Formats block set name. Returns String."""
    return "blockset"+str(num)


def copy_deque_files(group: Deque, dest: Text) -> None:
    """Copies files in group to 'dest/'. Returns None."""
    for file_ in group:
        shutil.copy(file_, dest)
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
def progress_bar(iteration, total, prefix='', suffix='', decimals=1,
                 length=100, fill='█'):
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
    percent = ("{0:." + str(decimals) +
               "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix),
          end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def valid_bins(num: int) -> bool:
    """Checks valid bin amount. Returns Boolean."""
    return 2 <= num and num <= 1000
