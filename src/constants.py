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
TRANSFERDIR = "/transfer/"
URL_FILE = "../data/uniqueurls.txt"

if DEBUG:
    DATA_DIR = "../testdata/"
    LYRICS_SET = "../testdata/lyrics_test.db"
    MEGA_SET = "../testdata/megaset_test.db"
    RESULTDIR = "../testdata/results/"
else:   # not debug
    LYRICS_SET = "../data/lyrics.db"
    MEGA_SET = "../data/megaset.db"
    if ismac():
        DATA_DIR = WEEKLYEXTERNALDRIVE
        LYRICS_DIR = MACEXTERNALDRIVE+"pi1data/data1/"
        RESULTDIR = MACEXTERNALDRIVE
    elif ispi():
        DATA_DIR = PIDATADIR
        RESULTDIR = "../results/"

if ispi():  # regardless of debug
    PISEARCHDIRS = [PIDATADIR+subdir for subdir in PISUBDATADIRS]
    COMBINEDRESULT = RESULTDIR+"finalresult.txt"
