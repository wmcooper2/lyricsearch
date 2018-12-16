#!/usr/bin/env python3
"""A GUI tool for finding an exact pattern match."""

#stand lib
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from multiprocessing import Lock
from multiprocessing import Pool
import os
from pathlib import Path
import re
import subprocess as sp
from time import time
import tkinter as tk
from tkinter import ttk

def ismac():
    """Checks if the machine is a mac. Returns Boolean."""
    if os.uname().sysname == "Darwin": return True
    else: return False

def ispi():
    """Checks if the machine is a pi node. Returns Boolean."""
    if os.uname().sysname == "Linux": return True
    else: return False

def makesavedir(pattern):
    """Makes 'root/searchresults/'. Returns None."""
    if not Path(pattern).exists():
        Path(pattern).mkdir()

def makeresultsfile(savefile):
    """Makes a results file. Returns None."""
    Path(savefile).touch()
    os.chmod(savefile, 0o777)

#def cli_search(targetdir, pattern):
def cli_search(list_):
    """Searches for the user-requested pattern. Returns None."""
    cwd = str(Path.cwd())
    dir_ = list_[0]
    pattern = list_[1]
    searchdir = "/mnt/usb"+dir_
    savedir = str(Path(cwd+"/results"))
    savefile = savedir+dir_+pattern+".txt"
    print("searchdir::", searchdir)
    print("savefile::", savefile)
    makesavedir(savedir)
    makeresultsfile(savefile)
    with open(savefile, "a+") as resultsfile:
        resultsfile.write("Banana")
        for file_ in Path(searchdir).glob("**/*.txt"):
#            print(file_)
            match = None
            try:
                with open(str(file_), "r") as f:
                    text = f.read()
#                    print("Searching...", file_)
                    match = re.search(pattern, text)
            except:
                print("FAIL")
            if match != None:
                resultsfile.write(str(file_)+"\n")
    return

def cli_search2(d, pattern, lock):
    """Searches for the user-requested pattern. Returns None."""
    start = time()
    searched = 0
    cwd = str(Path.cwd())
    dir_ = d
    searchdir = "/mnt/usb"+dir_
    savedir = str(Path(cwd+"/results"))
    savefile = savedir+dir_+pattern+".txt"
    makesavedir(savedir)
    makeresultsfile(savefile)

    def showcount(d):
        global total
        total += 1
        print(d, "::", total)

#    total = sum(1 for f in Path(searchdir).glob("**/*.txt"))
    total = sum(1 for f in Path(searchdir).iterdir())
#    [showcount(d) for c in Path(searchdir).iterdir()]
    with open(savefile, "a+") as resultsfile:
        for file_ in Path(searchdir).glob("**/*.txt"):
            match = None
            try:
                with open(str(file_), "r") as f:
                    text = f.read()
                    match = re.search(pattern, text)
            except:
                print("FAIL")
            if match != None:
                resultsfile.write(str(file_)+"\n")
            searched += 1
            if searched % 1000 == 0:
                print("[{0}] {1}/{2}".format(d, searched, total))
    #terminate worker?
    #join worker?
    #then get the time?
    end = time()
    timetaken = round(end - start, 6)
    print("[{0}] time taken :: {1}".format(d, timetaken))

if __name__ == "__main__":
    total = 0   #global
    if ismac():
        print("This file was made for a pi-node. Quitting...")

    elif ispi():
        start = time()
        pattern = input("Enter a search pattern: ") 
        dirs = [
            "/data1",
            "/data2",
            "/data3",
            "/data4"]
        
        workers = []
        lock = Lock()
        for d in dirs:
            workers.append(mp.Process(target=cli_search2, args=(d, pattern, lock)))
        for w in workers:
            w.start()
#        for w in workers:
#            w.terminate()
#        for w in workers:
#            print("pid      =", w.pid)
#            print("exitcode =", w.exitcode)
    else:
        print("Machine not recognized. Quitting program.")
