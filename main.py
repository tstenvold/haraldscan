#!/usr/bin/env python

# main.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#

import deviceclass
import discovery
import sqlite

#setup the device table for the lifetime of program
sqlite.setup_dev_table()

#shows devices in table
for i in range (1,10):

    #gets devices
    dis_devices = discovery.discover()

    result = sqlite.show_dev_table()

    for row in result:
        print "Mac: " + row[1] + " Name: " + row[2] + " Class: " + row[3] + " Manuf: " + row[4]

    print ""

#drops table at end of program life
sqlite.drop_dev_table()
