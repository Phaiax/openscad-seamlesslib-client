from seamlessclient.webfetch import run_server_request
from seamlessclient import get_client_version

not_up_to_date_message = """The Seamless Compiler is not up to date. \n
Current version: %d, Most recent version: %d\n
Please update this programm."""

old_server_message = """The Seamless Server (online library) you want to connect is not up to date. \n
Current Compiler version: %d, Maximum version supported by server: %d\n
Please choose another server or update server version info (if you're developing)."""

server_version_cache = {}

def get_server_version_info():
    if len(server_version_cache) == 0:
        server_version_cache.update(run_server_request('version-info'))
    return server_version_cache

def is_this_client_supported():
    server_info = get_server_version_info()
    client_version = get_client_version()
    return client_version >= server_info['min_supported_client'] and client_version <= server_info['most_recent_client_version']

def raise_if_unsupported():
    if not is_this_client_supported():
        server_info = get_server_version_info()
        client_version = get_client_version()
        if client_version > server_info['most_recent_client_version']:
            raise UnsupportedVersion(old_server_message %
                                     (client_version, server_info['most_recent_client_version']))
        else:
            raise UnsupportedVersion( not_up_to_date_message %
                                      (client_version, server_info['most_recent_client_version']))

def is_most_recent_version():
    server_info = get_server_version_info()
    client_version = get_client_version()
    return client_version >= server_info['most_recent_client_version']

class UnsupportedVersion(Exception):
    def __init__(self, msg):
        self.msg = msg
