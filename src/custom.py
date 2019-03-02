#!/usr/bin/env python3
"""Send custom commands to control the pi-cluster."""

#stand lib
import argparse as ap
import subprocess

#custom
from pi_ipaddresses import *

cluster     = [pi1, pi2, pi3, pi4]      # ip addresses
pi_outputs  = []                        # holds stdout from pis
given_args  = []                        # holds args from command line

format_cmd = lambda s1, s2: "{0} '{1}'".format(s1, s2)
format_node= lambda s: "pi@"+s
format_ssh = lambda s: "ssh "+s

def clear_terminal():
    """Clears the terminal window. Returns None."""
    subprocess.run(["clear"])

def show_outputs():
    """Shows the outputs of the pis. Returns None."""
    for output in pi_outputs:
        print(str(pi_outputs.index(output)), "::", output)

def print_kwargs():
    """Displays kwargs given at command line. Returns None."""
    for _, value in args._get_kwargs():
        given_args.append(value)
        print(_, "::", value)

def print_pi_outputs():
    """Displays contents of pi_outputs. Returns None."""
    [print(out.stdout) for out in pi_outputs]

def run_cmd(cmd):
    """Runs cmd in a subprocess. Returns stdout String."""
    return subprocess.run(cmd, encoding="utf-8", shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

def custom_cmd(pi, args):
    """Sends custom command to a node. Returns String."""
    node    = format_node(pi)
    ssh     = format_ssh(node)
    cmd     = format_cmd(ssh, args.command)
    result  = run_cmd(cmd)

    #subprocesses needed to branch here...
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

#def not_none(flag):
#    """Checks that args for a flag are not None. Returns Boolean."""
#    if flag[1] != None: return True
#    else:               return False

#def format_node(string):
#    """Formats the pi name. Returns String."""
#    piname = "pi@"+string
#    return piname

#def format_cmd(ssh, string):
#    """Formats the full command for a node. Returns String."""
#    return "{0} '{1}'".format(ssh, string)
