#!/usr/bin/python

import sys, getopt
from xbee import XBee
from serial import Serial

def main(argv):

	#this is for all command line argument parsing
	SerialNumber = ''
	Command = ''
	Parameter = ''

	try:
		opts, args = getopt.getopt(argv,"s:c:p:",["SerialNumber=","Command=","Parameter="])

	except getopt.GetoptError:
		print 'argtest.py -s SerialNumber -c Command -p Parameter'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -s <SerialNumber> -c <Command> -p <Parameter>'
			sys.exit()
		elif opt in ("-s", "SerialNumber"):
			SerialNumber = arg
		elif opt in ("-c", "Command"):
			Command = arg
		elif opt in ("-p", "Parameter"):
			Parameter = arg

	print 'Serial Number is:', SerialNumber
	print 'Command is:', Command
	print 'Parameter is:', Parameter

	#XBee Transmit Part
	PORT = '/dev/ttyAMA0'
	BAUD = 9600

	print 'start'

	ser = Serial(PORT, BAUD)
	print '1'
	xbee = XBee(ser)
	print '2'
	# Sends remote command from coordinator to the serial number, this only returns the value. In order to change
	#the value must add a parameter='XX'
	xbee.remote_at(frame_id='A',dest_addr_long=SerialNumber.decode('hex'), command=Command, parameter=Parameter.decode('hex'))
	print '3'
	# Wait for and get the response
	frame = xbee.wait_read_frame()
	
	print '4'
	print frame
	ser.close()

if __name__ == "__main__":
	main(sys.argv[1:])
   

