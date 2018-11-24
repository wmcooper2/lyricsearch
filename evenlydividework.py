#!/usr/bin/env python3
"""Divide '.txt' files fairly (as close to even, no fractions of a file)
    across 4 dirs."""

#stand lib
import math
import os
from pathlib import Path
from queue import Queue
import random
import shutil
from time import time

def loadpaths(searchpath):
    """Loads the paths of '.txt' files from a single dir. Returns Queue."""
    main = Queue()
    [main.put(relpath) for relpath in Path(searchpath).iterdir() \
        if str(relpath).endswith(".txt")]
    return main

def loadpathsfromdirs(searchpath):
    """Loads the paths of '.txt' files from each dir one level down from the
        given dir 'searchpath'. Loads the paths of '.txt' files only.
        Returns Queue."""
    main = Queue()
    for dir_ in Path(searchpath).iterdir():
        print("loading {}".format(dir_))
        [main.put(file_) if str(file_).endswith(".txt") \
            for file_ in Path(dir_).iterdir()]
#        for file_ in Path(dir_).iterdir():
#            if str(file_).endswith(".txt"):
#                main.put(file_)
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

    def divideremainingwork(a, b):
        """Try to put an element into QueueA from QueueB. Returns None."""
        try: a.put(b.get())
        except: pass

    workload = math.ceil(mainqueue.qsize()//numcores)
    workerqueues = []
    [workerqueues.append(Queue()) for x in range(numcores)]
    for x in workerqueues: 
        try:
            [x.put(mainqueue.get()) for i in range(workload)]
#            for y in range(workload):
#                x.put(mainqueue.get())
        except:
            pass

    #place the remainder workload, if any
    [divideremainingwork(i, mainqueue) \
        for i in workerqueues if not mainqueue.empty()]
#    for x in workerqueues:
#        if not q.empty():
#            try:
#                x.put(q.get())
#            except:
#                pass
    return workerqueues

if __name__ == "__main__":
#WHEN MOVED TO THE NODES...
#this module is to be run locally.
#this will prepare the file paths for the ProcessPoolExecutor
#run this once again on the nodes making one file for each core to process
#need to log times and counts (time is important for the end user)
#change data dir to "/mnt/usb/" on pi nodes

#each core in each node will have one queue to process
#when each core is finished, they will wait
#when all the cores are finished, the results are written to a single log
#when each node is finished, the results stay on each node until collected 
  # by the macbook

    start = time()
    datadir = "/Volumes/EMERGENCY/LyricsDatabase/alllyrics/"
    totalwork = countfiles(datadir)   #count files
    filecountingtime = time()
    print("time to count files=", filecountingtime-start)

    start = time()
    q = loadpathsfromdirs(datadir)
    fileloadingtime = time()
    print("time to load files=", fileloadingtime-start)

#    cpus = int(os.cpu_count())          #get machine cpu count
    cpus = 4
    fprint("total work", q.qsize())     #check total work

    start = time()
    workerqueues = dividework(q, cpus)  #divide work among cpus
    dividingtime = time()
    print("time to divide work=", dividingtime - start)

#    fprint("core workload", workerqueues[0].qsize())
#    fprint("cpu count", str(cpus))      #check cpu count
    [fprint("size", worker.qsize()) for worker in workerqueues]
    fprint("remainder", q.qsize())
    # check contents of queue
#    for x in range(workerqueues[0].qsize()):
#        print(workerqueues[0].get())
   

#RUN ONCE TO PREPARE FILES FOR PI NODES
#This is not set up for multiprocessing, takes several hours.
    copytimestart = time()
    for x in range(workerqueues[0].qsize()):
        shutil.copy(workerqueues[0].get(), "/Volumes/EMERGENCY/forpi1/")
        print(x)
    for x in range(workerqueues[1].qsize()):
        shutil.copy(workerqueues[1].get(), "/Volumes/EMERGENCY/forpi2/")
        print(x)
    for x in range(workerqueues[2].qsize()):
        shutil.copy(workerqueues[2].get(), "/Volumes/EMERGENCY/forpi3/")
        print(x)
    for x in range(workerqueues[3].qsize()):
        shutil.copy(workerqueues[3].get(), "/Volumes/EMERGENCY/forpi4/")
        print(x)
    copytimeend = time()
    print("copy time = ", copytimeend-copytimestart)
