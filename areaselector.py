import ctypes
import wx
import pygetwindow as gw

global selectionOffset, selectionSize

selectionOffset = ""
selectionSize = ""

class SelectableFrame(wx.Frame):
    c1 = None
    c2 = None

    def __init__(self, parent=None, id=wx.ID_ANY, title=""):
        self.style = wx.NO_BORDER
        self.title = "Multitool Capture"

        wx.Frame.__init__(self, parent, id, title=self.title, size=wx.DisplaySize(), style=self.style)
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.SetWindowStyle(wx.STAY_ON_TOP)

        self.center = wx.StaticText(self, -1, "Select an area while holding down LEFT mouse button.", (0, 300), wx.DisplaySize(), wx.ALIGN_CENTER)
        self.center.SetFont(wx.Font(26, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.center.SetForegroundColour((0, 0, 0, 0))

        self.center.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.center.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.center.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.center.Bind(wx.EVT_PAINT, self.OnPaint)
        self.center.Bind(wx.EVT_CHAR_HOOK, self.OnKey)

        self.Show()
        self.SetTransparent(100)

    def OnKey(self, event):
        keyCode = event.GetKeyCode() 
        if keyCode == wx.WXK_ESCAPE: 
            self.Destroy()

    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.c2 = event.GetPosition()
            self.Refresh()

    def OnMouseDown(self, event):
        self.c1 = event.GetPosition()

    def OnMouseUp(self, event):
        self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        self.Destroy()

    def OnPaint(self, event):
        global selectionOffset, selectionSize
        if self.c1 is None or self.c2 is None: return

        dc = wx.PaintDC(self.center)
        dc.SetPen(wx.Pen('black', 5))
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))

        dc.DrawRectangle(self.c1.x, self.c1.y, self.c2.x - self.c1.x, self.c2.y - self.c1.y)
        selectionOffset = (self.c1.x, self.c1.y)
        selectionSize = (abs(self.c2.x - self.c1.x), abs(self.c2.y - self.c1.y))

    def PrintPosition(self, pos):
        return str(pos.x) + "x" + str(pos.y)

class MyApp(wx.App):

    def OnInit(self):
        frame = SelectableFrame()
        return True

def get_area():
    try:
        win = gw.getWindowsWithTitle("Path of Exile")[0]
        win.activate()
    except Exception:
        ctypes.windll.user32.MessageBoxW(0, u"Path of Exile is probably not running.", u"An error happened", 0)
        return 0

    app = MyApp(redirect=False)
    app.MainLoop()
    print(f"Offset: {str(selectionOffset)}\nSelection size: {str(selectionSize)}")
    if selectionOffset:
        return selectionOffset, selectionSize
    else:
        return 0

get_area()