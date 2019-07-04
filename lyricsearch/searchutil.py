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
from filesanddirs import (
        file_path,
        count_files,
        count_db,
        get_files,
        )


def exact_match_search(possible: Tuple[List[Text], int],
                       pattern: Text) -> Tuple[List[Text], float]:
    """Checks text files for exact matches. Returns Tuple.

        returns; (<exact matches>: list, <time taken>: int): tuple
    """
    matches = []
    searched = 0
    start = time()
    for poss in possible[0]:
        if exact_search(poss, pattern):
            matches.append(poss)
        searched += 1
        progress_bar(searched, len(possible[0]), prefix="Exact:")
    end = time()
    return (matches, end-start)


def exact_search(target: Text, pattern: Text) -> bool:
    """Performs brute force pattern matching. Returns Boolean."""
    try:
        with open(target, "r") as f:
            match = re.search(pattern, f.read())
            if match is not None:
                return True
    except FileNotFoundError:
        print("File not found:", target)
    return False


def lyric_set(song: Text, dict_: Dict[Text, Text]) -> Set:
    """Gets the lyric's set. Returns Set."""
    return dict_[song][1]


def save(src: List[Text], dest: Text) -> None:
    """Appends 'src' elements to 'dest'. Returns None."""
    with open(dest, "a+") as file_:
        for line in src:
            if line is not None:
                file_.write(line + "\n")
    return None


def save_results(dir_: Text, results: List[Text], pattern: Text) -> None:
    """Saves to 'dir_<time stamp>/pattern.txt'. Returns None."""
    t = asctime().split(" ")
    file_name = [t[4], t[1], t[2], t[0], t[3]]
    save_to = dir_+"_".join(file_name)+"_"+pattern
    save(results, save_to)
    return None


def search_db(pattern: Text, db: Text) -> List[Text]:
    """Searches db for 'pattern'. Returns List."""
    pattern_set = set(pattern.split())
    return subset_matches(pattern_set, db)


def search_db_bigrams(pattern: Text, db: Text) -> List[Text]:
    """Searches db for 'pattern'. Returns List."""
    pattern_set = set(bigrams(word_tokenize(pattern)))
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


def subset_search(set_dir: Text,
                  search_funct: Callable[[Text, Text], List[Text]],
                  pattern: Text) -> Tuple[List[Text], float]:
    """Check for subset matches. Returns Tuple.

        - returns; (<possible matches>: list, <time taken>: float): tuple
        - displays progress bar
    """
    possible_matches = []
    searched = 0
    start = time()
    total = count_db(set_dir)
    for song_set_db in Path(set_dir).glob("**/*.db"):
        possible_matches += search_funct(pattern, str(song_set_db))
        searched += 1
        progress_bar(searched, total, prefix="Subsets:")
    end = time()
    return (possible_matches, end-start)
