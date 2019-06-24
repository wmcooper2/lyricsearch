#!/usr/bin/env python3.7
"""Simple, routine commands to control the pi-cluster."""
# stand lib
import argparse as ap
import os
from pathlib import Path
import subprocess
from typing import (
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
    PI5,
    )

cluster: List[Text] = [PI1, PI2, PI3, PI4]
pi_outputs: List[Text] = []
valid_args: List[Text] = ["1", "2", "3", "4"]
given_args: List[Text] = []
patternfile: Text = "searchpattern.txt"
noderesult: Text = "../results/noderesult.txt"


def good_arg(flag: List[Text]) -> bool:
    return flag[1] is not None


def format_cmd(s1: Text, s2: Text) -> Text:
    return "ssh "+s1+" '"+s2+"'"


def format_pi_name(pi_addr: Text) -> Text:
    return "pi@"+pi_addr


def valid(a) -> bool:
    """Validates the input arugments. Returns Boolean."""
    for line in a:
        if all([arg in valid_args for arg in line[1]]) and len(line[1]) <= 4:
            return True
    return False


def clear_terminal() -> None:
    """Clears the terminal window. Returns None."""
    subprocess.run(["clear"])
    return None


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


# def print_pi_outputs():
#     """Displays contents of pi_outputs. Returns None."""
#     for out in pi_outputs:
#         print(out.stdout)


def run_cmd(cmd: Text) -> Text:
    """Runs cmd in a subprocess. Returns stdout String."""
    return subprocess.run(cmd, encoding="utf-8", shell=True,
                          stdout=subprocess.PIPE).stdout


# def scp_from_pi(pi: Text, mac_dir: Text) -> Text:
#     """Copies all 'noderesult.txt' files to the macbook. Returns None."""
#     return "scp "+pi+":/home/pi/lyricsearch/results/noderesult.txt "+mac_dir


# def load_search_pattern(patternfile):
#     """Loads search pattern from '<rootdir>/results/'. Returns String."""
#     with open(patternfile) as f:
#         pattern = f.readlines()
#         return pattern[0]


def _reboot(pi) -> None:
    """Reboots all the nodes in cluster. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo reboot")
    run_cmd(cmd)


def _shutdown(pi) -> None:
    """Shutsdown all the nodes in cluster. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo shutdown -h now")
    run_cmd(cmd)


def _name(pi) -> None:
    """Displays the name of the machine. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "hostname")
    result = run_cmd(cmd)
    print(result.strip())


def _ipaddr(pi) -> None:
    """Displays the wlan0 ipaddress of the node. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "hostname -I")
    result = run_cmd(cmd)
    print("pi{}".format(pi), result.strip())


def _mount(pi) -> None:
    """Mount the usb drives to the nodes. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo mount /dev/sda1 /mnt/usb")
    run_cmd(cmd)
    print("{}: mounted {} at {}".format(name, "/dev/sda1", "/mnt/usb"))


def _umount(pi) -> None:
    """Unmounts the usb drives from the nodes. Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo umount /dev/sda1 /mnt/usb")
    run_cmd(cmd)
    print("{}: unmounted {} from {}".format(name, "/dev/sda1", "/mnt/usb"))


def _list(pi, args) -> None:
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


