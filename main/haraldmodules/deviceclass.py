#!/usr/bin/env python
# -*- coding: utf-8 -*-
# deviceclass.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#
# These functions are for determining a Devices Major | Minor and Service classes
#
# Major class designation is in bit positions 8-12
# Minor class is determined by major class and bit positions 2-7
#

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


import haraldargs

#Major classes for Bluetooth
def majordev_class(device_class):

    major_classes = ( "Miscellaneous",
                        "Computer",
                        "Phone",
                        "LAN/Network",
                        "Audio/Video",
                        "Peripheral",
                        "Imaging" )

    major_class = (device_class >> 8) & 0xf

    if major_class < 7:
        dev_class = major_classes[major_class]

        if major_class == 1:
            dev_class += "|" + minordev_computer(device_class)
        elif major_class == 2:
            dev_class += "|" + minordev_phone(device_class)
        elif major_class == 3:
            dev_class += "|" + minordev_lan(device_class)
        elif major_class == 4:
            dev_class += "|" + minordev_audio(device_class)
        elif major_class == 5:
            dev_class += "|" + minordev_peripheral(device_class)
        else:
            dev_class += "|" + minordev_image(device_class)

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

    minor_class = (device_class & 0xff) >> 2

    return minor_classes[minor_class]

#Minor classes for phone
def minordev_phone(device_class):

    minor_classes = ( "Miscellaneous",
                        "Cellular",
                        "Cordless",
                        "Smart Phone",
                        "Wireless Modem or Voice Gateway",
                        "Common  ISDN Gateway")

    minor_class = (device_class & 0xff) >> 2

    return minor_classes[minor_class]

#Minor classes for lan/networking
def minordev_lan(device_class):

    minor_classes = ( "Fully Available",
                        "1% - 17% Utilized",
                        "17% - 33% Utilized",
                        "33% - 50% Utilized",
                        "50% - 67% Utilized",
                        "67% - 83% Utilized",
                        "83% - 99% Utilized",
                        "No Service Available")

    #only uses bits 5,6,7

    minor_class = (device_class & 0xff) >> 5

    return minor_classes[minor_class]

#Minor classes for audio/video
def minordev_audio(device_class):

    minor_classes = ( "Miscellaneous",
                        "Headset Profile",
                        "Handsfree",
                        "?Reserved?",
                        "Microphone",
                        "Loudspeaker",
                        "Headphones",
                        "Portable Audio",
                        "Car Audio",
                        "Set-top box",
                        "HiFi Audio Device",
                        "VCR",
                        "Video Cameras",
                        "Camcorder",
                        "Video Monitor",
                        "Video Display and Speaker",
                        "Video Conferencing",
                        "?Reserved?",
                        "Gaming/Toy Audio/Video")

    minor_class = (device_class & 0xff) >> 2

    return minor_classes[minor_class]

#Minor classes for peripheral
def minordev_peripheral(device_class):

    top_minor_classes = ( "Miscellaneous",
                        "Keyboard",
                        "Pointing Device",
                        "Combo Keyboard/Pointing Device")

    bottom_minor_classes = ( "",
                        "|Joystick",
                        "|Gamepad",
                        "|Remote Control",
                        "|Sensing Device",
                        "|Digitizer Tablet",
                        "|Card Reader")

    #uses bits 6,7
    t_minor_class = (device_class & 0xff) >> 6
    #Uses bits 2,3,4,5
    b_minor_class = ((device_class & 0xff) >> 2) & 0xf

    return top_minor_classes[t_minor_class] + bottom_minor_classes[b_minor_class]

#Minor classes for Imaging
def minordev_image(device_class):

    minor_classes = ( " Display",
                        " Camera",
                        " Scanner",
                        " Printer")

    image_class = ''

    #only uses bits 4,5,6,7 can be multiple items
    for i in range (4,8):
        minor_class = (device_class >> i) & 0x1
        if minor_class != 0:
            image_class += minor_classes[i - 4]

    return image_class

#Services classes for bluetooth
def service_class(service_class):

    service_classes = ( (16, "Positioning"),
                        (17, "Networking"),
                        (18, "Rendering"),
                        (19, "Capturing"),
                        (20, "Object transfer"),
                        (21, "Audio"),
                        (22, "Telephony"),
                        (23, "Information"))

    serv_class = ''
    for bitpos, classname in service_classes:
        if service_class & (1 << (bitpos-1)):
            serv_class = classname

    return serv_class

if __name__ == "__main__":
    parser = haraldargs.cmd_parse([""])
    parser.print_help()
