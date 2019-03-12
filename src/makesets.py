"""Make a set of words from each song. Stored using shelve module."""
#stand lib
from constants import *
from pathlib import Path
import shelve
from time import time

def read_file_lines(file_: str) -> list:
    """Gets contents of a file, nested lines. Returns List."""
    with open(file_, "r") as s:
        return [line.strip() for line in s.readlines()]

def read_file(file_: str) -> list:
    """Gets contents of a file. Returns list."""
    with open(file_, "r") as s:
        return list(s.read().split())

def show_progress(num: int) -> None:
    """Update user terminal. Returns None."""
    if num % 5000 == 0:
        print(str(round((num/616324)*100, 2)), "%")

def count_files(dir_: str) -> int:
    return sum(1 for f in Path(dir_).glob("**/*.txt"))

def save_error(error: str) -> None:
    """Saves error to debug file. Returns None."""
    with open(DEBUGERRORS, "a+") as e:
        e.write(str(Path(error).resolve()))
        e.write("\n")

def make_song_set(dir_: str) -> dict:
    """Makes song sets of all text files in dir_. Returns Dict."""
    song_count  = 0
    song_sets   = {}
    start       = time()
    for song_file in Path(dir_).glob("**/*.txt"):
        try:
            key             = str(song_file.name).strip(".txt")
            lyrics          = set(read_file(str(song_file)))
            song_sets[key]  = lyrics
            song_count += 1
            show_progress(song_count)
        except:
            save_error(str(song_file))
            print("Error:", song_file)
    end = time()
    print("Time taken:", round(end-start, 2))
    return song_sets

def make_mega_set(dir_: str) -> set:
    """Make single large song set from .txt files in dir_. Returns Set."""
    mega_set    = set()
    song_count  = 0
    start       = time()
    for song_file in Path(dir_).glob("**/*.txt"):
        try:
            lyrics = set(read_file(str(song_file)))
            for word in lyrics:
                mega_set.add(word)
            song_count += 1
            show_progress(song_count)
        except:
            save_error(str(song_file))
            print("Error:", song_file)
    end = time()
    print("Time taken:", round(end-start, 2))
    return mega_set

def setup_sets() -> None:
    """Setup the mega and song sets. Returns None."""
    song_set        = make_song_set(DATA_DIR)   #set objects in dict
    songs           = shelve.open(LYRICS_SET)   #shelve database
    songs["songset"]= song_set
    songs.close()

    mega_set        = make_mega_set(DATA_DIR)   #set object
    mega            = shelve.open(MEGA_SET)     #shelve db
    mega["megaset"] = mega_set
    mega.close()

if __name__ == "__main__":
    setup_sets()
    print("Lyrics and Mega databases created in 'data/'.")
