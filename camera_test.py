#!/usr/bin/python
#basic script to listen to the serial port
import CameraClient as cl
hostname=cl.getLocalIp()
port=44444
camClient = cl.CameraClient(hostname,port)

while True:
	try:
		command = raw_input()
		camClient.send(command)
	
	except KeyboardInterrupt:
		break

