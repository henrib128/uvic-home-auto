#!/usr/bin/python

import sys
import SerialMonitor as sm
from struct import *

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print('Invalid argc')
		sys.exit(1)
		
	bytes = pack('QB', int(sys.argv[1]), int(sys.argv[2]))
	
	try:
		writer = sm.SerialMonitor("/dev/pts/4", 9600, None)
		writer.sendState(bytes)
		
	except Exception, e:
		print str(e)
		sys.exit(1)
		
	sys.exit(0)
