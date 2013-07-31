#!/usr/bin/python
"""
Python script for managing database
"""
import MySQLdb


# Function to create MySQL database connection
def getDBCon():
	return MySQLdb.connect(host="localhost", # your host, usually localhost
		                   user="ceng499", # your username
		                   passwd="ceng499", # your password
		                   db="pihome") # name of the data base
		                        
# Function to create fresh database tables
def initDatabase():
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Create Devices table, drop previous table if existed
	dbcur.execute("SHOW TABLES LIKE 'Devices'")
	result=dbcur.fetchone()
	if not (result is None or result[0] is None):
		dbcur.execute("DROP TABLE Devices")
	dbcur.execute("CREATE TABLE Devices(serial BIGINT UNSIGNED PRIMARY KEY, type TINYINT, name VARCHAR(20), status TINYINT, active TINYINT, message VARCHAR(50))")

	# Create Credential table, drop previous table if existed
	dbcur.execute("SHOW TABLES LIKE 'Credential'")
	result=dbcur.fetchone()
	if not (result is None or result[0] is None):
		dbcur.execute("DROP TABLE Credential")
	dbcur.execute("CREATE TABLE Credential(username VARCHAR(20) PRIMARY KEY, password VARCHAR(20))")
	dbcur.execute("INSERT INTO Credential VALUES('pihome','pihomepass')")

	# Create Emails table, drop previous table if existed
	dbcur.execute("SHOW TABLES LIKE 'Emails'")
	result=dbcur.fetchone()
	if not (result is None or result[0] is None):
		dbcur.execute("DROP TABLE Emails")
	dbcur.execute("CREATE TABLE Emails(email VARCHAR(20) PRIMARY KEY)")
	dbcur.execute("INSERT INTO Emails VALUES('pimation@email.com')")

	# Create RecordTime table, drop previous table if existed
	dbcur.execute("SHOW TABLES LIKE 'RecordTime'")
	result=dbcur.fetchone()
	if not (result is None or result[0] is None):
		dbcur.execute("DROP TABLE RecordTime")
	dbcur.execute("CREATE TABLE RecordTime(recordtime TINYINT PRIMARY KEY)")
	dbcur.execute("INSERT INTO RecordTime VALUES(10)")
	
	# Create Nodes table, drop previous table if existed
	dbcur.execute("SHOW TABLES LIKE 'Nodes'")
	result=dbcur.fetchone()
	if not (result is None or result[0] is None):
		dbcur.execute("DROP TABLE Nodes")
	dbcur.execute("CREATE TABLE Nodes(nodename VARCHAR(10) PRIMARY KEY, ipaddress VARCHAR(15))")

	# Create Playbacks table, drop previous table if existed
	dbcur.execute("SHOW TABLES LIKE 'Playbacks'")
	result=dbcur.fetchone()
	if not (result is None or result[0] is None):
		dbcur.execute("DROP TABLE Playbacks")
	dbcur.execute("CREATE TABLE Playbacks(nodename VARCHAR(10), recordfolder VARCHAR(24))")

	# Create DoorTriggers table, drop previous table if existed
	dbcur.execute("SHOW TABLES LIKE DoorTriggers")
	result=dbcur.fetchone()
	if not (result is None or result[0] is None):
		dbcur.execute("DROP TABLE DoorTriggers")
	dbcur.execute("CREATE TABLE DoorTriggers(doorserial BIGINT UNSIGNED PRIMARY KEY, switchserial BIGINT UNSIGNED, action TINYINT)")

	# Create SwitchTriggers table, drop previous table if existed
	dbcur.execute("SHOW TABLES LIKE SwitchTriggers")
	result=dbcur.fetchone()
	if not (result is None or result[0] is None):
		dbcur.execute("DROP TABLE SwitchTriggers")
	dbcur.execute("CREATE TABLE SwitchTriggers(switchserial BIGINT UNSIGNED PRIMARY KEY, ondailytime TINYINT, offdailytime TINYINT)")
		
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to add new device
#db.addDevice(0013a20040a57ae9,0,'Switch',0,1,'New')
def addDevice(_serial, _type, _name, _status, _active, _message):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Check if device is already existed
	dbcur.execute("SELECT * FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		# Insert new entry to Devices table
		dbcur.execute("INSERT INTO Devices VALUES(%s,%s,%s,%s,%s,%s)", (_serial,_type,_name,_status,_active,_message))
		
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to remove device
def removeDevice(_serial):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Remove device if existed
	dbcur.execute("SELECT * FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Device %s does not exist" % _serial)
	else:		
		dbcur.execute("DELETE FROM Devices WHERE serial=%s", _serial)
		
	# Commit, close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()
	
# Function to get device information
def getDevice(_serial):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Get device
	dbcur.execute("SELECT serial,type,name,status,active,message FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()

	# Close db cursor, connection
	dbcur.close()
	dbcon.close()

	# Return result	
	if result is None or result[0] is None:
		print("Device %s does not exist" % _serial)
		return None
	else:		
		# Return device info
		return result


# Function to get all devices
def getDevices():
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Find all devices
	dbcur.execute("SELECT * FROM Devices")
	results=dbcur.fetchall()
		
	# Close db cursor, connection
	dbcur.close()
	dbcon.close()
	return results
		
# Function to update device status
def updateDeviceStatus(_serial, _status):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Check if device exists
	dbcur.execute("SELECT * FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Device %s does not exist" % _serial)
	else:		
		# Update status of device
		dbcur.execute("UPDATE Devices SET status=%s WHERE serial=%s", (_status,_serial))
		
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to update device message
def updateDeviceMessage(_serial, _message):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Check if device exists
	dbcur.execute("SELECT * FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Device %s does not exist" % _serial)
	else:		
		# Update status of device
		dbcur.execute("UPDATE Devices SET message=%s WHERE serial=%s", (_message,_serial))
		
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to activate or deactivate device
def updateDeviceActive(_serial, _active):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Check if device exists
	dbcur.execute("SELECT * FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Device %s does not exist" % _serial)
	else:		
		# Update active of device
		dbcur.execute("UPDATE Devices SET active=%s WHERE serial=%s", (_active,_serial))
		
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()
	
# Function to change device name
def changeDeviceName(_serial, _name):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Check if device exists
	dbcur.execute("SELECT * FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Device %s does not exist" % _serial)
	else:		
		# Change name of device
		dbcur.execute("UPDATE Devices SET name=%s WHERE serial=%s", (_name,_serial))
		
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to change device type
def changeDeviceType(_serial, _type):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Check if device exists
	dbcur.execute("SELECT * FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Device %s does not exist" % _serial)
	else:		
		# Change type of device
		dbcur.execute("UPDATE Devices SET type=%s WHERE serial=%s", (_type,_serial))
		
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()
	
# Function to change password
def changePassword(_user, _oldpass, _newpass):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Check if user credential is correct
	dbcur.execute("SELECT * FROM Credential WHERE username=%s AND password=%s", (_user,_oldpass))
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Incorrect username and password %s %s" % (_user,_oldpass))
	else:		
		# Update new password
		dbcur.execute("UPDATE Credential SET password=%s WHERE username=%s", (_newpass,_user))
		
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to get all emails
def getEmails():
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Find all emails
	dbcur.execute("SELECT * FROM Emails")
	results=dbcur.fetchall()

	# Close db cursor, connection
	dbcur.close()
	dbcon.close()
	
	return results

# Function to get record time
def getRecordTime():
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Find all emails
	dbcur.execute("SELECT recordtime FROM RecordTime")
	results=dbcur.fetchall()

	# Close db cursor, connection
	dbcur.close()
	dbcon.close()
	
	return results
	
# Function to add email
def addEmail(_email):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Add new email if not existed
	dbcur.execute("SELECT email FROM Emails WHERE email=%s", _email)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		dbcur.execute("INSERT INTO Emails VALUES(%s)", _email)
	# Close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to remove email
def removeEmail(_email):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Remove email if existed
	dbcur.execute("SELECT email FROM Emails WHERE email=%s", _email)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Email %s does not exist" % _email)
	else:
		dbcur.execute("DELETE FROM Emails WHERE email=%s", _email)
	# Close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to get all nodes
def getNodes():
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Find all emails
	dbcur.execute("SELECT * FROM Nodes")
	results=dbcur.fetchall()

	# Close db cursor, connection
	dbcur.close()
	dbcon.close()
	
	return results


# Function to get node information
def getNode(_nodename):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Get node info if existed
	dbcur.execute("SELECT * FROM Nodes WHERE nodename=%s", _nodename)
	result=dbcur.fetchone()

	# Close db cursor, connection
	dbcur.close()
	dbcon.close()
	
	if result is None or result[0] is None:
		print("Node %s does not exist" % _nodename)
		return None
	else:
		return result

			
# Function to add new node
def addNode(_nodename, _ipadd):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Add new node if not existed
	dbcur.execute("SELECT * FROM Nodes WHERE nodename=%s", _nodename)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		dbcur.execute("INSERT INTO Nodes VALUES(%s,%s)", (_nodename,_ipadd))

	# Commit, close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to remove node
def removeNode(_nodename):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Remove node if existed
	dbcur.execute("SELECT * FROM Nodes WHERE nodename=%s", _nodename)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Node %s does not exist" % _nodename)
	else:
		dbcur.execute("DELETE FROM Nodes WHERE nodename=%s", _nodename)

	# Commit, close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to update node ipaddress and port
def updateNode(_nodename, _ipadd):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Update node if existed
	dbcur.execute("SELECT * FROM Nodes WHERE nodename=%s", _nodename)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Node %s does not exist" % _nodename)
	else:
		dbcur.execute("UPDATE Nodes SET ipaddress=%s WHERE nodename=%s", (_ipadd,_nodename))

	# Commit, close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to get all playbacks
def getPlaybacks():
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Find all emails
	dbcur.execute("SELECT * FROM Playbacks")
	results=dbcur.fetchall()

	# Close db cursor, connection
	dbcur.close()
	dbcon.close()
	
	return results
		
# Function to add new playback
def addPlayback(_nodename, _recordfolder):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Add new playback if not existed
	dbcur.execute("SELECT * FROM Playbacks WHERE nodename=%s AND recordfolder=%s", (_nodename,_recordfolder))
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		dbcur.execute("INSERT INTO Playbacks VALUES(%s,%s)", (_nodename,_recordfolder))

	# Commit, close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()	
	
# Function to remove playback
def removePlayback(_nodename,_recordfolder):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Remove playback if existed
	dbcur.execute("SELECT * FROM Playbacks WHERE nodename=%s AND recordfolder=%s", (_nodename,_recordfolder))
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Playback %s,%s does not exist" % (_nodename,_recordfolder))
	else:
		dbcur.execute("DELETE FROM Playbacks WHERE nodename=%s AND recordfolder=%s", (_nodename,_recordfolder))

	# Commit, close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()
	
# Function to get door trigger information
def getDoorTrigger(_serial):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Get device
	dbcur.execute("SELECT doorserial,switchserial,action FROM DoorTriggers WHERE doorserial=%s", _serial)
	result=dbcur.fetchone()

	# Close db cursor, connection
	dbcur.close()
	dbcon.close()

	# Return result	
	if result is None or result[0] is None:
		print("DoorTrigger %s does not exist" % _serial)
		return None
	else:		
		# Return device info
		return result
		
