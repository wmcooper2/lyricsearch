#/usr/bin/env python3.7
"""Divide the lyrics text files (fairly) evenly into sets."""
# stand lib
from collections import deque
from math import floor
import sys
from typing import Callable, Deque, Text

# custom
from dividefilesutil import (
        block_set,
        progress_bar,
        )
from dividesetsutil import user_input_sets, set_timer
from filesanddirs import count_files, get_files


@set_timer()
def divide_sets(src_dir: Text,
                dest_dir: Text,
                set_funct: Callable[[Deque, Text, Text], None]) -> None:
    """Divide the sets into smaller, more manageable blocks. Returns None.
        -asks for user input
        -displays;
            -src and dest
            -file count
            -progress bar
    """
    print("{0:<12} {1:<20}".format("Source dir:", src_dir))
    print("{0:<12} {1:<20}".format("Dest dir:", dest_dir))
    print("Counting files...")
    file_tot = count_files(src_dir)
    print("File count:", str(file_tot))

    set_tot = user_input_sets()
    deq = deque()
    files = 0
    sets = 1
    for file_ in get_files(src_dir):
        deq.append(file_)
        files += 1
        if len(deq) >= floor(file_tot/set_tot):
            set_name = str(block_set(sets))
            set_funct(deq, dest_dir, set_name)
            progress_bar(sets, set_tot, prefix="Making sets:")
            sets += 1
            deq = deque()

    set_funct(deq, dest_dir, set_name)  # catch last one
    return None
