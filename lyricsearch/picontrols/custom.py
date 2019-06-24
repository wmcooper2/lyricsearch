#!/usr/bin/env python3.7
"""Send custom commands to control the pi-cluster."""
# stand lib
import argparse as ap
import subprocess
from typing import (
    Any,
    List,
    Text,
    )

# custom
# from constants import *
from personal import (
    PI1,
    PI2,
    PI3,
    PI4,
    )

cluster: List[Text] = [PI1, PI2, PI3, PI4]
pi_outputs: List[Text] = []
given_args: List[Text] = []


def clear_terminal() -> None:
    """Clears the terminal window. Returns None."""
    subprocess.run(["clear"])
    return None


def format_cmd(s1: Text, s2: Text) -> Text:
    return "{0} '{1}'".format(s1, s2)


def format_node(pi_addr: Text) -> Text:
    return "pi@" + pi_addr


def format_ssh(pi: Text) -> Text:
    return "ssh " + pi


# outputs is "pi_outputs" var
def show_outputs(outputs: Any) -> None:
    """Shows the outputs of the pis. Returns None."""
    for msg in outputs:
        print(str(outputs.index(msg)), "::", msg)
    return None


def print_kwargs() -> None:
    """Displays kwargs given at command line. Returns None."""
    for _, value in args._get_kwargs():
        given_args.append(value)
        print(_, "::", value)
    return None


def print_pi_outputs():
    """Displays contents of pi_outputs. Returns None."""
    for out in pi_outputs:
        print(out.stdout) 


def run_cmd(cmd):
    """Runs 'cmd' in a subprocess. Returns String."""
    return subprocess.run(cmd, encoding="utf-8", shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout


def custom_cmd(pi: Text, args: Any) -> Text:
    """Sends custom command to a node. Returns String."""
    node = format_node(pi)
    ssh = format_ssh(node)
    cmd = format_cmd(ssh, args.command)
    result = run_cmd(cmd)

    # subprocesses needed to branch here...
    # currently only runs on the first node
    print("result == ", result)
    if args.verbose:
        print(result.strip())
    return "pi@{0}".format(pi)+"\n"+result.strip()


if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Custom cmds for pi-cluster.")
    parser.add_argument("command", help="A string to run at the CLI.")
    parser.add_argument("-v", "--verbose", help="Be verbose.",
                        action="store_true")
    args = parser.parse_args()
    clear_terminal()
    print("\n")
    for pi in cluster:
        custom_cmd(pi, args)
    parser.exit(status=0, message="Finished.\n")
