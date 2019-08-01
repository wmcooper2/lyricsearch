#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# stand lib
import argparse
from pprint import pprint
from typing import List, Text

# custom
from constants import (
        BIGRAMSETS,
        LYRICS,
        PATHS,
        RESULTS,
        VOCABRESULTS,
        VOCABSETS,
        )
from dividefiles import divide_all_files
from dividesets import divide_sets
from dividesetsutil import (
        bigram_sets,
        vocab_sets,
        )
from lyricsearchutil import (
        user_input_dirs,
        user_input_match_ratio,
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
    group = parser.add_mutually_exclusive_group()
    # search
    group.add_argument("-m", "--messages",
                        help="Search with helpful messages in terminal.",
                        action="store_true")
    group.add_argument("-e", "--exact",
                        help="Search for exact match.",
                        action="store_true")
    group.add_argument("-r", "--rank",
                        help="Performs ranked search.",
                        action="store_true")
#     group.add_argument("-l", "--listsearch",
#                         help="Performs ranked search, takes input list.",
#                         nargs=1,  # not right
#                         action="store_true")

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

    # quick checks
    group.add_argument("-p", "--pathcheck",
                       help="Print paths info",
                       action="store_true")
    args = parser.parse_args()

    # search
    if not args.bigramsets \
        and not args.vocabsets \
        and not args.dividefiles \
        and not args.pathcheck:
        pattern = user_input_pattern()
        print("Searching for: \n\t'"+pattern+"'")

        if args.messages:
            verbose_paths(PATHS)
            possible: List[Text] = rough_search(pattern,
                                                BIGRAMSETS,
                                                RESULTS,
                                                search_db_bigrams)
            rankings: List[Text] = ranking_search(pattern, possible)
            save_results(pattern, RESULTS, rankings)
        elif args.exact:
            matches: List[Text] = vocab_search(pattern, 100,
                                               VOCABSETS)
            save_results(pattern, VOCABRESULTS, matches)
            pprint(matches[:10])
        elif args.rank:
            matches: List[Text] = vocab_search(pattern, 0,
                                               VOCABSETS)
            save_results(pattern, VOCABRESULTS, matches)
            pprint(sorted(matches, key=lambda x: x[0], reverse=True)[:10])
    
    # divide files
    elif args.dividefiles:
        num_dirs = user_input_dirs()
        dividefiles.divide_all_files(LYRICS, num_dirs)

    # divide sets
    elif args.bigramsets:
        divide_sets(LYRICS, BIGRAMSETS, bigram_sets)
    elif args.vocabsets:
        divide_sets(LYRICS, VOCABSETS, vocab_sets)
    elif args.pathcheck:
        verbose_paths(PATHS)
    else:
        print("Please use a flag. Try '--help' for a list of commands.")
    print("\nFinished.")

    # flexible search
        # performing gap search
        # searching for artists
        # searching for song names
