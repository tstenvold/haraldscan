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

import sqlite3
import deviceclass
import discovery
import haraldsql
import haraldcli
import haraldargs
import haraldusage
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

    def minus_w(self, filename):
        self.filename = filename
        self.write_file = True

    def cleanup(self, connection, cursor):
        haraldcli.clear()
        haraldcli.move(0,0)
        haraldsql.drop_dev_table(cursor)
        haraldsql.close_database(connection)

def init_dbcon(scanner):
    if scanner.memdb is False:
        connection = haraldsql.open_database()
    else:
        connection = haraldsql.open_database_mem()
        haraldsql.build_db(connection)

    return connection


#init main class and handle args
scanner = Harald_main()
haraldargs.handle_args(sys.argv[1:],scanner)

connection = init_dbcon(scanner)
cursor = haraldsql.get_cursor(connection)
haraldsql.setup_dev_table(connection)
num_devices = 0

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

        if scanner.write_file and num_devices > scanner.num_entry:
            haraldsql.write_dev_table(cursor, scanner.filename)

        if num_devices > scanner.num_entry:
            scanner.num_entry = num_devices

        haraldcli.redraw_screen(scanner, cursor)

#adapter not present
except bluetooth.btcommon.BluetoothError:
    scanner.cleanup(connection, cursor)
    haraldusage.bluetooth_error()

#some sql function failed
except (sqlite3.OperationalError, sqlite3.IntegrityError):
    scanner.cleanup(connection, cursor)
    haraldusage.no_db()

#ctrl-c caught and handled to exit gracefully
except (KeyboardInterrupt, SystemExit):
    scanner.cleanup(connection, cursor)
