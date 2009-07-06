#!/usr/bin/env python

# discovery.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#
# Used for discoverying broadcasting Bluetooth devices and getting the services
# available on those devices.

import bluetooth
import deviceclass
import sys,os
import haraldsql
import haraldusage

#This is really poorly done!
class harald_discoverer(bluetooth.DeviceDiscoverer):

    def set_cursor(self, cursor):
        self.cursor = cursor

    def pre_inquiry(self):
        self.done = False

    def device_discovered(self, addr, device_class, name):

        devclass = deviceclass.majordev_class(device_class)
        devman = haraldsql.mac_resolve(self.cursor, addr)

        haraldsql.insert_dev_table(self.cursor, addr, name, devclass, devman)

    def inquiry_complete(self):
        self.done = True


#Takes a mac address and tries to discover services available if in range.
#returns the service available or 0 if it couldn't find any
def service_discover(mac_addr):

    services = bluetooth.find_service(address=target)

    if len(services) > 0:
        return services
    else:
        return 0

"""This Function will be used to send information to a php page but for now does nothing"""
def unkown_mac(mac_addr):
    results = service_discover(mac_addr)
    name = lookup_name(address, timeout=8)

    line = mac_addr
    line += name

    for svc in services:
        line += svc["description"]
        line += svc["provider"]

if __name__ == '__main__':
  haraldusage.usage()
