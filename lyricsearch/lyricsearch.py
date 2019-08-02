#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# stand lib
import argparse
from pprint import pprint
from typing import List, Text

# custom
from constants import (
        BIGRAMSETS,
        DEBUG,
        LISTS,
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
from filesanddirs import (
        read_file_lines,
        collect_file_names,
        )
from searchutil import (
        fuzzy_search,
        ranking_search,
        rough_search,
        save_results,
        search_db_bigrams,
        user_input_dirs,
        user_input_match_ratio,
        user_input_pattern,
        verbose_paths,
        vocab_search,
        )
from setuputil import (
        make_artist_list,
        make_artist_song_lists,
        make_song_list,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        description="Search through lyrics files.")
    group = parser.add_mutually_exclusive_group()
    # search
    group.add_argument("-a", "--artist",
                        help="Search for artist name.",
                        action="store_true")
    group.add_argument("-e", "--exact",
                        help="Search for exact match.",
                        action="store_true")
    group.add_argument("-g", "--grammar",
                        help="Search for grammar patterns with unknown words between them.",
                        action="store_true")
    group.add_argument("-m", "--messages",
                        help="Search with helpful messages in terminal.",
                        action="store_true")
    group.add_argument("-r", "--rank",
                        help="Performs ranked search.",
                        action="store_true")
    group.add_argument("-s", "--song",
                        help="Search for song name.",
                        action="store_true")
#     group.add_argument("-l", "--listsearch",
#                         help="Performs ranked search, takes input list.",
#                         nargs=1,  # not right
#                         action="store_true")

    # preprocessing sets
    group.add_argument("-b", "--bigramsets",
                       help="Preprocesses bigram sets.",
                       action="store_true")
    group.add_argument("-f", "--dividefiles",
                       help="Divides files into multiple dirs.",
                       action="store_true")
    group.add_argument("-v", "--vocabsets",
                       help="Preprocesses vocabulary sets.",
                       action="store_true")
    group.add_argument("-x", "--setupartists",
                       help="Preprocesses artist list.",
                       action="store_true")
    group.add_argument("-y", "--setupsongs",
                       help="Preprocesses song list.",
                       action="store_true")
    group.add_argument("-z", "--setupartistsongs",
                       help="Preprocesses artists' song lists.",
                       action="store_true")

    # quick checks
    group.add_argument("-p", "--pathcheck",
                       help="Print paths info",
                       action="store_true")

    args = parser.parse_args()
    file_gen = collect_file_names(LYRICS)  # generator

    # search
    if args.artist:
        pattern = user_input_pattern()
        artists = read_file_lines(LISTS+"artistnames.txt")
        matches = fuzzy_search(pattern, artists)
        pprint(sorted(matches, key=lambda x: x[0], reverse=True)[:10])
    elif args.song:
        pattern = user_input_pattern()
        songs = read_file_lines(LISTS+"songtitles.txt")
        matches = fuzzy_search(pattern, songs)
        pprint(sorted(matches, key=lambda x: x[0], reverse=True)[:10])
    elif args.grammar:
        print("This functionality is not finished.")
        # flexible search ???
        # performing gap search
        # example:
        #   pattern = "as ... as"
        #   gap limit = 3
        #   test lyrics = "I'm as smart as the next guy."
        #   returns a match, gap < 3
        #   test lyrics = "I'm as cool and smart as the next guy."
        #   also returns a match, gap == 3
        #   test lyrics = "I'm as cool, smart, funny and rich as the next guy."
        #   doesn't return a match, gap > 3
        pass




    elif args.messages:
        pattern = user_input_pattern()
        verbose_paths(PATHS)
        possible: List[Text] = rough_search(pattern,
                                            BIGRAMSETS,
                                            RESULTS,
                                            search_db_bigrams)
        rankings: List[Text] = ranking_search(pattern, possible)
        save_results(pattern, RESULTS, rankings)
    elif args.exact:
        pattern = user_input_pattern()
        matches: List[Text] = vocab_search(pattern, 100, VOCABSETS)
        save_results(pattern, VOCABRESULTS, matches)
        pprint(matches[:10])
    elif args.rank:
        pattern = user_input_pattern()
        matches: List[Text] = vocab_search(pattern, 0, VOCABSETS)
        save_results(pattern, VOCABRESULTS, matches)
        pprint(sorted(matches, key=lambda x: x[0], reverse=True)[:10])
    
    # PREPROCESSING; these steps take a long time to complete
    elif args.dividefiles:
        num_dirs = user_input_dirs()
        dividefiles.divide_all_files(LYRICS, num_dirs)

    # make sets
    elif args.bigramsets:
        divide_sets(LYRICS, BIGRAMSETS, bigram_sets)
    elif args.vocabsets:
        divide_sets(LYRICS, VOCABSETS, vocab_sets)
    
    # make lists
    elif args.setupartists:
        make_artist_list(LISTS+"artistnames.txt", file_gen)
    elif args.setupsongs:
        make_song_list(LISTS+"songtitles.txt", file_gen)
    elif args.setupartistsongs:
        make_artist_song_lists(file_gen)

    # debugging stuff
    elif args.pathcheck:
        print("\tDEBUG ==", DEBUG)
        verbose_paths(PATHS)
    else:
        print("You need to add a flag. Try '--help' for a list of commands.")
    print("\nFinished.")

