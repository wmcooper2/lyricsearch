# stand lib
import os
from pathlib import Path
import sys
from typing import List, Text

# custom
from constants import RESULTSDIR
from searchutil import (
        exact_search,
        save_results,
        search_db,
        search_db_bigrams,
        rough_search,
        )


def exact_lyrics(pattern: Text, set_dir: Text) -> None:
    """Performs exact match search. Returns None."""
    possible_results = rough_search(set_dir, search_db, pattern)
    exact_results = exact_search(possible_results, pattern)
    save_results(RESULTSDIR, exact_results[0], pattern)
    return None


def exact_lyrics_bigram(pattern: Text, set_dir: Text) -> None:
    """Performs exact bigram search. Returns None."""
    possible_results = rough_search(set_dir, search_db_bigrams, pattern)
    exact_results = exact_search(possible_results, pattern)
    save_results(RESULTSDIR, exact_results[0], pattern)
    return None


def exact_lyrics_verbose(pattern: Text, set_dir: Text) -> None:
    possible_results = rough_search(set_dir, search_db, pattern)
    verbose_possible_results(possible_results)
    exact_results = exact_search(possible_results, pattern)
    verbose_exact_results(exact_results)
    save_results(RESULTSDIR, exact_results[0], pattern)
    return None


def exact_lyrics_bigram_verbose(pattern: Text, set_dir: Text) -> None:
    possible_results = rough_search(set_dir, search_db_bigrams, pattern)
    verbose_possible_results(possible_results)
    exact_results = exact_search(possible_results, pattern)
    verbose_exact_results(exact_results)
    save_results(RESULTSDIR, exact_results[0], pattern)
    return None


# def rough_search(pattern:Text,
#                  set_dir: Text,
#                  results_dir: Text,
#                  search_funct: Callable[[]]) -> None:
#     """Performs a rough search of the sets. Returns None."""
#     possible_results = rough_search(set_dir, search_db_bigrams, pattern)
#     # just skip to rough_search()

#     exact_results = exact_search(possible_results, pattern)
#     save_results(results_dir, exact_results[0], pattern)
#     return None


def user_input_dirs() -> int:
    """Gets dir amount from user. Returns Integer."""
    try:
        bins = int(input("How many dirs do you want to divide among? "))
    except ValueError:
        print("Please choose a number. Quitting...")
        quit()
    return bins


def user_input_pattern() -> Text:
    """Gets search pattern from user. Returns String."""
    try:
        pattern = input("What do you want to search for? ")
        if len(pattern) is 0:
            print("Give a string to search for.")
            quit()
    except:
        print("Unknown error getting user input. Naked exception.")
        quit()
    return pattern


def verbose_paths(pattern: Text, paths: List[Text]) -> None:
    """Prints path info to terminal. Returns None"""
    print("Paths status;")
    for name in paths:
        print("\t{0} {1:<15}".format(Path(name).exists(),
              name))
    print("Searching for: \n\t'"+pattern+"'")
    return None


def verbose_exact_results(results: List[Text]) -> None:
    print("\t{0:<20} {1:>6}".format("Exact matches:",
          len(results[0])))
    print("\t{0:<20} {1:>6}".format("Search time (sec):",
          round(results[1], 2)))
    return None


def verbose_possible_results(possible: List[Text]) -> None:
    print("\t{0:<20} {1:>6}".format("Possible matches:",
          len(possible[0])))
    print("\t{0:<20} {1:>6}".format("Search time (sec):",
          round(possible[1], 2)))
    return None
