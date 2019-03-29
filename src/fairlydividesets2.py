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

# get user input
try:
    bins = int(input("How many sets do you want to sort into? "))
except ValueError:
    print("Please choose a number. Quitting...")
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
        if len(deq) >= floor(file_amt/bins):
            blockname = str(block_set(setcount))
            pi_set_from_deque(deq, SET_DIR, blockname)
            print("blockname:", blockname)
            setcount += 1
            deq = deque()
    pi_set_from_deque(deq, SET_DIR, blockname)
    end = time()
    print("TIME:", end - start)
 
#     # collect paths
#     fs: Deque = deque()
#     print("Collecting files...")
#     collected = 0
#     for f in get_files(DATA_DIR):
#         fs.append(str(f.resolve()).strip())
#         collected += 1
#         progress(collected, file_amt, 100)
#     print("Finished collecting files.")
# 
#     # put paths into deques
#     print("Dividing files...")
#     groups = fairly_divide(fs, bins)
#     print("Finished dividing files.")
# else:
#     print("Please choose a number between 1 and 100.")
#     quit()
# prep_finish = time()
# 
# make "bins" number of sets
# print("Making block sets...")
# block_start = time()
# setcount = 0
# for dque in groups:
#     setcount += 1
#     blockname = str(block_set(setcount))
#     pi_set_from_deque(dque, SET_DIR, blockname)
#     progress(setcount, len(groups), 1)
# print("Sets completed.")
# block_finish = time()
# print("Preparation time:", str(round(prep_finish - prep_start, 2)))
# print("Set block time:", str(round(block_finish - block_start, 2)))
