#!/usr/bin/env python3.7
"""Constants module for Lyric Search program."""
# stand lib
from pathlib import Path
from pprint import pprint
import os

# custom
from personal import (
        DEBUGDIR,
        DEBUGFILE,
        LYRICSDIR,
        RESULTSDIR,
        SETSDIR,
        SOURCETEXT,
        )
# from personal import MAC_EXT_DRIVE_RESULT_DIR 
# from personal import PI_NODES
# from personal import PI_DATA_DIR
# from personal import PI_RESULT_DIR
# from personal import PI_SET_DIR
# from personal import PI5_DATA_DIR
# from personal import TEST_DIR
# from personal import WEEKLY_EXT_DRIVE




# def ps1() -> str:
#     """Returns $PS1 as a String."""
#     return os.popen("echo $PS1").read().strip()


# CLUSTER = PI_NODES
# DEBUG = True
DEBUG = False
VERBOSE = True


if DEBUG:
    DEBUGDIR = ".debug/"
    LYRICSDIR = DEBUGDIR+"lyrics/"  # 54 files
    RESULTSDIR = DEBUGDIR+"results/"
    SETSDIR = DEBUGDIR+"sets/"
    SOURCETEXT = DEBUGDIR+"sourcetext/"

NAMED_PATHS = [
    ("DEBUGDIR", DEBUGDIR),
    ("LYRICSDIR", LYRICSDIR),
    ("RESULTSDIR", RESULTSDIR),
    ("SETSDIR", SETSDIR),
    ("SOURCETEXT", SOURCETEXT)]

PATHS = [
     DEBUGDIR,
     LYRICSDIR,
     RESULTSDIR,
     SETSDIR,
     SOURCETEXT,]
