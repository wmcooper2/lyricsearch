#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# stand lib
import argparse

# custom
from constants import SETSDIR, NAMEDPATHS
from dividefiles import divide_all_files
from dividesets import make_sets
from lyricsearchutil import (
        exact_lyrics,
        exact_lyrics_bigram,
        exact_lyrics_verbose,
        exact_lyrics_bigram_verbose,
        get_user_input,
        verbose_paths,
        )
# from searchutil import 


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search through lyrics files.")
    parser.add_argument("-v", "--verbose", help="Make Verbose.", action="store_true")
    parser.add_argument("-e", "--exact", help="Perform exact search.", action="store_true")
    parser.add_argument("-b", "--bigram", help="Perform exact bigram search.", action="store_true")

    group = parser.add_mutually_exclusive_group()
    # moving files to dir blocks
    group.add_argument("-f", "--dividefiles", help="Divides files into multiple dirs.", action="store_true")
    # making sets
    group.add_argument("-s", "--dividesets", help="Divides sets into multiple shelve.db files.", action="store_true")
    args = parser.parse_args()
    
    if not args.dividesets:
        pattern = get_user_input()

    # search
    if args.verbose:
        verbose_paths(pattern, NAMEDPATHS)
        if args.bigram:
            exact_lyrics_bigram_verbose(pattern, SETSDIR)
        else:
            exact_lyrics_verbose(pattern, SETSDIR)
    elif args.bigram:
        exact_lyrics_bigram(pattern, SETSDIR)
    elif args.exact:
        # ISSUE: time stamp on results file is weird with this path in the code.
        exact_lyrics(pattern, SETSDIR)
    
    # divide files
    elif args.dividefiles:
        dividefiles.divide_all_files()

    # divide sets
    elif args.dividesets:
        make_sets()
    else:
        print("Please use a flag. Try '--help' for a list of commands.")
    print("Finished.")

    # flexible search
        # performing gap search
        # searching for artists
        # searching for song names
