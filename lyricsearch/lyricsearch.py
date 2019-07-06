#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# stand lib
import argparse
from pprint import pprint
from typing import List, Text

# custom
from constants import (
        SETS,
        LYRICS,
        PATHS,
        RESULTS,
        VOCABSETS,
        VOCABRESULTS,
        )
from dividefiles import divide_all_files
from dividesets import divide_sets
from dividesetsutil import (
        bigram_sets,
        vocab_sets,
        ensure_exists,
        )
from lyricsearchutil import (
        user_input_dirs,
        user_input_pattern,
        verbose_paths,
        )
from searchutil import (
        ranking_search,
        rough_search,
        save_results,
        search_db_bigrams,
        vocab_search,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        description="Search through lyrics files.")
    # search
    parser.add_argument("-m", "--messages",
                        help="Search with helpful messages in terminal.",
                        action="store_true")
    parser.add_argument("-e", "--exact",
                        help="Search for exact match.",
                        action="store_true")
    parser.add_argument("-w", "--words",
                        help="Search for vocabulary match.",
                        action="store_true")

    group = parser.add_mutually_exclusive_group()
    # preprocessing sets
    group.add_argument("-f", "--dividefiles",
                       help="Divides files into multiple dirs.",
                       action="store_true")
    group.add_argument("-b", "--bigramsets",
                       help="Makes bigram sets.",
                       action="store_true")
    group.add_argument("-v", "--vocabsets",
                       help="Makes vocabulary sets.",
                       action="store_true")
    args = parser.parse_args()

    # search
    if not args.bigramsets \
        and not args.vocabsets \
        and not args.dividefiles:
        pattern = user_input_pattern()

        if args.messages:
            verbose_paths(pattern, PATHS)
            possible: List[Text] = rough_search(pattern,
                                                SETS,
                                                RESULTS,
                                                search_db_bigrams)
            rankings: List[Text] = ranking_search(pattern, possible)
            save_results(pattern, RESULTS, rankings)
        elif args.exact:
            print("Need to work on exact search.")
        elif args.words:
            matches: List[Text] = vocab_search(pattern, VOCABSETS)
            save_results(pattern, VOCABRESULTS, matches)
#             pprint(matches[:10])
    
    # divide files
    elif args.dividefiles:
        num_dirs = user_input_dirs()
        dividefiles.divide_all_files(LYRICS, num_dirs)

    # divide sets
    elif args.bigramsets:
        divide_sets(LYRICS, SETS, bigram_sets)
    elif args.vocabsets:
        divide_sets(LYRICS, VOCABSETS, vocab_sets)
    else:
        print("Please use a flag. Try '--help' for a list of commands.")
    print("Finished.")

    # flexible search
        # performing gap search
        # searching for artists
        # searching for song names
