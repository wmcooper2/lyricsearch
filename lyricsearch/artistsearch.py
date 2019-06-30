"""Search for artist in lyrics database."""
# stand lib
from pathlib import Path
from pprint import pprint
import shelve
from typing import Any, Text, Tuple


# custom
from constants import LYRICSDIR
from filesanddirs import collect_file_names, artist_song, count_files


# make artist db
lyricsdir = "../"+LYRICSDIR
print("Making artist database...")
make_artist_db(lyricsdir, ARTIST_DB)


# "Overtime" in a["artists"]["Akon"]
