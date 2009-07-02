#!/usr/bin/env python

# main.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#

import deviceclass
import discovery
import haraldsql
import time,sys,os

def move(new_x, new_y):
    print '\033[' + str(new_x) + ';' + str(new_y) + 'H'

def clear():
  print '\033[2J'

def write_screen(cursor):

    result = haraldsql.show_dev_table(cursor)

    move(0,0)

    print "HaraldScan"
    print "-"*20
    print "Press Q to Quit"
    print "-"*20
    print "MAC\t\t\tName\t\t\tClass\t\t\tManufacturer"
    print ""

    if result != None:
        for row in result:
            print row[1] + '\t' + row[2][:16] + '\t' + row[3][:16] + '\t\t' + row[4]

#Open database and get connection and cursor
connection = haraldsql.open_database()
cursor = haraldsql.get_cursor(connection)


#For Building Database should be a command line option
haraldsql.refresh_maclist(connection)
#for k, v in status.iteritems():
#    print k, ': ', v

#setup the device table for the lifetime of program
haraldsql.setup_dev_table(connection)
clear()

#Discovers devices
d = discovery.harald_discoverer()
d.set_cursor(cursor)
for i in range(1,3):
    d.find_devices(lookup_names=True)

    while True:
        d.process_event()
        write_screen(cursor)
        if d.done == True:
            break
#drops table at end of program life and close the database
haraldsql.drop_dev_table(cursor)
haraldsql.close_database(connection)
