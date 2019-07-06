#!/usr/bin/env python3.7
"""Utility module for Lyric Search program."""
# stand lib
from collections import deque
import multiprocessing as mp
from multiprocessing import Lock
import os
from pathlib import Path
from pprint import pprint
import re
import shelve
import shutil
import subprocess
import sys
from time import asctime, time
from typing import (
        Any,
        Callable,
        Deque,
        Dict,
        List,
        Set,
        Text,
        Tuple,
        )

# 3rd party
from nltk import bigrams, word_tokenize

# custom
from dividefilesutil import progress_bar
from dividesetsutil import normalized_pattern
from filesanddirs import (
        file_path,
        count_files,
        count_db,
        get_files,
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


def exact_search(possible: Tuple[List[Text], int],
                       pattern: Text) -> Tuple[List[Text], float]:
    """Checks text files for exact matches. Returns Tuple.

        returns; (<exact matches>: list, <time taken>: int): tuple
    """
    matches = []
    searched = 0
    start = time()
    for poss in possible[0]:
        if brute_force_search(poss, pattern):
            matches.append(poss)
        searched += 1
        progress_bar(searched, len(possible[0]), prefix="Exact:")
    end = time()
    return (matches, end-start)


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

# now its the same as exact_match()
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
    total = count_db(set_dir)
    for song_db in Path(set_dir).glob("**/*.db"):
        matches += search_funct(pattern, str(song_db))
        searched += 1
        progress_bar(searched, total,
                     prefix="Subsets: "+str(len(matches)))
    return matches


def save(src: List[Text], dest: Text) -> None:
    """Appends 'src' elements to 'dest'. Returns None."""
    with open(dest, "a+") as file_:
        for line in src:
            if line is not None:
                file_.write(line + "\n")
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
#     pattern_set = set(pattern.split())
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


def vocab_search(pattern: Text, set_dir: Text) -> List[Text]:
    """Checks sets for vocab matches. Returns List."""
    pattern_set = set(normalized_pattern(pattern))
    matches = []
    searched = 0
    song_dbs = Path(set_dir).glob("**/*.db")
    for db in song_dbs:
        with shelve.open(str(db)) as miniset:
            for name, tuple_ in miniset.items():
                song = lyric_set(name, miniset)
                if pattern_set.issubset(song):
                    matches.append(file_path(name, miniset))
                searched += 1
                progress_bar(searched, 616323,
                             prefix="Vocab: "+str(len(matches)))
    return matches
