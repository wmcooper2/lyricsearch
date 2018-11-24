#!/usr/bin/env python3
"""Thread based pattern search through an actual text file."""

#stand lib
import math
from multiprocessing import Process
import subprocess as sp
from threading import Thread
from time import time
from queue import Queue
import re


def calc():
    for i in range(0, 3000000):
        math.sqrt(i)

def patternsearch():
    global pattern
    with open(lorem, "r") as f:
        string = f.readlines()
        re.match(pattern, str(string))

pattern = "Chicken pork chop"
lorem   = "loremipsum.txt"
iters   = 200
something   = patternsearch



###multithreading
threadstart = time()
q = []
#create worker
for x in range(iters):
#    print("making worker {}".format(x))
    q.append(Thread(target=something)) 
#start worker
for worker in q:
    worker.start()
#join workers
for worker in q:
    worker.join()
threadend = time()

###multiprocessing
processstart = time()
p = []
#create worker
for x in range(iters):
#    print("making worker {}".format(x))
    p.append(Process(target=something)) 
#start worker
for worker in p:
    worker.start()
#join workers
for worker in p:
    worker.join()
#print("time taken, multiprocess:: ", str(round(time() - start, 6)))
processend = time()

###serial execution
serialstart = time()
for x in range(iters):
    something()
serialend = time()
print("time taken, not threaded:: ", str(round(serialend-serialstart, 6)))
print("time taken, threaded    :: ", str(round(threadend-threadstart, 6)))
print("time taken, multiprocess:: ", str(round(processend-processstart, 6)))



"""
Results;
time taken, not threaded::  48.896398
time taken, threaded    ::  52.435942
time taken, multiprocess::  31.411792

multiprocessing is better, for this application, but I would need to test them on the picluster for searching through a lot of text files.

initial thoughts;
    - need to separate the files into blocks for each process/thread?
    - how many threads/processes are ideal?
    - start a single process/thread for each directory?
        - not fair becauase there are uneven amounts of files in each dir
        - need to put all files in a queue then divide evenly to workers?




"""
