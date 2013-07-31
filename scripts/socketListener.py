#!/usr/bin/python

import socket
from xbee import XBee
import serial
import string
import time

host = '142.104.165.35'
port = 44444

ser = serial.Serial()
ser.port = '/dev/ttyAMA0'
ser.baudrate = '9600'

def processFrame(data):
	print data

try:
	ser.open()
	xbee = XBee(ser, callback=processFrame)

except Exception, e:
	print "error open serial port: " + str(e)
	exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(10)

while 1:
	try:
		conn, addr = s.accept()
		data = conn.recv(1024)
		conn.close()
		
		words = data.split()
		if len(words) != 2:
			print 'Invalid input'
			continue
		
		param = ''
		
		if words[0] == 'off':
			param = '04'
		elif words[0] == 'on':
			param = '05'
		else:
			print 'Invalid input'
			continue
		
		xbee.remote_at(frame_id='A',dest_addr_long=words[1].decode('hex'), command='D0', parameter=param.decode('hex'))
		
	except KeyboardInterrupt:
		break
		exit()
		
	except Exception as e:
		print str(e)
		exit()
		
