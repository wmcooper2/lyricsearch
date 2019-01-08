"""Utility module for Lyric Search program."""
#stand lib
from collections import deque
import multiprocessing as mp
from multiprocessing import Lock
import os
from pathlib import Path
import re

#custom
from constants import *

def ismac():
    """Checks if the machine is a mac. Returns Boolean."""
    if os.uname().sysname == "Darwin": return True
    else: return False

def ispi():
    """Checks if the machine is a pi node. Returns Boolean."""
    if os.uname().sysname == "Linux": return True
    else: return False

def show_progress(string):
    """Writes progress message to terminal. Returns None."""
    print("Progress:", string, "%")

def mac_search(lyric_dir, pattern):
    """Searches lyric_dir for pattern. Returns 2 Integers."""
    matched     = 0
    searched    = 0
    save_file    = format_file_name(RESULTDIR, pattern)
    lyrics      = deque(set(text_files(lyric_dir)))
    print("len lyrics:",len(lyrics))
    errors      = deque()
    results     = deque()
    for f in lyrics:
        try:
            with open(f, "r") as text:
                match = re.search(pattern, text.read())
                if match != None:
                    results.append(str(f)+"\n")
                    matched += 1
        except:
            errors.append(f)
        searched += 1
        if searched % 10000 == 0:
            show_progress(str(round((searched/len(lyrics)*100), 2)))
    print("Errors:", str(len(errors)))
    save(results, save_file)
    save(errors, DEBUGERRORS)
    return matched, searched

def cluster_search(pattern):
    """Sends a command to the pi-cluster. Returns None."""
    for pi in CLUSTER:
        try:
            #This is the point where a valid command need to be sent to
            # each node. The command should run a version of 
            # pi_search(pattern)

            command = "ssh pi@"+pi+\
                " 'sudo python3 lyricsearch_pi.py "+pattern+"'"
            cmd = format_pi_cmd(pi, pattern)
            subprocess.run([cmd])
        except: print("Sending command to pi",pi,"failed.")

def pi_search(pattern):
    """Searches lyric_dir for pattern. 
        Starts new subprocesses. Returns None."""
    workers = []
    lock = Lock()
    
    #if I use fairlydividework() here, then I dont need to have 4 dirs.
    for d in PISEARCHDIRS:
        workers.append(mp.Process(target=worker_search, 
            args=(d, pattern, lock)))
    for w in workers:
        w.start()

def worker_search(dir_, pattern, lock):
    """Searches dir_ for the user-requested pattern. Returns None."""
    #need to run on the cluster before removing comments
    searched    = 0
#    lyrics      = list(text_files(dir_))
    lyrics      = deque(text_files(dir_))
    total       = len(lyrics)
#    errors      = []
#    results     = []
    errors      = deque()
    results     = deque()
    for f in sorted(lyrics):
        try:
            with open(str(f), "r") as text:
                match = re.search(pattern, text.read())
                if match != None:
                    results.append(str(f)+"\n")
        except:
            errors.append(f)
        #update user
        searched += 1
        if searched % 1000 == 0:
            show_progress(str(round((searched/len(lyrics)*100), 2)))
            print("[{0}] {1}/{2}".format(dir_, searched, total))
    #write results
    lock.acquire()
    save_file = RESULTDIR+pattern+".txt"
    make_file(save_file)
    save(results, save_file)
    save(errors, DEBUGERRORS)
    lock.release()

#replaced make_results_file()
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

def format_file_name(dir_, string):
    """Formats file save name. Returns String."""
    return dir_+string+".txt"

#replaced makesavedir
def make_dir(dir_):
    """Makes 'dir_' if it doesn't exist. Returns None."""
    if not Path(dir_).exists(): Path(dir_).mkdir()

#replaced makeresultsfile
def make_file(file_):
    """Makes file_. Returns None."""
    Path(file_).touch()
    os.chmod(file_, 0o777)

def format_pi_cmd(pi, pattern):
    """Formats a command line string for pi-node. Returns String."""
    return "ssh pi@"+pi+" 'sudo python3 lyricsearch/src/lyricsearch_pi.py "+pattern+"'"
#    return "ssh pi@"+pi+" 'sudo python3 lyricsearch/src/searchutil.py "+pattern+"'"

def save(list_, location):
    """Appends list_ to location. Returns None. """
    with open(location, "a+") as file_:
        [file_.write(el+"\n") for el in list_]
