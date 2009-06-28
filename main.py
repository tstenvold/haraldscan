#!/usr/bin/env python

# main.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#

import deviceclass
import discovery
import sqlite

#setup the device table for the lifetime of program
sqlite.setup_dev_table()

#gets devices
dis_devices = discovery.discover()

#shows devices in table
sqlite.show_dev_table()

#drops table at end of program life
sqlite.drop_dev_table()
