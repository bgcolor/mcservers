#!/bin/python
__author__ = 'bgcolor'

import sys
import os
import re

def main():
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        print 'port is needed.'
        exit()

    pids = []
    pre = re.compile('^root\s+(\d+)\s')
    with os.popen('ps -eF | grep minecraft.*%s' % (port)) as f:
        for l in f.readlines():
            if l.find('grep') == -1:
                # res = re.search('^root\s+(\d)+\s', l)
                res = pre.match(l)
                pids.append(res.group(1))
    if len(pids) > 0:
        for pid in pids:
            if os.system('kill %s' % (pid)) == 0:
                print 'killed %s' % (pid)

if __name__ == '__main__':
    main()