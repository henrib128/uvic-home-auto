from xbee import XBee
import serial
import string
import time

#ser = serial.Serial('/dev/ttyAMA0',9600)
ser = serial.Serial()
ser.port='/dev/ttyAMA0'
ser.baudrate='9600'

def processFrame(data):
		print data
		time.sleep(10)
		print 'done'

try:
		ser.open()
		#xbee = XBee(ser)
		xbee = XBee(ser, callback=processFrame)
		
except Exception, e:
		print "error open serial port: " + str(e)
		exit()

print 'starting'


while True:
	try:
		Parameter = raw_input()
		dest_addr='0013a20040a57ae9'
		xbee.remote_at(frame_id='A',dest_addr_long=dest_addr.decode('hex'), command='D0', parameter=Parameter.decode('hex'))
	
	except KeyboardInterrupt:
		break
	
xbee.halt()
ser.close()

