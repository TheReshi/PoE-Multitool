import ctypes, errorcodes, win32con, win32gui, wx
import pywinauto as pwa

global selectionOffset, selectionSize

selectionOffset = ""
selectionSize = ""

class SelectableFrame(wx.Frame):
    c1 = None
    c2 = None

    def __init__(self, parent=None, id=wx.ID_ANY, title="Multitool Capture"):
        self.style = wx.NO_BORDER

        wx.Frame.__init__(self, parent, id, title, size=wx.DisplaySize(), style=self.style)
        self.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.SetWindowStyle(wx.STAY_ON_TOP)

        self.text_canvas = wx.StaticText(self, id, "Select an area while holding down LEFT mouse button.", (0, 300), wx.DisplaySize(), wx.ALIGN_CENTER)
        self.text_canvas.SetFont(wx.Font(26, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.text_canvas.SetForegroundColour((255, 0, 0, 0))

        self.text_canvas.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.text_canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.text_canvas.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.text_canvas.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKey)

        self.SetTransparent(200)

    def OnKey(self, event):
        print("Key pressed!")
        key_code = event.GetKeyCode()
        print(key_code)
        if key_code == wx.WXK_ESCAPE:
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

        dc = wx.PaintDC(self.text_canvas)
        dc.SetPen(wx.Pen('black', 5))
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))

        dc.DrawRectangle(self.c1.x, self.c1.y, self.c2.x - self.c1.x, self.c2.y - self.c1.y)
        selectionOffset = (self.c1.x, self.c1.y)
        selectionSize = (abs(self.c2.x - self.c1.x), abs(self.c2.y - self.c1.y))

    def PrintPosition(self, pos):
        return str(pos.x) + "x" + str(pos.y)

class MyApp(wx.App):

    def OnInit(self):
        self.frame = SelectableFrame()
        self.frame.Show()
        print(self.frame.HasFocus())
        return True

def set_foreground_window(title, winclass = None):
    win_handle = pwa.findwindows.find_window(title_re=title, class_name=winclass)
    win32gui.ShowWindow(win_handle, win32con.SW_RESTORE)
    win32gui.SetWindowPos(win_handle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)  
    win32gui.SetWindowPos(win_handle, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)  
    win32gui.SetWindowPos(win_handle, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)

def get_area():
    try:
        set_foreground_window(".*Path of Exile.*", "POEWindowClass")
    except Exception:
        ctypes.windll.user32.MessageBoxW(0, u"Path of Exile is not running.\n\nError code: {0}".format(errorcodes.POE_NOT_RUNNING), u"An error happened", 0)
        return 0

    app = MyApp(redirect=False)
    app.MainLoop()
    print(f"Offset: {str(selectionOffset)}\nSelection size: {str(selectionSize)}")
    if selectionOffset and selectionSize:
        return selectionOffset, selectionSize
    else:
        return 0

get_area()