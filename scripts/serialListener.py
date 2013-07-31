#!/usr/bin/python
#basic script to listen to the serial port

import SerialMonitor as sm
import DBManager as db

if __name__ == "__main__":
	SerialListener = sm.SerialMonitor("/dev/pts/3", 9600, None)
	
	# Initialize database
	db.initDatabase()
	
	# Populate database with some test values
	# Nodes
	db.addNode('router','24.52.152.172')
	db.addNode('cam1','10.0.2.15')
	db.addNode('cam2','192.168.0.190')
	
	# Emails
	db.addEmail('trihuynh87@gmail.com')
	db.addEmail('minhtri@uvic.ca')
	# Devices
	db.addDevice(1000000000,1,'Main Door',0,1)
	db.addDevice(1000000001,1,'Front Door',1,1)
	db.addDevice(1000000002,1,'Back Door',0,0)
	db.addDevice(1000000003,0,'Front Lamp',1,1)
	db.addDevice(1000000004,0,'Back Lamp',0,0)
	
	# Initialzize camera client socket
	sm.createCamclients()

	# Start camera streaming by sending 'INIT' command. -Taken care by CameraMonitor itself.
					
	print 'Serial Listener starting'
	SerialListener.pollLine()

