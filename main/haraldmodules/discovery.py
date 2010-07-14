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

import bluetooth
import deviceclass
import sys,os
import haraldsql
import haraldusage
import haraldargs


class harald_discoverer(bluetooth.DeviceDiscoverer):

    def set_cursor(self, cursor):
        self.cursor = cursor

    def set_service(self, service, noservice):
        self.service = service
        self.noservice = noservice

    def pre_inquiry(self):
        self.done = False

    def device_discovered(self, addr, device_class, name):

        devclass = deviceclass.majordev_class(device_class)
        devman = haraldsql.mac_resolve(self.cursor, addr)

        if self.noservice is False:
            if ((devman == 'Unknown' or self.service) \
            and not haraldsql.device_exists(self.cursor, addr)):
                unkown_mac(addr, name, devclass)

        haraldsql.insert_dev_table(self.cursor, addr, name, devclass, devman)

    def inquiry_complete(self):
        self.done = True


"""Takes a mac address and tries to discover services available if in range.
returns the service available or 0 if it couldn't find any"""
def service_discover(addr):

    services = bluetooth.find_service(address=addr)

    if len(services) > 0:
        return services
    else:
        return "No Services"

"""This will get all possible info on an unresolved device MAC addr
Please Send these files to me at tstenvold@gmail.com"""
def unkown_mac(addr, name, devclass):

    new_services = service_discover(addr)

    fp = open(addr + ".xml" , "wb+")
    fp.write("<?xml version=\"1.0\"?>\n")

    if "No Services" in new_services:
        fp.write("<device>\n")
        fp.write("\t<name>%s</name>\n" % name)
        fp.write("\t<address>%s</address>\n" % addr[0:8])
        fp.write("\t<class>%s</class>\n" % devclass)
        fp.write("\t<services>" + new_services + "</services>\n")
        fp.write("</device>")
    else:
        fp.write("\t<device>\n")
        fp.write("\t<name>%s</name>\n" % name)
        fp.write("\t<address>%s</address>\n" % addr[0:8])
        fp.write("\t<class>%s</class>\n" % devclass)
        fp.write("\t<services>\n")
        for svc in new_services: 		#writes each new service to the file
            fp.write("\t\t<servicename>%s</servicename>\n" % svc["name"])
            fp.write("\t\t<host>%s</host>\n" % svc["host"])
            fp.write("\t\t<description>%s</description>\n" % svc["description"])
            fp.write("\t\t<provider>%s</provider>\n" % svc["provider"])
            fp.write("\t\t<protocol>%s</protocol>\n" % svc["protocol"])
            fp.write("\t\t<channel>%s</channel>\n" % svc["port"])
            fp.write("\t\t<svcclasses>%s</svcclasses>\n"% svc["service-classes"])
            fp.write("\t\t<profile>%s</profile>\n"% svc["profiles"])
            fp.write("\t\t<svcid>%s</svcid>\n"% svc["service-id"])
        fp.write("\t</services>\n")
        fp.write("</device>")

    fp.close() #closes file

if __name__ == "__main__":
    parser = haraldargs.cmd_parse([""])
    parser.print_help()
