#!/usr/bin/env python

# discovery.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#

import bluetooth
import sys

def discover():

    found_devices = bluetooth.discover_devices(duration=6, flush_cache=True, lookup_names=True)

    return found_devices

def service_discover(mac_addr):

    services = bluetooth.find_service(address=target)

    if len(services) > 0:
        return services
    else:
        return 0
