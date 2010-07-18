#!/usr/bin/env python3
# haraldusage.py
# July 2009
# Terence Stenvold <tstenvold@gmail.com>
#
#Help info for the running of harald scan

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

import sys
import haraldmodules.haraldargs

def os_error():

    print("Error:\n\tYour Operating System is not supported or undetectable\n")
    sys.exit(1)

def bluetooth_error():

    print("Error:\n\tNo Bluetooth Adapter Found. Please run 'hciconfig hci0 up' If Adapter is present but not working\n")
    sys.exit(1)

def no_db():

    print("Error:\n\tDatabase not found or Corrupt. Please run 'haraldscan.py -b'\n")
    sys.exit(1)

if __name__ == "__main__":
    parser = haraldargs.cmd_parse([""])
    parser.print_help()
