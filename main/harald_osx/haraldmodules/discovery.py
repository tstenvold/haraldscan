#!/usr/bin/env python
# -*- coding: utf-8 -*-
# discovery.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#
# Used for discoverying broadcasting Bluetooth devices and getting the services
# available on those devices.

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

import lightblue
import deviceclass
import sys,os
import haraldsql
import haraldusage
import haraldargs

"""OS X Class for scanning """
class harald_lightblue():

    def set_cursor(self, cursor):
        self.cursor = cursor

    def set_service(self, service, noservice):
        self.service = service
        self.noservice = noservice

    def find_devices(self):
        nearby_devices = lightblue.finddevices()

        for addr, name, devclass in nearby_devices:
            self.device_discovered(addr, devclass ,name)

    def device_discovered(self, addr, device_class, name):

        devclass = deviceclass.majordev_class(device_class)
        devman = haraldsql.mac_resolve(self.cursor, addr)

        if self.noservice is False:
            if ((devman == 'Unknown' or self.service) \
            and not haraldsql.device_exists(self.cursor, addr)):
                unkown_mac(addr, name, devclass)

        haraldsql.insert_dev_table(self.cursor, addr, name, devclass, devman)



"""Takes a mac address and tries to discover services available if in range.
returns the service available or 0 if it couldn't find any"""
def service_discover(address):

    services = lightblue.findservices(addr=address)

    if len(services) > 0:
        return services
    else:
        return "No Services"

"""This will get all possible info on an unresolved device MAC addr
Please Send these files to me at tstenvold@gmail.com"""
def unkown_mac(addr, name, devclass):

    new_services = service_discover(addr)

    fp = open("%s" % addr[0:8] , "ab+")

    if "No Services" in new_services:
        fp.write(new_services)
        fp.write("\nDevice Address: %s Name: %s Class: %s \n\n" % (addr[0:8],name,devclass))
    else:
        fp.write("Device Address: %s Name: %s Class: %s \n\n" % (addr[0:8],name,devclass))
        for svc in new_services: 		#writes each new service to the file
            fp.write("Service Name: %s\n"    % svc[2])
            fp.write("    service id:  %s \n\n"% svc[1])

    fp.close() #closes file

if __name__ == "__main__":
    parser = haraldargs.cmd_parse([""])
    parser.print_help()
