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

from pysqlite2 import dbapi2 as sqlite
import deviceclass
import discovery
import haraldsql
import haraldcli
import haraldargs
import haraldusage
import time,sys,os
import lightblue

class Harald_main:

    def __init__(self):
        self.write_file = False
        self.filename = None
        self.service = False
        self.buildb = False
        self.num_entry = 0

    def minus_w(self, filename):
        self.filename = filename
        self.write_file = True

    def minus_b(self):
        self.buildb = True

    def minus_s(self):
        self.service = True

    def cleanup(self, connection, cursor):
        haraldcli.clear()
        haraldcli.move(0,0)
        haraldsql.drop_dev_table(cursor)
        haraldsql.close_database(connection)


#init main class and handle args
scanner = Harald_main()
haraldargs.cmdargs(sys.argv[1:],scanner)

#init the database and get connections
connection = haraldsql.open_database()
cursor = haraldsql.get_cursor(connection)
haraldsql.setup_dev_table(connection)
num_devices = 0

if scanner.buildb:
    haraldargs.build_db(connection)

#sets up the discoverer
dosx = discovery.harald_lightblue()
dosx.set_cursor(cursor)
dosx.set_service(scanner.service)

#init the screen
haraldcli.init_screen()

#start the main loop
try:
    while True:

        dosx.find_devices()

        haraldsql.commit_db(connection)
        num_devices = haraldsql.number_devices(cursor)

        if scanner.write_file and num_devices > scanner.num_entry:
            haraldsql.write_dev_table(cursor, scanner.filename)

        if num_devices > scanner.num_entry:
            scanner.num_entry = num_devices

        haraldcli.redraw_screen(scanner)
        haraldcli.write_screen(cursor)

#some sql function failed
except (sqlite.OperationalError, sqlite.IntegrityError):
    scanner.cleanup(connection, cursor)
    haraldusage.no_db()

#adapter not present
except lightblue._lightbluecommon.BluetoothError:
    scanner.cleanup(connection, cursor)
    haraldusage.bluetooth_error()

#ctrl-c caught and handled to exit gracefully
except (KeyboardInterrupt, SystemExit):
    scanner.cleanup(connection, cursor)
