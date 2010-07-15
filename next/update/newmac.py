#!/usr/bin/env python3
# newmac.py
# July 2010
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

def in_addr(addr):
    fp = open("oui", "r")
    
    for line in fp:
        if addr[0:8] == line[0:8]:
            return line[9:]
            fp.close()
    
    fp.close()
    return False
    
def add_new(addr):

    fp = open("MACLIST", "r+")
    
    for line in fp:
        #print("Comparing %s - %s " % addr[0:8], line[0:8])
        if addr[0:8] == line[0:8]:
            fp.close()
            return False
    
    fw = open("MACLIST", "a")
    
    print ("ADDING NEW: %s " % addr[:-1])
    fw.write(addr)
    fw.close()
    fp.close()
    return True

fw = open("macin" , "r")

for addr in fw:
    oui = in_addr(addr)
    if oui is not False:
        add_new(addr[0:8] + "," + oui)
        
fw.close()
        

