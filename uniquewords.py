#!/usr/bin/env python3
"""Makes a set of unique words from all the text files in the target dir."""

#stand lib
from glob import glob
from pathlib import Path
from time import time

targetdir   = "testdata/"
uniquewords = set()
totallines  = 0
totalwords  = 0

def countlines():
    global totallines
    for p in Path(targetdir).glob("**/*.txt"):
        with open(p, "r") as f:
            text = f.readlines()
        totallines += sum(1 for line in text)
    print("lines ::", totallines)

def countwords():
    global totalwords
    for p in Path(targetdir).glob("**/*.txt"):
        with open(p, "r") as f:
            text = f.readlines()
        for line in text:
            totalwords += sum(1 for word in line.split())
    print("words ::", totalwords)

def wordset():
    global uniquewords
    for p in Path(targetdir).glob("**/*.txt"):
        with open(p, "r") as f:
            text = f.readlines()
        for line in text:
            words = line.split()
            for el in words:
                uniquewords.add(el)
    print("unique words ::", len(uniquewords))


if __name__ == "__main__":
    start = time()
    countlines()
    countwords()
    wordset()
    end = time()
    print("time taken ::", end-start)
