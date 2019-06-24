#!/usr/bin/env python3.7
# searchutil.py
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
        Deque,
        Dict,
        List,
        Set,
        Text,
        Tuple,
        )

# custom
from constants import (
        DEBUG,
        DEBUGDIR,
        RESULTSDIR,
        SETSDIR,
        VERBOSE,
        )
from dividingwork.fairlydivideutil import progress_bar
from filesanddirs import file_path


def exact_match_search(possible: Tuple[List[Text], int],
                       pattern: Text) -> Tuple[List[Text], float]:
    """Checks text files for exact matches. Returns Tuple.

        returns; (<exact matches>: list, <time taken>: int): tuple
    """
    exact_matches = []
    searched = 0
    start = time()
    for match in possible[0]:
        if exact_search(match, pattern):
            if VERBOSE and DEBUG:
                print("{0:<15} {1}".format("Exact match:",
                      Path(match).name))
            exact_matches.append(match)
        searched += 1
        progress_bar(searched, len(possible[0]), prefix="Progress:",
                     suffix="Complete:", decimals=1, length=100,
                     fill="█")
    end = time()
    return (exact_matches, end - start)


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


def save_results(results: List[Text], pattern: Text) -> None:
    """Saves to RESULTSDIR<time stamp>/pattern.txt. Returns None."""
    t = asctime().split(" ")
    try:
        file_name = [t[5], t[1], t[3], t[0], t[4]]
    except:
        file_name = "tempsave"
    save_to = RESULTSDIR + "_".join(file_name) + "_" + pattern
    save(results, save_to)
    return None


def search_db(pattern: Text, db: Text) -> List[Text]:
    """Searches db for 'pattern'. Returns List."""
    pset = set(pattern.split())
    matches = []
    if VERBOSE and DEBUG:
        print("\tSearching:", Path(db).resolve())
    with shelve.open(db) as miniset:
        for name, tuple_ in miniset.items():
            if subset_match(lyric_set(name, miniset), pset):
                matches.append(file_path(name, miniset))
    return matches


def subset_match(song: Set[Any], pattern: Set[Any]) -> bool:
    """Checks if pattern is subset of song. Returns Boolean. """
    return pattern.issubset(song)


def subset_search(pattern: Text) -> Tuple[List[Text], float]:
    """Check for subset matches. Returns Tuple.

        returns; (<possible matches>: list, <time taken>: int): tuple
    """
    possible_matches = []
    searched = 0
    start = time()
    total = 1000
    for song_set_db in Path(SETSDIR).glob("**/*.db"):
        possible_matches += search_db(pattern, str(song_set_db))
        searched += 1
        progress_bar(searched, total, prefix="Progress:",
                     suffix="Complete:", decimals=1, length=100,
                     fill="█")
        if VERBOSE and DEBUG:
            print("\tSearched:", song_set_db)
    end = time()
    return (possible_matches, end - start)
