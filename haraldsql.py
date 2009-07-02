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


"""Opens Database and returns the cursor to it"""
def open_database():

        return sqlite.connect('macinfo.db')

def get_cursor(connection):

        return connection.cursor()

"""Closes the Database duh"""
def close_database(connection):

    connection.commit()
    connection.close()


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
def drop_dev_table(cursor):

    cursor.execute('DROP TABLE devices;')

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
def insert_dev_table(cursor, addr, name, devclass, manufacturer):

    query = 'INSERT INTO devices (macaddr, name, devclass, manufacturer) VALUES (?, ?, ?, ?)'
    try:
        cursor.execute(query, (addr, name, devclass, manufacturer))
    except sqlite.IntegrityError:
        pass

"""Attempts to enter the data found in the MACLIST file into the database specified
on the first line on the function."""
def refresh_maclist(connection):

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

            insert_address_object(mac_address, cursor):

    connection.commit()

"""Sets up the devices table by destroying it and creating
a new table. Should be run at the begining of the program"""
def setup_dev_table(connection):

    cursor = connection.cursor()

    # if the table cannot be created, it probably exists already.
    # catching OperationalError is probably not the best solution,
    # might want to look into a better way of doing this.
    try:
        drop_dev_table(cursor)
    except sqlite.OperationalError:
        pass

    try:
        create_dev_table(cursor)
    except sqlite.OperationalError:
        pass

    connection.commit()

"""Shows the devices table by returning the results of the query"""
def show_dev_table(cursor):

    try:
        cursor.execute('SELECT * FROM devices')
        return cursor
    except sqlite.IntegrityError:
        return 0

"""Writes the devices table to a file specified
by the parameter passed in"""
#Needs error handling
def write_dev_table(cursor, filename):

    fp = open(filename, 'w')

    results = show_dev_table(cursor)

    for row in results:
        fp.write("Mac: " + row[1] + " Name: " + row[2] + " Class: " + row[3] + " Manuf: " + row[4] + "\n")

    fp.write("\n")
    fp.close()


"""Resolves mac address to a manufacture
Take a full mac address and resolves it using it's first 3 bytes"""
def mac_resolve(cursor, macaddr):

    query = 'SELECT * FROM macinfo WHERE prefix LIKE ?'

    try:
        cursor.execute(query, [macaddr[0:8]])
        for row in cursor:
            return row[2]
    except sqlite.IntegrityError:
        return 0

    return "Unknown"
