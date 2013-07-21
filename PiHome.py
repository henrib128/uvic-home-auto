#!/usr/bin/python
"""
Main PiHome script
"""

import XbeeMonitor as xm
import DBManager as db
from struct import *
import socket
import serial

host = '142.104.165.35'
port = 50000

if __name__ == "__main__":
	XbeeMonitor = xm.XbeeMonitor("/dev/ttyAMA0", 9600, None)
	
	# Initialize database
	db.initDatabase()
	
	# Populate database with some test values
	# Nodes
	db.addNode('router','24.52.152.172')
	db.addNode('cam1','10.0.2.15')
	#db.addNode('cam2','192.168.0.190')
	
	# Emails
	db.addEmail('trihuynh87@gmail.com')
	#db.addEmail('minhtri@uvic.ca')
	# Devices
	db.addDevice(0x0013a20040a57ae9,0,'Switch',0,1,'New')
	db.addDevice(0x0013a20040a57b39,1,'Front Door',1,1,'New')
	
	# Start local camera monitor
	
	# Initialzize camera client socket
	#xm.createCamclients()
				
	print 'PiHome starting!'
	XbeeMonitor.start()
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(10)
	
	while True:
		try:
			conn, addr = s.accept()
			data = conn.recv(1024)
			conn.close()
		
			words = data.split()
			if len(words) != 2 or len(words[1]) != 16:
				print 'Invalid input'
				continue
		
			param = ''
			command = 'D0'
			
			if words[0] == 'off':
				param = '04'
			elif words[0] == 'on':
				param = '05'
			else:
				print 'Invalid input'
				continue
				
			XbeeMonitor.sendFrameHex(words[1],command,param)
			#XbeeMonitor.sendFrameInt(0x0013a20040a57b39, command, parameter)
	
		except KeyboardInterrupt:
			exit()
		except Exception as e:
			print str(e)
			exit()
			

