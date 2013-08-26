
from seamlessclient import mainloop
from seamlessclient.config import Config
import Queue
import os.path
import sys
import wx

class GUI(object):
    def __init__(self, queue):
        self.app = wx.App(False)
        self.queue = queue
        self.make_window()

    def make_window(self):
        self.frame = CompilerMainFrame(None, "Seamless Compiler For OpenSCAD", self.queue)
        

    def run(self):
        self.app.MainLoop()
        
    

# wxFrame = Window, wxWindow = Base class for Buttons etc
class CompilerMainFrame(wx.Frame):
    """ We simply derive a new class of Frame. """
    def __init__(self, parent, title, queue):
        wx.Frame.__init__(self, parent, title=title, size=(-1,-1))
        
        self.queue = queue
        self.timer_update_intervall = 100

        self.text_choose_server = wx.StaticText(self,label="Select server")
        self.sizer_select_server = wx.BoxSizer(wx.HORIZONTAL)
        self.selected_server = wx.TextCtrl(self, 2)
        self.selected_server.SetValue(Config().get_server())
        self.Bind(wx.EVT_TEXT, self.on_server_changed, self.selected_server)
        
        self.sizer_select_server.Add(self.text_choose_server, 1, wx.EXPAND)
        self.sizer_select_server.Add(self.selected_server, 4, wx.EXPAND)
        
        self.text_choose_folder = wx.StaticText(self,label="Select Folder to scan for .scad files")
        self.sizer_select_folder = wx.BoxSizer(wx.HORIZONTAL)
        self.selected_folder = wx.TextCtrl(self, 2)
        self.selected_folder.SetEditable(False)
        self.selected_folder.SetValue(Config().get_watch_folder())
        self.choose_folder_button = wx.Button(self, -1, "Choose Folder")
        self.Bind(wx.EVT_BUTTON, self.on_choose_watch_folder, self.choose_folder_button)
        
        self.sizer_select_folder.Add(self.selected_folder, 4, wx.EXPAND)
        self.sizer_select_folder.Add(self.choose_folder_button, 1, wx.EXPAND)
        
        self.sizer_actions = wx.BoxSizer(wx.HORIZONTAL)
        self.text_current_status = wx.StaticText(self)
        self.start_button = wx.Button(self, -1, "Start")
        self.Bind(wx.EVT_BUTTON, self.on_start, self.start_button)
        self.stop_button = wx.Button(self, -1, "Stop")
        self.Bind(wx.EVT_BUTTON, self.on_stop, self.stop_button)

        self.sizer_actions.Add(self.text_current_status, 7, wx.EXPAND )
        self.sizer_actions.Add(self.start_button, 1, wx.EXPAND)
        self.sizer_actions.Add(self.stop_button, 1, wx.EXPAND)

        self.console = wx.TextCtrl(self, 5, style=wx.TE_MULTILINE)
        self.console.SetEditable(False)
        
        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.text_choose_folder, 1, wx.EXPAND)
        self.sizer.Add(self.sizer_select_folder, 1, wx.EXPAND)
        self.sizer.Add(self.sizer_select_server, 1, wx.EXPAND)
        self.sizer.Add(self.sizer_actions, 1, wx.EXPAND)
        self.sizer.Add(self.console, 15, wx.EXPAND)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_update, self.timer)
        self.timer.Start(self.timer_update_intervall)

        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        #Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.update_status()
        self.Center()
        self.Show(True)

    def timer_update(self, e):
        try:
            while True:
                self.console.AppendText(self.queue.get_nowait())
        except:
            pass
        self.timer.Start(self.timer_update_intervall)
        
    def on_server_changed(self, e):
        server = self.selected_server.GetValue()
        print "Now using: %s" % server
        Config().set_server(server)

    def on_choose_watch_folder(self,e):
        """ Open a file"""
        folder = Config().get_watch_folder()
        dlg = wx.DirDialog(self, "Choose a folder", folder, style=wx.DD_DIR_MUST_EXIST|wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            folder = dlg.GetPath()
            Config().set_watch_folder(folder)
            self.selected_folder.SetValue(folder)
        dlg.Destroy()
        
    def on_stop(self, e):
        mainloop.instance.stop_watch()
        self.update_status()
        
    def on_start(self, e):
        folder = Config().get_watch_folder()
        if os.path.isdir(folder):
            mainloop.instance.start_watch(folder)
        self.update_status()
        
    def on_close(self, e):
        restore_stdout()
        self.on_stop(e)
        self.Destroy()
        
        
    def update_status(self):
        if mainloop.instance.is_running():
            self.text_current_status.SetLabel("Status: running")
        else:
            self.text_current_status.SetLabel("Status: stopped")
            

class StdoutCatcher(object):
    def __init__(self, queue):
        self.queue = queue
    def write(self, text):
        self.queue.put(text)

def run():
    catcher = StdoutCatcher(Queue.Queue())
    sys.stdout_bu = sys.stdout
    sys.stdout = catcher
    G = GUI(catcher.queue)
    G.run()

def restore_stdout():
    sys.stdout = sys.stdout_bu  # @UndefinedVariable