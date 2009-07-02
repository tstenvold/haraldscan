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


def init_screen():

    clear()
    print " "*35, 
    print "Harald Scan"
    print "#"*80
    print "Press Ctrl-Z or Ctrl-C to Quit"
    print "#"*80
    print "MAC\t\t\tName\t\t\tClass\t\t\tManufacturer"

def write_screen(cursor):

    result = haraldsql.show_dev_table(cursor)

    move(0,6)
    
    if result != None:
        for row in result:
            print row[1] + '\t' + row[2][:16] + '\t' + row[3][:16] + '\t\t' + row[4]

def cleanup(connection, cursor):
    haraldsql.drop_dev_table(cursor)
    haraldsql.close_database(connection)
    

buildb = False
write_file = False

if buildb:
    #For Building Database should be a command line option
    haraldsql.refresh_maclist(connection)
    #for k, v in status.iteritems():
    #    print k, ': ', v


#Calls to initialize the program
connection = haraldsql.open_database()
cursor = haraldsql.get_cursor(connection)
haraldsql.setup_dev_table(connection) 
d = discovery.harald_discoverer()
d.set_cursor(cursor)
init_screen()

try:
    for i in range(1,10):
        d.find_devices(lookup_names=True)

        while True:
            d.process_event()
            write_screen(cursor)
            if d.done == True:
                break
except (KeyboardInterrupt, SystemExit):
    cleanup(connection, cursor)
