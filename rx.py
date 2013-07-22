from xbee import XBee
import serial
import string

#ser = serial.Serial('/dev/ttyAMA0',9600)
ser = serial.Serial()
ser.port='/dev/ttyAMA0'
ser.baudrate='9600'
try:
	ser.open()
	xbee = XBee(ser)
except Exception, e:
	print "error open serial port: " + str(e)
	exit()

print 'starting'

while True:
        try:
                response = xbee.wait_read_frame()
                print response
#		if response['samples'][0]['dio-0'] == 0 and response['id'] == 'rx_io_data_long_addr':
#                        print 'false'

        except KeyboardInterrupt:
                break

ser.close()
