#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="ceng499", # your username
                      passwd="ceng499", # your password
                      db="pihome") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the query you need
cur = db.cursor() 




# Use all the SQL you like
cur.execute("SELECT * FROM Devices")

# print all the first cell of all the rows
for row in cur.fetchall() :
    print row[2]

nodeip='192.168.0.190'
nodetype=1
mjpgport=8080
cur.execute("SELECT mjpgport FROM Nodes WHERE ipaddress=%s AND type=%s", (nodeip, nodetype))
value = cur.fetchone()
if value[0]==8080: print 'try'
#print value[0]

cur.execute("SELECT ipaddress FROM Nodes WHERE mjpgport=%s AND type=%s", (mjpgport, nodetype))
value = cur.fetchone()
if value[0] == '192.168.0.190': print 'true'

val=10000000000
cur.execute("SELECT serial FROM Devices")
value = cur.fetchone()
if value[0]==val: print 'yes'
print value[0]


serial=input("Serial number:")
status=input("Status:")
# Check if device exist
#cur.execute("SELECT name FROM Devices WHERE serial=%s", serial)
cur.execute("UPDATE Devices SET status=%s WHERE serial=%s", (status,serial))
db.commit()

cur.close()
db.close()





