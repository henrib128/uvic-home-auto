#!/usr/bin/python
#basic script to listen to the serial port

from SerialMonitor import SerialMonitor

if __name__ == "__main__":
	SerialListener = SerialMonitor("/dev/pts/3", 9600, None)
	print 'Serial Listener starting'
	SerialListener.pollLine()

