#!/usr/bin/python
"""
Python module to run on remote Pi to monitor socket request from the main Pi to start/stop local mjpeg streamer
Need to also send back reply with information on the local directory of the playback file to update database?
Or this script can update database directly using socket as well... (maybe not a good idea).
"""
import socket
import sys
import os, subprocess
import time, datetime
import threading

# Camera thread class
class CameraThread(threading.Thread):
	# Default class constructor __init__ function, ran upon instantiation
	def __init__(self, main, server, conn):
		self.main = main
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
		if self.command == 'STARTPLAYBACK' or \
		   self.command == 'STARTRECORD' or \
		   self.command == 'DELPLAYBACK':
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
				print "Received command: %s" % self.command
				response = "Received %s command" % self.command
				
				# Stop all local mjpg-streamer
				self.main.stopAllStream()

				# Start http stream at port 8080
				self.main.startHttpStream()
				
				# Start playback stream at port 8081
				self.main.startPlaybackStream()
												
			elif self.command == "STOPALL":
				print "Received command: %s" % self.command
				response = "Received %s command" % self.command
				
				# Stop all local mjpg-streamer
				self.main.stopAllStream()

			elif self.command == "STARTHTTP":
				print "Received command: %s" % self.command
				response = "Received %s command" % self.command
				
				# Start http streaming
				self.main.startHttpStream()

			elif self.command == "STARTRECORD":
				print "Received command: %s,%s" % (self.command, self.recordfolder)
				response = "Received %s command" % self.command
				
				# First stop all stream
				self.main.stopAllStream()
				
				# Resume playback stream on port 8081
				self.main.startPlaybackStream()
				
				# Start dual streaming for record stream and http stream
				# Need to start at the same time for real webcam
				self.main.startRecordStream(self.recordfolder)
				
			elif self.command == "STARTPLAYBACK":
				print "Received command: %s,%s" % (self.command, self.recordfolder)
				response = "Received %s command" % self.command
					
				# Start playback from certain folder to port 8081
				self.main.playFolder(self.recordfolder)

			elif self.command == "DELPLAYBACK":
				print "Received command: %s,%s" % (self.command, self.recordfolder)
				response = "Received %s command" % self.command
				
				# Delete specified folder
				self.main.delPlayback(self.recordfolder)
												
			elif self.command == "EMPTY_CMD":
				print "Empty command"
			
			else:
				print "Unrecognized command: %s" % self.command
				response = "Unrecognized command: %s" % self.command
				
			# Synchronization back
			self.conn.send(response)

		except Exception, err:
			print "CameraThread error: %s" % str(err)
			response = "CameraThread error: %s" % str(err)
			self.conn.send(response)


# CameraMonitor class
class CameraMonitor(object):
	# Class attributes (static variables, accessed by <class>.var or self.__class__.var)
	#server="CameraMonitor"

	# Class constructor __init__ function (default defined by python), ran upon instantiation
	def __init__(self,hostname=socket.gethostname(),port=44444,mbasedir='/home/pi/mjpg-streamer/mjpg-streamer',mrecordir='/tmp/mjpg-streamer'):
		# Data attributes (specific for each instance, accessed by self.var)
		self.hostname = hostname
		self.port = port
		self.mbasedir = mbasedir
		self.mrecordir = mrecordir
		self.should_run = True

	# class methods, can be used by all instances of class
	def process_request(self, conn):
		CameraThread(self,self.hostname, conn).start()

	def start(self):
		# First initialize default mjpg_streamer
		self.stopAllStream()
		self.startHttpStream()
		self.startPlaybackStream()
		
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

	# Function to stop all instances of mjpg-streamer
	def stopAllStream(self):
		os.system("killall mjpg_streamer")

	# Function to start single instance of mjpg-streamer for http stream at port 8080
	def startHttpStream(self):
		_mBaseDir = self.mbasedir
		_mWebDir = _mBaseDir + '/www'
	
		# Command for mjpg_streamer
		cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_uvc.so -f 30 -r 640x480" -o "' + \
			_mBaseDir + '/output_http.so -p 8080 -w ' + _mWebDir + '" &'
		#cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_testpicture.so -d 1000" -o "' + \
		#	_mBaseDir + '/output_http.so -p 8080 -w ' + _mWebDir + '" &'
	
		# Start streaming
		os.system(cmd)

	# Function to start single instance of mjpg-streamer for playback stream at port 8081
	def startPlaybackStream(self):
		_mBaseDir = self.mbasedir
		_mWebDir = _mBaseDir + '/www'
		_tmpDir = _mBaseDir + '/tmp'
	
		# Make new directory
		os.system("mkdir -p %s" % _tmpDir)

		# Command for mjpg-streamer to output from a local folder
		cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_file.so -r -f ' + _tmpDir + '" -o "' + \
			_mBaseDir + '/output_http.so -p 8081 -w ' + _mWebDir + '" &'

		# Start streaming
		os.system(cmd)
	
	# Function to start single instance of mjpg-streamer for dual streaming to http and a local directory
	def startRecordStream(self,_mFolder):
		_mBaseDir = self.mbasedir
		_mRecordDir = self.mrecordir
		_mWebDir = _mBaseDir + '/www'
		_mPlaybackFolder = _mRecordDir + '/' + _mFolder
	
		# Make new directory
		os.system("mkdir -p %s" % _mPlaybackFolder)

		# Command for mjpg-streamer dual streaming
		cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_uvc.so -f 30 -r 640x480" -o "' + \
                	_mBaseDir + '/output_http.so -p 8080 -w ' + _mWebDir + '" -o "' + \
                	_mBaseDir + '/output_file.so -d 500 -f ' + _mPlaybackFolder + '" &'
		
		#cmd = _mBaseDir + '/mjpg_streamer -i "' + _mBaseDir + '/input_testpicture.so -d 1000" -o "' + \
		#	_mBaseDir + '/output_http.so -p 8080 -w ' + _mWebDir + '" -o "' + \
		#	_mBaseDir + '/output_file.so -f ' + _mPlaybackFolder + '" &'

		# Start streaming
		os.system(cmd)
	
	# Function to copy pictures from recordfolder to playback stream tmp folder to simulate playback
	def playFolder(self,_mFolder):
		_mBaseDir = self.mbasedir
		_mRecordDir = self.mrecordir
		_mPlaybackFolder = _mRecordDir + '/' + _mFolder
		_tmpDir = _mBaseDir + '/tmp'
		
		#print "Playing from this folder: %s to this folder: %s" % (_mPlaybackFolder,_tmpDir)
		# Start refreshing script
		for pic in sorted(os.listdir(_mPlaybackFolder)):
			os.system("cp %s/%s %s/playback.jpg" % (_mPlaybackFolder,pic,_tmpDir))
			#print "copied this pic %s" % pic
			time.sleep(1)

	# Function to delete playback folder
	def delPlayback(self,_mFolder):
		_mRecordDir = self.mrecordir
		_mPlaybackFolder = _mRecordDir + '/' + _mFolder
	
		# Remove directory
		os.system("rm -rf %s" % _mPlaybackFolder)





