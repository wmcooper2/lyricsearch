#!/usr/bin/env python3.7
"""Utility module for making sets of the lyrics files."""
# stand lib
from pathlib import Path
from pprint import pprint
import shelve
from time import time
from typing import (
        Any,
        Deque,
        Dict,
        List,
        Text,
        )

# custom
from constants import DEBUGFILE
from filesanddirs import count_files


def filepath(song: Text, dict_: Dict[Text, Text]) -> Text:
    """Gets the song path. Returns String."""
    return dict_[song][0]


def lyricset(song: Text, dict_: Dict[Text, Text]) -> Text:
    """Gets the lyric's set. Returns Set."""
    return dict_[song][1]



def make_mega_set(dir_: Text) -> set:
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
#             show_progress(song_count)
        except UnicodeDecodeError:
            save_error(str(song_file))
            print("Error:", song_file)
    end = time()
    print("Time taken:", round(end-start, 2))
    return mega_set


def pi_set_from_dir(song_dir: Text, dest_dir: Text) -> None:
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
#             progress(finished_songs, song_count, 500)


def make_set(song_list: Deque, dest_dir: Text, name: Text) -> None:
    """Saves song sets to 'name.db' in 'song_dir'. Returns None."""
    song_count = len(song_list)
    save_to = dest_dir+name+".db"
#     breakpoint()
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
            finished_songs += 1
        set_end = time()


# def progress(finished: int, total: int, step: int) -> None:
#     """Prints progress to terminal. Returns None."""
#     if finished % step == 0:
#         print("% completed:", str(round((finished/total)*100, 2)))
#     return None


def read_file(file_: Text) -> List[Text]:
    """Gets contents of a file. Returns list."""
    with open(file_, "r") as s:
        return list(s.read().split())


def read_file_lines(file_: Text) -> List[Text]:
    """Gets contents of a file, nested lines. Returns List."""
    with open(file_, "r") as s:
        return [line.strip() for line in s.readlines()]


def save_error(error: Text) -> None:
    """Saves error to debug file. Returns None."""
    with open(DEBUGFILE, "a+") as e:
        e.write(str(Path(error).resolve()))
        e.write("\n")
    return None


# def show_progress(num: int) -> None:
#     """Update user terminal. Returns None."""
#     if num % 5000 == 0:
#         print(str(round((num/616324)*100, 2)), "%")
#     return None
