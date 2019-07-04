# stand lib
import os
from pathlib import Path
import sys
from typing import List, Text

# custom
from constants import (
        PATHS,
        RESULTSDIR,
        )
from searchutil import (
        exact_search,
        save_results,
        search_db,
        search_db_bigrams,
        subset_search,
        )


def exact_lyrics(pattern: Text, set_dir: Text) -> None:
    """Performs exact match search. Returns None."""
    possible_results = subset_search(set_dir, search_db, pattern)
    exact_results = exact_search(possible_results, pattern)
    save_results(RESULTSDIR, exact_results[0], pattern)
    return None


def exact_lyrics_bigram(pattern: Text, set_dir: Text) -> None:
    """Performs exact bigram search. Returns None."""
    possible_results = subset_search(set_dir, search_db_bigrams, pattern)
    exact_results = exact_search(possible_results, pattern)
    save_results(RESULTSDIR, exact_results[0], pattern)
    return None


def exact_lyrics_verbose(pattern: Text, set_dir: Text) -> None:
    possible_results = subset_search(set_dir, search_db, pattern)
    verbose_possible_results(possible_results)
    exact_results = exact_search(possible_results, pattern)
    verbose_exact_results(exact_results)
    save_results(RESULTSDIR, exact_results[0], pattern)
    return None


def exact_lyrics_bigram_verbose(pattern: Text, set_dir: Text) -> None:
    possible_results = subset_search(set_dir, search_db_bigrams, pattern)
    verbose_possible_results(possible_results)
    exact_results = exact_search(possible_results, pattern)
    verbose_exact_results(exact_results)
    save_results(RESULTSDIR, exact_results[0], pattern)
    return None


def get_user_input() -> Text:
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


def verbose_paths(pattern: Text, named: List[Text]) -> None:
    """Prints path info to terminal. Returns None"""
    print("Machine:", os.uname().sysname)
    print("Paths status;")
    for result in named:
        print("\t{0} {1:<15} {2}".format(Path(result[1]).exists(),
              result[0], Path(result[1]).resolve()))
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
