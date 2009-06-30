#!/usr/bin/env python

# main.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#

import deviceclass
import discovery
import sqlite
import time,sys,os

def move(y,x):
        sys.stdout.write("\x1b[%i;%iH"%(y+1,x+1))

def write_screen():
    result = sqlite.show_dev_table()

    move(0,0)
    
    for row in result:
        print "Mac: " + row[1]
        print "Name: " + row[2]
        print "Class: " + row[3]
        print "Manuf: " + row[4]
        print ""

#setup the device table for the lifetime of program
sqlite.setup_dev_table()

#Discovers devices
d = discovery.harald_discoverer()

d.find_devices(lookup_names=True)
d.process_inquiry()

while d.done == False:
    time.sleep(1)
    write_screen()
    if d.done == True:
        break

#drops table at end of program life
sqlite.drop_dev_table()

