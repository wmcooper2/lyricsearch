#!/usr/bin/env python3
"""A GUI tool template for running commands in stages, manually."""

#stand lib
from pathlib import Path
import tkinter as tk
from tkinter import ttk

#3rd party

#custom
#from constants import *
import commands as cmds #make the commands.py file for each project.

#Main
win = tk.Tk()
win.title("Template GUI")

main_box = ttk.Frame(win)
main_box.grid(column=0, row=0, pady=6, padx=6)

L_WIDTH = 30
templatestring = "template"
address_frame = ttk.LabelFrame(main_box, text="Template", width=L_WIDTH)
address_frame.grid(column=0, row=0, sticky=tk.W, pady=6, padx=6)
address = ttk.Label(address_frame, text=templatestring)
address.grid(column=0, row=0, sticky=tk.W, pady=6, padx=6)

status_frame = ttk.LabelFrame(main_box)
status_frame.grid(column=0, row=1, pady=6, padx=6)

#to perform the search (see README.md)
 #the gui will run 'multicoresearch.py'
 #after the search, run 'python3 src/simplecluster.py -c'
 #after the combination (as in the previous step), run 'python3 src/simplecluster -t'
 #** Ideally, click one button, but until then run these three steps








def row1():
    leftbtn1 = ttk.Button(status_frame, text="Row1", 
        command=cmds.test)
    leftbtn1.grid(column=0, row=1, pady=6, padx=6)
    result1a = ttk.Label(status_frame, 
        text="text1")
    result1a.grid(column=1, row=1, pady=6, padx=6)
    result1b = ttk.Label(status_frame, 
        text="text2")
    result1b.grid(column=2, row=1, pady=6, padx=6)
    rightbtn1 = ttk.Button(status_frame, text="recover", 
        command=cmds.test)
    rightbtn1.grid(column=3, row=1, pady=6, padx=6)

def row2():
    leftbtn2 = ttk.Button(status_frame, text="Row2", 
        command=cmds.test)
    leftbtn2.grid(column=0, row=2, pady=6, padx=6)
    result2a = ttk.Label(status_frame, 
        text="text3")
    result2a.grid(column=1, row=2, pady=6, padx=6)
    result2b = ttk.Label(status_frame, 
        text="text4")
    result2b.grid(column=2, row=2, pady=6, padx=6)
    rightbtn2 = ttk.Button(status_frame, text="recover", 
        command=cmds.test)
    rightbtn2.grid(column=3, row=2, pady=6, padx=6)

def row3():
    leftbtn3 = ttk.Button(status_frame, text="Row3", 
        command=cmds.test)
    leftbtn3.grid(column=0, row=3, pady=6, padx=6)
    result3a = ttk.Label(status_frame, 
        text="text5")
    result3a.grid(column=1, row=3, pady=6, padx=6)
    result3b = ttk.Label(status_frame, 
        text="text6")
    result3b.grid(column=2, row=3, pady=6, padx=6)
    rightbtn3 = ttk.Button(status_frame, text="recover", 
        command=cmds.test)
    rightbtn3.grid(column=3, row=3, pady=6, padx=6)

def row4():
    leftbtn4 = ttk.Button(status_frame, text="Row4", 
        command=cmds.test)
    leftbtn4.grid(column=0, row=4, pady=6, padx=6)
    result4a = ttk.Label(status_frame, 
        text="text7")
    result4a.grid(column=1, row=4, pady=6, padx=6)
    result4b = ttk.Label(status_frame, 
        text="text8")
    result4b.grid(column=2, row=4, pady=6, padx=6)
    rightbtn4 = ttk.Button(status_frame, text="recover", 
        command=cmds.test)
    rightbtn4.grid(column=3, row=4, pady=6, padx=6)

#bottom
button_frame = ttk.LabelFrame(main_box)
button_frame.grid(column=0, row=2, sticky=tk.W, pady=6, padx=6)
run_tests_btn = ttk.Button(button_frame, text="Run", 
    command=cmds.test)
run_tests_btn.grid(column=0, row=0, sticky=tk.W, pady=6, padx=6)

row1()
row2()
row3()
row4()
win.mainloop()
