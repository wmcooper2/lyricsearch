#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# stand lib
import os
from pathlib import Path
import sys

# custom
from constants import (
        NAMED_PATHS,
        PATHS,
        RESULTSDIR,
        SETSDIR,
        VERBOSE,
        )
from dividingwork.dividefilesutil import progress_bar
from filesanddirs import (
        path_check,
        )
from searchutil import (
        exact_match_search,
        save_results,
        subset_search,
        )


def cli_search() -> None:
    try:
        pattern = input("What do you want to search for? ")
    except:
        print("Unknown error getting user input. Naked exception.")
    if len(pattern) is 0:
        print("Give a string to search for.")
        quit()

    if VERBOSE:
        print("Machine:", os.uname().sysname)
        print("Paths status;")
        for path in NAMED_PATHS:
            print("\t{0} {1:<15} {2}".format(Path(path[1]).exists(),
                  path[0], Path(path[1]).resolve()))

#         path_check(PATHS)
        print("Searching for: '" + pattern + "'. Please wait...")

        possible_results = subset_search(SETSDIR, pattern)
        print("{0:<20} {1:>6}".format("Possible matches:",
              len(possible_results[0])))
        print("{0:<20} {1:>6}".format("Search time (sec):",
              round(possible_results[1], 2)))

        exact_results = exact_match_search(possible_results, pattern)
        print("{0:<20} {1:>6}".format("Exact matches:",
              len(exact_results[0])))
        print("{0:<20} {1:>6}".format("Search time (sec):",
              round(exact_results[1], 2)))
        save_results(RESULTSDIR, exact_results[0], pattern)
        print("Finished.")
    else:
        possible_results = subset_search(SETSDIR, pattern)
        exact_results = exact_match_search(possible_results, pattern)
        save_results(RESULTSDIR, exact_results[0], pattern)
    return None


if __name__ == "__main__":
    cli_search()
