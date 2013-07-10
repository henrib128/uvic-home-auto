#!/usr/bin/python
#basic script to listen to the serial port

import SerialMonitor

if __name__ == "__main__":
	SerialWriter = SerialMonitor.SerialMonitor("/dev/pts/4", 9600, None)
	print 'Serial Writer starting'

	while 1:
		# get keyboard input
		input = raw_input(">> ")
		
		# send the character to the device
		SerialWriter.writeLine(input)
		
		if input == 'exit':
			break

	#SerialMonitor.close()
	exit()

