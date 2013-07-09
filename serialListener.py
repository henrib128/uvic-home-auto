#!/usr/bin/python
#basic script to listen to the serial port
import time
import serial
import threading

# Serial thread class
class SerialThread(threading.Thread):
	def __init__(self, threadid, data):
		self.threadid = threadid
		self.data = data
		super(SerialThread, self).__init__()
		print "Serial thread#%d: total threads: %d" % (self.threadid, threading.active_count())

	def run(self):
		# Process data
		self.processRequest(self.data)

	def processRequest(self, request):
		# Print data
		print "Thread# %d: %s" % (self.threadid, request)

# Serial Monitor class
class SerialMonitor(object):
    # Static Var (class attribute): accessed by <class>.var or self.__class__.var
    # server="SerialMonitor"

    # Class constructor __init__ function (default defined by python), ran upon instantiation
    def __init__(self, sport="/dev/pts/3", sbaud=9600, stimeout=None):
        # Data attributes (specific for each instance, accessed by self.var)
        self.ser = serial.Serial()
        self.sport = sport
        self.sbaud = sbaud
        self.stimeout = stimeout
        self.count = 0

    def start(self):
		# Initialize serial chanel properties
		self.ser.port = self.sport
		self.ser.baudrate = self.sbaud
		self.ser.timeout = self.stimeout  #None is block read. 1 is non-block read, 2 is timeout block read
		self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
		self.ser.parity = serial.PARITY_NONE #set parity check: no parity
		self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
		self.ser.xonxoff = False     #disable software flow control
		self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
		self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
		self.ser.writeTimeout = 2     #timeout for write
		    
		try: 
			self.ser.open()

		except Exception, e:
			print "error open serial port: " + str(e)
			exit()

		if self.ser.isOpen():
			try:
				self.ser.flushInput() #flush input buffer, discarding all its contents
				self.ser.flushOutput()#flush output buffer, aborting current output 
							     	  #and discard all that is in buffer
				while True:
					response = self.ser.readline() # if block-read, expected eol '\n' char, if not wait forever!
					print("read data: " + response)
					# Spawn new thread to take care of this request
				
					if (response == 'exit\n'):
						break
						
					if response:
						self.count += 1
						SerialThread(self.count,response).start()
		   
				self.ser.close()

			except Exception, e1:
				print "error communicating...: " + str(e1)

		else:
			print "cannot open serial port "


# Main body
if __name__ == "__main__":
    SerialMonitor = SerialMonitor("/dev/pts/3", 9600, None)
    print 'Seiral Listener starting'
    SerialMonitor.start()
    

"""
#initialization and open the port
#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

ser = serial.Serial()
# This /dev/pts/4 virtual port only works if we have socat running in background to connect port 3 and 4
# socat -d -d TTY: TTY: &
ser.port = "/dev/pts/3"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
ser.timeout = None          #block read
#ser.timeout = 1            #non-block read
#ser.timeout = 2              #timeout block read
ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write

try: 
	ser.open()

except Exception, e:
	print "error open serial port: " + str(e)
	exit()

if ser.isOpen():
	try:
		ser.flushInput() #flush input buffer, discarding all its contents
		ser.flushOutput()#flush output buffer, aborting current output 
			             #and discard all that is in buffer
		count=0
		while True:
		    response = ser.readline() # if block-read, expected eol '\n' char, if not wait forever!
		    print("read data: " + response)
		    # Spawn new thread to take care of this request
		    
		    if (response == 'exit\n'):
		        break
		        
		    if response:
		    	count += 1
		    	SerialThread(count,response).start()
   

		ser.close()

	except Exception, e1:
		print "error communicating...: " + str(e1)

else:
	print "cannot open serial port "

"""
            
