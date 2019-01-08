"""Directory and File setup for Lyric Search program."""
#stand lib
from pathlib import Path

#3rd party
import pytest

#custom
from constants import *
from searchutil import *

def test_dirs_and_files():
    assert Path(DEBUGERRORS).exists() == True
    assert Path(RESULTDIR).exists() == True
    assert Path(TRANSFERDIR).exists() == True
    assert Path(MACSEARCHDIR).exists() == True
    assert Path(DIVIDEDDATADIR).exists() == True
    assert Path(COMBINEDRESULT).exists() == True
#    assert Path().exists() == True


# lists of files
#cluster
#pisearchdirs
