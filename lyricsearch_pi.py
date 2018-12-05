#!/usr/bin/env python3
"""A GUI tool for finding an exact pattern match."""

#stand lib
import os
from pathlib import Path
import re
import subprocess as sp
import time
import tkinter as tk
from tkinter import ttk

#change targetdir to the data dir where the text files are kept

class LyricsCli:
    def __init__(self):
#        self.songcount = 0
#        self.matchcount = 0
        self.cwd = str(Path.cwd())
        self.targetdir = Path("./testlyrics/")
        self.makesavedir()

    def makesavedir(self):
        """Makes 'root/searchresults/'. Returns None."""
        savedir = Path(self.cwd+"/results")
        if not savedir.exists():
            savedir.mkdir()
        self.savedir = savedir

    def cli_search(self):
        """Searches for the user-requested pattern. Returns None."""
        self.songcount = 0
        self.matchcount = 0
        pattern = self.userinput.get()

        savefile = str(self.savedir)+"/"+pattern+".txt"
        resultsfile = open(savefile, "a+")

# use thread to send to nodes, use subprocess while inside the node

        #change this for the pi
        #dont need to use glob if the queues are already setup
        for file_ in Path(self.cwd).glob("**/*.txt"):
            #change text file handler to context manager 'with'
            text = open(file_, "r").read()
            match = re.search(pattern, text)

            if match != None:
                resultsfile.write(str(file_)+"\n")
                self.matchcount += 1
                self.displaymatches()
            self.songcount += 1
            self.displaytotal()
        resultsfile.close()
        print("PATTERN::", pattern, " :::  MATCHES::", str(self.matchcount))

    #print output to file
    def displaymatches(self):
        """Writes song matches found to a file. Returns None."""
        pass

    #print simplified output to terminal
    def displaytotal(self):
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
        cli = LyricsCli()
        #needs to take a string pattern and display/log results
    else:
        print("Machine not recognized. Quitting program.")
