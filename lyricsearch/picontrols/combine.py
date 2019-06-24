#!/usr/bin/env python3.7
"""Combines the results files on each pi-node."""
# stand lib
import os
from pathlib import Path
import subprocess
from typing import List, Text

# custom
from constants import (
    COMBINEDIR,
    RESULTSDIR,
    )
# from searchutil import *
from filesanddirs import (
    node_result_name,
    node_result_files,
    )


def get_node_name() -> Text:
    """Gets node name. Returns String."""
    return (subprocess.run("hostname", shell=True,
            stdout=subprocess.PIPE).stdout).decode("utf-8")


def node_results() -> None:
    """Combine each core's results on a pi-node into a single text file.
        Returns None."""
    node = get_node_name()
    with open(node_result_name(node), "a+") as combined:
        for file_ in node_result_files():
            with open(file_, "r") as results:
                results_count = 0
                for line in results.readlines():
                    results_count += 1
                    combined.write(line.strip()+"\n")
                print("lines in results:", str(results_count))
            os.remove(file_)
