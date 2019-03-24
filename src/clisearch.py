"""A CLI tool for pattern matching in the lyrics text files."""
# custom
from constants import *
from pprint import pprint
from searchutil import *
import sys
from time import time


"""Performs CLI search. Returns List."""
if ismac():
    print("Search dir:", exists(SETDIR), SETDIR)
    print("Data dir:", exists(DATADIR), DATADIR)
    pattern = str(input("Enter a search pattern: "))
    print("Searching for: " + pattern)
elif ispi():
    try:
        pattern = sys.argv[1]
    except IndexError:
        pattern = None
    if pattern is not None:
        print("Searching for: " + pattern)
    else:
        print("Give a string to search for.")
        quit()
else:
    print("Machine not recognized. Quitting program.")
    quit()

start = time()
for db in Path(SETDIR).glob("**/*.db"):
    possible_matches = search_db(pattern, str(db))
end = time()
print("Search time:", round(end - start, 2))

if possible_matches is not None:
    final_results = exact_search(possible_matches)
else:
    print([])

print("Possible matches:", len(possible_matches))
pprint(final_results)
