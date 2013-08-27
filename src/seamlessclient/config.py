import wx
import simplejson
from seamlessclient import get_config_path, default_servers

class Config(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    
    path = ""
    def getPath(self):
        if self.path == "":
            self.path = get_config_path()
        return self.path
    
    def getFile(self, mode="r"):
        return open(self.getPath(), mode)
    
    config = None
    def readConfig(self):
        try:
            cfile = self.getFile()
            self.config = simplejson.load(cfile, encoding="UTF-8")
            cfile.close()
        except IOError:
            self.config = {}
    
    def writeConfig(self):
        cfile = self.getFile(mode="w+")
        simplejson.dump(self.config, cfile, encoding="UTF-8", indent="  ")
        cfile.close()
    
    def __init__(self):
        if self.config is None:
            self.readConfig()
    
    def save(self, name, value):
        self.config[name] = value
        self.writeConfig()
        pass
    
    def get(self, name, default):
        if name in self.config:
            return self.config[name]
        return default
    
    
    def get_watch_folder(self):
        return self.get('watch_folder', '')
    
    def set_watch_folder(self, watch_folder):
        self.save('watch_folder', watch_folder)
    
    def get_server(self):
        return self.get('server', default_servers[0])
    
    def set_server(self, server):
        self.save('server', server)
        
    def save_module(self, name, module_dict, trigger_write=True):
        if 'modulecache' not in self.config:
            self.config['modulecache'] = {}
        self.config['modulecache'][name] = module_dict
        if trigger_write:
            self.writeConfig()
    
    def get_module(self, name):
        return self.config['modulecache'][name]
    
    def clear(self):
        self.config = {}
        self.writeConfig()