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
        NOPUNCTNORMSETS,
        RESULTSDIR,
        SETSDIR,
        SOURCETEXT,
        )

# DEBUG = True
DEBUG = False

if DEBUG:
    ARTISTDB = DEBUGDIR+"artist.db"
    LYRICSDIR = DEBUGDIR+"lyrics/"  # 54 files
    RESULTSDIR = DEBUGDIR+"results/"
    SETSDIR = DEBUGDIR+"sets/"
    SOURCETEXT = DEBUGDIR+"sourcetext/"
    BIGRAMSETS = DEBUGDIR+"bigramsets/"
    NOPUNCTNORMSETS = DEBUGDIR+"nopunctnormsets/"

NAMED_PATHS = [
    ("ARTISTDB", ARTISTDB),
    ("DEBUGDIR", DEBUGDIR),
    ("LYRICSDIR", LYRICSDIR),
    ("NOPUNCTNORMSETS", NOPUNCTNORMSETS),
    ("RESULTSDIR", RESULTSDIR),
    ("SETSDIR", SETSDIR),
    ("SOURCETEXT", SOURCETEXT)]

PATHS = [
     ARTISTDB,
     DEBUGDIR,
     LYRICSDIR,
     NOPUNCTNORMSETS,
     RESULTSDIR,
     SETSDIR,
     SOURCETEXT,]
