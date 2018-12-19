"""Performs a search from a remote machine (the macbook)."""

#stand lib
import argparse as ap
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

def makesavedir(pattern):
    """Makes 'root/searchresults/'. Returns None."""
    if not Path(pattern).exists():
        Path(pattern).mkdir()

def makeresultsfile(savefile):
    """Makes a results file. Returns None."""
    Path(savefile).touch()
    os.chmod(savefile, 0o777)

def local_search(d, pattern, lock):
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
    end = time()
    timetaken = round(end - start, 6)
    print("[{0}] time taken :: {1}".format(d, timetaken))

def remote_search(pattern):
    """The main search function. Returns None."""
    dirs = [                             
        "/data1",
        "/data2",
        "/data3",
        "/data4"]
    
    workers = []
    lock = Lock()
    for d in dirs:
        workers.append(mp.Process(target=local_search, 
            args=(d, pattern, lock)))
    for w in workers:
        w.start()

parser = ap.ArgumentParser(description="Run remote search through lyrics.")
parser.add_argument("pattern", help="A search pattern string.")
args = parser.parse_args()
a = args._get_kwargs()[0][1]
remote_search(a)
