#!/usr/bin/env python
# -*- coding: utf-8 -*-
# haraldscan.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#
#Main script for the running of harald scan

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

from haraldmodules import *
import sqlite3
import time,sys,os
import bluetooth

class Harald_main:

    def __init__(self):
        self.write_file = False
        self.filename = None
        self.service = False
        self.buildb = False
        self.num_entry = 0
        self.time_start = time.time()
        self.time_interval = 15
        self.memdb = False
        self.noservice = False
        self.flush = 0

    def minus_w(self, filename):
        self.filename = filename + ".xml"
        self.write_file = True

    def cleanup(self, connection, cursor, conflush):
        haraldcli.clear()
        haraldcli.move(0,0)
        haraldsql.drop_dev_table(cursor)
        haraldsql.close_database(connection)
        if self.flush is not 0:
            haraldsql.close_database(conflush)


"""Sets up the database(s) when required."""
def init_dbcon(scanner):

    if scanner.memdb is False:
        connection = haraldsql.open_database('macinfo.db')
    else:
        connection = haraldsql.open_database_mem()
        haraldsql.build_db(connection)

    return connection

"""Runs the commands needed to flush the devices to the other database"""
def run_flushdb(con, conflush, cursor, curflush):

        haraldsql.flushdb(cursor, curflush)
        haraldsql.commit_db(conflush)
        haraldsql.commit_db(connection)

"""Sets up the scanner and processes the args"""
scanner = Harald_main()
haraldargs.handle_args(sys.argv[1:],scanner)

"""Initializes the db's connections'"""
connection = init_dbcon(scanner)
cursor = haraldsql.get_cursor(connection)

conflush = 0
if scanner.flush is not 0:
    conflush = haraldsql.open_database('macinfo-%f.db' % time.time())
    curflush = haraldsql.get_cursor(conflush)
    haraldsql.setup_dev_table(conflush)

haraldsql.setup_dev_table(connection)
num_devices = 0
num_flushed = 0

if scanner.buildb:
    haraldsql.build_db(connection)
    sys.exit(0)

#sets up the discoverer
d = discovery.harald_discoverer()
d.set_cursor(cursor)
d.set_service(scanner.service, scanner.noservice)


#init the screen
haraldcli.init_screen(scanner.time_interval)

#start the main loop
try:
    while True:

        d.find_devices(lookup_names=True)

        while True:
            d.process_event()
            if d.done == True:
                break

        haraldsql.commit_db(connection)
        num_devices = haraldsql.number_devices(cursor)

        if scanner.write_file and (num_devices + num_flushed) > scanner.num_entry:
            haraldsql.write_dev_table(cursor, scanner.filename)

        scanner.num_entry = num_devices + num_flushed

        haraldcli.redraw_screen(scanner, cursor)

        if scanner.flush is not 0 and num_devices >= scanner.flush:
            num_flushed += num_devices
            run_flushdb(connection, conflush, cursor, curflush)

#adapter not present
except bluetooth.btcommon.BluetoothError:
    scanner.cleanup(connection, cursor, conflush)
    haraldusage.bluetooth_error()

#some sql function failed
except (sqlite3.OperationalError, sqlite3.IntegrityError):
    scanner.cleanup(connection, cursor, conflush)
    haraldusage.no_db()

#ctrl-c caught and handled to exit gracefully
except (KeyboardInterrupt, SystemExit):
    if scanner.flush is not 0:
        run_flushdb(connection, conflush, cursor, curflush)
    scanner.cleanup(connection, cursor, conflush)
