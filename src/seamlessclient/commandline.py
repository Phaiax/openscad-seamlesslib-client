from seamlessclient import mainloop
import argparse
import time


parser = argparse.ArgumentParser(description="""Precompile openscad files that are using calls to online functions""")

parser.add_argument('path', help="This folder is watched for changes")

#parser.add_argument('-s', '--servers', help="Display the server list, from which the sourcecode is required",
#                    action='store_true')

def run(args, block_thread = False):
    args = parser.parse_args(args)
    if args.path is not None and args.path != "":
        mainloop.instance.start_watch(args.path)
        if block_thread:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                mainloop.instance.stop_watch()
                print "Exit."

