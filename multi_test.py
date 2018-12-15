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
            print(file_)

#            match = None
#            try:
#                with open(str(file_), "r") as f:
#                    text = f.read()
#                    print("Searching...", file_)
#                    match = re.search(pattern, text)
#            except:
#                print("FAIL")
#            if match != None:
#                resultsfile.write(str(file_)+"\n")
##    return

#def cli_search(targetdir, pattern):
def cli_search2(d, pattern, lock):
    """Searches for the user-requested pattern. Returns None."""
    cwd = str(Path.cwd())
    dir_ = d
    searchdir = "/mnt/usb"+dir_
    savedir = str(Path(cwd+"/results"))
    savefile = savedir+dir_+pattern+".txt"
#    print("searchdir::", searchdir)
#    print("savefile::", savefile)
    makesavedir(savedir)
    makeresultsfile(savefile)
    with open(savefile, "a+") as resultsfile:
#        resultsfile.write("Banana")
        for file_ in Path(searchdir).glob("**/*.txt"):
#            lock.acquire()
#            print(file_)
#            lock.release()

            match = None
            try:
                with open(str(file_), "r") as f:
                    text = f.read()
                    lock.acquire()
                    print("Searching...", file_)
                    lock.release()
                    match = re.search(pattern, text)
            except:
                print("FAIL")
            if match != None:
                resultsfile.write(str(file_)+"\n")
##    return
if __name__ == "__main__":

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
        
#        p = ProcessPoolExecutor()
        workers = []
        lock = Lock()
        for d in dirs:
#            workers.append(p.submit(cli_search, [d, pattern]))
            workers.append(mp.Process(target=cli_search2, args=(d, pattern, lock)))
        for w in workers:
            w.start()
        for w in workers:
            w.join(3)
        for w in workers:
            print("pid      =", w.pid)
            print("exitcode =", w.exitcode)

    else:
        print("Machine not recognized. Quitting program.")
    print("PATTERN ::", pattern)
    end = time()
    print("time taken::", end-start)
