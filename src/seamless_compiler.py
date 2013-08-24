#!/usr/bin/python

import application.commandline
from sys import argv


if __name__ == '__main__':
    application.commandline.run(argv[1:], True)