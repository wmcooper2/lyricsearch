"""Main program module."""
#custom
from clisearch import cli_search
from constants import *
from guisearch import LyricsGui
from personal import *

if __name__ == "__main__":
    if ismac():
        gui = LyricsGui()
    elif ispi():
        pattern = input("Enter a search pattern: ") 
        cli_search(SEARCHDIR, pattern)
