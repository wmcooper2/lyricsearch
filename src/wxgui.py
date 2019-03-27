#!/usr/bin/env python3.7
"""GUI for lyric searching program."""
# may be issues with running in a virtual environment.
# see note here; https://realpython.com/python-gui-with-wxpython/


# stand lib

# 3rd party
import wx

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Hello World')
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
