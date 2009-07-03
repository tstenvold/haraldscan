#!/usr/bin/env python

# main.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#

import deviceclass
import discovery
import haraldsql
import haraldcli
import time,sys,os


def cleanup(connection, cursor):
    haraldcli.clear()
    haraldcli.move(0,0)
    haraldsql.drop_dev_table(cursor)
    haraldsql.close_database(connection)


buildb = True
write_file = False
filename = ""

#Calls to initialize the program
connection = haraldsql.open_database()
cursor = haraldsql.get_cursor(connection)

if buildb:
    #For Building Database should be a command line option
    status = haraldsql.refresh_maclist(connection)
    #for k, v in status.iteritems():
    #    print k, ': ', v


haraldsql.setup_dev_table(connection)
d = discovery.harald_discoverer()
d.set_cursor(cursor)
haraldcli.init_screen()

try:
    while True:
        d.find_devices(lookup_names=True)

        while True:
            d.process_event()
            if d.done == True:
                break

        haraldcli.write_screen(cursor)

        if write_file:
            haraldsql.write_dev_table(self.cursor,'devices.txt')

except (KeyboardInterrupt, SystemExit):
    cleanup(connection, cursor)
