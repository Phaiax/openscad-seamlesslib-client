
from seamlessclient import mainloop
from seamlessclient.config import Config
import Queue
import os.path
import sys
import wx
from seamlessclient.version import UnsupportedVersion

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
        wx.Frame.__init__(self, parent, title=title, size=(-1, -1))
        
        self.queue = queue
        self.timer_update_intervall = 100

        self.Wsizer_select_folder = wx.BoxSizer(wx.HORIZONTAL)

        self.Wtext_choose_folder = wx.StaticText(self, label="Select Folder to scan for .scad files", style=wx.ALIGN_CENTER)
        self.Wselected_folder = wx.TextCtrl(self, 2)
        self.Wselected_folder.SetEditable(False)
        self.Wselected_folder.SetValue(Config().get_watch_folder())
        self.Wchoose_folder_button = wx.Button(self, -1, "Choose Folder")
        self.Bind(wx.EVT_BUTTON, self.on_choose_watch_folder, self.Wchoose_folder_button)
        
        self.Wsizer_select_folder.Add(self.Wtext_choose_folder, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 6)
        self.Wsizer_select_folder.Add(self.Wselected_folder, 4, wx.EXPAND)
        self.Wsizer_select_folder.Add(self.Wchoose_folder_button, 1, wx.EXPAND)
        
        self.Wsizer_actions = wx.BoxSizer(wx.HORIZONTAL)
        self.Wtext_current_status = wx.StaticText(self)
        self.Wstart_button = wx.Button(self, -1, "Start")
        self.Bind(wx.EVT_BUTTON, self.on_start, self.Wstart_button)
        self.Wstop_button = wx.Button(self, -1, "Stop")
        self.Bind(wx.EVT_BUTTON, self.on_stop, self.Wstop_button)

        self.Wsizer_actions.Add(self.Wtext_current_status, 7, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 6)
        self.Wsizer_actions.Add(self.Wstart_button, 1, wx.EXPAND)
        self.Wsizer_actions.Add(self.Wstop_button, 1, wx.EXPAND)

        self.Wconsole = wx.TextCtrl(self, 5, style=wx.TE_MULTILINE)
        self.Wconsole.SetEditable(False)
        
        # Use some sizers to see layout options
        self.Wsizer = wx.BoxSizer(wx.VERTICAL)
        self.Wsizer.AddSpacer((10, 10))
        self.Wsizer.Add(self.Wsizer_select_folder, 1, wx.EXPAND)
        self.Wsizer.AddSpacer((10, 10))
        self.Wsizer.Add(self.Wsizer_actions, 1, wx.EXPAND)
        self.Wsizer.Add(self.Wconsole, 15, wx.EXPAND)

        self.Wtimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.timer_update, self.Wtimer)
        self.Wtimer.Start(self.timer_update_intervall)

        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        # Layout sizers
        self.SetSizer(self.Wsizer)
        self.SetAutoLayout(1)
        self.Wsizer.Fit(self)
        
        self.init_menu()
        self.update_status()
        
        self.Center()
        self.Show(True)

    def init_menu(self):
        # Setting up the menu.
        self.Wmenu_pref = wx.Menu()
        
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        self.Wmenu_pref_server = self.Wmenu_pref.Append(wx.ID_SETUP, "&Server", "Select Server")
        
        # self.servermenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        # self.menu_pref.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.on_menu_pref_server, self.Wmenu_pref_server)
        # self.servermenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        
        # Creating the menubar.
        self.Wmenu_bar = wx.MenuBar()
        self.Wmenu_bar.Append(self.Wmenu_pref, "&Preferences")  # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(self.Wmenu_bar)
    def on_menu_pref_server(self, e):
        pref_server_dialog = wx.TextEntryDialog(self, "Select server (url without http)", "Select server", Config().get_server())
        pref_server_dialog.ShowModal()
        Config().set_server(pref_server_dialog.GetValue())
        print "Server changed to %s" % Config().get_server()
        pref_server_dialog.Destroy()
        
    def timer_update(self, e):
        try:
            while True:
                self.Wconsole.AppendText(self.queue.get_nowait())
        except:
            pass
        self.Wtimer.Start(self.timer_update_intervall)
        
    
    def on_choose_watch_folder(self, e):
        """ Open a file"""
        folder = Config().get_watch_folder()
        dlg = wx.DirDialog(self, "Choose a folder", folder, style=wx.DD_DIR_MUST_EXIST | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            folder = dlg.GetPath()
            Config().set_watch_folder(folder)
            self.Wselected_folder.SetValue(folder)
        dlg.Destroy()
        
    def on_stop(self, e):
        mainloop.instance.stop_watch()
        self.update_status()
        
    def on_start(self, e):
        folder = Config().get_watch_folder()
        if os.path.isdir(folder):
            try:
                mainloop.instance.start_watch(folder)
            except UnsupportedVersion, e:
                self.show_message(message=e.msg)
        else:
            self.show_message(message="Please select folder")
        self.update_status()
        
    def show_message(self, message, title="Seamless Compiler"):
        message_dialog = wx.MessageDialog(self, message, title, wx.OK)
        message_dialog.ShowModal()
        message_dialog.Destroy()
        
    def on_close(self, e):
        restore_stdout()
        self.on_stop(e)
        self.Destroy()
        
        
    def update_status(self):
        if mainloop.instance.is_running():
            self.Wtext_current_status.SetLabel("Status: running")
            self.Wstop_button.Enable()
            self.Wstart_button.Disable()
            self.Wchoose_folder_button.Disable()
        else:
            self.Wtext_current_status.SetLabel("Status: stopped")
            self.Wstop_button.Disable()
            self.Wstart_button.Enable()
            self.Wchoose_folder_button.Enable()
            

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
