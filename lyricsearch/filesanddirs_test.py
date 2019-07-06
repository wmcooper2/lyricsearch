"""Test module for filesanddirs.py"""
import filesanddirs as fd
from pathlib import Path
import os

from constants import DEBUGDIR

LYRICS = DEBUGDIR+"lyrics/"
SETS = DEBUGDIR+"sets/"
PATHS = [("1", DEBUGDIR), ("2", LYRICS), ("3", SETS),]
NONPATHS = [("1", "cheese/"), ("2", "cats/"), ("3", "artifacts/"),]
FAKEPATHS = [("notneeded", "somepath/"),]
DIR_ = "mydir/"
STRING = "string"
SONG = "I like to eat"
DICT_ = {"I like to eat": ("its/here/boss.txt", "apples and bananas")}
 
def test_block_dir_0():
    assert fd.block_dir(0) == "block0"

def test_block_dir_1():
    assert fd.block_dir(1) == "block1"

def test_count_files():
    assert fd.count_files(LYRICS) == 54

def test_count_db():
    assert fd.count_db(SETS) > 0

def test_file_name():
    assert fd.file_name(DIR_, STRING) == "mydir/string.txt"

def test_file_path():
    assert fd.file_path(SONG, DICT_) == "its/here/boss.txt"

def test_get_dbs():
    assert len(list(fd.get_dbs(SETS))) == 2

def test_get_dbs_returns_generator():
    assert type(fd.get_dbs(SETS)).__name__ == "generator"

def test_get_files_returns_list():
    assert isinstance(fd.get_files(LYRICS), list)

def test_get_files_all_files():
    assert len(fd.get_files(LYRICS)) == 54

def test_get_files_returns_0_from_nonexsistent_dir():
    assert len(fd.get_files("nonexistent/dir/")) == 0

def test_get_files_non_recursive_returns_one_file():
    assert len(fd.get_files_non_recursive(DEBUGDIR)) == 1  # only error file

def test_get_files_non_recursive_returns_list():
    assert isinstance(fd.get_files_non_recursive(DEBUGDIR), list)

def test_get_files_non_recursive_returns_0_from_nonexistent_dir():
    assert len(fd.get_files_non_recursive("nonexistentdir/")) == 0

def test_make_dir():
    fakedir = "fakedir"
    assert not Path(fakedir).exists()
    fd.make_dir("fakedir")
    assert Path(fakedir).exists()
    os.rmdir(fakedir)
    assert not Path(fakedir).exists()

def test_make_file():
    fakefile = "fakefile.txt"
    assert not Path(fakefile).exists()
    fd.make_file(fakefile)
    assert Path(fakefile).exists()
    os.remove(fakefile)
    assert not Path(fakefile).exists()

def test_missing_FAKEPATHS():
    assert fd.missing(FAKEPATHS) == [("somepath/", False)]

def test_missing_empty_list():
    assert fd.missing([]) == []

def test_node_result_name():
    assert fd.node_result_name("somedir/", "1") == "somedir/node1result.txt"

def test_node_result_name_empty_string():
    assert fd.node_result_name("", "") == "noderesult.txt"

def test_path_check():
    pass

def test_paths_okay_PATHS():
    assert fd.paths_okay(PATHS)

def test_paths_okay_NONPATHS():
    assert not fd.paths_okay(NONPATHS)


