# deviceclass.py
# June 2009
# Terence Stenvold <tstenvold@gmail.com>
#

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
         class = major_classes[major_class]
         #class += the return from minor class
    else:
         class = "Uncategorized"
 
    return class

def minordev_computer(device_class):
    
    minor_classes = ( "Miscellaneous", 
                        "Desktop", 
                        "Server", 
                        "Laptop", 
                        "Handheld PC/PDA (clam)", 
                        "Palm sized PC/PDA", 
                        "Wearable Computer(Watch sized)" )
        #take only first 8 bits then shift right 1 bit to check class
    

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
