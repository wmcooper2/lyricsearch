#!/usr/bin/env python3.7
"""Module for checking paths."""
# stand lib
from constants import *
from pathlib import Path
from typing import List
from typing import Tuple


def paths_okay(paths: List[str]) -> bool:
    """Checks that all paths exist. Returns Boolean."""
    return all(Path(path).exists for path in paths)
            
def missing(paths: List[str]) -> List[Tuple[str, bool]]:
    """Returns List of missing paths."""
    temp = []
    for path in paths:
        temp.append((path, Path(path).exists()))
    return temp
