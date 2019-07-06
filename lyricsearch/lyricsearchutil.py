# stand lib
from pathlib import Path
from typing import List, Text


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
