#!/usr/bin/python
#basic script to listen to the serial port
import time
import serial
print 'Seiral Listener starting'

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

		while True:
		    response = ser.readline()
		    print("read data: " + response)
		    
		    if (response == 'exit\n'):
		        break
		ser.close()

	except Exception, e1:
		print "error communicating...: " + str(e1)

else:
	print "cannot open serial port "
            
