#!/usr/bin/env python

# discovery.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#

import bluetooth
import sys

def discovery():

    found_devices = bluetooth.discover_devices(duration=6, flush_cache=True, lookup_names=True)
    #print statements used for debugging right now to be removed
    print "found %d devices" % len(found_devices)

    for addr, name in found_devices:
        print "  %s - %s" % (addr, name)

    return found_devices
    
def service_discovery(mac_addr):
    
    services = bluetooth.find_service(address=target)
    
    #print statements used for debugging right now to be removed
    if len(services) > 0:
        print "found %d services on %s" % (len(services), sys.argv[1])
        return services
    else:
        print "no services found"
         return 0

	
