#!/usr/bin/python
"""
Python module to run on remote Pi to monitor socket request from the main Pi to start/stop local mjpeg streamer
Need to also send back reply with information on the local directory of the playback file to update database?
Or this script can update database directly using socket as well... (maybe not a good idea).
"""
import socket
import sys
import os
import time, datetime
import threading

# Camera thread class
class CameraThread(threading.Thread):
	# Default class constructor __init__ function, ran upon instantiation
	def __init__(self, server, conn):
		self.server = server
		self.conn = conn
		super(CameraThread, self).__init__() # trigger run method
		print "Total camera threads: %d" % threading.active_count()

	# Run function triggered by super method
	def run(self):
		connected = True
		while connected:
			try:
				# Waiting for new data
				data = self.conn.recv(1024)
				
				# Receiving new data
				if data:
					print "Data: %s" % data
					self.processRequest(data)
				else:
					connected = False

			except socket.timeout:
				print "Camera child: Connection timed out"

	def parseRequest(self, request):
		# Try parsing SerialMonitor request based on generic template
		# command,data
		params = request.split(",")

		# Retrieve command
		try:
			self.command = params[0]
		except KeyError:
			self.command = "EMPTY_CMD"

		# Retrieve arg if command is STARTPLAYBACK
		if self.command == 'STARTPLAYBACK' or self.command == 'STARTRECORD':
			try:
				self.recordfolder = params[1]
			except Exception:
				self.recordfolder = ""
			
	def processRequest(self, data):
		# First parse the request
		self.parseRequest(data)

		# Perform action based on request
		try:
			if self.command == "INIT":
				print "Received %s command" % self.command
				response = "Received %s command" % self.command
				
				# Stop all local mjpg-streamer
				stopAllStream()

				# Start http stream at port 8080
				startHttpStream()
				
				# Start playback stream at port 8081
				startPlaybackStream()
												
			elif self.command == "STOPALL":
				print "Received %s command" % self.command
				response = "Received %s command" % self.command
				
				# Stop all local mjpg-streamer
				stopAllStream()

			elif self.command == "STARTHTTP":
				print "Received %s command" % self.command
				response = "Received %s command" % self.command
				
				# Start http streaming
				startHttpStream()

			elif self.command == "STARTRECORD":
				print "Received %s command %s recordfolder" % (self.command, self.recordfolder)
				response = "Received %s command" % self.command
				
				# Pass record folder
				MRECORD_FOLDER = self.recordfolder
				
				# First stop all stream
				stopAllStream()
				
				# Resume playback stream on port 8081
				startPlaybackStream()
				
				# Start dual streaming for record stream and http stream
				# Need to start at the same time for real webcam
				startRecordStream(MRECORD_FOLDER)
				
			elif self.command == "STARTPLAYBACK":
				print "Received %s command %s recordfolder" % (self.command, self.recordfolder)
				response = "Received %s command" % self.command
				
				# Pass record folder
				MRECORD_FOLDER = self.recordfolder
				
				# Start playback from certain folder to port 8081
				playFolder(MRECORD_FOLDER)
								
			elif self.command == "EMPTY_CMD":
				print "Empty command"
			
			else:
				print "Unrecognized command: %s" % self.command
				response = "Unrecognized command: %s" % self.command
				
			# Synchronization back
			self.conn.send(response)

		except Exception, err:
			sys.stderr.write("CameraThread error: %s\n" % str(err))
			print "CameraThread error: %s" % str(err)
			response = 'FAIL'
			self.conn.send(response)


# CameraMonitor class
class CameraMonitor(object):
	# Class attributes (static variables, accessed by <class>.var or self.__class__.var)
	#server="CameraMonitor"

	# Class constructor __init__ function (default defined by python), ran upon instantiation
	def __init__(self, hostname=socket.gethostname(), port=44437):
		# Data attributes (specific for each instance, accessed by self.var)
		self.hostname = hostname
		self.port = port
		self.should_run = True

	# class methods, can be used by all instances of class
	def process_request(self, conn):
		CameraThread(self.hostname, conn).start()

	def start(self):
		# open and bind TCP socket for synchronous streaming
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((self.hostname, self.port))

		# keep listen to the socket's port
		while self.should_run:
			try:
				sock.listen(100)
				conn, _ = sock.accept()
				# Create a child thread to handle new connection
				self.process_request(conn)

			except socket.error as err:
				sys.stderr.write(str(err))

		# close socket connection
		sock.close()

	def stop(self):
		self.should_run = False

	

