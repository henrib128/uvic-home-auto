#!/usr/bin/python

import socket
import DBManager as db

def getLocalIp():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	ipaddr = s.getsockname()[0]
	s.close()
	return ipaddr

if __name__ == "__main__":

	# Initialize database
	db.initDatabase()

	# Populate database with some test values
	#db.addNode('router','24.52.152.172')
	db.addNode('Main Cam',getLocalIp())
	db.addEmail('trihuynh87@gmail.com')
	db.addDevice(0x0013a20040a57ae9,0,'First Switch',0,1,'New')
	db.addDevice(0x0013a20040a57b39,1,'Front Door',1,1,'New')
	
