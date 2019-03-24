"""Constants module for Lyric Search program."""
# stand lib
from pathlib import Path
import os

# custom
from personal import *

ismac = lambda: os.uname().sysname == "Darwin"
ispi = lambda: os.uname().sysname == "Linux"

CLUSTER = PINODES
DEBUG = False
DEBUGERRORS = "../debug/debugerrors.txt"
RESULTDIR = "../results/"
SETDIR = "../setdir/"
TRANSFERDIR = "/transfer/"
URL_FILE = "../data/uniqueurls.txt"

if DEBUG:
    DATADIR = "../testdata/"
    LYRICS_SET = "../testdata/lyrics_test.db"
    MEGA_SET = "../testdata/megaset_test.db"
else:
    LYRICS_SET = "../data/lyrics.db"
    MEGA_SET = "../data/megaset.db"
    if ismac():
#         DATADIR = WEEKLYEXTERNALDRIVE  # changed for mac testing
        DATADIR = "/Volumes/PI1/"
        LYRICS_DIR = MACEXTERNALDRIVE+"pi1data/data1/"
        RESULTDIR = MACEXTERNALDRIVE
    elif ispi():
        DATADIR = PIDATADIR

# regardless of debug
if ispi():
    PISEARCHDIRS = [PIDATADIR+subdir for subdir in PISUBDATADIRS]
    COMBINEDRESULT = RESULTDIR+"finalresult.txt"
