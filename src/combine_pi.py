#!/usr/bin/env python3
"""Combines the results files on each pi-node."""

#stand lib
import os
from pathlib import Path

resultsdir = "results/"
oldresults = []

for p in Path(resultsdir).iterdir():
    if str(p).endswith(".txt"):
        oldresults.append(p)

finalresult = "results/finalresult.txt"
with open(finalresult, "a+") as f:
    for p in oldresults:
        with open(str(p), "r") as old:
            for line in old.readlines():
                f.write(line.strip())
                f.write("\n")
        os.remove(str(p))
