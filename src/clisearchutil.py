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
from time import asctime
from time import time
from typing import Any
from typing import Deque
from typing import List
from typing import Set
from typing import Text
from typing import Tuple

# custom
from constants import *

add_suffix = lambda x: x+".txt"
file_name = lambda d, s: d+s+".txt"
progress = lambda s: print("Progress:", s, "%")
wkr_progress = lambda d, s, t: print("[{0}] {1}/{2}".format(d, s, t))


def count_files(dir_: str) -> int:
    """Counts the files that end in '.txt' in 'path_'. Returns Integer."""
    return sum([1 for x in Path(dir_).glob("**/*.txt")])


def exact_match_search(possible: Tuple[List[str], int], 
                       pattern: str) -> Tuple[List[str], int]:
    """Checks text files for exact matches. Returns Tuple.
    
        returns; (<exact matches>: list, <time taken>: int): tuple
    """
    exact_matches = []
    start = time()
    for match in possible[0]:
        if exact_search(match, pattern):
            exact_matches.append(match)
    end = time()
    return (exact_matches, end - start)


def exact_search(target: str, pattern: str) -> bool:
    """Performs brute force pattern matching. Returns Boolean."""
    try:
        with open(target, "r") as f:
            match = re.search(pattern, f.read())
            if match is not None:
                return True
    except FileNotFoundError:
        print("File not found:", target)
    return False


def exists(path: str) -> bool:
    """Checks if path exists. Returns Boolean."""
    return Path(path).exists()


def file_path(song: str, dict_: dict) -> str:
    """Gets the song path. Returns String."""
    return dict_[song][0]


# def format_pi_cmd(pi, pattern):
#     """Formats a command for pi-node. Returns String."""
#     return "ssh pi@" + \
#            pi + " 'sudo python3 lyricsearch/src/lyricsearch_pi.py " + \
#            pattern + "'"


def get_files(dir_: str) -> list:
    """Gets text files from dir_, recursively. Returns List."""
    return [file_ for file_ in Path(dir_).glob("**/*.txt")]


def lyric_set(song: str, dict_: dict) -> set:
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


def missing(paths: List[str]) -> List[Tuple[str, bool]]:
    """Returns List of missing paths."""
    temp = []
    for path in paths:
        temp.append((path, Path(path).exists()))
    return temp


def path_check(paths: List[str]) -> None:
    """Performs an 'existence' check for the needed paths. Returns None."""
    if paths_okay(paths):
        print("Files and directories check complete.")
    else:
        pprint(missing(paths))
        raise Exception("Error: Missing paths. Quitting...")
        quit()


def paths_okay(paths: List[str]) -> bool:
    """Checks that all paths exist. Returns Boolean."""
    return all(Path(path).exists for path in paths)
            

def possible_match_search(pattern: str) -> Tuple[List[str], int]:
    """check the sets for possible matches. Returns Tuple.
    
        returns; (<possible matches>: list, <time taken>: int): tuple
    """
    start = time()
    possible_matches = []
    for song_set_db in Path(SET_DIR).glob("**/*.db"):
        possible_matches += search_db(pattern, str(song_set_db))
    end = time()
    return (possible_matches, end - start)


def print_stats(possible: Tuple[List[str], int], 
                exact: Tuple[List[str], int]) -> None:
    """Prints stats to screen. Returns None."""
    try:
        print("Possible match example:", possible[0][0])
        print("Possible matches:", len(possible[0]))
        print("Set-Search time:", round(possible[1], 2))
    except IndexError:
        print("No possible matches")
    try:
        print("Exact match example:", exact[0][0])
        print("Exact matches:", len(exact[0]))
        print("Exact-Search time:", round(exact[1], 2))
    except IndexError:
        print("No exact matches")
    return None


def save(src: List[str], dest: str) -> None:
    """Appends 'src' elements to 'dest'. Returns None."""
    with open(dest, "a+") as file_:
        for line in src:
            if line is not None:
                file_.write(line + "\n")
    return None


def save_results(results: List[str], pattern: str) -> None:
    """Saves to RESULT_DIR/<time stamp>/pattern.txt. Returns None."""
    t = asctime().split(" ")
    file_name = [t[4], t[1], t[2], t[3], t[0]]
    save_to = RESULT_DIR + "_".join(file_name) + "_" + pattern
    save(results, save_to)
    return None


def search_db(pattern: str, db: str) -> List[str]:
    """Searches db for 'pattern'. Returns List."""
    pset = set(pattern.split())
    matches = []
    with shelve.open(db) as miniset:
        for name, tuple_ in miniset.items():
            if subset_match(lyric_set(name, miniset), pset):
                matches.append(file_path(name, miniset))
    return matches


def search_pattern() -> str:
    """decides which machine is running, gets search pattern."""
    if ismac():
        pattern = str(input("Enter a search pattern: "))
        print("Searching for: '" + pattern + "'. Please wait...")
    elif ispi():
        try:
            pattern = sys.argv[1]
        except IndexError:
            pattern = None
        if pattern is not None:
            print("Searching for: " + pattern)
        else:
            print("Give a string to search for.")
            quit()
    else:
        print("Machine not recognized. Quitting program.")
        quit()
    return pattern


def subset_match(song: Set[Any], pattern: Set[Any]) -> bool:
    """Checks if pattern is subset of song. Returns Boolean. """
    return pattern.issubset(song)


def text_files(dir_):
    """Returns generator of dir_'s '.txt' files, recursive."""
#     if ismac():
#     return ((yield str(f)) for f in Path(dir_).rglob("*.txt"))
    return ((yield str(f)) for f in Path(dir_).glob("**/*.txt"))
#     elif ispi():
#         return ((yield str(f)) for f in Path(dir_).glob("*.txt"))




def start_processes(processes: List[str]) -> List[Any]:
    """Starts subprocesses. Returns List of workers."""
    a = subprocess.run(processes[0], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    b = subprocess.run(processes[1], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    c = subprocess.run(processes[2], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    d = subprocess.run(processes[3], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    workers = [a]

    workers = [a,b,c,d]
    for w in workers:
        print(w)
    print(a.strip())
    return workers


def pi_cmd(pi: str, pattern: str) -> str:
    """Formats search command for the pi. Returns String."""
    return "ssh pi@" + pi + \
           " \"sudo python3.7 lyricsearch/src/clisearch.py " + \
           "'" + pattern + "'" + "\""
#     return "ssh pi@" + pi + " 'sudo echo $PS1'"
#     return "ssh pi@" + pi + " hostname"
#     print(os.popen("echo $PS1").read().strip())

# TEST_CLUSTER = ["192.168.1.33"]
# TEST_CLUSTER = ["192.168.1.11"]
def cluster_commands(pattern: str) -> List[str]:
    """Formats commands for the cluster. Returns List."""
    commands = []
    for pi in CLUSTER:
#     for pi in TEST_CLUSTER:
        commands.append(pi_cmd(pi, pattern))
    return commands
