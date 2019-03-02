"""Utility module for Lyric Search program."""
#stand lib
from collections import deque
import multiprocessing as mp
from multiprocessing import Lock
import os
from pathlib import Path
from pprint import pprint
import re

#custom
from constants import *

file_name    = lambda d, s: d+s+".txt"
ismac        = lambda: os.uname().sysname == "Darwin"
ispi         = lambda: os.uname().sysname == "Linux"
progress     = lambda s: print("Progress:", s, "%")
wkr_progress = lambda d, s, t: print("[{0}] {1}/{2}".format(d, s, t))

def make_file(file_): #replaced make_results_file
    """Makes file_ if it doesn't exist. Returns None."""
    if not Path(file_).exists(): Path(file_).touch()

def text_files(dir_):
    """Makes a generator of dir_'s '.txt' files, recursively. 
        Returns Generator."""
    if ismac():
        return ((yield str(f)) for f in Path(dir_).rglob("*.txt"))
    elif ispi():
        return [str(f) for f in Path(dir_).glob("*.txt")]

def make_dir(dir_): #replaced makesavedir
    """Makes 'dir_' if it doesn't exist. Returns None."""
    if not Path(dir_).exists(): Path(dir_).mkdir()

def make_file(file_): #replaced makeresultsfile
    """Makes file_. Returns None."""
    Path(file_).touch()
    os.chmod(file_, 0o777)

def format_pi_cmd(pi, pattern):
    """Formats a command for pi-node. Returns String."""
    return "ssh pi@"+\
           pi+" 'sudo python3 lyricsearch/src/lyricsearch_pi.py "+\
           pattern+"'"

def save(list_, location):
    """Appends list_ to location. Returns None."""
    with open(location, "a+") as file_:
        [file_.write(el) for el in list_ if el != None]

#main
def mac_search(lyric_dir, pattern): #factor out save()
    """Searches lyric_dir, saves results. Returns 2 Integers."""
    errors      = deque()
    lyrics      = deque(set(text_files(lyric_dir)))
    matched     = 0
    results     = deque()
    save_file   = file_name(RESULTDIR, pattern)
    searched    = 0
    for file_ in lyrics:
        try:
            with open(file_, "r") as f:
                match = re.search(pattern, f.read())
                if match != None:
                    results.append(str(file_)+"\n")
                    matched += 1
        except:
            errors.append(file_)
        searched += 1
        if searched % 10000 == 0:
            progress(str(round((searched/len(lyrics)*100), 2)))
    print("Errors:", str(len(errors)))
    print("results:", results)
    print("save file:", save_file)
    save(results, save_file)
    save(errors, DEBUGERRORS)
    return matched, searched
 
def pi_search(pattern):
    """Starts new subprocesses. Returns None."""
    workers = []
    lock = Lock()
    
    #if I use fairlydividework() here, then I dont need to have 4 dirs.
    for d in PISEARCHDIRS:
        workers.append(mp.Process(target=worker_search, 
            args=(d, pattern, lock)))
    for w in workers:
        w.start()

def cluster_search(pattern):
    """Sends commands to nodes in cluster. Returns None."""
    for pi in CLUSTER:
        try:
            command = "ssh pi@"+pi+\
                " 'sudo python3 lyricsearch_pi.py "+pattern+"'"
            cmd = format_pi_cmd(pi, pattern)
            subprocess.run([cmd]) #runs pi_search()
        except: print("Sending command to pi",pi,"failed.")

def worker_search(dir_, pattern, lock):
    """Searches dir_ for the user-requested pattern. Returns None."""
    errors      = deque()
    lyrics      = deque(text_files(dir_))
    results     = deque()
    searched    = 0
    total       = len(lyrics)
    for file_ in sorted(lyrics):
        try:
            with open(str(file_), "r") as f:
                match = re.search(pattern, f.read())
                if match != None:
                    results.append(str(file_)+"\n")
        except:
            errors.append(file_)
        searched += 1
        if searched % 1000 == 0: #update user
            wkr_progress(dir_, searched, total)

    #write results
    lock.acquire()
    save_file = RESULTDIR+pattern+".txt"
    make_file(save_file)
    save(results, save_file)
    save(errors, DEBUGERRORS)
    lock.release()
