#!/usr/bin/python
#basic script to listen to the serial port

import time, datetime
import SerialMonitor
import CameraClient
import socket

cam1 = socket.gethostname()
camport = 44437
camclient = CameraClient.CameraClient(cam1,camport)

# Base directory for mjpg_streamer
MBASE_DIR='/home/tri/ceng499/mjpg-streamer/mjpg-streamer'
# Recording folder
MRECORD_DIR='/tmp/mjpg-streamer'
DATE_TIME = '13_07_11.00_01_30'
DATE_TIME = datetime.datetime.now().strftime("%y_%m_%d.%H_%M_%S")
MRECORD_FOLDER = MRECORD_DIR + '/record_' + DATE_TIME

camclient.send_wait("INIT")

camclient.send_wait("STARTRECORD,%s" % MRECORD_FOLDER)
RECORD_SECONDS=10
time.sleep(RECORD_SECONDS)
camclient.send_wait("INIT")

camclient.send("STARTPLAYBACK,%s" % MRECORD_FOLDER)

"""
camclient.send_wait("STOPALL")

camclient.send_wait("STARTHTTP")

camclient.send_wait("STOPALL")

camclient.send_wait("STARTDUAL")

camclient.send_wait("STOPALL")

camclient.send_wait("STARTHTTP")

camclient.send_wait("STARTPLAYBACK,%s" % playbackfolder)

camclient.send_wait("BS")

camclient.send("")

camclient.send_wait("hg jj jjj ,k,k")


RECORD_SECONDS = 10
# Base directory for mjpg_streamer
MBASE_DIR='/home/tri/ceng499/mjpg-streamer/mjpg-streamer'
# Recording folder
MRECORD_DIR='/tmp/mjpg-streamer'
DATE_TIME = datetime.datetime.now().strftime("%y_%m_%d.%H_%M_%S")
MRECORD_FOLDER = MRECORD_DIR + '/record_' + DATE_TIME

SerialMonitor.stopAllStream()
SerialMonitor.startDualStream(MBASE_DIR,MRECORD_FOLDER)
time.sleep(10)
SerialMonitor.stopAllStream()
SerialMonitor.startHttpStream(MBASE_DIR)


SerialMonitor.startPlayback(MBASE_DIR,MRECORD_FOLDER)
"""
