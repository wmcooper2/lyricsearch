#!/usr/bin/env python3
"""Simple, routine commands to control the pi-cluster."""

#stand lib
import argparse as ap
import os
from pathlib import Path
import subprocess

#custom
from pi_ipaddresses import *
from personaldata import *

cluster     = [pi1, pi2, pi3, pi4]      # ip addresses
pi_outputs  = []                        # holds stdout from pis
valid_args  = ["1", "2", "3", "4"]
given_args  = []                        # holds args from command line
patternfile = "searchpattern.txt"
noderesult  = "../results/noderesult.txt"
#factor out this line;
#    name = format_pi_name(cluster[int(pi)-1])

def not_none(flag):
    """Checks that args for a flag are not None. Returns Boolean."""
    if flag[1] != None: return True
    else: return False

def valid(a):
    """Validates the input arugments. Returns Boolean."""
    for line in a:
        if all([arg in valid_args for arg in line[1]]) and len(line[1])<=4: 
            return True
    return False

def clear_terminal():
    """Clears the terminal window. Returns None."""
    subprocess.run(["clear"])

def show_outputs():
    """Shows the outputs of the pis. Returns None."""
    for output in pi_outputs:
        print(str(pi_outputs.index(output)), "::", output)

def format_pi_name(string):
    """Formats the pi name. Returns String."""
    piname = "pi@"+string
    return piname

def format_cmd(str1, str2):
    """Formats the command. Returns String."""
    return "ssh "+str1+" '"+str2+"'"

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
        stdout=subprocess.PIPE).stdout

def scp_from_pi(pi):
    """Copies all 'noderesult.txt' files to the macbook. Returns None."""
    return "scp "+pi+":/home/pi/lyricsearch/results/noderesult.txt "+macbookresultsdir

def load_search_pattern(patternfile):
    """Loads search pattern from '<rootdir>/results/'. Returns String."""
    with open(patternfile) as f:
        pattern = f.readlines()
        return pattern[0]

def _reboot(pi):
    """Reboots all the nodes in cluster. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo reboot")
    run_cmd(cmd)

def _shutdown(pi):
    """Shutsdown all the nodes in cluster. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo shutdown -h now")
    run_cmd(cmd)

def _name(pi):
    """Displays the name of the machine. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "hostname")
    result = run_cmd(cmd)
    print(result.strip())

def _ipaddr(pi):
    """Displays the wlan0 ipaddress of the node. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "hostname -I")
    result = run_cmd(cmd)
    print("pi{}".format(pi), result.strip())

def _mount(pi):
    """Mount the usb drives to the nodes. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo mount /dev/sda1 /mnt/usb")
    run_cmd(cmd)
    print("{}: mounted {} at {}".format(name, "/dev/sda1", "/mnt/usb"))

def _umount(pi):
    """Unmounts the usb drives from the nodes. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo umount /dev/sda1 /mnt/usb")
    run_cmd(cmd)
    print("{}: unmounted {} from {}".format(name, "/dev/sda1", "/mnt/usb"))

def _list(pi, args):
    """List the dir names of a node's /mnt/usb."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = None
    if args.verbose:
        cmd = format_cmd(name, "ls -al /mnt/usb/")
    else:
        cmd = format_cmd(name, "ls /mnt/usb/")
    print(name)
    print(run_cmd(cmd).strip())
    print("\n")

def _combine(pi):
    """Combines results files in '/home/pi/lyricsearch/results/'. 
        Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo python3 lyricsearch/combine.py")
    result = run_cmd(cmd)
    print("pi{}".format(pi), "results combined at node.")

def _transfer(pi):
    """Transfers/combines node results to macbook's results dir.
        Returns None.

        macbook's results dir: <rootdir>/results/
    """
    #transfer to mac, one file at a time
    name = format_pi_name(cluster[int(pi)-1])
    cmd = scp_from_pi(name)
    run_cmd(cmd)
    resultsfile = "../results/"+load_search_pattern(patternfile).strip()+".txt"

    if not Path(resultsfile).exists():
        Path(resultsfile).touch()
    else:
        #copy contents of results to a single file
        with open(Path(noderesult), "r") as f:
            with open(resultsfile, "a+") as f2:
                temp = f.readlines()
                for line in temp:
                    f2.write(line.strip())
                    f2.write("\n")
        #delete the file
        os.remove(noderesult)

def run_simple(a):
    """Runs a simple command. Returns None."""
    if args.reboot:
        [_reboot(arg) for arg in set(args.reboot)]
    elif args.shutdown:
        [_shutdown(arg) for arg in set(args.shutdown)]
    elif args.name:
        [_name(arg) for arg in set(args.name)]
    elif args.ipaddr:
        [_ipaddr(arg) for arg in set(args.ipaddr)]
    elif args.mount:
        [_mount(arg) for arg in set(args.mount)]
    elif args.umount:
        [_umount(arg) for arg in set(args.umount)]
    elif args.list:
        [_list(arg, args) for arg in set(args.list)]
    elif args.combine:
        [_combine(arg) for arg in set(args.combine)]
    elif args.transfer:
        [_transfer(arg) for arg in set(args.transfer)]

if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Commands for the pi-cluster.")
    parser.add_argument("-v", "--verbose", help="Be verbose.", 
        action="store_true")

    # simple, common commands
    simple = parser.add_mutually_exclusive_group()
    simple.add_argument("-r", "--reboot", help="Reboots the cluster.", 
        nargs="?", const=valid_args)
    simple.add_argument("-s", "--shutdown", help="Shuts down the cluster.",
        nargs="?", const=valid_args)
    simple.add_argument("-n", "--name", help="Displays name of the node.",
        nargs="?", const=valid_args)
    simple.add_argument("-i", "--ipaddr", help="Displays node's ipaddress.",
        nargs="?", const=valid_args)
    simple.add_argument("-m", "--mount", help="Mounts the usb drives.",
        nargs="?", const=valid_args)
    simple.add_argument("-u", "--umount", help="Unmounts the usb drives.",
        nargs="?", const=valid_args)
    simple.add_argument("-l", "--list", help="List dirs in /mnt/usb",
        nargs="?", const=valid_args)
    simple.add_argument("-c", "--combine", help="combines files in /home/pi/lyricsearch/results/",
        nargs="?", const=valid_args)
    simple.add_argument("-t", "--transfer", help="transfers/combines node results to macbook '<rootdir>/results/'", 
        nargs="?", const=valid_args)

    args = parser.parse_args()
    clear_terminal()
    print("\n")     # for nice terminal output
    a = filter(not_none, args._get_kwargs())    #filter args != None

    if valid(a):
        run_simple(a)
    else:
        print("Please choose any combination of the four nodes (1 2 3 or 4).\nYou can choose a maximum of four nodes at a time.\nLeave blank to choose all.\n")

    # End program
    parser.exit(status=0, message="Finished.\n")
