"""Search for artist in lyrics database."""
# stand lib


# custom
from constants import LYRICSDIR
# from .searchutil import collect_file_names
from filesanddirs import collect_file_names


# collect the file names.
print(Path(LYRICSDIR).resolve())
a = collect_file_names(LYRICSDIR)
print(type(a))
# print(next(a))


# split the file names into artist and song
# write the sorted artist list to a shelve.db
# same for songs
