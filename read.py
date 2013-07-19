#!/usr/bin/python

import sys
import SerialMonitor as sm
import DBManager as db
from struct import *

if __name__ == "__main__":
	try:
		reader = sm.SerialMonitor("/dev/pts/5", 9600, None)
		reader.stateListener()
		
	except Exception, e:
		print str(e)
		sys.exit(1)
	
	sys.exit(0)
