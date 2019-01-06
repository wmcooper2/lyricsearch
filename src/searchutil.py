"""Utility module for Lyric Search program."""
#stand lib
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
    errors      = 0
    savefile    = format_file_name(RESULTDIR, pattern)
    lyrics      = list(set(text_files(lyric_dir)))
    with open(savefile, "a+") as s:
        for f in lyrics:
            try:
                with open(f, "r") as text:
                    match = re.search(pattern, text.read())
                    if match != None:
                        s.write(str(f)+"\n")
                        matched += 1
                    searched += 1
            except:
                errors += 1
            if searched % 10000 == 0:
                show_progress(str(round((searched/len(lyrics)*100), 2)))
    print("Errors:", str(errors))
    return matched, searched

def cluster_search(pattern):
    """Sends a command to the pi-cluster. Returns None."""
    for pi in CLUSTER:
        try:
#            command = "ssh pi@"+pi+\
#                " 'sudo python3 lyricsearch_pi.py "+pattern+"'"
            cmd = format_pi_cmd(pi, pattern)
            subprocess.run([cmd])
        except: print("Sending command to pi",pi,"failed.")

#def pi_search(lyric_dir, pattern):
def pi_search(pattern):
    """Searches lyric_dir for pattern. 
        Starts new subprocesses. Returns None."""
    workers = []
    lock = Lock()
    for d in PISEARCHDIRS:
        workers.append(mp.Process(target=worker_search, 
            args=(d, pattern, lock)))
    for w in workers:
        w.start()

def worker_search(dir_, pattern, lock):
    """Searches dir_ for the user-requested pattern. Returns None."""
    searched = 0
    todo = list(text_files(dir_))

    total = len(todo)
#    print("lyric file count:", str(total))

    errors   = []
    results = []
#    with open(save_file, "a+") as r:
    for file_ in sorted(todo):
        try:
            with open(str(file_), "r") as text:
                match = re.search(pattern, text.read())
                if match != None:
                    results.append(str(file_)+"\n")
                    r.write(str(file_)+"\n")
        except:
#            print("FAIL")
            #save errors for analysis
            errors.append(file_)

        searched += 1
        if searched % 1000 == 0:
            print("[{0}] {1}/{2}".format(dir_, searched, total))

    #write results
    lock.acquire()
    save_file = RESULTDIR+pattern+".txt"
    make_file(save_file)
    #doesnt work
#    with open(save_file, "a+") as s:
#        map(lambda x: s.write(x), results)
    save(errors, "../errors/debugerrors.txt")
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
#    os.chmod(file_, 0o777)
    os.chmod(file_, 0o766)

def format_pi_cmd(pi, pattern):
    """Formats a command line string for pi-node. Returns String."""
    return "ssh pi@"+pi+" 'sudo python3 lyricsearch/src/lyricsearch_pi.py "+pattern+"'"

#def testprocess(pattern):
#    cmd = "sudo python3 /home/pi/lyricsearch/remotesearch.py "+'"'+pattern+'"'
#    sp.run(["python3", "customcluster.py", cmd])

def save(list_, location):
    """Appends list_ to location. Returns None. """
    with open(location, "a+") as file_:
        [file_.write(el+"\n") for el in list_]