def _combine(pi) -> None:
    """Combines results files in '/home/pi/lyricsearch/results/'.
        Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo python3 lyricsearch/combine.py")
    result = run_cmd(cmd)
    print("pi{}".format(pi), "results combined at node.")


def _setupsets(pi) -> None:
    """Makes the mega and song sets in '/home/pi/lyricsearch/data/'.
        Returns None."""
    name = format_pi_name(cluster[int(pi)-1])
    cmd = format_cmd(name, "sudo python3 lyricsearch/makesets.py")
    result = run_cmd(cmd)
    print("pi{}".format(pi), "Set objects created in data/.")


# def _transfer(pi):
#     """Transfers/combines node results to macbook's results dir.
#         Returns None.
#
#         macbook's results dir: <rootdir>/results/
#     """
#     # transfer to mac, one file at a time
#     name = format_pi_name(cluster[int(pi)-1])
#     cmd = scp_from_pi(name)
#     run_cmd(cmd)
#     resultsfile = "../results/"+\
#                   load_search_pattern(patternfile).strip()+\
#                   ".txt"
#
#     if not Path(resultsfile).exists():
#         Path(resultsfile).touch()
#     else:
#         # copy contents of results to a single file
#         with open(Path(noderesult), "r") as f:
#             with open(resultsfile, "a+") as f2:
#                 temp = f.readlines()
#                 for line in temp:
#                     f2.write(line.strip())
#                     f2.write("\n")
#         # delete the file
#         os.remove(noderesult)
#
def run_simple(a):  # possible error with arg?
    """Runs a simple command. Returns None."""
    if args.combine:
        [_combine(arg) for arg in set(args.combine)]
    elif args.ipaddr:
        [_ipaddr(arg) for arg in set(args.ipaddr)]
    elif args.list:
        [_list(arg, args) for arg in set(args.list)]
    elif args.name:
        [_name(arg) for arg in set(args.name)]
    elif args.mount:
        [_mount(arg) for arg in set(args.mount)]
    elif args.reboot:
        [_reboot(arg) for arg in set(args.reboot)]
    elif args.setup:
        [_setupsets(arg) for arg in set(args.setup)]
    elif args.shutdown:
        [_shutdown(arg) for arg in set(args.shutdown)]
#     elif args.transfer:
#         [_transfer(arg)for arg in set(args.transfer)]
    elif args.umount:
        [_umount(arg) for arg in set(args.umount)]


if __name__ == "__main__":
    parser = ap.ArgumentParser(description="Commands for the pi-cluster.")
    parser.add_argument("-v", "--verbose", help="Be verbose.",
                        action="store_true")

    # simple, common commands
    simple = parser.add_mutually_exclusive_group()
    simple.add_argument("-c", "--combine",
                        help="combines files in /home/pi/lyricsearch/results/",
                        nargs="?", const=valid_args)
    simple.add_argument("-i", "--ipaddr", help="Displays node ipaddress.",
                        nargs="?", const=valid_args)
    simple.add_argument("-l", "--list", help="List dirs in /mnt/usb",
                        nargs="?", const=valid_args)
    simple.add_argument("-m", "--mount", help="Mounts the usb drives.",
                        nargs="?", const=valid_args)
    simple.add_argument("-n", "--name", help="Displays name of the node.",
                        nargs="?", const=valid_args)
    simple.add_argument("-r", "--reboot", help="Reboots the cluster.",
                        nargs="?", const=valid_args)
    simple.add_argument("-s", "--shutdown", help="Shuts down cluster.",
                        nargs="?", const=valid_args)
    simple.add_argument("-t", "--transfer",
                        help="transfers results to macbook RESULTS_DIR",
                        nargs="?", const=valid_args)
    simple.add_argument("-u", "--umount", help="Unmounts the usb drives.",
                        nargs="?", const=valid_args)
    simple.add_argument("-x", "--setup", help="Setup the mega and song sets.",
                        nargs="?", const=valid_args)

    args = parser.parse_args()
    clear_terminal()
    print("\n")     # nice terminal output
    request = filter(good_arg, args._get_kwargs())    # filter args != None

    if valid(request):
        run_simple(request)
    else:
        # examples
        print("Please choose any combination of the nodes (1 2 3 or 4).")
        print("You can choose a maximum of four nodes at a time.")
        print("Leave blank to choose all.")
        print("Example; 'python3 simple.py 234'")
        print("...or")
        print("         'python3 simple.py'")

    # End program
    parser.exit(status=0, message="Finished.\n")
