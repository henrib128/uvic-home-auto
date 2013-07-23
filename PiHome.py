#!/usr/bin/python
"""
Main PiHome script
"""
import socket, time

# Required custome modules
import XbeeMonitor as xm
import DBManager as db
import CameraClient as cl

# Function to get local ipaddress (i.e. 192.168.0.190)
def getLocalIp():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	ipaddr = s.getsockname()[0]
	s.close()
	return ipaddr

# Function to add new xbee device to current Xbee network
# Assumptions:
#	- Xbee Coordinator is configured: SCAN = off, KY = <network key>
#   - Xbee EndDevice is default: SCAN = on, KY = default, SLEEP = off
def addXbeeDevice(_xbm,_dserial):
	default_key='012345'
	# 0. Retrieve network key
	network_key='0ABCDE'

	# 1. Change Coordinator to default KY
	_xbm.sendCoorHexApply('KY',default_key)
	time.sleep(1)
	
	# 2. Change EndDevice to network KY
	_xbm.sendRemoteHexApply(_dserial,'KY',network_key)
	time.sleep(1)
	
	# 3. Change Coordinator to network KY
	_xbm.sendCoorHexApply('KY',network_key)
	time.sleep(1)
	
	# 4. Lock EndDevice to Coordinator
	_xbm.sendRemoteHexApply(_dserial,'A1','04')
	
	# 5. Write changes to EndDevice
	_xbm.sendRemoteHexApply(_dserial,'WR')

	# Retrieving device type based on NI field
	_xbm.sendRemoteHexApply(_dserial,'NI')
	# Wait for a bit for response to come back and device type is updated
	
	# Set sleep mode if it's a DoorSensor
	if dtype == 'DS':
		# 6. Set EndDevice SLEEP mode to 1 WITHOUT APPLYING CHANGE
		_xbm.sendRemoteHexNotApply(_dserial,'SM','01')
	
		# 7. Write changes to EndDevice
		_xbm.sendRemoteHexApply(_dserial,'WR')
	
		# 8. Apply changes to enable SLEEP MODE
		_xbm.sendRemoteHex(_dserial,'AC')


# Main body of script
if __name__ == "__main__":

	print "PiHome starting!"
	
	# Initialize database
	db.initDatabase()

	# Populate database with some test values
	#db.addNode('router','24.52.152.172')
	db.addNode('Main Cam','142.104.165.35')
	db.addNode('Rear Cam','142.104.167.186')
	db.addEmail('trihuynh87@gmail.com')
	db.addDevice(0x0013a20040a57ae9,0,'First Switch',0,1,'New')
	db.addDevice(0x0013a20040a57b39,1,'Front Door',1,1,'New')
	db.addDevice(0x0013a20040a184ce,1,'Back Door',1,0,'New')
	
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
	XbeeMonitor.startAsync()
	print "Start listnening to XBee frames in background..."
	
	# Create socket to listen to PHP Webserver request
	host = getLocalIp()
	port = 50000
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host, port))
	sock.listen(100)
	
	# Always listening to new socket connection request from Webserver PHP script
	while True:
		try:
			# Receiving new socket connection request
			conn, addr = sock.accept()
			# Receive new data
			data = conn.recv(1024)
			conn.close()
			print data
			
			# Parse data for valid PHP requests
			# Valid request should be in form of "webcommand dserial"
			words = data.split()
			if len(words) != 2 or len(words[1]) < 16:
				print 'Invalid input'
				continue

			# Assuming valid request in form of webcommand and device serial
			webcommand = words[0]
			dserial = words[1]
			
			# Perform actions based on webcommand
			if webcommand == 'off':
				# Turn off power switch command
				# Send request to remote Device							
				XbeeMonitor.sendRemoteHexApply(dserial,'D0','04')
							
			elif webcommand == 'on':
				# Turn on power switch command
				# Send request to remote Device							
				XbeeMonitor.sendRemoteHexApply(dserial,'D0','05')
				
			elif webcommand == 'add':
				print "This is add command from the web for %s\nShut XbeeMonitor down. Wait 10 sec. Then turn it back on." % dserial
				# Stop XBeeMonitor
				XbeeMonitor.stop()
				
				# Start XbeeMonitor with synchronous mode
				XbeeMonitor.startSync()
				
				# Adding new device command
				time.sleep(10)
				#addXbeeDevice(dserial)
				
				# Restart XBeeMonitor and have it run in background again
				XbeeMonitor.stop()
				XbeeMonitor.startAsync()
				
			else:
				print 'Invalid input'
				continue
	
		except KeyboardInterrupt:
			conn.close()
			sock.close()
			exit()
		except Exception as e:
			conn.close()
			sock.close()
			print str(e)
			exit()
			

