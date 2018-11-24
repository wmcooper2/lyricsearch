#!/usr/bin/env python3
"""A GUI tool for finding an exact pattern match."""

#stand lib
from pathlib import Path
import re
import time
import tkinter as tk
from tkinter import ttk

class LyricsGui:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Lyrics Search")
        self.songcount = 0
        self.matchcount = 0
        self.cwd = str(Path.cwd())
        self.targetdir = Path("./testlyrics/")

        self.frame = ttk.LabelFrame(self.win, 
            text="What do you want to search for?")
        self.frame.grid(column=0, row=0)

        self.userinput = ttk.Entry(self.frame, width=39)
        self.userinput.grid(column=0, row=0, columnspan=4)

        self.searchbutton = ttk.Button(self.frame, 
            text="Search", command=self._search)
        self.searchbutton.grid(column=0, row=1, sticky=tk.W)

        self.quitbutton = ttk.Button(self.frame, 
            text="Quit", command=self._quit)
        self.quitbutton.grid(column=1, row=1, sticky=tk.W)

        self.makesavedir()
        self.displaytotal()
        self.displaymatches()
        self.userinput.focus()
        self.win.mainloop()

    def _quit(self):
        """Quits the program. Returns None."""
        self.win.quit()
        self.win.destroy()

    def makesavedir(self):
        """Makes 'root/searchresults/'. Returns None."""
        savedir = Path(self.cwd+"/results")
        if not savedir.exists():
            savedir.mkdir()
        self.savedir = savedir

    def _search(self):
        """Searches for the user-requested pattern. Returns None."""
        self.songcount = 0
        self.matchcount = 0
        self.totaldisplay.grid_forget()
        self.matchdisplay.grid_forget()
        pattern = self.userinput.get()

        self.userinput.focus()
        savefile = str(self.savedir)+"/"+pattern+".txt"
        resultsfile = open(savefile, "a+")

        for file_ in Path(self.cwd).glob("**/*.txt"):
            text = open(file_, "r").read()
            match = re.search(pattern, text)

            if match != None:
                resultsfile.write(str(file_)+"\n")
                self.matchcount += 1
                self.matchdisplay.grid_forget()
                self.displaymatches()
            self.songcount += 1
            self.totaldisplay.grid_forget()
            self.displaytotal()
        resultsfile.close()
        print("PATTERN::", pattern, " :::  MATCHES::", str(self.matchcount))

    def _threadedsearch(self):
        """Sends string pattern to different module to perform a thread
            based search. Returns None."""
        pattern = self.userinput.get()
        subprocess.run(["threadedsearch.py", pattern])

    def displaymatches(self):
        """Displays the file matches found in the gui. Returns None."""
        self.matchdisplay = ttk.Label(self.frame, 
            text="Matches: "+str(self.matchcount))
        self.matchdisplay.grid(column=2, row=1, sticky=tk.E)

    def displaytotal(self):
        """Displays the searched song count in the gui. Returns None."""
        self.totaldisplay = ttk.Label(self.frame, 
            text="Searched: "+str(self.songcount))
        self.totaldisplay.grid(column=3, row=1, sticky=tk.E)
gui = LyricsGui()