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


def ensure_exists(path: Text) -> None:
    """If 'path' doesn't exist, it is created. Returns None."""
    dest = Path(path)
    if not dest.exists():
        if dest.is_dir():
            dest.mkdir()
        elif dest.is_file():
            dest.touch()
        print(dest, "created")
    return None


def filepath(song: Text, dict_: Dict[Text, Text]) -> Text:
    """Gets the song path. Returns String."""
    return dict_[song][0]


def lyricset(song: Text, dict_: Dict[Text, Text]) -> Text:
    """Gets the lyric's set. Returns Set."""
    return dict_[song][1]


def bigram_sets(songs: Deque, dest_dir: Text, name: Text) -> None:
    """Saves song sets to 'name.db' in 'song_dir'. Returns None."""
    song_count = len(songs)
    save_to = dest_dir+name+".db"
#     breakpoint()
    with shelve.open(save_to) as db:
        finished_songs = 0
        set_start = time()
        for song in songs:
            try:
                # default; lowercase, no punct, bigrams
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
        except UnicodeDecodeError:
            save_error(str(song_file))
            print("Error:", song_file)
    end = time()
    print("Time taken:", round(end-start, 2))
    return mega_set


# def make_no_punct_norm_set(songs: Deque,
#                            dest_dir: Text,
#                            name: Text) -> None:
#     """Make set entries into 'name.db'. Returns None."""
#     song_count = len(songs)
#     save_to = dest_dir+name+".db"
#     with shelve.open(save_to) as db:
#         finished_songs = 0
#         set_start = time()
#         for song in songs:
#             try:
#                 title = str(Path(song).resolve().name).strip(".txt")
#                 wordset = set(normalized(str(Path(song))))
#                 artist_song = str(Path(song).resolve())
#                 value = (artist_song, wordset)
#                 db[title] = value
#             except UnicodeDecodeError:
#                 save_error(str(song))
#             finished_songs += 1
#         set_end = time()
 

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


# def pi_set_from_dir(song_dir: Text, dest_dir: Text) -> None:
#     """Set up database with the same name as 'song_dir'. Returns None."""
#     db_name = dest_dir+str(Path(song_dir).name)+".db"
#     print("Counting files...")
#     song_count = count_files(song_dir)
#     print(song_count, "files")
#     with shelve.open(db_name) as db:
#         song_list = Path(song_dir).glob("**/*.txt")
#         finished_songs = 0
#         for song in song_list:
#             try:
#                 title = str(Path(song).resolve().name).strip(".txt")
#                 words = set(read_file(str(Path(song))))
# 
#                 # Tuple(artist_song, set)
#                 value = (str(Path(song).resolve()), words)
#                 db[title] = value
#             except UnicodeDecodeError:
#                 save_error(str(song))
#                 print("Error:", str(song))
#             finished_songs += 1
#     return None


def read_file(file_: Text) -> List[Text]:
    """Gets contents of a file. Returns list."""
    with open(file_, "r") as s:
        return list(s.read().split())


def read_file_lines(file_: Text) -> List[Text]:
    """Gets contents of a file, nested lines. Returns List."""
    ### ISSUE: What do I mean by "nested lines"?
    with open(file_, "r") as s:
        return [line.strip() for line in s.readlines()]


def normalized(file_: Text) -> List[Text]:
    """Gets contents of a file without punctuation and normalized
       (all lowercased). Returns List."""
    with open(file_, "r") as f:
        whole_file = f.read()
    tokens = word_tokenize(whole_file)
    return remove_empty_elements(tokens)


def remove_empty_elements(tokens: List[Text]) -> List[Text]:
    """Removes empty elements from list. Returns List."""
    result = []
    for token in tokens:
        new_token = no_punct_normalize(token)
        if new_token != None:
            result.append(new_token)
    return result


def no_punct_normalize(word: Text) -> Text:
    """Removes punctuation from the word. Returns String."""
    result = ''.join([char.lower() for char in word if char.isalpha()]) 
    if len(result) > 0 and result != None:
        return result 


def save_error(error: Text) -> None:
    """Saves error to debug file. Returns None."""
    with open(DEBUGFILE, "a+") as e:
        e.write(str(Path(error).resolve()))
        e.write("\n")
    return None
