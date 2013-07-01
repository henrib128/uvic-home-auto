#!/usr/bin/python
"""
Python script for monitoring serial input and updating database as needed
"""
import DBManager as db
		
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
db.addNode('master','192.168.1.12',8080)
db.addNode('camera1','192.168.1.11',8081)
db.updateNode('camera1','192.168.1.15',8082)
db.removeNode('router')
print db.getNode('router')
nodeinfo=db.getNode('camera1')
print nodeinfo

devices=db.getDevices()
for device in devices:
	print device
