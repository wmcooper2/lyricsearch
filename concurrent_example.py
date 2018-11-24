#!/usr/bin/env python3
"""Trying to use concurrent.futures module."""

#stand lib
import concurrent.futures as cf
import time

def fun():
    time.sleep(1)
    return "yay"

pool = cf.ProcessPoolExecutor()
future = pool.submit(fun)
#for key, value in pool.__dict__.items():
#    print(key, " :: ", value)
#print("workers on this node ==", pool.__dict__["_max_workers"])

time.sleep(2)
print(future.done())
#print(pool.done())
print(future.result())

