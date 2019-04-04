#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# stand lib
import os
from pathlib import Path

# custom
from constants import NAMED_PATHS
from constants import PATHS
from constants import VERBOSE
from clisearchutil import exact_match_search
from clisearchutil import path_check
from clisearchutil import print_stats
from clisearchutil import save_results
from clisearchutil import search_pattern
from clisearchutil import subset_search


def cli_search() -> None:
    path_check(PATHS)

    if VERBOSE:
        print("Machine:", os.uname().sysname)
        print("Paths status;")
        for path in NAMED_PATHS:
            print("\t{0} {1:<15} {2}".format(Path(path[1]).exists(),
                  path[0], path[1]))

        pattern = search_pattern()
        print("Searching for: '" + pattern + "'. Please wait...")

        possible_results = subset_search(pattern)
        print("{0:<20} {1:>6}".format("Possible matches:",
              len(possible_results[0])))
        print("{0:<20} {1:>6}".format("Search time:",
              round(possible_results[1], 2)))

        exact_results = exact_match_search(possible_results, pattern)
        print("{0:<20} {1:>6}".format("Exact matches:",
              len(exact_results[0])))
        print("{0:<20} {1:>6}".format("Search time:",
              round(exact_results[1], 2)))
        save_results(exact_results[0], pattern)
        print("Saved results.")
        

    else:
        pattern = search_pattern()
        possible_results = subset_search(pattern)
        exact_results = exact_match_search(possible_results, pattern)
        save_results(exact_results[0], pattern)

#     print_stats(possible_results, exact_results)
    return None


if __name__ == "__main__":
    cli_search()
