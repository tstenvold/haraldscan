#!/usr/bin/env python
# -*- coding: utf-8 -*-
# haraldargs.py
# July 2009
# Terence Stenvold <tstenvold@gmail.com>
#
#Command Line Args handling

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

import haraldusage
import haraldsql
import sys
import getopt

def build_db(connection):

    status = haraldsql.refresh_maclist(connection)
    for k, v in status.iteritems():
       print k, ': ', v
    print "Database Built"
    sys.exit(1)

def cmdargs(argv, c):

    try:
        opts, args = getopt.getopt(argv, "hw:bs", ["help", "write=", "build","service"])
    except getopt.GetoptError, err:
        print str("Unknown Command use --help for information")
        haraldusage.usage()

    for o, a in opts:
        if o in ("-b", "--build"):
            c.minus_b()
        elif o in ("-w", "--write"):
            c.minus_w(a)
        elif o in ("-h", "--help"):
	        haraldusage.usage()
        elif o in ("-s", "--service"):
	        c.minus_s()
        else:
            assert False, "unhandled option"

    if haraldsql.chk_database() == False and c.buildb == False:
        haraldusage.no_db()
