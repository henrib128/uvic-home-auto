"""
Camera client module to interface with CameraMonitor server using socket
"""
import socket
import sys

class CameraClient(object):
	# Function to open new socket connection and send transaction request
	def __init__(self, hostname=socket.gethostname(), port=44437):
		# open TCP socket for SYNCHRONOUS streaming
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((hostname, port))

	def send(self, request):

		############ TIME STAMP THE RESPONSE #############
		# This can be used as START-POINT of request

		# send request to transaction server
		self.sock.send(request)
				
	def send_wait(self, request):

		############ TIME STAMP THE RESPONSE #############
		# This can be used as START-POINT of request

		# send request to transaction server
		self.sock.send(request)

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
		
	
	def close(self):
		# close socket connection
		self.sock.close()
