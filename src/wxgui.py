#!/usr/bin/env python3.7
"""GUI for lyric searching program."""
# 3rd party
import wx

# custom
from clisearchutil import *

COL_1 = 20
COL_2 = 60
ROW_1 = 20
ROW_2 = 60

class Gui(wx.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Centre()
        self.menu_()
        self.search_input_()
        self.button_()
        self.Bind(wx.EVT_BUTTON, self.search, id=self.button.GetId())
        self.SetBackgroundColour(wx.BLACK)
        self.SetTitle("Lyric Search")

    def menu_(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        menu_bar.Append(file_menu, "File")
        exit_item = file_menu.Append(wx.ID_EXIT, item="Exit",
                                     helpString="status message...")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, self.quit_, exit_item)
        self.Show(True)

    def search_input_(self):
        self.search_box = wx.TextCtrl(self, size=(250,-1))
        self.search_box.SetPosition((COL_1, ROW_1))
        self.search_box.SetBackgroundColour(wx.WHITE)
        self.Show(True)

    def button_(self):
        self.button = wx.Button(self, pos=(COL_2, ROW_2), label="Search")
        self.Show(True)

    def search(self, event):
        pattern = self.search_box.GetValue()
        path_check(PATHS)
        possible_results = possible_match_search(pattern)
        exact_results = exact_match_search(possible_results, pattern)
        save_results(exact_results[0], pattern)
        print_stats(possible_results, exact_results)

    def quit_(self, event):
        self.Close()

app = wx.App()
gui = Gui(None)
app.MainLoop()
