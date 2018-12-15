#!/usr/bin/env python3
"""A GUI tool for finding an exact pattern match."""

#stand lib
import os
from pathlib import Path
import re
import subprocess as sp
from time import time
import tkinter as tk
from tkinter import ttk

#change targetdir to the data dir where the text files are kept

#        songcount = 0
#        matchcount = 0
cwd = str(Path.cwd())
#targetdir = Path("./testlyrics/")
#targetdir = Path("/mnt/usb/")
targetdir = Path("/mnt/usb/data1/")
savedir = Path(cwd+"/results")

def makesavedir():
    """Makes 'root/searchresults/'. Returns None."""
    if not savedir.exists():
        savedir.mkdir()

def makeresultsfile(savefile):
    """Makes a results file. Returns None."""
    Path(savefile).touch()
    os.chmod(savefile, 0o777)

def cli_search():
    """Searches for the user-requested pattern. Returns None."""
    songcount = 0
    matchcount = 0
    pattern = input("Enter a search pattern: ") 

    savefile = str(savedir)+"/"+pattern+".txt"
    makeresultsfile(savefile)
    resultsfile = open(savefile, "a+")

# use thread to send to nodes, use subprocess while inside the node
    for file_ in Path(targetdir).glob("**/*.txt"):
        match = None
        with open(str(file_), "r") as f:
            text = f.read()
            print("Searching...", file_)
            match = re.search(pattern, text)

        if match != None:
            resultsfile.write(str(file_)+"\n")
            matchcount += 1
            displaymatches()
        songcount += 1
        displaytotal()
    resultsfile.close()
    print("PATTERN::", pattern, " :::  MATCHES::", str(matchcount))

#print output to file
def displaymatches():
    """Writes song matches found to a file. Returns None."""
    pass

#print simplified output to terminal
def displaytotal():
    """Prints song count match totals in the terminal. Returns None."""
    pass

def ismac():
    """Checks if the machine is a mac. Returns Boolean."""
    if os.uname().sysname == "Darwin": return True
    else: return False

def ispi():
    """Checks if the machine is a pi node. Returns Boolean."""
    if os.uname().sysname == "Linux": return True
    else: return False

if __name__ == "__main__":
    if ismac():
        gui = LyricsGui()
    elif ispi():
#        cli = LyricsCli()
        makesavedir()
#        makeresultsfile()
        cli_search()
        #needs to take a string pattern and display/log results
        #load the data (dirs 1-4) paths into queues using all 4 cores. 
        #time it
    else:
        print("Machine not recognized. Quitting program.")
