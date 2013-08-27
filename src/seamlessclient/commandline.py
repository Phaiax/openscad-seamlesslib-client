from seamlessclient import mainloop
from seamlessclient.exceptions import DisplayMessageToUserException
from seamlessclient.version import UnsupportedVersion
import argparse
import sys as _sys
import time


parser = argparse.ArgumentParser(description="""Precompile openscad files that are using calls to online functions""")

parser.add_argument('path', help="This folder is watched for changes")

#parser.add_argument('-s', '--servers', help="Display the server list, from which the sourcecode is required",
#                    action='store_true')

def run(args, block_thread = False):
    args = parser.parse_args(args)
    if args.path is not None and args.path != "":
        try:
            mainloop.instance.start_watch(args.path)
        except DisplayMessageToUserException, e:
            print e.msg
            _sys.exit()
        if block_thread:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                mainloop.instance.stop_watch()
                print "Exit."

