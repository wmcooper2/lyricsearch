"""Divide the lyrics text files (fairly) evenly into sets."""
# stand lib
from collections import deque
import sys
from time import time

# custom
from constants import *
from fairlydivideutil import *
from setutil import pi_set_from_deque
from setutil import progress
from typing import Deque

# src_dir = sys.argv[1]
src_dir = DATA_DIR
print("Source dir:", src_dir)
print("Save dir:", SETDIR)

try:
    bins = int(input("How many sets do you want to sort into? "))
except ValueError:
    print("Please choose a number. Quitting...")
    quit()

start = time()
if valid_bins(bins):
    print("Counting files...")
    file_amt = count_files(src_dir)
    print("File count:", str(file_amt))

    fs: Deque = deque()
    print("Collecting files...")
    collected = 0
    for f in get_files(src_dir):
        fs.append(str(f.resolve()).strip())
        collected += 1
        progress(collected, file_amt, 100)
    print("Finished collecting files.")

    print("Dividing files...")
    groups = fairly_divide(fs, bins)
    print("Finished dividing files.")
else:
    print("Please choose a factor of 2 between 2 and 16.")
    quit()
finish = time()
print("Preparation time:", str(round(finish-start, 2)))

print("Making block sets...")
start = time()
setcount = 0
for dque in groups:
    setcount += 1
    blockname = str(block_set(setcount))
    pi_set_from_deque(dque, SETDIR, blockname)
    progress(setcount, len(groups), 1)
print("Sets completed.")
finish = time()
print("Set completion time:", str(round(finish-start, 2)))
