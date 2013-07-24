#!/usr/bin/python
"""
PiCam script
"""
import socket

# Required custome modules
import CameraMonitor as cm

# Function to get local ipaddress (i.e. 192.168.0.190)
def getLocalIp():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	ipaddr = s.getsockname()[0]
	s.close()
	return ipaddr

# Main body
if __name__ == "__main__":
	# Hostname and port the script is listening at
	hostname = getLocalIp()
	hostport = 44444

	# Base directory for mjpg_streamer
	#mbasedir = '/home/tri/ceng499/mjpg-streamer/mjpg-streamer'
	mbasedir = '/home/pi/mjpg-streamer/mjpg-streamer' 

	# Default recording base directory (where playbacks are stored)
	mrecorddir='/home/pi/tmp/mjpg-streamer'

	# Create camera monitor object
	CameraMonitor = cm.CameraMonitor(hostname,hostport,mbasedir,mrecorddir)
	
	# Start camera monitor
	print "Camera monitor starting on %s,%s" % (hostname,hostport)
	CameraMonitor.start()

	

	
	
	
	
