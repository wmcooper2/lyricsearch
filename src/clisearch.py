#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# custom
from constants import *
from pathcheck import *
from pprint import pprint
from clisearchutil import *
import sys
from time import time
from time import asctime

# path check
if paths_okay(PATHS):
    print("Files and directories check complete.")
else:
    pprint(missing(PATHS))
    raise Exception("Error: Missing paths. Quitting...")
    quit()

# decides which machine is running, gets search pattern
if ismac():
    pattern = str(input("Enter a search pattern: "))
    print("Searching for: '" + pattern + "'. Please wait...")
elif ispi():
    try:
        pattern = sys.argv[1]
    except IndexError:
        pattern = None
    if pattern is not None:
        print("Searching for: " + pattern)
    else:
        print("Give a string to search for.")
        quit()
else:
    print("Machine not recognized. Quitting program.")
    quit()

# check the sets for possible matches
set_start = time()
possible_matches = []
for song_set_db in Path(SET_DIR).glob("**/*.db"):
    possible_matches += search_db(pattern, str(song_set_db))
set_end = time()

# check the text files for exact matches
try:
    exact_matches = []
    exact_start = time()
    for match in possible_matches:
        if exact_search(match, pattern):
            exact_matches.append(match)
    exact_end = time()
    
    # stats
    print("Possible match example:", possible_matches[0])
    print("Possible matches:", len(possible_matches))
    print("Set-Search time:", round(set_end - set_start, 2))
    print("Exact match example:", exact_matches[0])
    print("Exact matches:", len(exact_matches))
    print("Exact-Search time:", round(exact_end - exact_start, 2))

    # save results
    t = asctime().split(" ")
    file_name = [t[4], t[1], t[2], t[3], t[0]]
    save_to = RESULT_DIR + pattern + "_" + "_".join(file_name)
    save(exact_matches, save_to)

except IndexError:
    print("No matches.")
