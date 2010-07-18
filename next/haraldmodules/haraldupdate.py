#!/usr/bin/env python3
# haraldupdate.py
# September 2009
# Terence Stenvold <tstenvold@gmail.com>
#
#Updating script for the running of harald scan

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

import sys,os
import urllib.request, urllib.parse, urllib.error
import haraldmodules.haraldargs


def reporthook(*a): print(a)


def check_now():

    rlines = 0
    llines = 0


    flocal = open('MACLIST', 'rb')

    for line in flocal:
        llines+=1

    if flocal == None:
        print("Could not open MACLIST")
        sys.exit(1)

    try:
        url = 'http://haraldscan.googlecode.com/svn/trunk/MACLIST'
        fweb = urllib.request.urlopen(url)


        for lines in fweb.readlines():
            rlines+=1

    #should be in usage
    except urllib.error.URLError:
        print("Could not retrieve file")
        print("Please check your internet connection")
        sys.exit(1)

    if rlines > llines:
        urllib.request.urlretrieve(url, 'MACLIST', reporthook)
        print("Updated MACLIST Retrieved")
        print("Rebuilding Database Now")
        return True
    else:
        print("Already using the newest version")

    return False

if __name__ == "__main__":
    parser = haraldargs.cmd_parse([""])
    parser.print_help()
