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
import urllib2
import time;

from email.mime.text import MIMEText
from subprocess import Popen, PIPE

# Required packages
import DBManager as db
		
          
######################## Functions
           
# Function to send email
def sendEmail(_email,_dname):
	msg = MIMEText("Hello, we have detected your %s was opened Please click below for live stream update" % (_dname))
	msg["From"] = "minhtri@uvic.ca"
	msg["To"] = _email
	msg["Subject"] = "Notification from UVicPiHome"
	p = Popen(["/usr/sbin/sendmail", "-toi"], stdin=PIPE)
	p.communicate(msg.as_string())


# Function to submit url to refresh Apache server
def refreshUI():
    base = 'home'
    arg_string = 'Yo=Lo&Ha=y'
    url = "https://localhost/" + base + "?" + arg_string
    print url
    
    #Performs the actual submission of a URL generated for a command.
    #urllib2.urlopen(url)


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
			print 'Unknown device type: %s' % dtype
			return 'DB_ERROR'
		if dstatus != 0 and dstatus != 1:
			print 'Unknown device status: %s' % dstatus
			return 'DB_ERROR'
		if dactive != 0 and dactive != 1:
			print 'Unknown device active: %s' % dactive
			return 'DB_ERROR'
		
		# If new status is the same as current status, do nothing
		if dstatus == newStatus: return 'UNCHANGE'
		
		# Switch action
		if dtype == 0: event = 'SWITCH_UPDATE'
	
		# Door action
		if dtype == 1 and dactive == 0: event = 'DOOR_UPDATE'
		if dtype == 1 and dactive == 1 and dstatus == 1 and newStatus == 0: event = 'DOOR_CLOSE'
		if dtype == 1 and dactive == 1 and dstatus == 0 and newStatus == 1: event = 'DOOR_OPEN'
		
	# Cant find device serial
	else:
		print 'Device %s is not found' % _serial
		return 'NO_DEVICE'


	if event == 'SWITCH_UPDATE' or event == 'DOOR_UPDATE' or event == 'DOOR_CLOSE':
		print 'UPDATE'
		# Update DB
		db.updateDeviceStatus(_serial,_status)
		
		# Send WebUI refresh request
		refreshUI()
			
	if event == 'DOOR_OPEN':
		print 'DOOR_OPEN'
		# Update DB
		db.updateDeviceStatus(_serial,_status)
		
		# Send WebUI refresh request
		refreshUI()
		
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
			sendEmail(email[0],dname)
					
		# Perform camera actions
		
	
	

####### Main
db.initDatabase()

db.addNode('router','24.52.152.172')
db.addEmail('trihuynh87@gmail.com')
db.addEmail('minhtri@uvic.ca')
db.removeEmail('minhtri@uvic.ca')

db.addDevice(1000000000,0,'Living Lamp',0,1)
db.addDevice(1000000001,1,'Front Door',1,1)
db.addDevice(1000000002,1,'Back Door',0,1)
db.addDevice(1000000003,0,'Front Lamp',1,1)
db.addDevice(1000000004,0,'Back Lamp',0,1)


processEvent(10000000,0)
processEvent(1000000000,0)
processEvent(1000000000,1)
processEvent(1000000001,0)
processEvent(1000000001,1)
processEvent(1000000002,0)
#processEvent(1000000002,1)
processEvent(1000000003,0)
processEvent(1000000003,1)
processEvent(1000000004,0)
processEvent(1000000004,1)

"""
# Unit test
db.addDevice(1000000000,0,'Living Lamp',0,0)
db.addDevice(1000000001,1,'Front Door',0,0)
db.addDevice(1000000002,1,'Back Door',1,1)

db.removeDevice(1000000002)
db.removeDevice(1000000003)

db.updateDeviceStatus(1000000000,1)
db.updateDeviceStatus(1000000001,1)
db.updateDeviceActive(1000000001,1)
db.updateDeviceActive(1000000002,1)
db.changeDeviceName(1000000000,'trideptrai')
db.changeDeviceName(1000000001,'yolo')
db.changeDeviceType(1000000000,2)
db.changeDeviceType(1000000001,1)
device1 = db.getDevice(1000000000)
print device1
device2 = db.getDevice(1000000001)
print device2
db.changePassword('pihome','pihomepass','haha')
db.changePassword('pihome','pihomepass','haha')

db.addEmail('trihuynh87')
db.addEmail('trihuynh877')
db.removeEmail('trihuynh')
#removeEmail('trihuynh877')

emails=db.getEmails()
for email in emails:
	print email

db.addNode('router','24.52.152.172')
db.addNode('master','192.168.1.12')
db.addNode('camera1','192.168.1.11')
db.updateNode('camera1','192.168.1.15')
db.removeNode('router')
print db.getNode('router')
nodeinfo=db.getNode('camera1')
print nodeinfo

devices=db.getDevices()
for device in devices:
	print device
	
	
"""
