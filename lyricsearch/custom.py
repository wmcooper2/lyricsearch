#!/usr/bin/env python3.7
"""Send custom commands to control the pi-cluster."""
# stand lib
import argparse as ap
import subprocess
from typing import Any

# custom
from constants import *
from personal import *

cluster: list = [pi1, pi2, pi3, pi4]    # ip addresses
pi_outputs: list = []                      # holds stdout from pis
given_args: list = []                      # command line args


def clear_terminal() -> None:
    """Clears the terminal window. Returns None."""
    subprocess.run(["clear"])
    return None


def format_cmd(s1: str, s2: str) -> str:
    return "{0} '{1}'".format(s1, s2)


def format_node(pi_addr: str) -> str:
    return "pi@" + pi_addr


def format_ssh(pi: str) -> str:
    return "ssh " + pi


def show_outputs() -> None:
    """Shows the outputs of the pis. Returns None."""
    for output in pi_outputs:
        print(str(pi_outputs.index(output)), "::", output)
    return None


def print_kwargs() -> None:
    """Displays kwargs given at command line. Returns None."""
    for _, value in args._get_kwargs():
        given_args.append(value)
        print(_, "::", value)
    return None


def print_pi_outputs():
    """Displays contents of pi_outputs. Returns None."""
    [print(out.stdout) for out in pi_outputs]


def run_cmd(cmd):
    """Runs cmd in a subprocess. Returns stdout String."""
    return subprocess.run(cmd, encoding="utf-8", shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).stdout


def custom_cmd(pi: str, args: Any) -> str:
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
    [custom_cmd(pi, args) for pi in cluster]
    parser.exit(status=0, message="Finished.\n")