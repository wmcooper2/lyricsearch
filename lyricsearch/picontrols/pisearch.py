"""Module for Raspberry Pi lyrics search."""
# stand lib
from typing import (
        List,
        Text,
        )

from constants import CLUSTER

def cluster_commands(pattern: Text) -> List[Text]:
    """Formats commands for the cluster. Returns List."""
    commands = []
    for pi in CLUSTER:
        commands.append(pi_cmd(pi, pattern))
    return commands


def pi_cmd(pi: Text, pattern: Text) -> Text:
    """Formats search command for the pi. Returns String."""
    return "ssh pi@" + pi + \
           " \"sudo python3.7 lyricsearch/src/main.py " + \
           "'" + pattern + "'" + "\""
#     return "ssh pi@" + pi + " hostname"
#     print(os.popen("echo $PS1").read().strip())


def start_processes(processes: List[Text]) -> List[Any]:
    """Starts subprocesses. Returns List of workers."""
    a = subprocess.run(processes[0], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    b = subprocess.run(processes[1], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    c = subprocess.run(processes[2], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    d = subprocess.run(processes[3], encoding="utf-8", shell=True,
                       stdout=subprocess.PIPE).stdout
    return [a, b, c, d]
