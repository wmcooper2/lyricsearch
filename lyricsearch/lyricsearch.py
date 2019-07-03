#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# stand lib
import argparse

# custom
from dividefiles import divide_all_files
from lyricsearchutil import (
        exact_search,
        exact_search_verbose,
        get_user_input,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search through lyrics files.")
    parser.add_argument("-v", "--verbose", help="Make Verbose.", action="store_true")
    parser.add_argument("-e", "--exact", help="Perform exact search.", action="store_true")
    parser.add_argument("-b", "--bigram", help="Perform exact bigram search.", action="store_true")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--dividefiles", help="Divides files into multiple dirs.", action="store_true")
        # moving files to dir blocks
        # setting debug flag
        # making normal sets
    args = parser.parse_args()
    search_pattern = get_user_input()

    # performing exact search
    if args.verbose and args.bigram:
        exact_search_verbose(search_pattern, bigram_search=True)
    elif args.bigram:
        exact_search(search_pattern, bigram_search=True)
    elif args.verbose:
        exact_search_verbose(search_pattern)
    elif args.exact:
        # ISSUE: time stamp on results file is weird with this path in the code.
        exact_search(search_pattern)
    elif args.dividefiles:
        dividefiles.divide_all_files()
    else:
        print("Please use a flag. Try '--help' for a list of commands.")

    # flexible search
        # performing gap search
        # searching for artists
        # searching for song names
