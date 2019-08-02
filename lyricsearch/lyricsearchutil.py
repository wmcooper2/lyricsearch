# stand lib
from pathlib import Path
from typing import List, Text


def user_input_dirs() -> int:
    """Gets dir amount from user. Returns Integer.
        -gets user input from terminal
        -prints to terminal
    """
    try:
        ans = int(input("How many dirs do you want to divide among? "))
    except ValueError:
        print("Please choose a number. Quitting...")
        quit()
    return ans


def user_input_match_ratio() -> int:
    """Gets minimum vocabualry match ratio from user. Returns Integer.
        -gets user input from terminal
        -prints to terminal
    """
    try:
        ans = int(input("Choose a minimum match percentage [0-100]: "))
        if ans >= 0 and ans <=100:
            return ans
        else:
            print("Please choose a number between 0 and 100.")
            quit()
    except ValueError:
        print("Please choose a number. Quitting...")
        quit()


def user_input_pattern() -> Text:
    """Gets search pattern from user. Returns String.
        -gets user input from terminal
        -prints to terminal
    """
    try:
        pattern = input("What do you want to search for? ")
        if len(pattern) is 0:
            print("Give a string to search for.")
            quit()
    except:
        print("Unknown error getting user input. Naked exception.")
        quit()
    print("Searching for: \n\t'"+pattern+"'")
    return pattern


# def verbose_paths(pattern: Text, paths: List[Text]) -> None:
def verbose_paths(paths: List[Text]) -> None:
    """Prints path info to terminal. Returns None"""
    print("Paths status;")
    for name in paths:
        print("\t{0} {1:<15}".format(Path(name).exists(),
              name))
    return None


def verbose_exact_results(results: List[Text]) -> None:
    """Prints match and search time in terminal. Returns None."""
    print("\t{0:<20} {1:>6}".format("Exact matches:",
          len(results[0])))
    print("\t{0:<20} {1:>6}".format("Search time (sec):",
          round(results[1], 2)))
    return None


def verbose_possible_results(possible: List[Text]) -> None:
    """Prints match and search time in terminal. Returns None."""
    print("\t{0:<20} {1:>6}".format("Possible matches:",
          len(possible[0])))
    print("\t{0:<20} {1:>6}".format("Search time (sec):",
          round(possible[1], 2)))
    return None
