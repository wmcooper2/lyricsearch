"""Constants module for Lyric Search program."""
#stand lib
from pathlib import Path

#custom
import personal

#for mac and pi
CWD                 = str(Path.cwd())
DEBUG               = True
#DEBUG               = False
DEBUGERRORS         = CWD+"/debug/debugerrors.txt"
RESULTDIR           = CWD+"/results/"
TRANSFERDIR         = CWD+"/transfer/"

#for macbook
CLUSTER             = personal.PINODES
if DEBUG:
    MACSEARCHDIR    = CWD+personal.MACTESTDIR
else:
    MACSEARCHDIR        = personal.MACDATADIR
DIVIDEDDATADIR      = personal.MACDATADIR2

#for pi-nodes
PISEARCHDIRS        = [personal.PIDATADIR+subdir for subdir 
                       in personal.PISUBDATADIRS]
COMBINEDRESULT      = RESULTDIR+"finalresult.txt"
