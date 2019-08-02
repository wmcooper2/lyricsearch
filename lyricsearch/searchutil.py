#!/usr/bin/env python3.7
"""Utility module for Lyric Search program."""
# stand lib
import difflib
from pathlib import Path
import re
import shelve
from time import asctime
from typing import (
        Callable,
        Dict,
        List,
        Set,
        Text,
        Tuple,
        )

# 3rd party
from nltk import bigrams

# custom
from dividefilesutil import progress_bar
from dividesetsutil import normalized_pattern
from filesanddirs import (
        count_sets_in_dbs,
        file_path,
        )


def fuzzy_search(pattern: Text,
                 strings: List[Text]) -> List[Tuple[float, Text]]:
    """Performs ranked search of artist names. Returns List.
        -pattern: the pattern to search for
        -strings: list of string
    """
    matcher = difflib.SequenceMatcher()
    results = []
    for thing in strings:
            matcher.set_seqs(pattern, thing)
            results.append((round(matcher.ratio(), 2)*100, thing))
    return results

def brute_force_search(target: Text, pattern: Text) -> bool:
    """Performs brute force pattern matching. Returns Boolean."""
    try:
        with open(target, "r") as f:
            match = re.search(pattern, f.read())
            if match is not None:
                return True
    except FileNotFoundError:
        print("File not found:", target)
    return False


# is this needed?
# if vocab_search() is 100, then is that enough?
def exact_search(possible: Tuple[List[Text], int],
                 pattern: Text) -> List[Text]:
    """Checks text files for exact matches. Returns List."""
    matches = []
    searched = 0
    for poss in possible[0]:
        if brute_force_search(poss, pattern):
            matches.append(poss)
        searched += 1
        progress_bar(searched, len(possible[0]),
                     prefix="Exact:"+str(len(matches)))
    return matches


def lyric_set(song: Text, dict_: Dict[Text, Text]) -> Set:
    """Gets the lyric's set. Returns Set."""
    return dict_[song][1]


# need to research more about fuzzy string matching (fuzzywuzzy)
def ranking_search(pattern: Text,
                   possible: List[Text]) -> List[Text]:
    """Checks text files for approximate matches. Returns List."""
    matches = []
    searched = 0
    for poss in possible:
        if brute_force_search(poss, pattern):
            matches.append(poss)
        searched += 1
        progress_bar(searched, len(possible),
                     prefix="Ranking: "+str(len(matches)))
    return matches


#optimize
def rough_search(pattern: Text,
                 set_dir: Text,
                 result_dir: Text,
                 search_funct: Callable[[Text, Text], List[Text]],
                 ) -> List[Text]:
    """Check for subset matches. Returns List.
        - displays progress bar
    """
    matches = []
    searched = 0
    song_tot = count_sets_in_dbs(set_dir)
    breakpoint()
    for song_db in Path(set_dir).glob("**/*.db"):
        matches += search_funct(pattern, str(song_db))
        searched += 1
        progress_bar(searched, song_tot,
                     prefix="Matches: "+str(len(matches)))
    return matches


def save(data: List[Text], dest: Text) -> None:
    """Saves sorted 'data' elements to 'dest'. Returns None."""
    with open(dest, "a+") as file_:
        for line in sorted(data):
            if line is not None:
                file_.write(str(line) + "\n")
    return None


def save_results(pattern: Text,
                 dest_dir: Text,
                 results: List[Text]) -> None:
    """Saves to 'dest_dir<time stamp>/pattern.txt'. Returns None."""
    t = asctime().split(" ")
#     file_name = [t[4], t[1], t[2], t[0], t[3]]
    file_name = [t[5], t[1], t[3], t[0], t[4]]
    save_to = dest_dir+"_".join(file_name)+"_"+pattern
    save(results, save_to)
    return None


def search_db(pattern: Text, db: Text) -> List[Text]:
    """Searches db for 'pattern'. Returns List."""
    pattern_set = set(normalized_pattern(pattern))
    return subset_matches(pattern_set, db)


def search_db_bigrams(pattern: Text, db: Text) -> List[Text]:
    """Searches db for 'pattern'. Returns List."""
    pattern_set = set(bigrams(normalized_pattern(pattern)))
    return subset_matches(pattern_set, db)


def subset_matches(pattern_set: Set, db: Text) -> List[Text]:
    """Gets 'pattern_set' matches in db. Returns List."""
    matches = []
    with shelve.open(db) as miniset:
        for name, tuple_ in miniset.items():
            song = lyric_set(name, miniset)
            if pattern_set.issubset(song):
                matches.append(file_path(name, miniset))
    return matches


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


def vocab_ratio(song_set: Set, pattern_set: Set) -> float:
    """Calculates the similarity between two sets. Returns Float."""
    matches = sum([1 for word in pattern_set if word in song_set])
    try:
        return round(matches/len(pattern_set), 2) * 100
    except ZeroDivisionError:
        return 0.00


def vocab_search(pattern: Text,
                 minimum: int, 
                 set_dir: Text) -> List[Tuple[float, Text]]:
    """Checks sets for vocab matches. Returns List of Tuples."""
    pattern_set = set(normalized_pattern(pattern))
    matches = []
    searched = 0
    song_tot = count_sets_in_dbs(set_dir)
    song_dbs = Path(set_dir).glob("**/*.db")
    for db in song_dbs:
        with shelve.open(str(db)) as miniset:
            for name, tuple_ in miniset.items():
                song_set = lyric_set(name, miniset)
#                 if pattern_set.issubset(song_set):
#                     path = file_path(name, miniset)
#                     matches.append((100.00, path,))
#                 else:
                rank = vocab_ratio(song_set, pattern_set)
                if rank >= minimum:
                    matches.append((rank, name))

                searched += 1
                progress_bar(searched, song_tot,
                             prefix="Matches: "+str(len(matches)))
    return matches


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
