"""Utility module for making sets of the lyrics files."""
# stand lib
from constants import *
from pathlib import Path
from setutil import *
import shelve
from time import time
from typing import Any
from typing import Deque
from pprint import pprint

# filepath = lambda song, dict_: dict_[song][0]
# lyricset = lambda song, dict_: dict_[song][1]


def filepath(song: str, dict_: dict) -> str:
    """Gets the song path. Returns String."""
    return dict_[song][0]


def lyricset(song: str, dict_: dict) -> str:
    """Gets the lyric's set. Returns Set."""
    return dict_[song][1]


def count_files(dir_: str) -> int:
    """Counts files. Returns Integer."""
    files = 0
    for f in Path(dir_).glob("**/*.txt"):
        files += 1
    return files


# mega_set        = make_mega_set(DATA_DIR)   #set object
# mega            = shelve.open(MEGA_SET)     #shelve db
# mega["megaset"] = mega_set
# mega.close()
# print("Lyrics and Mega databases created in 'data/'.")


def make_mega_set(dir_: str) -> set:
    """Make single set from '.txt' files in dir_. Returns Set."""
    mega_set = set()
    song_count = 0
    start = time()
    for song_file in Path(dir_).glob("**/*.txt"):
        try:
            lyrics = set(read_file(str(song_file)))
            for word in lyrics:
                mega_set.add(word)
            song_count += 1
            show_progress(song_count)
        except UnicodeDecodeError:
            save_error(str(song_file))
            print("Error:", song_file)
    end = time()
    print("Time taken:", round(end-start, 2))
    return mega_set


def pi_set_from_dir(song_dir: str, dest_dir: str) -> None:
    """Set up database with the same name as 'song_dir'. Returns None."""
    db_name = dest_dir+str(Path(song_dir).name)+".db"
    print("Counting files...")
    song_count = count_files(song_dir)
    print(song_count, "files")
    with shelve.open(db_name) as db:
        song_list = Path(song_dir).glob("**/*.txt")
        finished_songs = 0
        for song in song_list:
            try:
                title = str(Path(song).resolve().name).strip(".txt")
                words = set(read_file(str(Path(song))))

                # Tuple(artist_song, set)
                value = (str(Path(song).resolve()), words)
                db[title] = value
            except UnicodeDecodeError:
                save_error(str(song))
                print("Error:", str(song))
            finished_songs += 1
            progress(finished_songs, song_count, 500)


def pi_set_from_deque(song_list: Deque, dest_dir: str, name: str) -> None:
    """Saves song sets to 'name.db' in 'song_dir'. Returns None."""
    song_count = len(song_list)
    save_to = dest_dir+name+".db"
    print("save to", save_to)
    with shelve.open(save_to) as db:
        finished_songs = 0
        set_start = time()
        for song in song_list:
            try:
                title = str(Path(song).resolve().name).strip(".txt")
                words = set(read_file(str(Path(song))))

                # Tuple(artist_song, set)
                value = (str(Path(song).resolve()), words)
                db[title] = value
            except UnicodeDecodeError:
                save_error(str(song))
                print("Error:", str(song))
            print(song)
            finished_songs += 1
        set_end = time()
        print("Time to make set block:", str(round(set_end - set_start, 2)))


def progress(finished: int, total: int, step: int) -> None:
    """Prints progress to terminal. Returns None."""
    if finished % step == 0:
        print("% completed:", str(round((finished/total)*100, 2)))
    return None


def read_file(file_: str) -> list:
    """Gets contents of a file. Returns list."""
    with open(file_, "r") as s:
        return list(s.read().split())


def read_file_lines(file_: str) -> list:
    """Gets contents of a file, nested lines. Returns List."""
    with open(file_, "r") as s:
        return [line.strip() for line in s.readlines()]


def save_error(error: str) -> None:
    """Saves error to debug file. Returns None."""
    with open(DEBUGERRORS, "a+") as e:
        e.write(str(Path(error).resolve()))
        e.write("\n")
    return None


def show_progress(num: int) -> None:
    """Update user terminal. Returns None."""
    if num % 5000 == 0:
        print(str(round((num/616324)*100, 2)), "%")
    return None


def single_db() -> None:
    """Makes a single set database. Returns None."""
    with shelve.open(LYRICS_SET) as db:
        song_list = Path(DATA_DIR).glob("**/*.txt")
        for song in song_list:
            title = str(Path(song).resolve().name).strip(".txt")
            words = set(read_file(str(Path(song))))

            # Tuple(artist_song, set)
            value = (str(Path(song).resolve()), words)
            db[title] = value
