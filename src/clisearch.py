"""A CLI tool for pattern matching in the lyrics text files."""
#custom
from constants import *
from pprint import pprint
from searchutil import *
import sys
from time import time

def cli_search() -> list:
    """Performs CLI search. Returns List."""
    if ismac():
        print("ismac")
        pattern = str(input("Enter a search pattern: "))
        print("Searching for: "+pattern)
        start = time()
        results = mac_search(pattern)
    elif ispi():
        try:
            pattern = sys.argv[1]
        except:
            pattern = None
        if pattern != None:
            print("Searching for: "+pattern)
            start = time()
            results = pi_search(pattern)
        else:
            print("Give a string to search for.")
    else: 
        print("Machine not recognized. Quitting program.")

    if results != None:
        return exact_search(results)    
    else:
        return results
    end = time()
    print("Time taken: ", round(end-start, 2))

if __name__ == "__main__":
    pprint(cli_search())
