#!/usr/bin/python
#
# Author: Carson Farrell
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
	"""Sets mac address prefix and the associated manufacturer"""
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

"""Inserts the values represented by a MacAddress object into an existing database.
Returns true if the value is unique, false otherwise"""
def insert_address_object(address, cursor):
	query = 'INSERT INTO macinfo(prefix, manufacturer) VALUES (?, ?)'
	try:
		cursor.execute(query, (address.prefix, address.maker))
		return True;
	except sqlite.IntegrityError:
		return False;

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

#For Testing to be removed
status = refresh_maclist()
for k, v in status.iteritems():
	print k, ': ', v
