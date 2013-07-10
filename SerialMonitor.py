#!/usr/bin/python
"""
Active Python script to always receive serial data inputs, i.e. XBEE requests, and perform needed actions
Expected Serial requests: serial, status(on/off)
Scope:
- Receive new Serial request in form of (serial, status)
- Check DB for serial -> map with device and extract current device status (on/off)
- If device is valid
	. Determine nature of Event based on previous status and device type and active
		+ If Door 
			Door is inactive -> DoorUpdate
			Door is active
			   preStatus = close and curStatus = open -> DoorOpen
			   PreStatus = open and curStatus = close -> DoorClose
			   PreStatus = curStatus (open/close) -> DoorUnchange
	    + If Switch
	    	Switch is inactive -> SwitchUpdate
	    	Switch is active -> SwitchUpdate

    . Depending on Event, perform the following actions
    	+ If DoorUpdate
    		Update DB for new door status
    		Update WebUI by sending internal URL 'refresh' request
    		
    	+ If DoorOpen
    		Update DB for new door status
    		Update WebUI by sending internal URL 'refresh' request
    		Send Email notification based on list of emails from DB
    		Camera actions:
    			Restart ALL mpjg-streamer servers to perform dual outputs www and internal dir for some period of time
    			Start timer:
    			#./mjpg_streamer -i "./input_testpicture.so" -o "./output_file.so -f ./record_DATE_TIME" -o "./output_http.so -w ./www" & 
       			./mjpg_streamer -i "./input_uvc.so -f 30 -r 640x480" -o "./output_file.so -f ./record_DATE_TIME" -o "./output_http.so -w ./www" & 
       			
    			End record time: Restart ALL mpjg-streamer with default www output
    			./mjpg_streamer -i "./input_uvc.so -f 30 -r 640x480" -o "./output_http.so -w ./www" & 
    			
    			Playback action: Restart certain mpjg-streamer to ouput www from a tmp directory:
    			./mjpg_streamer -i "./input_file.so -r -d 1 -f ./tmp" -o "./output_http.so -w ./www" &

    			Also run an 'update' script to refresh ./tmp/playback.jpg image from specified recorded $picdir directory
    			for pic in $picdir/* do	cp $pic $tmpdir/playback.jpg; sleep 1; done 
    			
    			After done, recover normal mjpg-streamer operation
    			./mjpg_streamer -i "./input_uvc.so -f 30 -r 640x480" -o "./output_http.so -w ./www" & 
    			    			    		
    	+ If DoorClose
    		Update DB for new door status
    		Update WebUI by sending internal URL 'refresh' request

    	+ If DoorUnchange -> do nothing
    	
    	+ If SwithcUpdate
    		Update DB for new switch status
    		Update WebUI by sending internal URL 'refresh' request
    	
"""

# Python packages
import sys
import time
import serial, threading

from email.mime.text import MIMEText
from subprocess import Popen, PIPE

# Required packages
import DBManager as db
		
######################## Classes
# Serial thread class
class SerialThread(threading.Thread):
	def __init__(self, threadid, data):
		self.threadid = threadid
		self.data = data
		super(SerialThread, self).__init__()
		print "Serial thread#%d: total threads: %d, data: %s" % (self.threadid, threading.active_count(), self.data)

	def run(self):
		# Parse data and process request
		self.processRequest(self.data)

	def processRequest(self, request):
		# Parse request, if request is indeed (_serial,_status)
		try:
			request=request.strip('\n') # strip out eol '\n' char from readline()
			request_split=request.split(" ")
			serial = request_split[0]
			status = request_split[1]
			print "Serial: %s Status: %s" % (serial, status)
			# Call processEvent function
			processEvent(serial, int(status))

		except Exception, e:
			print "Error parsing request: " + str(e)
		

