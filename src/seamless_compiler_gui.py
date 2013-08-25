#!/usr/bin/python

from sys import argv


if __name__ == '__main__':
    if len(argv) > 1:
        import seamlessclient.commandline
        seamlessclient.commandline.run(argv[1:], True)
    else:
        import seamlessclient.gui
        seamlessclient.gui.run()
    