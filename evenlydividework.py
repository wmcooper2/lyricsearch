#!/usr/bin/env python3
"""Trying to divide work evenly among mulitple cores."""

#stand lib
import math
import os
from pathlib import Path
import random
from queue import Queue

def tryprint(a):
    """Tries to print attributes of 'a'. Returns None."""
    try:
        print(os.a)
    except:
        print(a, "HAS NOTHING")

def testdata(limit):
    """Create test data. Returns Queue."""
    q = Queue()
    for x in range(0, limit):
        q.put(random.randint(0, 1000000))
    return q

def loadpaths(searchpath):
    """Loads the paths of '.txt' files only. Returns Queue."""
    q = Queue()
    [q.put(relpath) for relpath in Path(searchpath).iterdir() \
        if str(relpath).endswith(".txt")]
    return q

def loadpathsfromdirs(searchpath):
    """Iters through the dirs in searchpath.
        Loads the paths of '.txt' files only.
        Returns Queue."""
    main = Queue()
    for dir_ in Path(searchpath).iterdir():
        for file_ in Path(dir_).iterdir():
            if str(file_).endswith(".txt"):
                main.put(file_)
    return main

def countfiles(path_):
    """Counts the files that end in '.txt' in 'path_'. Returns Integer."""
    return sum(1 for x in Path(path_).iterdir())

def fprint(title, value):
    """Nicely formats output to terminal. Returns None."""
    print("{0:<15} {1:^6} {2:>15}"\
        .format(title, "=", value))

def dividework(mainqueue, numcores):
    """Evenly divides the work. Returns List of Queues."""
    workload = math.ceil(mainqueue.qsize()//numcores)
    workerqueues = []
    [workerqueues.append(Queue()) for x in range(numcores)]
    for x in workerqueues: 
        try:
            for y in range(workload):
                x.put(mainqueue.get())
        except:
            pass

    #place the remainder workload, if any
    for x in workerqueues:
        if not q.empty():
            try:
                x.put(q.get())
            except:
                pass
    return workerqueues

if __name__ == "__main__":

    #need to know;
    # amount of files total
    # number of cores available
    # paths of files

    datadir = "testdata/"
    totalwork = countfiles(datadir)   #count files

    q = loadpathsfromdirs(datadir)
    cpus = int(os.cpu_count())          #get machine cpu count
    fprint("total work", q.qsize())     #check total work
    workerqueues = dividework(q, cpus)  #divide work among cpus
#    fprint("core workload", workerqueues[0].qsize())
#    fprint("cpu count", str(cpus))      #check cpu count
    [fprint("size", worker.qsize()) for worker in workerqueues]
    fprint("remainder", q.qsize())
    # check contents of queue
#    for x in range(workerqueues[0].qsize()):
#        print(workerqueues[0].get())
