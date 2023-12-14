#!/usr/bin/env python3 
# Read a TMP101 sensor

import smbus
import time

bus = smbus.SMBus(2)
address1 = 0x49
address2 = 0x4A
while True:
    temp1 = bus.read_byte_data(address1, 0)
    temp2 = bus.read_byte_data(address2, 0)
    print(temp1," ", temp2, end="\r")
    time.sleep(0.25) 


