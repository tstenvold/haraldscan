#!/usr/bin/env python
# -*- coding: utf-8 -*-
# discovery.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#
# Used for discoverying broadcasting Bluetooth devices and getting the services
# available on those devices.

import lightblue
import deviceclass
import sys,os
import haraldsql
import haraldusage

"""OS X Class for scanning """
class harald_lightblue():

    def set_cursor(self, cursor):
        self.cursor = cursor

    def set_service(self, service):
        self.service = service

    def find_devices(self):
        nearby_devices = lightblue.finddevices()

        for addr, name, devclass in nearby_devices:
            self.device_discovered(addr, devclass ,name)

    def device_discovered(self, addr, device_class, name):

        devclass = deviceclass.majordev_class(device_class)
        devman = haraldsql.mac_resolve(self.cursor, addr)

        if (devman == 'Unknown' and not haraldsql.device_exists(self.cursor, addr)) \
        or (self.service and not haraldsql.device_exists(self.cursor, addr)):
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

if __name__ == '__main__':
  haraldusage.usage()
