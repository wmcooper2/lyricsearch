#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# stand lib
import argparse

# custom
from constants import (
        SETSDIR,
        LYRICSDIR,
        PATHS,
        RESULTSDIR,
        VOCABSETSDIR,
        )
from dividefiles import divide_all_files
from dividesets import divide_sets
from dividesetsutil import (
        bigram_sets,
        vocab_sets,
        ensure_exists,
        )
from lyricsearchutil import (
        exact_lyrics,
        exact_lyrics_bigram,
        exact_lyrics_verbose,
        exact_lyrics_bigram_verbose,
        user_input_dirs,
        user_input_pattern,
        verbose_paths,
        )
from searchutil import rough_search, search_db_bigrams


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
            possible = rough_search(pattern, SETSDIR, RESULTSDIR,
                                    search_db_bigrams)
            
#             save_results(results)

#             exact_lyrics_bigram_verbose(pattern, SETSDIR)
#             exact_lyrics_verbose(pattern, SETSDIR)
        elif args.exact:
            pass
#             exact_search(pattern, set_dir, search_funct)
#             exact_lyrics(pattern, SETSDIR) # time stamp issue
    
    # divide files
    elif args.dividefiles:
        num_dirs = user_input_dirs()
        dividefiles.divide_all_files(LYRICSDIR, num_dirs)

    # divide sets
    elif args.bigramsets:
        divide_sets(LYRICSDIR, SETSDIR, bigram_sets)
    elif args.vocabsets:
        divide_sets(LYRICSDIR, VOCABSETSDIR, vocab_sets)
    else:
        print("Please use a flag. Try '--help' for a list of commands.")
    print("Finished.")

    # flexible search
        # performing gap search
        # searching for artists
        # searching for song names
