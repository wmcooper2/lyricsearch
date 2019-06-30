"""Search for artist in lyrics database."""
# stand lib
from pathlib import Path
from pprint import pprint
import shelve
from typing import Any, Text, Tuple


# custom
from constants import LYRICSDIR, ARTISTDB
from filesanddirs import (
        collect_file_names,
        count_files,
        make_artist_db,)


# make artist db
# prepend because not ran in "./run"
lyricsdir = "../"+LYRICSDIR
print("Making artist database...")
make_artist_db(lyricsdir, "../"+ARTISTDB)
print("Artist database created.")


# "Overtime" in a["artists"]["Akon"]
