#!/usr/bin/python
"""
Python script for managing database

-- Type 0 switch (on/off), 1 door sensor (open/close) for TRUE/FALSE
DROP TABLE Devices;
CREATE TABLE Devices(serial BIGINT UNSIGNED PRIMARY KEY, type TINYINT, name VARCHAR(20), status TINYINT, active TINYINT);
INSERT INTO Devices VALUES(10000000000,0,'bedroom lamp',0, 1);
INSERT INTO Devices VALUES(10000000001,1,'front door',0, 0);

DROP TABLE Credential;
CREATE TABLE Credential(username VARCHAR(20) PRIMARY KEY, password VARCHAR(20));
INSERT INTO Credential VALUES('rpi','rpipass');

DROP TABLE Emails;
CREATE TABLE Emails(email VARCHAR(20) PRIMARY KEY);

--type: 0 public, 1 master, 2 slave
DROP TABLE Nodes;
CREATE TABLE Nodes(ipaddress VARCHAR(16) PRIMARY KEY, type TINYINT, mjpgport SMALLINT UNSIGNED);
INSERT INTO Nodes VALUES('24.68.152.172',0,NULL);
INSERT INTO Nodes VALUES('192.168.0.190',1,8080);
INSERT INTO Nodes VALUES('192.168.0.191',2,8081);
"""

import MySQLdb

# Function to return MySQL database connection
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
	
	# Create Devices table
	dbcur.execute("DROP TABLE Devices")
	dbcur.execute("CREATE TABLE Devices(serial BIGINT UNSIGNED PRIMARY KEY, type TINYINT, name VARCHAR(20), status TINYINT, active TINYINT)")

	# Create Credential table
	dbcur.execute("DROP TABLE Credential")
	dbcur.execute("CREATE TABLE Credential(username VARCHAR(20) PRIMARY KEY, password VARCHAR(20))")
	dbcur.execute("INSERT INTO Credential VALUES('pihome','pihomepass')")

	# Create Emails table
	dbcur.execute("DROP TABLE Emails")
	dbcur.execute("CREATE TABLE Emails(email VARCHAR(20) PRIMARY KEY)")

	# Create Nodes table
	dbcur.execute("DROP TABLE Nodes")
	dbcur.execute("CREATE TABLE Nodes(ipaddress VARCHAR(16) PRIMARY KEY, type TINYINT, mjpgport SMALLINT UNSIGNED)")
	
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to add new device
def addDevice(_serial, _type, _name, _status, _active):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Check if device is already existed
	dbcur.execute("SELECT * FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		# Insert new entry to Devices table
		dbcur.execute("INSERT INTO Devices VALUES(%s,%s,%s,%s,%s)", (_serial,_type,_name,_status,_active))
		
	# Commit querry and close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to get device information
def getDevice(_serial):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Check if device exists
	dbcur.execute("SELECT * FROM Devices WHERE serial=%s", _serial)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Device %s does not exist" % _serial)
	else:		
		# Return device info
		return result
		
	# Close db cursor, connection
	dbcur.close()
	dbcon.close()
	
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

# Function to get emails
def getEmails():
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Find all emails
	dbcur.execute("SELECT * FROM Emails")
	results=dbcur.fetchall()
	return results
		
	# Close db cursor, connection
	dbcur.close()
	dbcon.close()

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
		
# Function to add new node
def addNode(_ipadd, _type, _port):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Add new node if not existed
	dbcur.execute("SELECT * FROM Nodes WHERE ipaddress=%s", _ipadd)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		dbcur.execute("INSERT INTO Nodes VALUES(%s,%s,%s)", (_ipadd,_type,_port))

	# Commit, close db cursor, connection
	dbcon.commit()
	dbcur.close()
	dbcon.close()

# Function to get node information
def getNode(_ipadd):
	# Get database connection and cursor
	dbcon = getDBCon()
	dbcur = dbcon.cursor()
	
	# Get node info if existed
	dbcur.execute("SELECT * FROM Nodes WHERE ipaddress=%s", _ipadd)
	result=dbcur.fetchone()
	if result is None or result[0] is None:
		print("Node %s does not exist" % _ipadd)
	else:
		return result

	# Close db cursor, connection
	dbcur.close()
	dbcon.close()
		
####### Main
initDatabase()

addDevice(1000000000,1,'tridevice',0,1)

updateDeviceStatus(1000000000,1)
updateDeviceStatus(1000000001,1)
changeDeviceName(1000000000,'trideptrai')
changeDeviceName(1000000001,'yolo')
device1 = getDevice(1000000000)
print device1
device2 = getDevice(1000000001)
print device2
changePassword('pihome','pihomepass','haha')
changePassword('pihome','pihomepass','haha')

addEmail('trihuynh87')
addEmail('trihuynh877')
removeEmail('trihuynh')
removeEmail('trihuynh877')

emails=getEmails()
for email in emails:
	print email

addNode('192.168.1.12',0,8080)
print getNode('192.168.1.1')
nodeinfo=getNode('192.168.1.12')
print nodeinfo[0]


