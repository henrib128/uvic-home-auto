#!/usr/bin/python
"""
Main PiHome script
"""

# Required custome modules
import CameraMonitor as cm

# Main body
if __name__ == "__main__":
	# Hostname and port the script is listening at
	hostname = cm.getLocalIp()
	hostport = 44444

	# Base directory for mjpg_streamer
	#MBASE_DIR = '/home/pi/mjpg-streamer/mjpg-streamer' 
	mbasedir = '/home/tri/ceng499/mjpg-streamer/mjpg-streamer'

	# Default recording base directory (where playbacks are stored)
	mrecorddir='/tmp/mjpg-streamer'

	# Create camera monitor object
	CameraMonitor = cm.CameraMonitor(hostname,hostport,mbasedir,mrecorddir)
	
	# Start camera monitor
	print "Camera monitor starting on %s,%s" % (hostname,hostport)
	CameraMonitor.start()

	
	
	
	
	
