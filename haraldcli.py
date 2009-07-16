#!/usr/bin/env python
# -*- coding: utf-8 -*-
# haraldcli.py
# July 2009
# Terence Stenvold <tstenvold@gmail.com>
#
#Provides functions for the console interface

import haraldsql
import haraldusage
import sys,os

def move(new_x, new_y):
    print '\033[' + str(new_x) + ';' + str(new_y) + 'H'

def right(count):

    for i in range(1,count):
	    sys.stdout.write("\x1b[C")

def clear():
  print '\033[2J'

def clrtoeol():
  print '\033[K'


def savecursor():
	sys.stdout.write("\x1b7")

def restorecursor():
	sys.stdout.write("\x1b8")

def columns(col1, col2, col3, col4):

    clrtoeol()
    print col1[:17],
    right(20-len(col1[:17]))
    print col2[:13],
    right(15-len(col2[:15]))
    print col3[:18],
    right(20-len(col3[:20]))
    print col4[:25]
def init_screen():

    clear()
    move(0,0)
    print " "*35,
    print "Harald Scan"
    print "#"*80
    print "Press Ctrl-C to Quit"
    print "#"*80
    print ""
    columns("MAC","Name","Class","Vendor")
    savecursor()

def write_screen(cursor):

    result = haraldsql.show_dev_table(cursor)

    restorecursor()

    if result != None:
        for row in result:
            columns(row[1],row[2],row[3],row[4])

if __name__ == '__main__':
  haraldusage.usage()
