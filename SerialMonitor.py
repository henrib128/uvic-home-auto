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
import DBManager as db
		


######################## Functions


# Function to parse for Serial Data
#def parseSerialData():
	# empty


# Function to process Serial Data
def processSerialRequest(_serial, _data):
	# Extract device info based on serial number <dserial, dtype, dname, dstatus, dactive>
	device=db.getDevice(_serial)

	# Perform actions if device is valid
	#if device is not None:
		# Extract device info

####### Main
db.initDatabase()

db.addDevice(1000000000,1,'device1',0,1)
db.addDevice(1000000000,2,'device1',0,1)
db.addDevice(1000000001,0,'device2',1,1)
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
