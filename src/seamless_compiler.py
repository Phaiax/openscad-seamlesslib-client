#!/usr/bin/python

import seamlessclient.commandline
from sys import argv


if __name__ == '__main__':
    seamlessclient.commandline.run(argv[1:], True)