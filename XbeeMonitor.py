#!/usr/bin/python
"""
Xbee monitor module
"""
# Python packages
import serial
from xbee import XBee
import threading
import socket
import sys, time, datetime, string
import os, subprocess

from subprocess import Popen, PIPE

#Email/Twitter Packages
import smtplib
import twitter

# Required packages
import DBManager as db
import CameraClient as cl



# Xbee Monitor class
class XbeeMonitor(object):

	# Class constructor __init__ function (default defined by python), ran upon instantiation
	def __init__(self, sport="/dev/ttyAMA0", sbaud=9600, stimeout="None"):
		# Data attributes (specific for each instance, accessed by self.var)
		self.ser = serial.Serial()
		self.ser.port = sport
		self.ser.baudrate = sbaud
		self.ser.timeout = stimeout  #None is block read. 1 is non-block read, 2 is timeout block read
	
	# Function to stop xbee background listening thread and close serial port	
	def stop(self):
		self.xbee.halt()
		self.ser.close()

	# Function to send Xbee frame to remote device AND apply change right away (need hex address '0013a20040a57ae9')
	def sendRemoteHexApply(self,_destAddrHex,_command,_parameter=''):
		_destAddrHexString = str(_destAddrHex)
		_parameterString = str(_parameter)
		self.xbee.remote_at(frame_id='A',dest_addr_long=_destAddrHexString.decode('hex'),command=_command,parameter=_parameterString.decode('hex'))

	# Function to send Xbee frame to remote device BUT NOT apply change right away (need hex address '0013a20040a57ae9')
	def sendRemoteHexNotApply(self,_destAddrHex,_command,_parameter=''):
		_destAddrHexString = str(_destAddrHex)
		_parameterString = str(_parameter)
		self.xbee.remote_at(frame_id='A',dest_addr_long=_destAddrHexString.decode('hex'),command=_command,parameter=_parameterString.decode('hex'),options='\x00')

	# Function to send Xbee frame to local coordinator
	def sendCoorHexApply(self,_command,_parameter=''):
		#_parameterString = str(_parameter)
		self.xbee.at(frame_id='A',command=_command,parameter=_parameter.decode('hex'))

	# Function to BLOCK and Wait for Xbee frame
	def waitReadFrame(self,_command):
		# BLOCK WAIT for valid Xbee frame
		_frame = self.xbee.wait_read_frame()

		print "Received frame %s" % _frame
		# Try parsing the frame for crucial fields
		if _frame.has_key('id'): _fid = _frame['id']
		else:
			print "No frame id field."
			return False
		#print "frame id %s" % _fid
		if _frame.has_key('status'): _fstatus = _frame['status']
		else:
			print "No frame status field."
			return False
		if _frame.has_key('command'): _fcommand = _frame['command']
		else:
			print "No frame command field."
			return False
		
		# Ignore frame with 'id' field is 'rx_long_addr' (garbage)
		if _fid != 'rx_long_addr':
			#print "fid: %s" % _fid
			# Valid frame, check for frame status
			if _fstatus  == '\x00' and _fcommand == _command:
				# Success repsonse
				#print "Status 00 and correct command %s" % _command
				if _command == 'NI':
					# Return parameter field
					if _frame.has_key('parameter'):
						_parameter = _frame['parameter']
						return _parameter
					else:
						return False
				else:
					return True
			else:
				# Failed response
				return False
				
	# Function to process incoming frame
	def processFrame(self,xbeeframe):
		# Try to parse for 'source_addr_long'
		if xbeeframe.has_key('source_addr_long'):
			# Source address in Hex, need to convert to String
			fsourceAddrHex = xbeeframe['source_addr_long']
			fsourceAddrString = fsourceAddrHex.encode('hex')
			# Example: fsourceAddrHex = '\x01\xjd', fsourceAddrString='0013a20040a57ae9'
			# Now need to use this hex string to look up for device in database
			#db.getDevice(int('0013a20040a57ae9',16))
			
			# Check database if device serial is valid
			device = db.getDevice(int(fsourceAddrString,16)) 
			if device is not None:
				# Extract device info
				dserial = device[0]
				dtype = device[1]
				dname = device[2]
				dstatus = device[3]
				dactive = device[4]
				dmessage = device[5]
				
				# Now parse frame for 'id'
				if xbeeframe.has_key('id'):
					fid = xbeeframe['id']
					if fid == 'rx_io_data_long_addr':
						# This should be active xbee signal from Door Sensor for open/close event
						print "DoorSensor: open or close event signal frame!"
						
						# Check if device is really a door (1)
						if dtype != 1:
							# dtype should be 1 (door), user may have the wrong type
							print "Non-door type while device should be a door!"
							db.updateDeviceMessage(dserial,"ShouldBeDoorType")
						else:
							# Expected Door type, parse for Samples and dio-0_status
							if xbeeframe.has_key('samples'):
								fsamples = xbeeframe['samples']
								# Only 'dio-0' pin is activated for Door samples at samples[0]
								dio0Pin = fsamples[0]
								if dio0Pin.has_key('dio-0'):
									pstatus = dio0Pin['dio-0']
									
									# Check door status, True is closed, False is opened
									if pstatus:
										# Door Close
										print "Door is closed!"

										# Update door status and message
										db.updateDeviceStatus(dserial,0)
										db.updateDeviceMessage(dserial,"DoorClosed")
										
										# Check if door is active
										if dactive == 1:
											# First check if this door is associated with a switch
											doortrigger = db.getDoorTrigger(dserial)
											if doortrigger is not None:
												# There is active doortriger, try sending command to associated switch
												switchserial = doortrigger[1]
												dooraction = doortrigger[2]
												# Check if there is switchserial set
												if switchserial is not None:
													switchserialHex='00%x' % int(switchserial)
													print "Door Trigger: %s %s" % (switchserialHex,dooraction)
													# Send Xbee command to the switch depending on the dooraction flag
													if dooraction == 1 and len(switchserialHex) > 15:
														# Turn off switch when door closes
														print "Turn switch %s off!" % switchserialHex
														self.sendRemoteHexApply(switchserialHex,'D0','04')
													elif dooraction == 2 and len(switchserialHex) > 15:
														# Turn on switch when door closes
														print "Turn switch %s on!" % switchserialHex
														self.sendRemoteHexApply(switchserialHex,'D0','05')
									else:
										# Door Open
										print "Door is opened!"
										
										# Update door status
										db.updateDeviceStatus(dserial,1)
																				
										# Check if door is active
										if dactive == 1:
											# Door is active, send email notifcation and start camera recording
											print "Door is active, send email notifcation and start camera recording"
											db.updateDeviceMessage(dserial,"DoorOpenedAndActive")
											
											# First check if this door is associated with a switch
											doortrigger = db.getDoorTrigger(dserial)
											if doortrigger is not None:
												# There is active doortriger, try sending command to associated switch
												switchserial = doortrigger[1]
												dooraction = doortrigger[2]
												# Check if there is switchserial set
												if switchserial is not None:
													switchserialHex='00%x' % int(switchserial)
													print "Door Trigger: %s %s" % (switchserialHex,dooraction)
													# Send Xbee command to the switch depending on the dooraction flag
													if dooraction == 1 and len(switchserialHex) > 15:
														# Turn on switch when door opens
														print "Turn switch %s on!" % switchserialHex
														self.sendRemoteHexApply(switchserialHex,'D0','05')
													elif dooraction == 2 and len(switchserialHex) > 15:
														# Turn off switch when door opens
														print "Turn switch %s off!" % switchserialHex
														self.sendRemoteHexApply(switchserialHex,'D0','04')
																			
											# Spawn new thread to perform door open actions
											DoorOpenThread(dserial).start()
											
										elif dactive == 0:
											# Door is unactive, do nothing
											print "Door is unactive, do nothing."
											db.updateDeviceMessage(dserial,"DoorOpenedButUnactive")
										else:
											# Invalid device active value
											print "Device error: invalid device active value %s" % dactive
											db.updateDeviceMessage(dserial,"DoorOpenedButInvalidActiveValue")
										
								else:
									# Cant find dio0 field for door status
									print "Frame error: No dio-0 field"
									db.updateDeviceMessage(dserial,"NoDoorStatus")
										
							else:
								# Cant find samples field
								print "Frame error: No samples field."
								db.updateDeviceMessage(dserial,"NoSamplesField")						
					
					elif fid == 'remote_at_response':
						# This should be passive xbee response from switches
						# Parse for status
						if xbeeframe.has_key('status'):
							# Status is in Hex, need to convert to String
							fstatusHex = xbeeframe['status']
							fstatusString = fstatusHex.encode('hex')
							if fstatusString == '04':
								# Failure frame status, remote Xbee module maybe down
								print "Response frame status is failed. Xbee may be off!"
								db.updateDeviceMessage(dserial,"XBeeOff")
								
							elif fstatusString == '00':
								# Success frame status, parse for parameter
								if xbeeframe.has_key('parameter'):
									# This frame is response from D0 command
									fparameterHex = xbeeframe['parameter']
									fparameterString = fparameterHex.encode('hex')
									if fparameterString == '03':
										# Unexpected door response from D0
										print "Response from D0: Door is 03 (Unexpected querry to DoorSensor)"
										db.updateDeviceMessage(dserial,"UnexpectedDoorChecked")
										
									elif fparameterString == '04':
										# Switch is off as acknowledgement for D0
										print "Response from D0: Switch is off"
										db.updateDeviceStatus(dserial,0)
										db.updateDeviceMessage(dserial,"SwitchOff")
										
									elif fparameterString == '05': 
										# Switch is on as acknowledgement for D0
										print "Response from D0: Switch is on"
										db.updateDeviceStatus(dserial,1)
										db.updateDeviceMessage(dserial,"SwitchOn")
									else:
										# Unknown parameter
										print "Response error: Unknown frame parameter %s" % fparameterString
										db.updateDeviceMessage(dserial,"UnknownStatus")									
								else:
									# No parameter field! This is response from D0 0X command
									print "Response from D0 0X: %s\nSending D0 command to confirm status" % dname
									db.updateDeviceMessage(dserial,"Done")
									
									# Send D0 command to check for device status
									# Need to convert decimal string to hex string and add extra byte '00' at front
									#dserialHex ='00'+hex(dserial).strip('0x').strip('L')
									dserialHex='00%x' % int(dserial)
									self.sendRemoteHexApply(dserialHex,'D0')
								
							else:
								# Unknown frame status
								print "Response error: Unknown frame status %s" % fstatusString
								db.updateDeviceMessage(dserial,"UnknownFrameStatus")
								
						else:
							# Frame does not have 'status' field
							print "Frame error: No status field."
							db.updateDeviceMessage(dserial,"NoStatusField")
											
					else:
						# Unknown frame id
						print "Frame error: Unknown frame id %s." % fid
						db.updateDeviceMessage(dserial,"UnknownFrameId")
				else:
					# Frame does not have 'id' field.
					print "Frame error: No id field."
					db.updateDeviceMessage(dserial,"NoIdField")
			else:
				# Cannot find device, ignore frame
				print "Device serial %s not found. IGNORE." % fsourceAddrString
			
		else:
			# Frame does not have 'source_addr_long' field. Ignore frame
			print "Frame error: no source_addr_long field. IGNORE."
		
	def startAsync(self):
		# Start xbee asynchronous background single-threaded thread to listen for new frame at certain serial port
		# If receiving new frame, it will pass the frame to the callback function
		# Any new coming frame will be buffered if it is still processing previous frame
		try: 
			self.ser.open()
			self.xbee = XBee(self.ser, callback=self.processFrame)

		except Exception, e:
			print "error open serial port: " + str(e)
			exit()

        def startSync(self):
                # Start xbee synchronous thread to listen for new frame at certain serial port
                try:
                        self.ser.open()
                        self.xbee = XBee(self.ser)

                except Exception, e:
                        print "error open serial port: " + str(e)
                        exit()


