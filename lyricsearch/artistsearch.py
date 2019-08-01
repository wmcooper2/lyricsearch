"""Search for artist in lyrics database."""
# stand lib
from pathlib import Path
from pprint import pprint
import shelve
from typing import Any, Text, Tuple


# custom
from artistsearchutil import (
        make_artist_list,
        make_song_list,
        make_artist_song_lists,
        file_name_error_check)


from constants import LYRICS, ARTISTDB
from filesanddirs import (
        collect_file_names,
        count_files)


if __name__ == "__main__":
    file_count = sum(1 for file_ in collect_file_names(LYRICS))
    print("File count:", file_count)

# preprocessing of data, these steps take a long time to complete.
    # make complete list of artist names
#     files = collect_file_names(LYRICS)  # gen
#     make_artist_list("artistnames.txt", files)

    # check all file names for double underscore problem
#     files = collect_file_names(LYRICS)  # gen
#     pprint(file_name_error_check(files))

    # make complete list of song names
#     files = collect_file_names(LYRICS)  # gen
#     make_song_list("songtitles.txt", files)

    # make lists for each artist with their song names
#     files = collect_file_names(LYRICS)  # gen
#     make_artist_song_lists(files)
