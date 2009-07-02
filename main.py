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

    print "MAC\tName\tClass\tManufacturer"

    if result != None:
        for row in result:
            print row[1] + '\t' + row[2] + '\t' + row[3] + '\t' + row[4]

#Open database and get connection and cursor
connection = haraldsql.open_database()
cursor = haraldsql.get_cursor(connection)


#For Building Database
#status = haraldsql.refresh_maclist(connection)
#for k, v in status.iteritems():
#    print k, ': ', v

#setup the device table for the lifetime of program
haraldsql.setup_dev_table(connection)
clear()

#Discovers devices
d = discovery.harald_discoverer()
d.set_cursor(cursor)
for i in range(1,5):
    d.find_devices(lookup_names=True)
    print i

    while True:
        d.process_event()
        write_screen(cursor)
        if d.done == True:
            break
#drops table at end of program life and close the database
haraldsql.drop_dev_table(cursor)
haraldsql.close_database(connection)
