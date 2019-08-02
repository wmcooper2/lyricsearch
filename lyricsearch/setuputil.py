# stand lib
from itertools import tee
from pprint import pprint
import shelve
from typing import (
        Any,
        Generator,
        List,
        Text,
        Tuple)

# custom
from constants import LISTS
from dividefilesutil import progress_bar
from filesanddirs import (
        collect_file_names,
        count_files,
        read_file_lines,
        )


def artist_song(path: Any) -> Tuple[Text, Text]:
    """Extracts the artist and song name from 'path'. Returns String.
        -'path' is a Path object
    """
    parent = path.parents[0]
    parts = path.parts
    file_name = path.name
    stem = path.stem
    artist = stem.split("_")[0]
    song = stem.split("_")[1]
    return artist, song


def file_name_error_check(files: Generator[Text, None, None]) -> List[Text]:
    """Check the files for parsing errors. Returns None."""
    tee1, tee2 = tee(files)
    file_total = len(list(tee1))
    file_count = 0
    results = []
    for file_ in files:
        if str(file_.name).count("_") >= 2:
#         if str(file_.name).count("\\") >= 1:
            results.append(file_)
        progress_bar(file_count, file_total, prefix="Error Checking:")
        file_count += 1
    return results


def make_artist_db(dir_: Text, database: Text) -> None:
    """Creates the 'artist.db' from files in 'dir_'. Returns None."""
    artists = {}
    file_amt = count_files(dir_)
    for path in collect_file_names(dir_):  # recursive
        artist, song = artist_song(path)
        if artist not in artists:
            artists[artist] = set()
        artists[artist].add(song)
    pprint(artists)
    print("database:", database)
    with shelve.open(database) as db:
        db["artists"] = artists


def make_artist_list(file_name: Text,
                     files: Generator[Text, None, None]) -> None:
    """Makes a complete list of artist names. Returns None.
        -prints progress bar to terminal
        -saves artist names to 'file_name'
    """
    tee1, tee2 = tee(files)
    file_count = 0
    file_total = len(list(tee2))
    artists = set()
    for file_ in tee1:
        artists.add(file_.name.split("_")[0])
        file_count += 1
        progress_bar(file_count, file_total, prefix="Collecting Artists:")

    with open(file_name, "w+") as f:
        for artist in sorted(list(artists)):
            f.write(artist+"\n")
    return None


def make_song_list(file_name: Text,
                   files: Generator[Text, None, None]) -> None:
    """Makes a complete list of artist names. Returns None."""
    tee1, tee2 = tee(files)
    file_count = 0
    file_total = len(list(tee2))
    songs = set()
    for file_ in tee1:
        songs.add(file_.name.split("_")[1])
        file_count += 1
        progress_bar(file_count, file_total, prefix="Collecting Songs:")

    with open(file_name, "w+") as f:
        for song in sorted(list(songs)):
            f.write(song+"\n")
    return None


def make_artist_song_lists(files: Generator[Text, None, None]) -> None:
    """Makes a single file for each artist with only that artist's songs.
        Returns None.
        -makes a file for each artist in 'artistsonglists' directory
        -prints artist count to terminal
        -prints progress bar to terminal
        """
    filenames = list(files)

    # for artistname in set of artist names
    artists = read_file_lines(LISTS+"artistnames.txt")
    print("\tArtist count:", len(artists))
    songs = read_file_lines(LISTS+"songtitles.txt")
    print("\tSong count:", len(songs))

    artist_count = 0
    artist_total = len(artists)
    for artist in artists:
        artistsongs = []
        artistfile = LISTS+"artistsonglists/"+artist+".txt"
        for filename in filenames:
            if artist in str(filename):
                artistsongs.append(str(filename).rstrip(".txt"))
        with open(artistfile, "w+") as f:
            for name in artistsongs:
                f.write(name.split("_")[1]+"\n")
        artist_count += 1
        progress_bar(artist_count, artist_total,
                     prefix="Collecting artists' songs:")
    return None


def make_statistics_file() -> None:
    """Collects simple statistics about the lyrics dataset. Returns None."""
    pass
