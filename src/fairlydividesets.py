#!/usr/bin/env python3.7
"""Divide the lyrics text files (fairly) evenly into sets."""
# stand lib
from collections import deque
from math import floor
import sys
from time import time

# custom
from constants import DATA_DIR
from constants import SET_DIR
from constants import VERBOSE
from fairlydivideutil import block_set
from fairlydivideutil import get_files
from fairlydivideutil import progress_bar
from fairlydivideutil import valid_bins
from fairlydividesetsutil import count_files
from fairlydividesetsutil import pi_set_from_deque
from fairlydividesetsutil import progress
from typing import Deque


try:
    bins = int(sys.argv[1])
    print("bins", bins)
except ValueError:
    print("Please choose a number. Quitting...")
    quit()
except IndexError:
    print("Please add an argument. Quitting...")
    quit()


# divide the files into number of "bins"
prep_start = time()
if valid_bins(bins):
    if VERBOSE:
        print("{0:<12} {1:<20}".format("Source dir:", DATA_DIR))
        print("{0:<12} {1:<20}".format("Save dir:", SET_DIR))

        print("Counting files...")
        file_amt = count_files(DATA_DIR)
        print("File count:", str(file_amt))

        blockname = "blank"
        deq = deque()
        file_count = 0
        setcount = 1
        start = time()
        for file_ in get_files(DATA_DIR):
            deq.append(file_)
            file_count += 1
            progress_bar(file_count, file_amt, prefix="Progress:",
                         suffix="Complete:", decimals=1, length=100,
                         fill="█")

            # write to file, clear the deque
            if len(deq) >= floor(file_amt/bins):
                blockname = str(block_set(setcount))
                pi_set_from_deque(deq, SET_DIR, blockname)
                setcount += 1
#                 del deq         # remove
                deq = deque()   # remove
            else:
                pass

        # catch the last one
        pi_set_from_deque(deq, SET_DIR, blockname)
        end = time()
        print("Time to make block sets:", round(end - start, 0))

    else:
        file_amt = count_files(DATA_DIR)
        deq = deque()
        setcount = 1
        blockname = "blank"
        start = time()
        for file_ in get_files(DATA_DIR):
            deq.append(file_)

            # write to file, clear the deque
            if len(deq) >= floor(file_amt/bins):
                blockname = str(block_set(setcount))
                pi_set_from_deque(deq, SET_DIR, blockname)
                setcount += 1
                del deq         # remove
                deq = deque()   # remove
            else:
                pass

        # catch the last one
        pi_set_from_deque(deq, SET_DIR, blockname)
        end = time()
    print("Finished dividing sets.")
else:
    print("Choose between 2 and 100 sets to make.")