# Function to start camera stream
"""
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
"""


def stopAllStream():
	os.system("killall mjpg_streamer")

def startHttpStream():
	_mBaseDir = MBASE_DIR
	_mWebDir = _mBaseDir + '/www'
	
	# Command for mjpg_streamer
	#cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_testpicture.so -d 1000" -o "' + \
	cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_uvc.so -f 30 -r 640x480" -o "' + \
		  _mBaseDir + '/output_http.so -p 8080 -w ' + _mWebDir + '" &'
	
	# Start streaming
	os.system(cmd)

def startPlaybackStream():
	_mBaseDir = MBASE_DIR
	_mWebDir = _mBaseDir + '/www'
	_tmpDir = _mBaseDir + '/tmp'
	
	# Make new directory
	os.system("mkdir -p %s" % _tmpDir)

	# Command for mjpg-streamer to output from a local folder
	cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_file.so -r -d 1 -f ' + _tmpDir + '" -o "' + \
		  _mBaseDir + '/output_http.so -p 8081 -w ' + _mWebDir + '" &'

	# Start streaming
	os.system(cmd)
	
def startRecordStream(_mFolder):
	_mBaseDir = MBASE_DIR
	_mRecordDir = MRECORD_DIR
	_mRecordFolder = _mRecordDir + '/' + _mFolder
	
	# Make new directory
	os.system("mkdir -p %s" % _mRecordFolder)

	# Command for mjpg-streamer dual streaming
	#cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_testpicture.so -d 1000" -o "' + \
	cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_uvc.so -f 30 -r 640x480" -o "' + \
		  _mBaseDir + '/output_http.so -p 8080 -w ' + _mWebDir + '" -o "'
		  _mBaseDir + '/output_file.so -f ' + _mRecordFolder + '" &'

	# Start streaming
	os.system(cmd)
	
# Function to copy pictures from recordfolder to playback stream tmp folder to simulate playback
def playFolder(_mFolder):
	_mBaseDir = MBASE_DIR
	_mRecordDir = MRECORD_DIR
	_mPlaybackFolder = _mRecordDir + '/' + _mFolder
	_tmpDir = _mBaseDir + '/tmp'
	
	# Start refreshing script
	for pic in os.listdir(_mPlaybackFolder):
		os.system("cp %s/%s %s/playback.jpg" % (_mPlaybackFolder,pic,_tmpDir))
		time.sleep(1)

	
	
#################################################################### Main body
if __name__ == "__main__":
	# Hostname and port the script is listening at
	#hostname = socket.gethostname() # Just virtural name, i.e. tri-computer
	#hostname = socket.gethostbyname(hostname) # get actual address '127.0.0.1'
	#hostname = socket.gethostbyname(socket.getfqdn())
	#hostname = '10.0.2.15'
	# Need a way to get this dynamically, probably using ifconfig for either l0 or wlan0
	hostname = '192.168.0.190'
	hostport = 44444

	# This also needs to be extracted dynamically
	# Base directory for mjpg_streamer
	MBASE_DIR='/home/tri/ceng499/mjpg-streamer/mjpg-streamer'
	# Recording folder
	MRECORD_DIR='/tmp/mjpg-streamer'
	
	# Initialize camera streaming
	# This can be done by serialListener by sending 'INIT' request
	stopAllStream()
	startHttpStream()
	startPlaybackStream()
	
	# Creating camera monitor object
	CameraMonitor = CameraMonitor(hostname,hostport)
	print "Camera monitor starting on %s,%s" % (hostname,hostport)
	CameraMonitor.start()
