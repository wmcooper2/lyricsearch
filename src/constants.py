#!/usr/bin/env python3.7
"""Constants module for Lyric Search program."""
# stand lib
from pathlib import Path
from pprint import pprint
import os

# custom
from personal import *

ismac = lambda: os.uname().sysname == "Darwin"
ispi = lambda: os.uname().sysname == "Linux"

CLUSTER = PI_NODES
COMBINE_DIR = "../combine/"
DEBUG = False
DEBUG_ERRORS = "../debug/debugerrors.txt"


def ps1():
    """Returns $PS1 as a String."""
    return os.popen("echo $PS1").read().strip()


if ismac():
    DATA_DIR = MAC_EXT_DRIVE  # 38,520 songs
    RESULT_DIR = MAC_EXT_DRIVE_RESULT_DIR
    SET_DIR = MAC_EXT_DRIVE_SET_DIR
elif ispi():
    DATA_DIR = PI_DATA_DIR
    RESULT_DIR = PI_RESULT_DIR
    SET_DIR = PI_SET_DIR
    if ps1() == "pi5$":
        DATA_DIR = PI5_DATA_DIR


if DEBUG:
    DATA_DIR = "../testdata/"  # 54 songs

PATHS = [COMBINE_DIR,
         DATA_DIR,
         DEBUG_ERRORS,
         RESULT_DIR,
         SET_DIR]
print("Current path setup;")
pprint(PATHS)

