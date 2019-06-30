"""Test module for filesanddirs.py"""
import filesanddirs as fd
from pathlib import Path
import os


DEBUGDIR = "../.debug/"
LYRICSDIR = DEBUGDIR+"lyrics/"
SETSDIR = DEBUGDIR+"sets/"

 
def test_block_dir():
    assert fd.block_dir(1) == "block1"
    assert fd.block_dir(0) == "block0"

def test_count_files():
    assert fd.count_files(LYRICSDIR) == 54

def test_count_db():
    assert fd.count_db(SETSDIR) > 0

def test_file_name():
    dir_ = "mydir/"
    string = "string"
    assert fd.file_name(dir_, string) == "mydir/string.txt"

def test_file_path():
    song = "I like to eat"
    dict_ = {"I like to eat": ("its/here/boss.txt", "apples and bananas")}
    assert fd.file_path(song, dict_) == "its/here/boss.txt"

def test_get_dbs():
    assert len(list(fd.get_dbs(SETSDIR))) == 2
    assert type(fd.get_dbs(SETSDIR)).__name__ == "generator"

def test_get_files():
    assert isinstance(fd.get_files(LYRICSDIR), list)
    assert len(fd.get_files(LYRICSDIR)) == 54
    assert len(fd.get_files("nonexistent/dir/")) == 0

def test_get_files_non_recursive():
    assert len(fd.get_files_non_recursive(DEBUGDIR)) == 1  # only error file
    assert isinstance(fd.get_files_non_recursive(DEBUGDIR), list)
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

def test_missing():
    fakepaths = [("notneeded", "somepath/"),]
    assert fd.missing(fakepaths) == [("somepath/", False)]
    assert fd.missing([]) == []

def test_node_result_name():
    assert fd.node_result_name("somedir/", "1") == "somedir/node1result.txt"
    assert fd.node_result_name("", "") == "noderesult.txt"

def test_path_check():
    pass

def test_paths_okay():
    paths = [("1", DEBUGDIR), ("2", LYRICSDIR), ("3", SETSDIR),]
    nonpaths = [("1", "cheese/"), ("2", "cats/"), ("3", "artifacts/"),]
    assert fd.paths_okay(paths)
    assert not fd.paths_okay(nonpaths)


