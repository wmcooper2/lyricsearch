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

# 3rd party
from nltk import bigrams
from nltk import word_tokenize

# custom
from constants import DEBUGFILE
from filesanddirs import count_files
from filesanddirs import read_file
from dividefilesutil import valid_bins, progress_bar


def bigram_sets(songs: Deque, dest_dir: Text, name: Text) -> None:
    """Saves song sets to 'name.db' in 'song_dir'. Returns None."""
    song_count = len(songs)
    save_to = dest_dir+name+".db"
    with shelve.open(save_to) as db:
        finished_songs = 0
        set_start = time()
        for song in songs:
            try:
                # default; lowercase, no punct, bigrams, no empty element
                title = str(Path(song).resolve().name).strip(".txt")
                words = normalized(str(Path(song)))
                bi_grams = bigrams(words)  # gen obj
                bi_set = set(bi_grams)
                artist_song = str(Path(song).resolve())
                result = (artist_song, bi_set)
                db[title] = result
            except UnicodeDecodeError:
                save_error(str(song))
            except RuntimeError:  # gen error
                save_error("GEN:"+str(song))
            finished_songs += 1
        set_end = time()
    return None


def ensure_exists(path: Text) -> None:
    """If 'path' doesn't exist, it is created. Returns None."""
    dest = Path(path)
    if not dest.exists():
        if dest.is_dir():
            dest.mkdir()
        elif dest.is_file():
            dest.touch()
        else:
            print(dest, "is needed to continue. Quitting...")
            quit()
    return None


# def filepath(song: Text, dict_: Dict[Text, Text]) -> Text:
#     """Gets the song path. Returns String."""
#     return dict_[song][0]


def lyric_set(song: Text, dict_: Dict[Text, Text]) -> Text:
    """Gets the lyric's set. Returns Set."""
    return dict_[song][1]


def make_set(songs: Deque, dest_dir: Text, set_name: Text) -> None:
    """Saves song sets to 'set_name.db' in 'dest_dir'. Returns None."""
    song_count = len(songs)
    save_to = dest_dir+set_name+".db"
    with shelve.open(save_to) as db:
        finished_songs = 0
        set_start = time()
        for song in songs:
            try:
                title = str(Path(song).resolve().set_name).strip(".txt")
                words = set(read_file(str(Path(song))))

                # Tuple(artist_song, set)
                value = (str(Path(song).resolve()), words)
                db[title] = value
            except UnicodeDecodeError:
                save_error(str(song))
            finished_songs += 1
        set_end = time()


def remove_punct(word: Text) -> Text:
    """Removes punctuation from the word. Returns String."""
    result = ''.join([char.lower() for char in word if char.isalpha()]) 
    if len(result) > 0 and result != None:
        return result 


def normalized(file_: Text) -> List[Text]:
    """Gets contents of a file without punctuation and normalized
       (all lowercased). Returns List."""
    try:
        with open(file_, "r") as f:
            whole_file = f.read()
        tokens = word_tokenize(whole_file)
        return remove_empty_elements(tokens)
    except FileNotFoundError:
        return []


def normalized_pattern(pattern: Text) -> List[Text]:
    """Removes punctuation, makes lowercase, removes empty elements.
       Returns List."""
    tokens = word_tokenize(pattern)
    return remove_empty_elements(tokens)


# def read_file(file_: Text) -> List[Text]:
#     """Gets contents of a file. Returns list."""
#     with open(file_, "r") as s:
#         return list(s.read().split())
# 
# 
# def read_file_lines(file_: Text) -> List[Text]:
#     """Gets contents of a file, file lines become elements. Returns List."""
#     with open(file_, "r") as s:
#         return [line.strip() for line in s.readlines()]


def remove_empty_elements(tokens: List[Text]) -> List[Text]:
    """Removes empty elements from list. Returns List."""
    result = []
    for token in tokens:
        new_token = remove_punct(token)
        if new_token != None:
            result.append(new_token)
    return result


def save_error(error: Text) -> None:
    """Saves error to debug file. Returns None."""
    with open(DEBUGFILE, "a+") as e:
        e.write(str(Path(error).resolve()))
        e.write("\n")
    return None


def set_timer(*args) -> None:
    def wrap(funct):
        start = time()
        def wrapped_f(*args):
            funct(*args)
        return wrapped_f
        end = time()
        print("Time taken:", round(end-start, 0))
    return wrap


def user_input_sets() -> int:
    """Get amount of sets from user. Returns Integer."""
    try:
        set_tot = int(input("How many lyric sets do you want to make? "))
    except ValueError:
        print("Please choose a number. Quitting...")
        quit()
    if not valid_bins(set_tot):
        print("Choose between 2 and 1000 sets to make.")
        quit()
    return set_tot


def vocab_sets(songs: Deque, dest_dir: Text, name: Text) -> None:
    """Saves song sets to 'name.db' in 'song_dir'. Returns None."""
#     song_count = len(songs)
    save_to = dest_dir+name+".db"
    with shelve.open(save_to) as db:
#         finished_songs = 0
        set_start = time()
        for song in songs:
            try:
                # default; lowercase, no punct, no empty element
                song_path = Path(song).resolve()
                title = str(song_path.name).strip(".txt")
                word_set = set(normalized(str(song_path)))
                artist_song = str(song_path)
                result = (artist_song, word_set)
                db[title] = result
            except UnicodeDecodeError:
                save_error(str(song))
            except RuntimeError:  # gen error
                save_error("GEN:"+str(song))
#             finished_songs += 1
#             progress_bar(finished_songs, song_count, prefix="Vocab Sets:")
        set_end = time()
