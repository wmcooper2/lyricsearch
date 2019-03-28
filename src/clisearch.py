#!/usr/bin/env python3.7
"""A CLI tool for pattern matching in the lyrics text files."""
# custom
from constants import *
from pathcheck import *
from clisearchutil import *

def cli_search() -> None:
    path_check(PATHS)  # prints 
    pattern = search_pattern()  # prints
    possible_results = possible_match_search(pattern)
    exact_results = exact_match_search(possible_results, pattern)
    save_results(exact_results[0], pattern)
    print_stats(possible_results, exact_results)
    return None

if __name__ == "__main__":
    cli_search()
