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
	for i in range(1, 10):
		if _txtype == "coor":
			_xbm.sendCoorHexApply(_command,_param)
		elif _txtype == "dapply":
			_xbm.sendRemoteHexApply(_dserial,_command,_param)
		elif _txtype == "dnotapply":
			_xbm.sendRemoteHexNotApply(_dserial,_command,_param)

		# BLOCK WAIT for valid Xbee frame response
		response = _xbm.waitReadFrame(_command)

		if response: 
			OK = True
			time.sleep(1)
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

	# 0. First try if Coor can already talk to remote device on Network KY (existing device)
	#if not checkCommandResponse(_xbm,'dapply',_dserial,'SL',''):	
		# Cant talk to device the way it is, need to start normal setup
	
	# 1. Change Coordinator to default KY
	if not checkCommandResponse(_xbm,'coor','','KY',default_key):
		_message = "Failed to change coordinator to default KY"
		print _message
		return _message
	print "Done Coordinator KY default"

	# 1b. Confirm if Coordinator can talk to EndDevice now
	if not checkCommandResponse(_xbm,'dapply',_dserial,'SL',''):		
		_message = "Failed to talk to end device with default KY"
		print _message

		# Revert Coordinator back to Network key
		if not checkCommandResponse(_xbm,'coor','','KY',network_key):
			_message = "Failed to revert coordinator to network KY. Please restart Pi!"
			print _message
			return _message
	
		return _message
	print "Done checking talking in default KY"

	# 2. Change EndDevice to network KY
	if not checkCommandResponse(_xbm,'dapply',_dserial,'KY',network_key):	
		_message = "Failed to change end device to network KY"
		print _message
	
		# Revert Coordinator back to Network key
		if not checkCommandResponse(_xbm,'coor','','KY',network_key):
			_message = "Failed to revert coordinator to network KY. Please restart Pi!"
			print _message
			return _message
		
		return _message
	print "Done changing Device KY network"

	# 3. Change Coordinator to network KY
	if not checkCommandResponse(_xbm,'coor','','KY',network_key):
		_message = "Failed to change coordinator to network KY. Please restart Pi!"
		print _message
		return _message
	print "Done changing Coordinator KY network"	

	# 3.b Confirm if coordinator can talk to end device using network KY
	if not checkCommandResponse(_xbm,'dapply',_dserial,'SL',''):	
		_message = "Failed to talk to end device with network KY"
		print _message
		return _message
	print "Done talking to device in network KY"

	#else:
		# Device is already on Network KY! Proceed with step 4
	#	print "Device is already on network KY"
	
	# 4. Lock EndDevice to Coordinator
	if not checkCommandResponse(_xbm,'dapply',_dserial,'A1','04'):	
		_message = "Failed to lock end device with coordinator"
		print _message
		return _message
	print "Done locking device to network KY"

	# 5. Write changes to EndDevice
	if not checkCommandResponse(_xbm,'dapply',_dserial,'WR',''):
		_message = "Failed to write to end device"
		print _message
		return _message
	print "Done writing lock"

	# Retrieving device type based on NI field
	OK = False
	for i in range(1,10):
		_xbm.sendRemoteHexApply(_dserial,'NI')
		dtype = _xbm.waitReadFrame('NI')
		if dtype: 
			OK = True
			break
		
		# Wait for 2 sec before retry
		time.sleep(2)

	# If still havent got ok resposne, abort!
	if not OK:		
		_message = "Failed to write to end device"
		print _message
		return _message
	
	if dtype == 'DS': dtype = 1
	elif dtype == 'PS': dtype = 0
	else:
		_message = "Unknown device type %s" % dtype
		print _message
		return _message

	# Store device type to database ('0013A20040A57AE9') -> 0x0013A20040A57AE9
	db.changeDeviceType(int(_dserial,16),dtype)
	print "Done checking NI %s and storing device type to database" % dtype
		
	# Set sleep mode if it's a DoorSensor
	if dtype == 1:
		# 6. Set EndDevice SLEEP mode to 1 WITHOUT APPLYING CHANGE
		if not checkCommandResponse(_xbm,'dnotapply',_dserial,'SM','01'):
			_message = "Failed to configure sleep mode for end device"
			print _message
			return _message
		print "Done sleep mode"

		# 7. Write changes to EndDevice
		if not checkCommandResponse(_xbm,'dapply',_dserial,'WR',''):	
			_message = "Failed to write to end device"
			print _message
			return _message
		print "Done sleep write"

		# 8. Apply changes to enable SLEEP MODE
		if not checkCommandResponse(_xbm,'dapply',_dserial,'AC',''):
			_message = "Failed to apply changes to end device"
			print _message
			return _message
		print "Done apply changes"

		# Everything went through! Return okay
		_message = "New device is added successfully"
		return _message

