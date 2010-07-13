#!/usr/bin/python
# -*- coding: utf-8 -*-
# Authors:
#   Carson Farrell
#   Terence Stenvold <tstenvold@gmail.com>
# Date: June 26th 2009
#
# Written to read the MACINFO file into an sqlite3 database called macinfo.db for
# the haraldscanner program to work with. This script assumes that data given to it
# is in the correct format (comma seperated, two column; ie: 11:22:33, Spam)
# and makes no attempt to guess what the input means.
#
# This script will print the status (new or existing) of each entry in the file
# once it attempts to insert it into the database.

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
import time,sys,os
import haraldusage

"""Represents a mapping between prefix and vendor. Using this instead of a dictionary
so that validation business logic can be placed in later if needed."""
class MacAddress:

    def __init__(self, prefix, maker):
        self.prefix = unicode(prefix,"utf-8")
        self.maker = unicode(maker,"utf-8")


"""Checks if Database exists"""
def chk_database():

        if os.path.isfile("macinfo.db") == True:
            return True
        else:
            return False

"""Builds the database with MAC addresses"""
def build_db(connection):

    status = refresh_maclist(connection)
    for k, v in status.iteritems():
       print k, ': ', v
    print "Database Built"

"""Opens Database and returns the cursor to it"""
def open_database(namedb):

            con = sqlite3.connect(namedb)
            con.text_factory = str

            return con

"""Opens Database in memory and returns the cursor to it"""
def open_database_mem():

            con = sqlite3.connect(':memory:')
            con.text_factory = str

            return con

def get_cursor(connection):

        return connection.cursor()

"""Closes the Database duh"""
def close_database(connection):

    connection.commit()
    connection.close()

"""Flushes entries from one table to another"""
def flushdb(cursor, curflush):

    query = 'SELECT * FROM devices'
    query2 = 'INSERT INTO devices (macaddr, name, devclass, vendor, timestamp) VALUES (?, ?, ?, ?, ?);'
    query3 = 'DELETE FROM devices'

    try:
        result = cursor.execute(query)
        if result != None:
            for row in result:
                curflush.execute(query2,(row[1],row[2],row[3],row[4],row[5]))
        cursor.execute(query3)
    except sqlite3.IntegrityError:
        raise

"""Creates an SQLite database in an existing database.
If any error occurs, no operation is performed"""
def create_base_table(cursor):

    create_statement  = 'CREATE TABLE IF NOT EXISTS macinfo('
    create_statement += 'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    create_statement += 'prefix char(10) UNIQUE,'
    create_statement += 'vendor varchar(100));'

    cursor.execute(create_statement)

"""Creates the device table in the database
If any error occurs, no operation is performed"""
def create_dev_table(cursor):

    create_dev  = 'CREATE TABLE IF NOT EXISTS  devices('
    create_dev += 'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    create_dev += 'macaddr char(18) UNIQUE,'
    create_dev += 'name varchar(100),'
    create_dev += 'devclass varchar(100),'
    create_dev += 'vendor varchar(100),'
    create_dev += 'timestamp varchar(100));'

    cursor.execute(create_dev)

"""Drops the device table in the database should be run everytime program starts
in case of any premature program termination that results in the table being persistant
after the program closes
If any error occurs, no operation is performed"""
def drop_dev_table(cursor):

    cursor.execute('DROP TABLE IF EXISTS devices;')

"""Inserts the values represented by a MacAddress object into an existing database.
Returns true if the value is unique, false otherwise"""
def insert_address_object(address, cursor):

    query = 'INSERT INTO macinfo(prefix, vendor) VALUES (?, ?);'

    try:
        cursor.execute(query, (address.prefix, address.maker))
        return True;
    except sqlite3.IntegrityError:
        pass
        return False;

"""Inserts a device into the device table in the existing database."""
def insert_dev_table(cursor, addr, name, devclass, vendor):

    query = 'INSERT INTO devices (macaddr, name, devclass, vendor, timestamp) VALUES (?, ?, ?, ?, ?);'

    try:
        cursor.execute(query, (addr, name.rstrip('\n'), devclass.rstrip('\n'), vendor.rstrip('\n'), time.time()))
    except sqlite3.IntegrityError:
        pass

"""Commits current changes to database"""
def commit_db(connection):

    connection.commit()

"""Attempts to enter the data found in the MACLIST file into the database specified
on the first line on the function."""
def refresh_maclist(connection):

    cursor = connection.cursor()
    fp = open('MACLIST', 'rb')

    if fp == None:
        print "Could not Open File"
        system.exit(1)

    try:
        create_base_table(cursor)
    except sqlite3.OperationalError:
        raise

    status = {}

    for line in fp:
        mac_address = MacAddress(line[0:8], line[9:])

        if insert_address_object(mac_address, cursor):
            status[mac_address.prefix] = 'Added'
        else:
            status[mac_address.prefix] = 'Existed'


    connection.commit()
    return status

"""Sets up the devices table by destroying it and creating
a new table. Should be run at the begining of the program"""
def setup_dev_table(connection):

    cursor = connection.cursor()

    try:
        drop_dev_table(cursor)
        create_dev_table(cursor)
    except sqlite3.OperationalError:
        raise

    connection.commit()

"""Shows the devices table by returning the results of the query"""
def show_dev_table(cursor):

    try:
        cursor.execute('SELECT * FROM devices WHERE id >= ((SELECT max(id) FROM devices) - 15);')
        return cursor
    except sqlite3.IntegrityError:
        return 0

"""Writes the devices table to a file specified
by the parameter passed in"""
def write_dev_table(cursor, filename):

    if not os.path.isfile(filename):
        fp = open(filename, 'wb')
        fp.write("<?xml version=\"1.0\"?>\n")
    else
        fp = open(filename, 'wb')

    if fp == None:
        print "Could not open File"
        sys.exit(1)

    results = show_dev_table(cursor)

    fp.write("<devices>\n")

    for row in results:
        fp.write("\t<device>\n")
        fp.write("\t<name>%s</name>\n" % row[1])
        fp.write("\t<address>%s</address>\n" % row[2])
        fp.write("\t<class>%s</class>\n" % row[3])
        fp.write("\t<vendor>%s</vendor>\n" % row[4])
        fp.write("\t</device>\n")

    fp.write("<devices>\n")
    fp.close()

"""Returns the number of entries"""
def number_devices(cursor):

    try:
        cursor.execute('SELECT COUNT(*) FROM devices;')
        row = cursor.fetchone()
        if row == None:
            return 0
        else:
            return int(row[0])
    except sqlite3.IntegrityError:
        return 0

"""Returns the number of entries"""
def device_exists(cursor, addr):

    query = 'SELECT * FROM devices WHERE macaddr LIKE ?;'

    try:
        cursor.execute(query, (addr,))
        row = cursor.fetchone()
        if row == None:
            return False
        else:
            return True
    except (sqlite3.OperationalError, sqlite3.IntegrityError):
        return False

"""Resolves mac address to a vendor
Take a full mac address and resolves it using it's first 3 bytes"""
def mac_resolve(cursor, macaddr):

    query = 'SELECT * FROM macinfo WHERE prefix LIKE ?;'

    try:
        cursor.execute(query, [macaddr[0:8]])
        for row in cursor:
            return row[2]
    except sqlite3.IntegrityError:
        raise
    return "Unknown"
