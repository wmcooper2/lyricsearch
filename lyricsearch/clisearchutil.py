#!/usr/bin/env python3.7
# clisearchutil.py
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
        List,
        Set,
        Text,
        Tuple,
        )

# custom
# from constants import CLUSTER
from constants import (
        DEBUG,
        DEBUGDIR,
        RESULTSDIR,
        SETSDIR,
        VERBOSE,
        )
from fairlydivideutil import progress_bar


def cluster_commands(pattern: Text) -> List[Text]:
    """Formats commands for the cluster. Returns List."""
    commands = []
    for pi in CLUSTER:
        commands.append(pi_cmd(pi, pattern))
    return commands


def count_files(dir_: Text) -> int:
    """Counts files ending in '.txt'. Returns Integer."""
    return sum([1 for x in Path(dir_).glob("**/*.txt")])


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


def exists(path: Text) -> bool:
    """Checks if path exists. Returns Boolean."""
    return Path(path).exists()


def file_name(dir_: Text, string: Text) -> Text:
    return dir_+string+".txt"


def file_path(song: Text, dict_: dict) -> Text:
    """Gets the song path. Returns String."""
    return dict_[song][0]


def get_files(dir_: Text) -> List[Text]:
    """Gets text files from dir_, recursively. Returns List."""
    return [file_ for file_ in Path(dir_).glob("**/*.txt")]


def lyric_set(song: Text, dict_: dict) -> set:
    """Gets the lyric's set. Returns Set."""
    return dict_[song][1]


def make_dir(dir_):
    """Makes 'dir_' if it doesn't exist. Returns None."""
    if not Path(dir_).exists():
        Path(dir_).mkdir()


def make_file(file_):
    """Makes file_ if it doesn't exist. Returns None."""
    if not Path(file_).exists():
        Path(file_).touch()


def missing(paths: List[Tuple[Text, Text]]) -> List[Tuple[Text, bool]]:
    """Returns List of missing paths."""
    temp = []
    for path in paths:
        temp.append((path[1], Path(path[1]).exists()))
    return temp


def path_check(paths: List[Tuple[Text, Text]]) -> None:
    """Performs 'existence' check. Returns None."""
    if paths_okay(paths):
        print("Files and directories check complete.")
    else:
        pprint(missing(paths))
        raise Exception("Error: Missing paths. Quitting...")
        quit()


def paths_okay(paths: List[Tuple[Text, Text]]) -> bool:
    """Checks that all paths exist. Returns Boolean."""
    return all(Path(path[1]).exists for path in paths)


def pi_cmd(pi: Text, pattern: Text) -> Text:
    """Formats search command for the pi. Returns String."""
    return "ssh pi@" + pi + \
           " \"sudo python3.7 lyricsearch/src/main.py " + \
           "'" + pattern + "'" + "\""
#     return "ssh pi@" + pi + " hostname"
#     print(os.popen("echo $PS1").read().strip())


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


def start_processes(processes: List[Text]) -> List[Any]:
    """Starts subprocesses. Returns List of workers."""
    a = subprocess.run(processes[0], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    b = subprocess.run(processes[1], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    c = subprocess.run(processes[2], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    d = subprocess.run(processes[3], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    return [a, b, c, d]


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
    total = 100
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


def text_files(dir_):
    """Returns generator of dir_'s '.txt' files, recursive."""
    return ((yield str(f)) for f in Path(dir_).glob("**/*.txt"))