# Main body of script
if __name__ == "__main__":

	print "PiHome starting!"
	
	# Initialize database
	#db.initDatabase()

	# Populate database with some test values
	#mainnodename = 'Main Pi'
	#mainnodeaddr = getLocalIp()
	#db.addNode(mainnodename,mainnodeaddr)
	#db.addNode('Rear Cam','142.104.167.186')
	#db.addEmail('trihuynh87@gmail.com')
	#testswitch = '0013a20040a57ae9'
	#testdoor = '0013a20040a184ce'
	#db.addDevice(int(testswitch,16),0,'First Switch',0,1,'New')
	#db.addDevice(int(testdoor,16),1,'Back Door',1,0,'New')
	
	# Create XbeeMonitor instance
	XbeeMonitor = xm.XbeeMonitor("/dev/ttyAMA0", 9600, None)				
	XbeeMonitor.startAsync()
	print "Start listnening to XBee frames in background..."
	
	# Create socket to listen to PHP Webserver request
	host = getLocalIp()
	port = 50000
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set socket property
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((host, port))
	#sock.listen(100)
	
	# Always listening to new socket connection request from Webserver PHP script
	while True:
		try:
			sock.listen(100)
			# Receiving new socket connection request
			conn, addr = sock.accept()
			# Receive new data
			data = conn.recv(1024)
			conn.close()
			print data
			
			# Parse data for valid PHP requests
			# Valid request should be in form of "webcommand/pi/dserial"
			words = data.split('/pi/')
			if len(words) != 2:
				print 'Invalid request. Valid request should be in form of "webcommand dserial"'
				continue

			# Assuming valid request in form of webcommand and device serial
			webcommand = words[0]
			webparam = words[1]
			
			# Perform actions based on webcommand
			if webcommand == 'off':
				# Turn off power switch command
				dserial=webparam
				if len(webparam) < 16:
					# Dserial must be 16 or more letters
					print "Dserial must be 16 or more letters"
					continue
				# Send request to remote Device
				XbeeMonitor.sendRemoteHexApply(dserial,'D0','04')
							
			elif webcommand == 'on':
				# Turn on power switch command
				dserial=webparam
				if len(webparam) < 16:
					# Dserial must be 16 or more letters
					print "Dserial must be 16 or more letters"
					continue

				# Send request to remote Device						
				XbeeMonitor.sendRemoteHexApply(dserial,'D0','05')
				
			elif webcommand == 'adddevice':
				# Add new device, need to trigger configuration mode
				dserial=webparam
				print "Add device command from the web for %s." % dserial
				if len(dserial) < 16:
					# Dserial must be 16 or more letters
					print "Dserial must be 16 or more letters"
					continue
			
				# Stop XBeeMonitor
				XbeeMonitor.stop()
				print "Stopped current Asynchronous Xbee"

				# Start XbeeMonitor with synchronous mode
				XbeeMonitor.startSync()
				print "Started new Sychronous Xbee"

				# Adding new device command, update status for user
				message = addXbeeDevice(XbeeMonitor,dserial)
				db.updateDeviceMessage(int(dserial,16),message)
				
				# Remove garbage device from database if it is not added
				#if message != 'New device is added successfully':
					# Fail to add new device, remove it from database
					#db.removeDevice(int(dserial,16))
				
				# Restart XBeeMonitor and have it run in background again
				XbeeMonitor.stop()
				XbeeMonitor.startAsync()

			else:
				print 'Invalid input'
				continue
	
		except Exception as e:
			print "Exception: %s" % e
			sock.close()
			XbeeMonitor.stop()
			exit()
		except KeyboardInterrupt:
			sock.close()
			XbeeMonitor.stop()
			exit()

	# close socket connection
	print "Stop listening to Web server, close socket, stop XbeeMonitor"
	sock.close()
	XbeeMonitor.stop()
