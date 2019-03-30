#!/usr/bin/env python3.7
"""Divide the lyrics text files (fairly) evenly into sets."""
# stand lib
from collections import deque
from math import floor
import sys
from time import time

# custom
from constants import *
from fairlydivideutil import *
from fairlydividesetsutil import pi_set_from_deque
from fairlydividesetsutil import progress
from typing import Deque

# visual confirmation of source and destination
print("Source dir:", DATA_DIR)
print("Save dir:", SET_DIR)

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
    print("Counting files...")
    file_amt = count_files(DATA_DIR)
    print("File count:", str(file_amt))
 
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
            print("blockname:", blockname)
            setcount += 1
            deq = deque()

    #catch the last one
    pi_set_from_deque(deq, SET_DIR, blockname)
    end = time()
    print("Time to make block sets:", end - start)
