#!/usr/bin/python
"""
Main PiHome script
"""

import XbeeMonitor as xm
import DBManager as db

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
	
	while True:
		try:
			parameter = raw_input()
			command = 'D0'
			device='0013a20040a57ae9'
			XbeeMonitor.sendFrame(device, command, parameter)
	
		except KeyboardInterrupt:
			break	