# Serial Monitor class
class SerialMonitor(object):
    # Static Var (class attribute): accessed by <class>.var or self.__class__.var
    # server="SerialMonitor"

    # Class constructor __init__ function (default defined by python), ran upon instantiation
    def __init__(self, sport="/dev/pts/3", sbaud=9600, stimeout=None):
		# Data attributes (specific for each instance, accessed by self.var)
		self.ser = serial.Serial()
		self.count = 0
        
		# Initialize serial chanel properties
		self.ser.port = sport
		self.ser.baudrate = sbaud
		self.ser.timeout = stimeout  #None is block read. 1 is non-block read, 2 is timeout block read
		self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
		self.ser.parity = serial.PARITY_NONE #set parity check: no parity
		self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
		self.ser.xonxoff = False     #disable software flow control
		self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
		self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
		self.ser.writeTimeout = 2     #timeout for write
		
    def pollLine(self):
		# Start reading from serial port
		try: 
			self.ser.open()

		except Exception, e:
			print "error open serial port: " + str(e)
			exit()

		if self.ser.isOpen():
			try:
				self.ser.flushInput() #flush input buffer, discarding all its contents
				self.ser.flushOutput()#flush output buffer, aborting current output 
							     	  #and discard all that is in buffer
				while True:
					response = self.ser.readline() # if block-read, expected eol '\n' char, if not wait forever!
					print("read data: " + response)
					# Spawn new thread to take care of this request
				
					if (response == 'exit\n'):
						break
						
					if response:
						self.count += 1
						SerialThread(self.count,response).start()
		   
				self.ser.close()

			except Exception, e1:
				print "error communicating...: " + str(e1)

		else:
			print "cannot open serial port "

    def writeLine(self, data):
		# Start writing to serial port
		try: 
			self.ser.open()

		except Exception, e:
			print "error open serial port: " + str(e)
			exit()

		if self.ser.isOpen():
			try:
				self.ser.flushInput() #flush input buffer, discarding all its contents
				self.ser.flushOutput()#flush output buffer, aborting current output 
							     	  #and discard all that is in buffer
				# Write to serial port with eol char
				self.ser.write(data + '\n')
		   		
		   		# Close port afterward
				self.ser.close()

			except Exception, e1:
				print "error communicating...: " + str(e1)

		else:
			print "cannot open serial port "
			

######################## Functions
           
# Function to send email
def sendEmail(_email,_dname):
	msg = MIMEText("Hello, we have detected your %s was opened Please click below for live stream update" % (_dname))
	msg["From"] = "minhtri@uvic.ca"
	msg["To"] = _email
	msg["Subject"] = "Notification from UVicPiHome"
	p = Popen(["/usr/sbin/sendmail", "-toi"], stdin=PIPE)
	p.communicate(msg.as_string())


# Function to determine Event, assuming input parameters are in correct format
# _serial: 1000000000 (16 bit big int number)
# _data: 0 for off, 1 for on
def processEvent(_serial, _status):
	# Extract device info based on serial number <dserial, dtype, dname, dstatus, dactive>
	device = db.getDevice(_serial)
	
	# Current device status (0 for off, 1 for on)
	newStatus = _status
	
	# Perform actions if device is valid
	if device is not None:
		# Extract device info
		dserial = device[0]
		dtype = device[1]
		dname = device[2]
		dstatus = device[3]
		dactive = device[4]
		
		# Debug
		print "Current device info: %s %s %s %s %s" % (dserial,dtype,dname,dstatus,dactive)
		print "New device status: %s" % newStatus
		
		# First sanitize database data
		if dtype != 0 and dtype != 1:
			print "Unknown device type: %s" % dtype
			return
		if dstatus != 0 and dstatus != 1:
			print "Unknown device status: %s" % dstatus
			return
		if dactive != 0 and dactive != 1:
			print "Unknown device active: %s" % dactive
			return
		
		# Sanitize status change request
		if newStatus != 0 and newStatus != 1:
			print "Unknown device status: %s" % newStatus
			return
			
		# If new status is the same as current status, do nothing
		if dstatus == newStatus:
			print 'UNCHANGE'
			return
		
		# Switch action
		if dtype == 0: event = 'SWITCH_UPDATE'
	
		# Door action
		if dtype == 1 and dactive == 0: event = 'DOOR_UPDATE'
		if dtype == 1 and dactive == 1 and dstatus == 1 and newStatus == 0: event = 'DOOR_CLOSE'
		if dtype == 1 and dactive == 1 and dstatus == 0 and newStatus == 1: event = 'DOOR_OPEN'
		
	# Cant find device serial
	else:
		print 'Device %s is not found' % _serial
		return

	# Take action for valid event
	if event == 'SWITCH_UPDATE' or event == 'DOOR_UPDATE' or event == 'DOOR_CLOSE':
		print 'UPDATE'
		# Update DB
		db.updateDeviceStatus(_serial,_status)
			
	if event == 'DOOR_OPEN':
		print 'DOOR_OPEN'
		# Update DB
		db.updateDeviceStatus(_serial,_status)
		
		# Send email notifications
		localtime = time.asctime(time.localtime(time.time()))
		print localtime
		router_ip=db.getNode('router')[1]
 		link = "http://%s/camera" % router_ip
 		print link
		emails = db.getEmails()
		for email in emails:
			print email[0]
			#sendEmail(email[0],dname,localtime,link)
			#sendEmail(email[0],dname)
					
		# Perform camera actions


