#!/usr/bin/env python3
"""Make a corpus of many files."""

#stand lib
import json
import os
import subprocess

#3rd party
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import words

def valid_word(word):
    return word in english_words

def invalid_word(word):
    return word not in english_words

if __name__ == "__main__":
    #fileids() are the names of the files; "Xzibit_The Gambler.txt"
    # basic functionality of the corpus object on page 50 of nltk book

    # pi's lyrics_dir
    lryics_dir = "/mnt/usb/"

    valid = set()
    invalid = set()

    #English word list
    english_words = words.words("en")
    print("english word count::", len(english_words)) 

    # lyrics word list 
    print("Loading corpus...")
    corpus_root = "./testlyrics_small"
    lyrics_corpus = PlaintextCorpusReader(corpus_root, ".*")

    for song in lyrics_corpus.fileids():
        print("Working... {}".format(song))
        valid_words = set(filter(valid_word, lyrics_corpus.words(song)))
        invalid_words = set(filter(invalid_word, lyrics_corpus.words(song)))

        #add valid and invalid to main ones
        valid = valid.union(valid_words)
        invalid = invalid.union(invalid_words)

    # make lowercase and double check invalid words
    if invalid_words:
        temp = set()
        [temp.add(word.lower()) for word in invalid_words]

        del invalid_words
        invalid_words = set()

        temp_valid = set(filter(valid_word, temp))
        temp_invalid = set(filter(invalid_word, temp))
        invalid_words = temp_invalid


    all_valid = valid_words.union(temp_valid)
    all_invalid = invalid_words.union(temp_invalid)

    print("valid words    ::", len(all_valid))
    print("invalid words  ::", len(all_invalid))
    print("total word set ::", str(len(all_valid) + len(all_invalid)))

    # for pi
    #hostname = subprocess.run("hostname -I").stdout()
    #valid_words_file = "./validwords.txt"

    # save the contents of both sets in text files to be loaded later.
    valid_file = "./validwords.txt"
    with open(valid_file, "w+") as file_:
        json.dump(sorted(list(all_valid)), file_, indent=4)

