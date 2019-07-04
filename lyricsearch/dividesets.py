#!/usr/bin/env python3.7
"""Divide the lyrics text files (fairly) evenly into sets."""
# stand lib
from collections import deque
from math import floor
import sys
from time import time
from typing import Callable, Deque

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
        make_bigram_set,
        make_set,
        make_no_punct_norm_set,
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


# @divide_sets_messages()  # works
@divide_sets_messages  # not tested yet
def divide_sets(bins: int, make_bigrams: bool) -> None:
    print("Counting files...")
    file_tot = count_files(LYRICSDIR)
    print("File count:", str(file_tot))

    deq = deque()
    files = 0
    sets = 1
    for file_ in get_files(LYRICSDIR):
        deq.append(file_)
        files += 1
        progress_bar(files, file_tot)

        # write to file when deque is full
        if len(deq) >= floor(file_tot/bins):
            blockname = str(block_set(sets))
            if make_bigrams:
                #change SETSDIR to BIGRAMSETSDIR
                make_bigram_set(deq, SETSDIR, blockname)
            else:
                # change SETSDIR to NOPUNCTNORMSETSDIR
                make_no_punct_norm_set(deq, SETSDIR, blockname)
#                 make_set(deq, SETSDIR, blockname)
            sets += 1
            deq = deque()

    # catch the last deque (not full)
    if make_bigrams:
        #change SETSDIR to BIGRAMSETSDIR
        make_bigram_set(deq, SETSDIR, blockname)
    else:
        # change SETSDIR to NOPUNCTNORMSETSDIR
        make_no_punct_norm_set(deq, SETSDIR, blockname)
#           make_set(deq, SETSDIR, blockname)
    return None


def make_sets() -> None:
    try:
        bins = int(input("How many lyric sets do you want to make? "))
    except ValueError:
        print("Please choose a number. Quitting...")
        quit()

    if valid_bins(bins):
        print(str(bins)+" sets will be created.")
    else:
        print("Choose between 2 and 1000 sets to make.")
        quit()

    try:
        answer = str(input("Do you want to make bigram sets? [y/n]: ")).lower()
    except ValueError:
        print("Please choose yes or no. Quitting...")
        quit()

    if answer == "y" or answer == "yes":
        make_bigrams = True
    else:
        make_bigrams = False

    divide_sets(bins, make_bigrams)
    return None


if __name__ == "__main__":
    if DEBUG:
        SETSDIR = "../"+SETSDIR
        LYRICSDIR = "../"+LYRICSDIR
    make_sets()
