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
        VERBOSE,
        )
from dividingwork.fairlydivideutil import progress_bar
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
#         pattern = sys.argv[1]
        pattern = input("What do you want to search for? ")
    except IndexError:
        pattern = None
    if pattern is None:
        print("Give a string to search for.")
        quit()

    path_check(PATHS)
    if VERBOSE:
        print("Machine:", os.uname().sysname)
        print("Paths status;")
        for path in NAMED_PATHS:
            print("\t{0} {1:<15} {2}".format(Path(path[1]).exists(),
                  path[0], path[1]))

        print("Searching for: '" + pattern + "'. Please wait...")

        possible_results = subset_search(pattern)
        print("{0:<20} {1:>6}".format("Possible matches:",
              len(possible_results[0])))
        print("{0:<20} {1:>6}".format("Search time (sec):",
              round(possible_results[1], 2)))

        exact_results = exact_match_search(possible_results, pattern)
        print("{0:<20} {1:>6}".format("Exact matches:",
              len(exact_results[0])))
        print("{0:<20} {1:>6}".format("Search time (sec):",
              round(exact_results[1], 2)))
        save_results(exact_results[0], pattern)
        print("Finished.")
    else:
        possible_results = subset_search(pattern)
        exact_results = exact_match_search(possible_results, pattern)
        save_results(exact_results[0], pattern)
    return None


if __name__ == "__main__":
    cli_search()