# Door Thread class
class DoorOpenThread(threading.Thread):
	def __init__(self, dserial):
		self.dserial = dserial
		self.camnodes = {}
		self.recordtime = 10
		super(DoorOpenThread, self).__init__()
		print "Total active Door threads: %d, Door: %s" % (threading.active_count(), self.dserial)

	def run(self):
		# Perform camera actions
		timestamp = datetime.datetime.now().strftime("%y_%m_%d.%H_%M_%S")
		mrecordfolder = 'record_' + timestamp
		
		# Getting device name
		dname = db.getDevice(self.dserial)[2]
		
		# Send email notifications
		emails = db.getEmails()
		for email in emails:
			print email[0]
			#sendEmail(email[0],dname,localtime,link)
			self.sendEmail(email[0],dname)
			
		#Send Twitter direct message
		api = twitter.Api(consumer_key='rovCalWcvqgzQpCp1ca5Rg',consumer_secret='Sas5tE0ljI3vYS7QXng3CB6yL3Fac4KaIaepLDFjkA',access_token_key='1632009878-fz4krrdmMSm6Fs1tLpfbzQlwS0UuUpC1ft5nkdJ',access_token_secret='bwn78QdcmhrRmW2QwnbjRWtj5f1OgAVms6AEimTwQg')
		directMessage = api.PostDirectMessage('@PiMationUVic', 'Sensor ' + dname + ' has been triggered on ' + timestamp)
		print directmessage
		
		# First get a list of all nodes in the system and add new socket if not existed
		nodes = db.getNodes()
		for node in nodes:
			nodename = node[0]
			nodeaddress = node[1]
			if not self.camnodes.has_key(nodename):
				# Try create a socket to the camera node
				camclient = cl.CameraClient(nodeaddress,44444)
				self.camnodes[nodename] = camclient	
				
		
		# For each of camera node, send recording request	
		for (nodename,camclient) in self.camnodes.items():
			print nodename, camclient
			camclient.send_wait("STARTRECORD,%s" % mrecordfolder)

		# Wait for recording time
		# Here should retrieve record time from database
		#self.recordtime = db.getRecordTime()
		time.sleep(self.recordtime)
		
		# For each of camera node, send resume request	
		for (nodename,camclient) in self.camnodes.items():
			print nodename, camclient
			camclient.send_wait("INIT")
			
			# Stored playback to database
			db.addPlayback(nodename,mrecordfolder)

		# Print all playback
		playbacks = db.getPlaybacks()
		for playback in playbacks:
			print "Nodename: %s recordfolder: %s" % (playback[0],playback[1])
		
	
		# Close all socket connections to remote cameras
		for (nodename,camclient) in self.camnodes.items():
			camclient.close()
		
	def sendEmail(self,_email,_dname):
	
		fromaddr = 'pimation.uvic@gmail.com'
		msg = "\r\n".join([
			"From: pimation.uvic@gmail.com",
			"Subject: PiMation Sensor Alert",
			"",
			"Sensor" + _dname + "has been triggered."
		])
		username = 'pimation.uvic@gmail.com'
	
		password = 'raspberrypimation'
		print 'start'
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(username,password)
		server.sendmail(fromaddr, _email, msg)
		server.quit()
		print 'end'


			
