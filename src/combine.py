#!/usr/bin/env python3
"""Combines the results files on each pi-node."""

#stand lib
import os
from pathlib import Path
import subprocess

#custom
from constants import *
from searchutil import *

def node_result_files():
    """Collect the result's file names on a pi-node. Returns List."""
    return [str(p) for p in Path(RESULTDIR).glob("*.txt")]

def node_result_name(node):
    """Formats the final result file's name on a pi-node. 
        Returns String."""
    return TRANSFERDIR+"node"+node+"result.txt"

def get_node_name():
    """Gets node name. Returns String."""
    return (subprocess.run("hostname", shell=True, 
        stdout=subprocess.PIPE).stdout).decode("utf-8")

def node_results():
    """Combine each core's results on a pi-node into a single text file. 
        Returns None."""
    node = get_node_name()
    with open(node_result_name(node), "a+") as f1:
        for file_ in node_result_files():
            with open(file_, "r") as f2:
                count2 = 0
                for line in f2.readlines():
                    count2 += 1
                    f1.write(line.strip()+"\n")
                print("lines in f2:", str(count2))
            os.remove(file_)
