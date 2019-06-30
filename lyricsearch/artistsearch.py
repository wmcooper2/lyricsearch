"""Search for artist in lyrics database."""
# stand lib
from pathlib import Path
from typing import Any, Text, Tuple


# custom
from constants import LYRICSDIR
from filesanddirs import collect_file_names, artist_song


# collect the file names.
print(Path(LYRICSDIR).resolve())
a = collect_file_names(LYRICSDIR)
b = next(a)
print(artist_song(b))

# write the sorted artist list to an sql database?
