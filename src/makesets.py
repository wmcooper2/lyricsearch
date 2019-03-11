"""Make a set of words from each song. Stored using shelve module."""
#stand lib
from constants import *
from pathlib import Path
import shelve
from time import time

def file_lines(file_):
    """Gets a file's lines. Returns List."""
    lines = []
    with open(file_, "r") as s:
        for line in s.readlines():
            lines.append(line.strip())
    return lines

def make_set(list_):
    """Makes a set of words. Returns Set."""
    song_set = set()
    for line in list_:
        for word in line.split():
            song_set.add(word)
    return song_set

def show_progress(num: int) -> None:
    """Update user terminal. Returns None."""
    if num % 100 == 0:
        print(str(round((num/616324)*100, 2)), "%")

def count_files(dir_: str) -> int:
    return sum(1 for f in Path(dir_).glob("**/*.txt"))

def make_song_set(dir_: str) -> dict:
    """Makes song sets of all text files in dir_. Returns Dict."""
    song_count  = 0
    song_sets   = {}
    start       = time()
    for song_file in Path(dir_).glob("**/*.txt"):
        try:
            key             = str(song_file.name).strip(".txt")
            lyrics          = file_lines(song_file)
            song_set        = make_set(lyrics)
            song_sets[key]  = song_set

            song_count += 1
            show_progress(song_count)
        except:
            #need to save errors to debug
            print("Error:", song_file)
    end = time()
    print("Time taken:", round(end-start, 2))
    return song_sets

def make_mega_set(dir_: str) -> set:
    """Make single large song set from .txt files in dir_. Returns Set."""
    song_count  = 0
    mega_set    = set()
    start       = time()
    for song_file in Path(dir_).glob("**/*.txt"):
        try:
            lyrics          = file_lines(song_file)
            song_set        = make_set(lyrics)
            for word in song_set:
                mega_set.add(word)

            song_count += 1
            show_progress(song_count)
        except:
            #need to save errors to debug
            print("Error:", song_file)
    end = time()
    print("Time taken:", round(end-start, 2))
    return mega_set

def setup_sets(dir_: str, songdb: str, megadb: str) -> None:
    """Setup the mega and song sets. Returns None."""
    song_set        = make_song_set(dir_)
    songs           = shelve.open(songdb)
    songs["songset"]= song_set
    songs.close()

    mega_set        = make_mega_set(dir_)
    mega            = shelve.open(megadb)
    mega["megaset"] = mega_set
    mega.close()

if __name__ == "__main__":
    setup_sets(SONG_DIR, LYRICS_SET, MEGA_SET)
    print("Lyrics and Mega databases created in 'data/'.")
