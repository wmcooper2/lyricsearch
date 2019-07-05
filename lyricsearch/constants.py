#!/usr/bin/env python3.7
"""Constants module for Lyric Search program."""
# stand lib
from pathlib import Path
from pprint import pprint
import os

# custom
from personal import (
        ARTISTDB,
        BIGRAMSETS,
        DEBUGDIR,
        DEBUGFILE,
        LYRICSDIR,
        NOPUNCTNORMSETSDIR,
        RESULTSDIR,
        SETSDIR,
        SOURCETEXT,
        VOCABSETSDIR,
        )

# DEBUG = True
DEBUG = False

if DEBUG:
    ARTISTDB = DEBUGDIR+"artist.db"
    BIGRAMSETS = DEBUGDIR+"bigramsets/"
    LYRICSDIR = DEBUGDIR+"lyrics/"  # 54 files
    NOPUNCTNORMSETSDIR = DEBUGDIR+"nopunctnormsets/"
    RESULTSDIR = DEBUGDIR+"results/"
    SETSDIR = DEBUGDIR+"sets/"
    SOURCETEXT = DEBUGDIR+"sourcetext/"
    VOCABSETSDIR = DEBUGDIR+"vocabsets/"

# remove?
NAMEDPATHS = [
    ("ARTISTDB", ARTISTDB),
    ("DEBUGDIR", DEBUGDIR),
    ("LYRICSDIR", LYRICSDIR),
    ("NOPUNCTNORMSETSDIR", NOPUNCTNORMSETSDIR),
    ("RESULTSDIR", RESULTSDIR),
    ("SETSDIR", SETSDIR),
    ("SOURCETEXT", SOURCETEXT),
    ("VOCABSETSDIR", VOCABSETSDIR),]

PATHS = [
     ARTISTDB,
     DEBUGDIR,
     LYRICSDIR,
     NOPUNCTNORMSETSDIR,
     RESULTSDIR,
     SETSDIR,
     SOURCETEXT,
     VOCABSETSDIR,]
