#!/usr/bin/python
#basic script to listen to the serial port
import CameraMonitor as cm
import CameraClient as cl
hostname=cm.getLocalIp()
port=44444
camClient = cl.CameraClient(hostname,port)

while True:
	try:
		command = raw_input()
		camClient.send(command)
	
	except KeyboardInterrupt:
		break

