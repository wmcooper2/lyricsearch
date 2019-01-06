"""Constants module for Lyric Search program."""
#stand lib
from pathlib import Path

#custom
import personal

#for mac and pi
CWD                 = str(Path.cwd())
RESULTDIR           = CWD+"/../results/"

#for macbook
CLUSTER             = personal.PINODES
#MACLYRICDIR         = personal.MACDATADIR
MACSEARCHDIR        = personal.MACDATADIR
MACSEARCHTESTDIR    = CWD+personal.MACTESTDIR   #for debugging

#for pi-nodes
#PINODESEARCHDIRS    = [personal.PIDATADIR+dir_ for dir_ in personal.PISEARCHDIRS]
#PISEARCHDIR         = personal.PIDATADIR
#PINODERESULTDIR     = CWD+personal.PIRESULTDIR
PISEARCHDIRS         = [personal.PIDATADIR+subdir for subdir in personal.PISUBDATADIRS]
