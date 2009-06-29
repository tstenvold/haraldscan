#!/usr/bin/python
#
# Authors:
#   Carson Farrell
#   Terence Stenvold <tstenvold@gmail.com>
# Date: June 26th 2009
#
# Written to read the MACINFO file into an sqlite database called macinfo.db for
# the haraldscanner program to work with. This script assumes that data given to it
# is in the correct format (comma seperated, two column; ie: 11:22:33, Spam)
# and makes no attempt to guess what the input means.
#
# This script will print the status (new or existing) of each entry in the file
# once it attempts to insert it into the database.

from pysqlite2 import dbapi2 as sqlite

"""Represents a mapping between prefix and manufacturer. Using this instead of a dictionary
so that validation business logic can be placed in later if needed."""
class MacAddress:

    def __init__(self, prefix, maker):
        self.prefix = prefix
        self.maker = maker


"""Creates an SQLite database in an existing database.
If any error occurs, no operation is performed"""
def create_base_table(cursor):
    create_statement  = 'CREATE TABLE macinfo ('
    create_statement += 'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    create_statement += 'prefix char(8) UNIQUE,'
    create_statement += 'manufacturer varchar(100));'

    cursor.execute(create_statement)

"""Creates the device table in the database
If any error occurs, no operation is performed"""
def create_dev_table(cursor):

    create_dev  = 'CREATE TABLE devices ('
    create_dev += 'id INTEGER PRIMARY KEY AUTOINCREMENT,'
    create_dev += 'macaddr char(17) UNIQUE,'
    create_dev += 'name varchar(100),'
    create_dev += 'devclass varchar(100),'
    create_dev += 'manufacturer varchar(100));'

    cursor.execute(create_dev)

"""Drops the device table in the database should be run everytime program starts
in case of any premature program termination that results in the table being persistant
after the program closes
If any error occurs, no operation is performed"""
def drop_dev_table():

    with sqlite.connect('macinfo.db') as connection:
        cursor = connection.cursor()

    create_statement  = 'DROP TABLE devices;'

    cursor.execute(create_statement)

"""Inserts the values represented by a MacAddress object into an existing database.
Returns true if the value is unique, false otherwise"""
def insert_address_object(address, cursor):
    query = 'INSERT INTO macinfo(prefix, manufacturer) VALUES (?, ?)'
    try:
        cursor.execute(query, (address.prefix, address.maker))
        return True;
    except sqlite.IntegrityError:
        return False;

"""Inserts a device into the device table in the existing database."""
def insert_dev_table(addr, name, devclass, manufacturer):

    with sqlite.connect('macinfo.db') as connection:
        cursor = connection.cursor()

    query = 'INSERT INTO devices (macaddr, name, devclass, manufacturer) VALUES (?, ?, ?, ?)'
    try:
        cursor.execute(query, (addr, name, devclass, manufacturer))
    except sqlite.IntegrityError:
        pass

    connection.commit()

"""Attempts to enter the data found in the MACLIST file into the database specified
on the first line on the function."""
def refresh_maclist():
    with sqlite.connect('macinfo.db') as connection:
        cursor = connection.cursor()

    # if the table cannot be created, it probably exists already.
    # catching OperationalError is probably not the best solution,
    # might want to look into a better way of doing this.
    try:
        create_base_table(cursor)
    except sqlite.OperationalError:
        pass

    status = {}

    with open('MACLIST') as f:
        for line in f:
            x = line.split(',')
            mac_address = MacAddress(x[0].strip(), x[1].strip())

            if insert_address_object(mac_address, cursor):
                status[mac_address.prefix] = 'new'
            else:
                status[mac_address.prefix] = 'exists'

    connection.commit()
    return status

def setup_dev_table():

    with sqlite.connect('macinfo.db') as connection:
        cursor = connection.cursor()

    # if the table cannot be created, it probably exists already.
    # catching OperationalError is probably not the best solution,
    # might want to look into a better way of doing this.
    try:
        drop_dev_table()
    except sqlite.OperationalError:
        pass

    try:
        create_dev_table(cursor)
    except sqlite.OperationalError:
        pass

    connection.commit()

def show_dev_table():

    with sqlite.connect('macinfo.db') as connection:
        cursor = connection.cursor()

    query = 'SELECT * FROM devices'
    try:
        cursor.execute(query)
        connection.commit()
        return True;
    except sqlite.IntegrityError:
        connection.commit()
        return False;

#Resolves mac address to a manufacture
#Take a full mac address and resolves it using it's first 3 bytes
def mac_resolve(macaddr):

    with sqlite.connect('macinfo.db') as connection:
        cursor = connection.cursor()

    query = 'SELECT * FROM macinfo WHERE prefix LIKE ?'
    
    try:
        cursor.execute(query, [macaddr[0:8]])
        for row in cursor:
            return row[2]
    except sqlite.IntegrityError:
        return 0;


#print mac_resolve('00:1C:EE:00:34:23')

#For Testing to be removed
#status = refresh_maclist()
#for k, v in status.iteritems():
    #print k, ': ', v
