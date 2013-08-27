import os
import platform

app_name = "openscad-seamless-compiler"

config_files = {'Linux' : "$HOME/.config/seamless-compiler.config",
                'Windows' : "%APPDATA%\\seamless-compiler.config",
                'Darwin' : "$HOME/.config/seamless-compiler.config" }

default_servers = ['seamless.invisibletower.de']
#default_servers = ['localhost:8000']

def get_client_version():
    return 2

compiled_filename_extension = ".compiled.scad"
scad_extension = ".scad"
test_path = os.path.join(os.getcwd(), "folderwatchtestdirectory")

def get_os():
    return platform.system()

def get_config_path():
    path = config_files[get_os()]
    if "$HOME" in path:
        path = path.replace("$HOME", os.environ['HOME'])
    if "%APPDATA%" in path:
        path = path.replace("%APPDATA%", os.environ['APPDATA'])
    return path