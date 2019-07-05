#!/usr/bin/env python3.7
"""Divide the lyrics text files (fairly) evenly into sets."""
# stand lib
from collections import deque
from math import floor
import sys
from time import time
from typing import Callable, Deque, Text

# custom
from constants import (
        BIGRAMSETS,
        DEBUG,
        LYRICSDIR,
        SETSDIR,
        )
from dividefilesutil import (
        block_set,
        progress_bar,
        valid_bins,
        )
from dividesetsutil import (
        bigram_sets,
        ensure_exists,
        )
from filesanddirs import count_files, get_files


def divide_sets_messages(*args) -> None:
    def wrap(funct):
        print("{0:<12} {1:<20}".format("Source dir:", LYRICSDIR))
        print("{0:<12} {1:<20}".format("Save dir:", SETSDIR))
        start = time()
        def wrapped_f(*args):
            funct(*args)
        return wrapped_f
        end = time()
        print("Time to make block sets:", round(end-start, 0))
    return wrap


@divide_sets_messages()
def divide_sets(set_tot: int,
                src_dir: Text,
                dest_dir: Text,
                set_funct: Callable[[Deque, Text, Text], None]) -> None:
    print("Counting files...")
    file_tot = count_files(src_dir)
    print("File count:", str(file_tot))

    deq = deque()
    files = 0
    sets = 1
    for file_ in get_files(src_dir):
        deq.append(file_)
        files += 1
        progress_bar(files, file_tot)

        if len(deq) >= floor(file_tot/set_tot):
            set_name = str(block_set(sets))
            set_funct(deq, dest_dir, set_name)
            sets += 1
            deq = deque()

    set_funct(deq, dest_dir, set_name)  # catch last one
    return None


def make_sets() -> None:
    try:
        set_tot = int(input("How many lyric sets do you want to make? "))
    except ValueError:
        print("Please choose a number. Quitting...")
        quit()

    if valid_bins(set_tot):
        print(str(set_tot)+" sets will be created.")
    else:
        print("Choose between 2 and 1000 sets to make.")
        quit()

    ensure_exists(SETSDIR)
    divide_sets(set_tot, LYRICSDIR, SETSDIR, bigram_sets)
    return None


if __name__ == "__main__":
#     if DEBUG:
#         SETSDIR = "../"+SETSDIR
#         LYRICSDIR = "../"+LYRICSDIR
    make_sets()
