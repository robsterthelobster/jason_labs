import socket
import sys

#Format: client.py (serverip) (password) (command) (param)
serverIP = sys.argv[1]
inputPW  = sys.argv[2]
command  = sys.argv[3]
param    = "[None]"
if len(sys.argv) == 5:
	param = sys.argv[4]

print("Server IP: " + str(serverIP))
print("Password : " + str(inputPW))
print("Command  : " + str(command))
print("Param    : " + str(param))

#Start
sckt = socket.socket()
sckt.connect((serverIP, port))
#Try password
sckt.send(inputPW)
pwPass = sckt.recv();
sckt.send(command, param)

#def commandAction(command, param):
#	return{
#		"list"  : list()
#		"get"   : get(param)
#		"put"   : put(param)
#		"delete": delete(param)
#	}
#	
#def list():
#
#def get(param):
#
#def put(param):
#
#def delete(param):
