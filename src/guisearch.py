"""A GUI tool for pattern matching in the lyrics text files."""
# stand lib
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import ttk

# custom
from constants import *
from searchutil import *


class LyricsGui:
    def __init__(self):
        self.debug = DEBUG
        self.matchcount = 0
        self.songcount = 0
        self.win = tk.Tk()
        self.win.title("Lyrics Search")

        self.frame = ttk.LabelFrame(self.win,
                                    text="Enter search sentence.")
        self.frame.grid(column=0, row=0)

        self.userinput = ttk.Entry(self.frame, width=39)
        self.userinput.grid(column=0, row=0, columnspan=4)

        self.searchbutton = ttk.Button(self.frame,
                                       text="Search", command=self.search)
        self.searchbutton.grid(column=0, row=1, sticky=tk.W)

        self.quitbutton = ttk.Button(self.frame,
                                     text="Quit", command=self._quit)
        self.quitbutton.grid(column=1, row=1, sticky=tk.W)

        self.displaytotal()
        self.displaymatches()
        self.userinput.focus()
        self.win.mainloop()

    def _quit(self):
        """Quits the program. Returns None."""
        self.win.quit()
        self.win.destroy()

    def search(self):
        """Searches for the user-requested pattern. Returns None."""
        self.songcount = 0
        self.matchcount = 0
        self.totaldisplay.grid_forget()
        self.matchdisplay.grid_forget()
        pattern = self.userinput.get()

        if self.debug:
            self.results = mac_search(pattern)
        else:
            pi_search(pattern)
        self.matchdisplay.grid_forget()
        self.totaldisplay.grid_forget()
        self.displaymatches()
        self.displaytotal()
        self.userinput.focus()

    def displaymatches(self):
        """Displays the file matches found in the gui. Returns None."""
        self.matchdisplay = ttk.Label(self.frame,
                                      text="Matches: " +
                                      str(self.matchcount))
        self.matchdisplay.grid(column=2, row=1, sticky=tk.E)

    def displaytotal(self):
        """Displays the searched song count in the gui. Returns None."""
        self.totaldisplay = ttk.Label(self.frame,
                                      text="Searched: " +
                                      str(self.songcount))
        self.totaldisplay.grid(column=3, row=1, sticky=tk.E)


if __name__ == "__main__":
    if ismac():
        gui = LyricsGui()
    else:
        print("This script is setup for the macbook. Quitting...")
