#!/usr/bin/env python

# discovery.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#
# Used for discoverying broadcasting Bluetooth devices and getting the services
# available on those devices.

import bluetooth
import deviceclass
import sys
import select

class harald_discoverer(bluetooth.DeviceDiscoverer):

    def pre_inquiry(self):
        self.done = False

    def device_discovered(self, addr, device_class, name):
        #This is where discovered devices get put into database
        print "  %s - %s - %s" % (addr, name, deviceclass.majordev_class(device_class))

    def inquiry_complete(self):
        self.done = True


#Discovers devices
def discover():

    d = harald_discoverer()
    d.find_devices(lookup_names=True)

    readfiles = [ d, ]

    while True:
        rfds = select.select( readfiles, [], [] )[0]

        if d in rfds:
            d.process_event()

        if d.done: break


#Takes a mac address and tries to discover services available if in range.
#returns the service available or 0 if it couldn't find any
def service_discover(mac_addr):

    services = bluetooth.find_service(address=target)

    if len(services) > 0:
        return services
    else:
        return 0
