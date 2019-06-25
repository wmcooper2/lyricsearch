#!/usr/bin/env python3.7
"""Divide the lyrics text files (fairly) evenly into sets."""
# stand lib
from collections import deque
from math import floor
import sys
from time import time
from typing import Deque

# custom
from constants import (
        LYRICSDIR,
        SETSDIR,
        VERBOSE,
        )
from dividefilesutil import (
        block_set,
        progress_bar,
        valid_bins,
        )
from dividesetsutil import make_set
from filesanddirs import count_files, get_files

if __name__ == "__main__":
    try:
#         bins = int(sys.argv[1])
        bins = int(input("How many lyric sets do you want to make? "))
        print("Sets", bins)
    except ValueError:
        print("Please choose a number. Quitting...")
        quit()
#     except IndexError:
#         print("Please add an argument. Quitting...")
#         quit()


    # divide the files
    prep_start = time()
    if valid_bins(bins):
        if VERBOSE:
            print("{0:<12} {1:<20}".format("Source dir:", LYRICSDIR))
            print("{0:<12} {1:<20}".format("Save dir:", SETSDIR))

            print("Counting files...")
            file_amt = count_files(LYRICSDIR)
            print("File count:", str(file_amt))

            blockname = "blank"
            deq = deque()
            file_count = 0
            setcount = 1
            start = time()
            breakpoint()
            for file_ in get_files(LYRICSDIR):
                deq.append(file_)
                file_count += 1
                progress_bar(file_count, file_amt, prefix="Progress:",
                             suffix="Complete:", decimals=1, length=100,
                             fill="█")

                # write to file, clear the deque
                if len(deq) >= floor(file_amt/bins):
                    blockname = str(block_set(setcount))
                    make_set(deq, SETSDIR, blockname)
                    setcount += 1
                    deq = deque()   # remove
                else:
                    pass

            # catch the last one
            make_set(deq, SETSDIR, blockname)
            end = time()
            print("Time to make block sets:", round(end-start, 0))

        else:
            file_amt = count_files(LYRICSDIR)
            deq = deque()
            setcount = 1
            blockname = "blank"
            start = time()
            for file_ in get_files(LYRICSDIR):
                deq.append(file_)

                # write to file, clear the deque
                if len(deq) >= floor(file_amt/bins):
                    blockname = str(block_set(setcount))
                    make_set(deq, SETSDIR, blockname)
                    setcount += 1
                    deq = deque()   # remove
                else:
                    pass

            # catch the last one
            make_set(deq, SETSDIR, blockname)
            end = time()
        print("Finished dividing sets.")
    else:
        print("Choose between 2 and 100 sets to make.")
