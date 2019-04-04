#!/usr/bin/env python3.7
"""Constants module for Lyric Search program."""
# stand lib
from pathlib import Path
from pprint import pprint
import os

# custom
from personal import *


def ismac() -> bool:
    return os.uname().sysname == "Darwin"


def ispi() -> bool:
    return os.uname().sysname == "Linux"


def ps1() -> str:
    """Returns $PS1 as a String."""
    return os.popen("echo $PS1").read().strip()


CLUSTER = PI_NODES
COMBINE_DIR = "../combine/"
DEBUG = False
DEBUG_ERRORS = "../debug/debugerrors.txt"
VERBOSE = True

if ismac():
    DATA_DIR = MAC_EXT_DRIVE_DATA_DIR  # 616,323 files
    RESULT_DIR = MAC_EXT_DRIVE_RESULT_DIR
    SET_DIR = MAC_EXT_DRIVE_SET_DIR
elif ispi():
    DATA_DIR = PI_DATA_DIR
    RESULT_DIR = PI_RESULT_DIR
    SET_DIR = PI_SET_DIR
    if ps1() == "pi5$":
        DATA_DIR = PI5_DATA_DIR

if DEBUG:
    DATA_DIR = "../testdata/"  # 54 files

NAMED_PATHS = [
        ("COMBINE_DIR", COMBINE_DIR),
        ("DATA_DIR", DATA_DIR),
        ("DEBUG_ERRORS", DEBUG_ERRORS),
        ("RESULT_DIR", RESULT_DIR),
        ("SET_DIR", SET_DIR)]

PATHS = [COMBINE_DIR,
         DATA_DIR,
         DEBUG_ERRORS,
         RESULT_DIR,
         SET_DIR]
