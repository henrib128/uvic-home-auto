#!/usr/bin/python
"""
Main PiHome script
"""
import socket

# Required custome modules
import XbeeMonitor as xm
import DBManager as db
import CameraClient as cl

host = '142.104.165.35'
port = 50000


if __name__ == "__main__":

	print "PiHome starting!"
	
	# Initialize database
	db.initDatabase()

	# Populate database with some test values
	#db.addNode('router','24.52.152.172')
	db.addNode('Main Cam','142.104.165.35')
	db.addEmail('trihuynh87@gmail.com')
	db.addDevice(0x0013a20040a57ae9,0,'First Switch',0,1,'New')
	db.addDevice(0x0013a20040a57b39,1,'Front Door',1,1,'New')
	
	# Create a list of camera clients for each camera node
	camnodes={}
	nodes = db.getNodes()
	for node in nodes:
		nodename = node[0]
		nodeaddress = node[1]
		if nodename != 'router':
			print "Nodename: %s Ipaddress: %s" % (nodename,nodeaddress)
			# This must be a camera node, create camera client
			camclient = cl.CameraClient(nodeaddress,44444)
			camnodes[nodename] = camclient
				
	# Create XbeeMonitor instance
	XbeeMonitor = xm.XbeeMonitor(camnodes,"/dev/ttyAMA0", 9600, None)				
	XbeeMonitor.start()
	print "Start listnening to XBee frames in background..."
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	s.listen(10)
	
	while True:
		try:
			conn, addr = s.accept()
			data = conn.recv(1024)
			conn.close()
			print data
			words = data.split()
			if len(words) != 2 or len(words[1]) < 16:
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
			conn.close()
			exit()
		except Exception as e:
			conn.close()
			print str(e)
			exit()
			

