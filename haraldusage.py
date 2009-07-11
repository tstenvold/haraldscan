#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    print "\t-w --write file\t: Outputs discovered device info to (file) specified. Overwrites any existing file\n"
    sys.exit(1)

def bluetooth_error():

    print "Error:\n\tNo Bluetooth Adapter Found. Please run 'hciconfig hci0 up' If Adapter is present but not working\n"
    sys.exit(1)

def no_db():

    print "Error:\n\tDatabase not found or Corrupt. Please run 'haraldscan.py -b'\n"
    sys.exit(1)
