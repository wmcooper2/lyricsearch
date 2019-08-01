#!/usr/bin/env python3.7
"""Utility module for Lyric Search program."""
# stand lib
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
