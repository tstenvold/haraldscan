#!/usr/bin/env python
# -*- coding: utf-8 -*-
# haraldargs.py
# July 2009
# Terence Stenvold <tstenvold@gmail.com>
#
#Command Line Args handling

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
        opts, args = getopt.getopt(argv, "hw:b", ["help", "write=", "build"])
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
        else:
            assert False, "unhandled option"

    if haraldsql.chk_database() == False and c.buildb == False:
        haraldusage.no_db()
