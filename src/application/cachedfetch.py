
from application.config import Config
from application.webfetch import NotFound
from application import webfetch

def get_by_uniquename(uniquename):
    try:
        return Config().get_module(uniquename)
    except:
        mod = webfetch.get_by_uniquename(uniquename)
        Config().save_module(uniquename, mod)
        return mod
