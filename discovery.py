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


def device_class(device_class):

    major_classes = ( "Miscellaneous", 
                          "Computer", 
                          "Phone", 
                          "LAN/Network Access point", 
                          "Audio/Video", 
                          "Peripheral", 
                          "Imaging" )

    major_class = (device_class >> 8) & 0xf

    if major_class < 7:
         class = major_classes[major_class]
    else:
         class = "Uncategorized"
 

    return class

def service_class(service class):

    service_classes = ( (16, "positioning"), 
                        (17, "networking"), 
                        (18, "rendering"), 
                        (19, "capturing"),
                        (20, "object transfer"), 
                        (21, "audio"), 
                        (22, "telephony"), 
                        (23, "information"))

    serv_class = ""

    for bitpos, classname in service_classes:
        if device_class & (1 << (bitpos-1)):
            serv_class += classname

    return serv_class

	