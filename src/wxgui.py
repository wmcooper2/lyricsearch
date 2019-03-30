#!/usr/bin/env python3.7
"""GUI for lyric searching program."""
# stand lib
from pprint import pprint

# 3rd party
import wx

# custom
from clisearchutil import *

BUT_X = 396
BUT_COLOR = (21, 85, 227)  # macos blue button

CLUSTER_X = 396
CLUSTER_W = 84
CLUSTER_H = 100

COL_0 = 0
COL_1 = 20
COL_2 = 60
COL_3 = 290

ROW_0 = 0
ROW_1 = 20
ROW_2 = 80

SEARCH_W = 460
# SEARCH_H = 22

WIN_W = 500
WIN_H = 400

PROGRESS_W = 356
PROGRESS_H = 100

class Gui(wx.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = self
        w.SetSize((WIN_W, WIN_H))
        w.Centre()
        w.menu_()
        w.search_box()
#         w.input_box()
        w.search_button()
        w.progress_box()
        w.cluster_box()
        w.Bind(wx.EVT_BUTTON, w.search, id=w.button.GetId())
        w.SetBackgroundColour(wx.BLACK)
        w.SetTitle("Lyric Search")

    def menu_(w):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        menu_bar.Append(file_menu, "File")
        exit_item = file_menu.Append(wx.ID_EXIT, item="Exit",
                                     helpString="status message...")
        w.SetMenuBar(menu_bar)
        w.Bind(wx.EVT_MENU, w.quit_, exit_item)
        w.Show(True)

    def search_box(w):
        w.search_box_ = wx.StaticBox(w, wx.ID_ANY, "",
                                     size=(SEARCH_W, 30),
                                     pos=(COL_1, ROW_1))
        w.search_box_.Show(True)
        w.input_box()

    def input_box(w):
        w.input_ = wx.TextCtrl(w.search_box_, size=(350,-1))
        w.input_.SetPosition((0, 0))
        w.input_.SetBackgroundColour(wx.WHITE)
        w.Show(True)

    def search_button(w):
        w.button = wx.Button(w.search_box_, pos=(366, 0), 
                             label="Search")
        print(w.button.GetSize())
        w.button.Show(True)

    def search(w, event):
        pattern = w.input_.GetValue()
        w.progress_label()

        cmds = cluster_commands(pattern)
        pprint(cmds)

#         break up the search into stages that report back to the gui

#         results = start_processes(cmds)
#         for r in results:
#             print(r.strip())
#         path_check(PATHS)
#         possible_results = possible_match_search(pattern)
#         exact_results = exact_match_search(possible_results, pattern)
#         save_results(exact_results[0], pattern)
#         print_stats(possible_results, exact_results)
#         print(cluster_commands(pattern)[0])


    def progress_box(w):
        w.progress = wx.StaticBox(w, wx.ID_ANY, "Progress", 
                                  size=(PROGRESS_W, PROGRESS_H), 
                                  pos=(COL_1, ROW_2))
        w.progress.SetBackgroundColour(wx.WHITE)
        w.progress.Show(True)

    def progress_label(w):
        label = wx.StaticText(w.progress, wx.ID_ANY, label="Searching...",
                              pos=(COL_0, ROW_0))
        label.Show(True)

    def cluster_box(w):
        w.cluster = wx.StaticBox(w, wx.ID_ANY, "Cluster",
                                 size=(CLUSTER_W, CLUSTER_H),
                                 pos=(CLUSTER_X, ROW_2))
        w.cluster.SetBackgroundColour(wx.WHITE)
        w.pi1 = wx.StaticText(w.cluster, wx.ID_ANY, label="pi 1:",
                              pos=(5, 0))
        w.pi2 = wx.StaticText(w.cluster, wx.ID_ANY, label="pi 2:",
                              pos=(5, 20))
        w.pi3 = wx.StaticText(w.cluster, wx.ID_ANY, label="pi 2:",
                              pos=(5, 40))
        w.pi4 = wx.StaticText(w.cluster, wx.ID_ANY, label="pi 4:",
                              pos=(5, 60))
        

    def quit_(w, event):
        w.Close()

app = wx.App()
gui = Gui(None)
app.MainLoop()
