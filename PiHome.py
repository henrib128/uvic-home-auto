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
def checkCommandResponse(_xbm,_txtype,_dserial,_command,_param):
	OK = False
	for i in range(1, 5):
		if _txtype == "coor":
			_xbm.sendCoorHexApply(_command,_param)
		elif _txtype == "dapply":
			_xbm.sendRemoteHexApply(_dserial,_command,_param)
		elif _txtype == "dnotapply":
			_xbm.sendRemoteHexNotApply(_dserial,_command,_param)

		response = _xbm.waitReadFrame(_command)
		#print "Done waiting frame"
		if response: 
			OK = True
			break

		# Wait for 2 sec before retry
		time.sleep(2)
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
	# Try receiving up to 5 frames for ok response
	print "Entering addXbeeDevice"
	# 1. Change Coordinator to default KY
	if not checkCommandResponse(_xbm,'coor','','KY',default_key):
		print "Failed to change coordinator to default KY"
		return False
	print "Done Coordinator KY default"

	# 1b. Confirm if Coordinator can talk to EndDevice now
	if not checkCommandResponse(_xbm,'dapply',_dserial,'SL',''):		
		print "Failed to talk to end device with default KY"
		return False
	print "Done checking talking in default KY"
	
	# 2. Change EndDevice to network KY
	if not checkCommandResponse(_xbm,'dapply',_dserial,'KY',network_key):	
		print "Failed to change end device to network KY"
		return False
	print "Done changing Device KY network"
	
	# 3. Change Coordinator to network KY
	if not checkCommandResponse(_xbm,'coor','','KY',network_key):
		print "Failed to change coordinator to network KY"
		return False
	print "Done changing Coordinator KY network"	

	# 3.b Confirm if coordinator can talk to end device using network KY
	if not checkCommandResponse(_xbm,'dapply',_dserial,'SL',''):	
		print "Failed to talk to end device with network KY"
		return False
	print "Done talking to device in network KY"

	# 4. Lock EndDevice to Coordinator
	if not checkCommandResponse(_xbm,'dapply',_dserial,'A1','04'):	
		print "Failed to lock end device with coordinator"
		return False
	print "Done locking device to network KY"

	# 5. Write changes to EndDevice
	if not checkCommandResponse(_xbm,'dapply',_dserial,'WR',''):
		print "Failed to write to end device"
		return False
	print "Done writing lock"

	# Retrieving device type based on NI field
	OK = False
	for i in range(1,5):
		_xbm.sendRemoteHexApply(_dserial,'NI')
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
	print "Done checking NI %s" % dtype

	# Store device type to database ('0013A20040A57AE9') -> 0x0013A20040A57AE9
	db.changeDeviceType(int(_dserial,16),dtype)
	
	# Set sleep mode if it's a DoorSensor
	if dtype == 1:
		# 6. Set EndDevice SLEEP mode to 1 WITHOUT APPLYING CHANGE
		if not checkCommandResponse(_xbm,'dnotapply',_dserial,'SM','01'):
			print "Failed to configure sleep mode for end device"
			return False
		print "Done sleep mode"

		# 7. Write changes to EndDevice
		if not checkCommandResponse(_xbm,'dapply',_dserial,'WR',''):	
			print "Failed to write to end device"
			return False
		print "Done sleep write"

		# 8. Apply changes to enable SLEEP MODE
		if not checkCommandResponse(_xbm,'dapply',_dserial,'AC',''):
			print "Failed to apply changes to end device"
			return False
		print "Done apply changes"

		# Everything went through! Return okay
		return True

# Main body of script
if __name__ == "__main__":

	print "PiHome starting!"
	
	# Initialize database
	#db.initDatabase()

	# Populate database with some test values
	mainnodename = 'Main Pi'
	mainnodeaddr = getLocalIp()
	db.addNode(mainnodename,mainnodeaddr)
	#db.addNode('Rear Cam','142.104.167.186')
	db.addEmail('trihuynh87@gmail.com')
	testswitch = '0013a20040a57ae9'
	testdoor = '0013a20040a184ce'
	db.addDevice(int(testswitch,16),0,'First Switch',0,1,'New')
	db.addDevice(int(testdoor,16),1,'Back Door',1,0,'New')
	
	# Create a list of camera clients for each camera node
	# TODOO: This should be removed and should NOT be passed to XBeeMonitor.
	# All camera node socket clients should be stored in database, and XBeeMonitor should retrieved a list of clients from DB
	# So if new camera is added, all it's needed to do is create new socket client for that camera, add to datbase, and thats it
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
					db.updateDeviceMessage(int(dserial,16),"Added")
				else:
					db.updateDeviceMessage(int(dserial,16),"FailedToAdd")
				
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
			

