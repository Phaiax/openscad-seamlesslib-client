
from seamlessclient.config import Config
from seamlessclient.webfetch import NotFound
from seamlessclient import webfetch

def get_by_uniquename(uniquename):
    try:
        return Config().get_module(uniquename)
    except:
        mod = webfetch.get_by_uniquename(uniquename)
        if mod['finished'] is True:
            Config().save_module(uniquename, mod)
        return mod
