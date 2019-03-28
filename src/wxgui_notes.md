# App
import wx
app = wx.App()
app.mainloop()

# Window; https://docs.wxpython.org/wx.Window.html#wx.Window
wx.Window()

# Frame; https://docs.wxpython.org/wx.Frame.html
wx.Frame(parent, id=ID_ANY, title="", pos=DefaultPosition, size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)

# Displaying things;
<widget>.Show()

# Menu Basics
### Example
def menu(self):
    menu_bar = wx.MenuBar()
    file_menu = wx.Menu()
    menu_bar.Append(file_menu, "File")
    exit_item = file_menu.Append(wx.ID_EXIT, item="Exit", helpString="status message...")
    self.SetMenuBar(menu_bar)
    self.Bind(wx.EVT_MENU, self.quit_, exit_item)
    self.SetTitle("Lyric Search")
    self.Show(True)

### Order is important 
1. Make the menu bar:
  `menu_bar = wx.MenuBar()`
2. Make the drop down menus:
  `file_menu = wx.Menu()`
3. Append the menus to the menubar:
  `menu_bar.Append(file_menu, "File")`
4. Then, append the items to the drop down menus:
  `exit_item = file_menu.Append(wx.ID_EXIT, item="Exit", helpString="status message...")`
5. Set the menu bar:
  `self.SetMenuBar(menu_bar)`
6. Bind the buttons to an event, include ID's:
  `self.Bind(wx.EVT_MENU, self.quit_, exit_item)
7. (optional) Set the title:
  `self.SetTitle("some title")
8. Don't forget to show it:
  `self.Show(True)`
