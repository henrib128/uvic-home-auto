from xbee import XBee
import serial
import string

ser = serial.Serial('/dev/ttyAMA0',9600)

xbee = XBee(ser)

print 'starting'

while True:
        try:
                response = xbee.wait_read_frame()
                if response['samples'][0]['dio-0'] == 0 and response['id'] == 'rx_io_data_long_addr':
                        print 'false'

        except KeyboardInterrupt:
                break

ser.close()
