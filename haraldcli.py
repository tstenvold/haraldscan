#!/usr/bin/env python
# -*- coding: utf-8 -*-
# haraldcli.py
# July 2009
# Terence Stenvold <tstenvold@gmail.com>
#
#Provides functions for the console interface

#This file is part of Haraldscan.
#
#Haraldscan is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License Version 3 as
#published by the Free Software Foundation.
#
#Haraldscan is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License Version 3 for more details.
#
#You should have received a copy of the GNU General Public License
#Version 3 along with Haraldscan.  If not, see <http://www.gnu.org/licenses/>.

import haraldsql
import haraldusage
import time,sys,os

def move(new_x, new_y):
    print '\033[' + str(new_x) + ';' + str(new_y) + 'H'

def right(count):

    for i in range(1,count):
	    sys.stdout.write("\x1b[C")

def moveUp(lines):
  print '\033[' + str(lines) + 'A'


def clear():
  print '\033[2J'

def clrtoeol():
  print '\033[K'

def savecursor():
	sys.stdout.write("\x1b7")

def restorecursor():
	sys.stdout.write("\x1b8")

def columns(col1, col2, col3, col4):

    print col1[:17],
    right(20-len(col1[:17]))
    print col2[:13],
    right(15-len(col2[:15]))
    print col3[:18],
    right(20-len(col3[:20]))
    print col4[:25]

def init_screen(time_interval):

    clear()
    move(0,0)
    title_bar(0,time.time(),time_interval)
    savecursor()

def clearwholescreen():

    move(0,0)

    for i in range(0,24):
        move(0,i)
        clrtoeol()

    move(0,0)

def redraw_screen(scanner):
    clearwholescreen()
    title_bar(scanner.num_entry, scanner.time_start, scanner.time_interval)
 
def percentage_time(num_devices,time_start,time_interval):
	
    if (time.time() - time_start) <= time_interval : 
        return num_devices
    else:
	return (num_devices / (time.time()-time_start) * time_interval)		
#TODO
#add length of scan and dev per time option
def title_bar(num_devices, time_start, time_interval):
    print " "*35,
    print "Harald Scan"
    print "#"*80
    print "Press Ctrl-C to Quit",	
    mid1 = "%0.2f Device per 15 mins" % percentage_time(num_devices,time_start,time_interval) 
    mid2 = "%1d device(s) found" % num_devices
    print " "*(30 - len(mid1)),
    print mid1,
    print " "*(26 - len(mid2)),
    print mid2
    print "#"*80
    print ""
    columns("MAC","Name","Class","Vendor")

def write_screen(cursor):

    result = haraldsql.show_dev_table(cursor)

    restorecursor()

    if result != None:
        for row in result:
            columns(row[1],row[2],row[3],row[4])

if __name__ == '__main__':
  haraldusage.usage()
