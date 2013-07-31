"""
Camera client module to interface with CameraMonitor server using socket
"""
import socket
import sys

# Camera client class to send to certain socket
class CameraClient(object):
	# Function to open new socket connection and send transaction request
	def __init__(self, hostname=socket.gethostname(), port=44444):
		self.hostname = hostname
		self.port = port
		# open TCP socket for SYNCHRONOUS streaming
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((hostname, port))
		except socket.error as err:
			sys.stderr.write(str(err))
			print "Failed to connect to %s %s. %s" % (self.hostname, self.port, err)

	# Function to send request but not wait for response
	def send(self, request):

		############ TIME STAMP THE RESPONSE #############
		# This can be used as START-POINT of request

		# send request to transaction server
		try:
			self.sock.send(request)
		except socket.error as err:
			sys.stderr.write(str(err))
			print "Failed to send to %s %s. %s" % (self.hostname, self.port, err)
				
	# Function to send request and wait for response (blocking call)
	def send_wait(self, request):

		############ TIME STAMP THE RESPONSE #############
		# This can be used as START-POINT of request

		# send request to transaction server
		try:
			self.sock.send(request)
		except socket.error as err:
			sys.stderr.write(str(err))
			print "Failed to send to %s %s. %s" % (self.hostname, self.port, err)

		######## START of WAITING ###########
		# Sender thread wait for response from receiver thread
		try:
			response = self.sock.recv(1024)
		except Exception as ConnectionError:
			sys.stderr.write("Error communicating with Camera server: %s\n" % str(ConnectionError))
		######## END of WAITING #############

		############ TIME STAMP THE RESPONSE #############
		# This can be used as END-POINT of request

		# print out status message
		print "Received response: %s" % response
		
	# Function to close socket
	def close(self):
		# close socket connection
		try:
			self.sock.close()
		except socket.error as err:
			sys.stderr.write(str(err))
			print "Failed to close connection %s %s. %s" % (self.hostname, self.port, err)


