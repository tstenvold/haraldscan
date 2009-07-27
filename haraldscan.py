#!/usr/bin/env python
# -*- coding: utf-8 -*-
# haraldscan.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#
#Main script for the running of harald scan

from pysqlite2 import dbapi2 as sqlite
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
d = discovery.harald_discoverer()
d.set_cursor(cursor)
d.set_service(scanner.service)


#init the screen
haraldcli.init_screen()

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

        haraldcli.redraw_screen(scanner)
        haraldcli.write_screen(cursor)

#adapter not present
except bluetooth.btcommon.BluetoothError:
    scanner.cleanup(connection, cursor)
    haraldusage.bluetooth_error()

#some sql function failed
except (sqlite.OperationalError, sqlite.IntegrityError):
    scanner.cleanup(connection, cursor)
    haraldusage.no_db()

#ctrl-c caught and handled to exit gracefully
except (KeyboardInterrupt, SystemExit):
    scanner.cleanup(connection, cursor)
