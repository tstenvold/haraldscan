#!/usr/bin/env python
#
# haraldusage.py
# July 2009
# Terence Stenvold <tstenvold@gmail.com>
#
#Help info for the running of harald scan

import sys

def usage():

    print "usage: haraldscan.py [options]"
    print "Options:"
    print "\t-b --build\t: Builds MAC Addr database. Ignores all other options"
    print "\t-h --help\t: Shows this help menu"
    print "\t-w --write file\t: Outputs discovered device info to (file) specified. Overwrites any existing file"
    sys.exit(1)
