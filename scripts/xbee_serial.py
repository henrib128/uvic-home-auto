#!/usr/bin/python

# xbeetest.py
#basic script that listens to serial port and links it with the xbee library. 
#this displays the packet in a simple to read format. 

from xbee import XBee
import serial

PORT = '/dev/ttyAMA0'
BAUD = 9600
ser = Serial(PORT, BAUD)
xbee = XBee(ser)

print 'starting'
# Continuously read and print packets
while True:
    try:
        response = xbee.wait_read_frame()
        print response
    except KeyboardInterrupt:
        break
        
ser.close()


# xbeesend.py
from xbee import XBee
from serial import Serial

PORT = '/dev/ttyAMA0'
BAUD = 9600

print 'start'

ser = Serial(PORT, BAUD)

xbee = XBee(ser)
# Sends remote command from coordinator to the serial number, this only returns the value. In order to change
#the value must add a parameter='XX'
xbee.remote_at(frame_id='A',dest_addr_long='\x00\x13\xA2\x00\x40\xA5\x7B\x39', command='SH')

# Wait for and get the response
print(xbee.wait_read_frame())

#testing calling a script from inside a script (it works)
import os
print "I will call this other program called xbeetest.py"
os.system("python xbeetest.py")

ser.close()





