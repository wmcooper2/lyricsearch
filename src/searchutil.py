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
import sys
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


def get_files(dir_: str) -> list:
    """Gets text files from dir_, recursively. Returns List."""
    return [file_ for file_ in Path(dir_).glob("**/*.txt")]


def make_file(file_):
    """Makes file_ if it doesn't exist. Returns None."""
    if not Path(file_).exists():
        Path(file_).touch()


def text_files(dir_):
    """Makes a generator of dir_'s '.txt' files, recursively.
        Returns Generator."""
    if ismac():
        return ((yield str(f)) for f in Path(dir_).rglob("*.txt"))
    elif ispi():
        return [str(f) for f in Path(dir_).glob("*.txt")]


def make_dir(dir_):  # replaced makesavedir
    """Makes 'dir_' if it doesn't exist. Returns None."""
    if not Path(dir_).exists():
        Path(dir_).mkdir()


def format_pi_cmd(pi, pattern):
    """Formats a command for pi-node. Returns String."""
    return "ssh pi@" + \
           pi + " 'sudo python3 lyricsearch/src/lyricsearch_pi.py " + \
           pattern + "'"


def save(data: list, dest: str) -> None:
    """Appends data to dest. Returns None."""
    with open(dest, "a+") as file_:
        [file_.write(el) for el in data if el is not None]
    return None


def file_path(song: str, dict_: dict) -> str:
    """Gets the song path. Returns String."""
    return dict_[song][0]


def lyric_set(song: str, dict_: dict) -> str:
    """Gets the lyric's set. Returns Set."""
    return dict_[song][1]


def search_db(pattern: str, db: str) -> List[str]:
    """Searches db for 'pattern'. Returns List."""
    pset = set(pattern.split())
    matches = []
    with shelve.open(db) as miniset:
#         for key in miniset.keys():
#             if subset_match(lyric_set(key, miniset), pset):
#                 matches.append(key)
        for name, tuple_ in miniset.items():
            if subset_match(lyric_set(name, miniset), pset):
                matches.append(file_path(name, miniset))
    return matches


# def subset_match(song: set, pattern: set) -> bool:
def subset_match(song: Set[Any], pattern: Set[Any]) -> bool:
    """Checks if pattern is subset of song. Returns Boolean. """
    return pattern.issubset(song)
