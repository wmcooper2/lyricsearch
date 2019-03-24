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


def get_files(dir_: str) -> list:
    """Gets text files from dir_, recursively. Returns List."""
    return [file_ for file_ in Path(dir_).glob("**/*.txt")]


def make_file(file_):  # replaced make_results_file
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


def pi_search(pattern: str, spawn: bool = False) -> list:
    """Performs a search on a pi-node. Returns None."""
    if spawn:
        pass
#         spawn_workers()
    else:
        results = search(pattern)
        if DEBUG:
            pprint(results)
        return results
    return []


# def spawn_workers() -> None:
#     """Spawns worker subprocesses. Returns None."""
#     workers = []
#     lock    = Lock()
#     for d in PISEARCHDIRS:
#         workers.append(mp.Process(target=worker_search,
#             args=(d, pattern, lock)))
#     for w in workers:
#         w.start()
#     return None

def subset_match(song: set, pattern: set) -> bool:
    """Checks if pattern is subset of song. Returns Boolean. """
#     return song.issubset(pattern)
    return pattern.issubset(song)

def search(pattern: str) -> list:
    """Searches for songs containing 'pattern'. Returns List."""
    pset = set(pattern.split())
    matchcount = 0
    for db in Path(SETDIR).glob("**/*.db"):
        miniset = shelve.open(str(db))
        for key in miniset.keys():
            if subset_match(miniset[key][1], pset):
                print(key)
        miniset.close()

#         with shelve.open("set_") as miniset:
#             print(miniset["Akon_Yes"])

#                 if v[1].issubset(pattern):
#                     matchcount += 1
#                     print("Match:", matchcount)
#                 else:
#                     print("No match.")

#     if in_mega_set(pattern):
#         return song_set_search(pattern)
#     else:
#         return []


def in_mega_set(pattern: str) -> bool:
    """Checks that pattern is subset of the mega set. Returns Boolean."""
    set_ = set(pattern.split())
    mega = shelve.open(MEGA_SET)
    ans = set_.issubset(mega["megaset"])
    mega.close()
    return ans


def song_set_search(pattern: str) -> list:
    """Search for possible song matches. Returns List."""
    results = []
    songs = shelve.open(LYRICS_SET)
    set_ = set(pattern.split())
    for k, v in songs.items():  # nested dict
        for song, lyrics in v.items():
            if set_.issubset(lyrics):
                results.append(song)
    songs.close()
    return results


def exact_search(results: list) -> list:
    """Performs brute force pattern matching. Returns list."""
#     for file_ in sorted(results):
#         print(file_)
    print("exact search matches:", len(results))
    print(str(DATA_DIR+"/"+results[0]))
    return []

#          convert file_ to a path where it exists
#          try to search for an exact match in file_
#          save any errors to an error file
#          return exact match files as a list
#
#
#
#         try:
#             with open(str(file_), "r") as f:
#                 match = re.search(pattern, f.read())
#                 if match != None:
#                     results.append(str(file_)+"\n")
#         except:
#             errors.append(file_)
#    #write results
#     lock.acquire()
#     save_file = RESULTDIR+pattern+".txt"
#     make_file(save_file)
#     save(results, save_file)
#     save(errors, DEBUGERRORS)
#     lock.release()
#     return None
#
#
#
#
# def old_mac_search(lyric_dir: str, pattern: str) -> Tuple[int, int]:
#     save_file       = file_name(RESULTDIR, pattern)
#     Path(save_file).touch()
#     for file_ in lyrics:
#         try:
#             with open(file_, "r") as f:
#                 match = re.search(pattern, f.read())
#                 if match != None:
#                     results.append(str(file_)+"\n")
#                     matched += 1
#         except:
#             errors.append(file_)
#         searched += 1
#         if searched % 10000 == 0:
#             progress(str(round((searched/len(lyrics)*100), 2)))
#     save(results, save_file)
#     save(errors, DEBUGERRORS)
#     return matched, searched
#
# def cluster_search(pattern):
#     """Sends commands to nodes in cluster. Returns None."""
#     for pi in CLUSTER:
#         try:
#             command = "ssh pi@"+pi+\
#                 " 'sudo python3 clisearch.py "+pattern+"'"
# #                " 'sudo python3 lyricsearch_pi.py "+pattern+"'"
#             cmd = format_pi_cmd(pi, pattern)
#             subprocess.run([cmd]) #runs pi_search()
#         except: print("Sending command to pi",pi,"failed.")
#
# def worker_search(dir_, pattern, lock):
#     """Searches dir_ for the user-requested pattern. Returns None."""
#     errors      = deque()
#     lyrics      = deque(text_files(dir_))
#     results     = deque()
#     searched    = 0
#     total       = len(lyrics)
#     #exact_search
