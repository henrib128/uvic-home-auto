#!/usr/bin/python
#basic script to listen to the serial port
from serial import Serial

PORT = '/dev/ttyS10'
BAUD = 9600

serialport = Serial(PORT, BAUD)
print 'start'
x = serialport.readline()
serialport.write(x)
