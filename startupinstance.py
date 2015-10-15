#!/bin/python
import os
import sys

__author__ = 'bgcolor'


def main():
    if len(sys.argv) > 2:
        dir = sys.argv[1]
        port = sys.argv[2]
    else:
        print 'directory and port are needed.'
        exit()

    os.chdir(dir)
    os.system('./start.sh')

if __name__ == '__main__':
    main()
