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
import haraldupdate
import sys, time
import getopt
from optparse import OptionParser


def build_db(connection):

    status = haraldsql.refresh_maclist(connection)
    for k, v in status.iteritems():
       print k, ': ', v
    print "Database Built"
    sys.exit(1)

def cmd_parse(argv):

    parser = OptionParser(usage="usage: haraldscan.py [options]", version="%prog 0.32")
    
    parser.add_option("-w", "--write",
                      action="store",
                      type="string",
                      dest="filename",
                      default=str(time.time()),
                      help="Outputs discovered device info to a file you specify (unspecified: filename is a timestamp.")
    parser.add_option("-t", "--time",
                      action="store",
                      dest="numminutes",
                      type="int",
                      default=15,
                      help="Shows number of devices found per time specified in mins (default is 15 mins)")
    parser.add_option("--no-write",
                      action="store_true", # optional because action defaults to "store"
                      dest="nowrite",
                      default=False,
                      help="Disables writing discovered device info to a file")
    parser.add_option("-b", "--build",
                      action="store_true", # optional because action defaults to "store"
                      dest="build",
                      default=False,
                      help="Builds MAC Addr database. Ignores all other options.")
    parser.add_option("-s", "--service",
                      action="store_true", # optional because action defaults to "store"
                      dest="service",
                      default=False,
                      help="Does a service scan of all devices found and saves a file like a 'Unknown' device would.")
    parser.add_option("-u", "--update",
                      action="store_true", # optional because action defaults to "store"
                      dest="update",
                      default=False,
                      help="Updates the MACLIST if there are updates and rebuilds the database (requires and Internet connection).")                  
         
    return parser
    
def handle_args(argv,c):

    parser = cmd_parse(argv)
    
    (options, args) = parser.parse_args()
    
    if options.numminutes > 0:
        c.time_update(options.numminutes)       
    if options.build is True:
        c.minus_b()
    if options.service is True:
        c.minus_s()
    if options.nowrite is False:
        c.minus_w(options.filename)
    if options.update is True:
        if haraldupdate.check_now():
            c.minus_b()
        else:
            sys.exit(0)

    if haraldsql.chk_database() == False and c.buildb == False:
        haraldusage.no_db()

if __name__ == "__main__":
    parser = cmd_parse([""])
    parser.print_help()

