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


# Function to try checking frames
def checkCommandResponse(_xbm,_command):
	# Try receiving up to 5 frames for ok response
	OK = False
	for i in range(1, 5):
		response = _xbm.waitReadFrame(_command)
		print "Done waiting frame"
		if response: 
			OK = True
			break
	# If still havent got ok resposne, abort!
	return OK

# Function to add new xbee device to current Xbee network
# Assumptions:
#	- Xbee Coordinator is configured: SCAN = off, KY = <network key>
#   - Xbee EndDevice is default: SCAN = on, KY = default, SLEEP = off
def addXbeeDevice(_xbm,_dserial):
	default_key='012345'
	# 0. Retrieve network key
	network_key='0ABCDE'
	print "Entering addXbeeDevice"
	# 1. Change Coordinator to default KY
	_xbm.sendCoorHexApply('KY',default_key)
	print "Done sending coor hex"
	if not checkCommandResponse(_xbm,'KY'):
		print "Failed to change coordinator to default KY"
		return False
	
	print "Done Coordinator KY default"
	# 1b. Confirm if Coordinator can talk to EndDevice now
	_xbm.sendRemoteHexApply(_dserial,'SL')
	print "Done send remote"
	if not checkCommandResponse(_xbm,'SL'):		
		print "Failed to talk to end device with default KY"
		return False
	print "Done checking talking in default KY"
	
	# 2. Change EndDevice to network KY
	_xbm.sendRemoteHexApply(_dserial,'KY',network_key)
	# Try receiving up to 5 frames for ok response
	if not checkCommandResponse(_xbm,'KY'):	
		print "Failed to change end device to network KY"
		return False
	print "Done changing Device KY network"
	
	# 3. Change Coordinator to network KY
	_xbm.sendCoorHexApply('KY',network_key)
	# Try receiving up to 5 frames for ok response
	if not checkCommandResponse(_xbm,'KY'):
		print "Failed to change coordinator to network KY"
		return False
	print "Done changing Coordinator KY network"	

	# 3.b Confirm if coordinator can talk to end device using network KY
	_xbm.sendRemoteHexApply(_dserial,'SL')
	# Try receiving up to 5 frames for ok response
	if not checkCommandResponse(_xbm,'SL'):	
		print "Failed to talk to end device with network KY"
		return False
	print "Done talking to device in network KY"

	# 4. Lock EndDevice to Coordinator
	_xbm.sendRemoteHexApply(_dserial,'A1','04')
	# Try receiving up to 5 frames for ok response
	if not checkCommandResponse(_xbm,'A1'):	
		print "Failed to lock end device with coordinator"
		return False

	# 5. Write changes to EndDevice
	_xbm.sendRemoteHexApply(_dserial,'WR')
	# Try receiving up to 5 frames for ok response
	if not checkCommandResponse(_xbm,'WR'):
		print "Failed to write to end device"
		return False
		
	# Retrieving device type based on NI field
	_xbm.sendRemoteHexApply(_dserial,'NI')
	# Try receiving up to 5 frames for ok response
	OK = False
	for i in range(1,5):
		dtype = _xbm.waitReadFrame('NI')
		if dtype: 
			OK = True
			break
	# If still havent got ok resposne, abort!
	if not OK:		
		print "Failed to write to end device"
		return False
	
	if dtype == 'DS': dtype = 1
	elif dtype == 'PS': dtype = 0
	else:
		print "Unknown device type %s" % dtype
		return False
		
	# Store device type to database ('0013A20040A57AE9') -> 0x0013A20040A57AE9
	db.changeDeviceType(int(_dserial,16),dtype)
	
	# Set sleep mode if it's a DoorSensor
	if dtype == 1:
		# 6. Set EndDevice SLEEP mode to 1 WITHOUT APPLYING CHANGE
		_xbm.sendRemoteHexNotApply(_dserial,'SM','01')
		# Try receiving up to 5 frames for ok response
		if not checkCommandResponse(_xbm,'SM'):
			print "Failed to configure sleep mode for end device"
			return False
			
		# 7. Write changes to EndDevice
		_xbm.sendRemoteHexApply(_dserial,'WR')
		# Try receiving up to 5 frames for ok response
		if not checkCommandResponse(_xbm,'WR'):	
			print "Failed to write to end device"
			return False
	
		# 8. Apply changes to enable SLEEP MODE
		_xbm.sendRemoteHex(_dserial,'AC')
		# Try receiving up to 5 frames for ok response
		if not checkCommandResponse(_xbm,'AC'):
			print "Failed to apply changes to end device"
			return False
		
		# Everything went through! Return okay
		return True

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
	#db.addDevice(0x0013a20040a57ae9,0,'First Switch',0,1,'New')
	hexstring = '0013a20040a57ae9'
	db.addDevice(int(hexstring,16),0,'First Switch',0,1,'New')
	#db.addDevice(0x0013a20040a57b39,1,'Front Door',1,1,'New')
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
				print "Stop current Xbee"
				# Start XbeeMonitor with synchronous mode
				XbeeMonitor.startSync()
				print "Start new Sycn Xbee"
				# Adding new device command
				result = addXbeeDevice(XbeeMonitor,dserial)
				if result:
					db.updateDeviceMessage(dserial,"Added")
				else:
					db.updateDeviceMessage(dserial,"FailedToAdd")
				
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
			

