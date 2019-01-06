"""A CLI tool for pattern matching in the lyrics text files."""
#custom
from constants import *
from searchutil import *

if __name__ == "__main__":
    total = 0   #global
    pattern = input("Enter a search pattern: ") 
    make_dir(RESULTDIR)
    if ismac():
        mac_search(MACSEARCHDIR, pattern)
    elif ispi():
        pi_search(pattern)
    else:
        print("Machine not recognized. Quitting program.")
