#!/usr/bin/env python3
"""Make a corpus of many files."""

#stand lib
import subprocess
import time

#3rd party
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import words

#fileids() are the names of the files; "Xzibit_The Gambler.txt"
# basic functionality of the corpus object on page 50 of nltk book

#English word list
english = words.words("en")
print("word count ::", len(english)) 

#word sets from lyrics
validwords = set()
invalidwords = set()

# word list from lyrics
corpus_root = "./testlyrics_small"
wordlists = PlaintextCorpusReader(corpus_root, ".*")

def addtoset(song):
    """Adds words to valid or invalid sets. Returns None."""
    print("working on {}".format(song))
    lyrics = wordlists.words(song)
    for word in lyrics:
        if word in words.words():
            validwords.add(word)
        else:
            invalidwords.add(word)

start = time.time()
[addtoset(song) for song in wordlists.fileids()]

# make all words in 'english' and 'invalidwords' lowercase
invalidlower = set()
temp_set = set()
lowerenglish = set()
print("changing invalidwords to lowercase...")
[temp_set.add(word.lower()) for word in invalidwords]

# clear the old invalid set
del invalidwords
invalidwords = set()

# check that 'invalidwords' in 'english'
print("checking lower case invalid words...")
[lowerenglish.add(word.lower()) for word in english]
[validwords.add(word) for word in temp_set if word in lowerenglish]

# for pi
#hostname = subprocess.run("hostname -I").stdout()
#validwordsfile = "./validwords.txt"

# for macbook
#hostname = subprocess.run("hostname")

# save the contents of both sets in text files to be loaded later.
validwordsfile = "./validwords.txt"
with open(validwordsfile, "w+") as file_:
    for word in list(validwords):
        file_.write(word)
        file_.write("\n")

#print("host name ::", hostname)
print("time taken ::", str(time.time() - start))
print("valid words ::", len(validwords))
print("invalid words ::", len(invalidwords))
print("total word set ::", str(len(validwords) + len(invalidwords)))




