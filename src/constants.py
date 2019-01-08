"""Constants module for Lyric Search program."""
#stand lib
from pathlib import Path

#custom
import personal

#for mac and pi
CWD                 = str(Path.cwd())
DEBUGERRORS         = CWD+"/../debug/debugerrors.txt"
RESULTDIR           = CWD+"/../results/"
TRANSFERDIR         = CWD+"/../transfer/"

#for macbook
CLUSTER             = personal.PINODES
MACSEARCHDIR        = personal.MACDATADIR
#MACSEARCHTESTDIR    = CWD+personal.MACTESTDIR   #for debugging
DIVIDEDDATADIR      = personal.MACDATADIR2

#for pi-nodes
PISEARCHDIRS        = [personal.PIDATADIR+subdir for subdir 
                       in personal.PISUBDATADIRS]
COMBINEDRESULT      = RESULTDIR+"finalresult.txt"
