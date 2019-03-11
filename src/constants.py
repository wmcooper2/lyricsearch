"""Constants module for Lyric Search program."""
# stand lib
from pathlib import Path
import os

# custom
from personal import *

ismac       = lambda: os.uname().sysname == "Darwin"
ispi        = lambda: os.uname().sysname == "Linux"

CLUSTER     = PINODES
DEBUG       = True
DEBUGERRORS = "../debug/debugerrors.txt"
RESULTDIR   = "../results/"
TRANSFERDIR = "/transfer/"
URL_FILE    = "../data/uniqueurls.txt"

if DEBUG:
    DATA_DIR    = "../testdata/"
    LYRICS_SET  = "../testdata/lyrics_test.db"
    MEGA_SET    = "../testdata/megaset_test.db"
#    SONG_DIR    = "../testdata/"
    SEARCHDIR   = TESTDIR
else:   #not debug
    DATA_DIR    = "../data/"
    LYRICS_SET  = "../data/lyrics.db" 
    MEGA_SET    = "../data/megaset.db"
    if ismac():
#        SONG_DIR    = WEEKLY_SONG_DIR
        DATA_DIR    = WEEKLY_SONG_DIR
        LYRICS_DIR  = WEEKLY_SONG_DIR+"pi1data/data1/"
    elif ispi():
#        SONG_DIR    = PISONGDIR
        DATA_DIR    = PISONGDIR

if ispi():  #regardless of debug
    PISEARCHDIRS    = [PIDATADIR+subdir for subdir in PISUBDATADIRS]
    COMBINEDRESULT  = RESULTDIR+"finalresult.txt"
