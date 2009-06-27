#!/usr/bin/env python

# deviceclass.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#

#Major classes for Bluetooth
def majordev_class(device_class):

    major_classes = ( "Miscellaneous",
                        "Computer",
                        "Phone",
                        "LAN/Network Access point",
                        "Audio/Video",
                        "Peripheral",
                        "Imaging" )

    major_class = (device_class >> 8) & 0xf

    if major_class < 7:
        dev_class = major_classes[major_class]

        if major_class == 1:
            dev_class += "|" + minordev_computer(device_class)
        elif major_class == 2:
            dev_class += "|" + minordev_computer(device_class)

    else:
        dev_class = "Uncategorized"

    return dev_class

#Minor classes for Computer
def minordev_computer(device_class):

    minor_classes = ( "Miscellaneous",
                        "Desktop",
                        "Server",
                        "Laptop",
                        "Handheld PC/PDA (Clam style)",
                        "Palm sized PC/PDA",
                        "Wearable Computer(Watch sized)" )

    minor_class = ((device_class << 8) >> 9) & 0xf

    return minor_classes[minor_class]

#Minor classes for phone
def minordev_phone(device_class):

    minor_classes = ( "Miscellaneous",
                        "Cellular",
                        "Cordless",
                        "Smart Phone",
                        "Wireless Modem or Voice Gateway",
                        "Common  ISDN Gateway")

    minor_class = ((device_class << 8) >> 9) & 0xf

    return minor_classes[minor_class]


#Services classes for bluetooth
def service_class(service_class):

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
