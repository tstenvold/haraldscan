#!/usr/bin/env python
# -*- coding: utf-8 -*-
# haraldscan.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#
# Test script to push as many device(fake) in db


from haraldmodules import *
import sqlite3
import time,sys,os
import bluetooth

class Harald_main:

    def __init__(self):
        self.write_file = False
        self.filename = ""
        self.service = False
        self.buildb = False
        self.num_entry = 0
        self.time_start = time.time()
        self.time_interval = 15
        self.memdb = False
        self.noservice = False
        self.flush = 0

    def minus_w(self, filename):
        self.filename = filename
        self.write_file = True

    def cleanup(self, connection, cursor, conflush):
        haraldcli.clear()
        haraldcli.move(0,0)
        haraldsql.drop_dev_table(cursor)
        haraldsql.close_database(connection)
        if self.flush is not 0:
            haraldsql.close_database(conflush)

def init_dbcon(scanner):

    if scanner.memdb is False:
        connection = haraldsql.open_database('macinfo.db')
    else:
        connection = haraldsql.open_database_mem()
        haraldsql.build_db(connection)

    return connection

def run_flushdb(con, conflush, cursor, curflush):

        haraldsql.flushdb(cursor, curflush)
        haraldsql.commit_db(conflush)
        haraldsql.commit_db(connection)

#init main class and handle args
scanner = Harald_main()
haraldargs.handle_args(sys.argv[1:],scanner)


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
names = ["ԱԵՈՊԼՎ՞ՉՅ","ঘণধছরমফষ", "あけちねと","サッダソヅニ","ضثسعغب", "你好我的狗是朋友",
        "ԱԵՈՊԼՎ՞ՉՅ","ঘণধছরমফষ", "あけちねと","サッダソヅニ","ضثسعغب", "你好我的狗是朋友",
        "ԱԵՈՊԼՎ՞ՉՅ","ঘণধছরমফষ", "あけちねと","サッダソヅニ","ضثسعغب", "你好我的狗是朋友"]
#start the main loop
try:
    i = 0
    for e in names:
        addr = "00:00:00:00:00:%02d" %  i
        i+=1
        name = e
        device_class = 0x420209
        devclass = deviceclass.majordev_class(device_class)
        devman = haraldsql.mac_resolve(cursor, addr)

        haraldsql.insert_dev_table(cursor, addr, name, devclass, devman)

        haraldsql.commit_db(connection)
        num_devices = haraldsql.number_devices(cursor)
        scanner.num_entry = num_devices + num_flushed

        haraldcli.redraw_screen(scanner, cursor)

        if scanner.write_file:
            haraldsql.write_dev_table(cursor, scanner.filename)

        if scanner.flush is not 0 and num_devices >= scanner.flush:
            num_flushed += num_devices
            run_flushdb(connection, conflush, cursor, curflush)

#ctrl-c caught and handled to exit gracefully
except (KeyboardInterrupt, SystemExit):
    if scanner.flush is not 0:
        run_flushdb(connection, conflush, cursor, curflush)
    scanner.cleanup(connection, cursor, conflush)
