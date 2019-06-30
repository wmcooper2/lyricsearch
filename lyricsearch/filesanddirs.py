"""Module for working with files and directories."""
from pathlib import Path
from pprint import pprint
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Text,
    Tuple,
    )


def artist_song(path: Any) -> Tuple[Text, Text]:
    """Extracts the artist and song name from 'path'. Returns String."""
    parent = path.parents[0]
    parts = path.parts
    file_name = path.name
    stem = path.stem
    artist = stem.split("_")[0]
    song = stem.split("_")[1]
    return artist, song


def collect_file_names(dir_: Text) -> Generator[Text, None, None]:
    """Collect the file names from the database. Returns generator."""
    return Path(dir_).glob("**/*.txt")


def block_dir(num: int) -> Text:
    """Formats dir name. Returns String."""
    return "block"+str(num)


def count_files(dir_: Text) -> int:
    """Counts files ending in '.txt'. Returns Integer."""
    return sum([1 for x in Path(dir_).glob("**/*.txt")])


def count_db(db: Text) -> int:
    """Counts database files. Returns Integer."""
    return sum([1 for x in Path(db).glob("**/*.db")])


def file_name(dir_: Text, string: Text) -> Text:
    return dir_+string+".txt"


def file_path(song: Text, dict_: Dict[Text, Tuple[Text, Text]]) -> Text:
    """Gets the song path. Returns String."""
    return dict_[song][0]


# def get_files(dir_: Text) -> Any:
#     """Gets text files from dir_, recursively. Returns Generator."""
#     return (file_ for file_ in Path(dir_).glob("**/*.txt"))


def get_dbs(dir_: Text) -> Generator[Text, None, None]:
    """Gets databases from 'dir_'. Returns Generator."""
    return (file_ for file_ in Path(dir_).glob("*.db"))


# # list version
def get_files(dir_: Text) -> List[Text]:
    """Gets text files from dir_, recursively. Returns List."""
    return [file_ for file_ in Path(dir_).glob("**/*.txt")]


def get_files_non_recursive(dir_: Text) -> List[Text]:
    """Gets text file names, non-recursive. Returns List."""
    return [p for p in Path(dir_).glob("*.txt")]


def make_artist_db(dir_: Text) -> None:
    """Creates the 'artist.db' from files in 'dir_'. Returns None."""
    artists = {}
    file_amt = count_files(lyricsdir)
    for path in collect_file_names(dir_):  # recursive
        artist, song = artist_song(path)
        if artist not in artists:
            artists[artist] = set()
        artists[artist].add(song)
    pprint(artists)
    with shelve.open(ARTIST_DB) as db:
        db["artists"] = artists


def make_dir(dir_) -> None:
    """Makes 'dir_' if it doesn't exist. Returns None."""
    if not Path(dir_).exists():
        Path(dir_).mkdir()


def make_file(file_):
    """Makes file_ if it doesn't exist. Returns None."""
    if not Path(file_).exists():
        Path(file_).touch()


def missing(paths: List[Tuple[Text, Text]]) -> List[Tuple[Text, bool]]:
    """Determines which paths are missing. Returns List."""
    temp = []
    for path in paths:
        temp.append((path[1], Path(path[1]).exists()))
    return temp


def node_result_name(dir_: Text, node: Text) -> Text:
    """Formats final result file's name on pi-node. Returns String."""
    return dir_+"node"+node+"result.txt"


def path_check(paths: List[Tuple[Text, Text]]) -> None:
    """Performs 'existence' check. Returns None."""
    if paths_okay(paths):
        print("Files and directories check complete.")
    else:
        pprint(paths)
        raise Exception("Error: Missing paths. Quitting...")
        quit()


def paths_okay(paths: List[Tuple[Text, Text]]) -> bool:
    """Checks that all paths exist. Returns Boolean."""
    return all(Path(pair[1]).exists() for pair in paths)
