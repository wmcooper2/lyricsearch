# stand lib
import os
from pathlib import Path
import sys
from typing import Text

# custom
from constants import (
        NAMED_PATHS,
        PATHS,
        RESULTSDIR,
        SETSDIR,
        )
from searchutil import (
        exact_match_search,
        save_results,
        subset_search,
        subset_search_bigrams,
        )


def exact_search(pattern: Text, bigram_search=False) -> None:
    """Performs exact match search. Returns None."""
    if bigram_search:
        possible_results = subset_search_bigrams(SETSDIR, pattern)
    else:
        possible_results = subset_search(SETSDIR, pattern)
    exact_results = exact_match_search(possible_results, pattern)
    save_results(RESULTSDIR, exact_results[0], pattern)
    return None


def exact_search_verbose(pattern: Text, bigram_search=False) -> None:
    print("Machine:", os.uname().sysname)
    print("Paths status;")
    for path in NAMED_PATHS:
        print("\t{0} {1:<15} {2}".format(Path(path[1]).exists(),
              path[0], Path(path[1]).resolve()))
    print("Searching for: \n\t'"+pattern+"'")

    if bigram_search:
        possible_results = subset_search_bigrams(SETSDIR, pattern)
    else:
        possible_results = subset_search(SETSDIR, pattern)
    print("\t{0:<20} {1:>6}".format("Possible matches:",
          len(possible_results[0])))
    print("\t{0:<20} {1:>6}".format("Search time (sec):",
          round(possible_results[1], 2)))

    exact_results = exact_match_search(possible_results, pattern)
    print("\t{0:<20} {1:>6}".format("Exact matches:",
          len(exact_results[0])))
    print("\t{0:<20} {1:>6}".format("Search time (sec):",
          round(exact_results[1], 2)))

    save_results(RESULTSDIR, exact_results[0], pattern)
    print("Finished.")


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
