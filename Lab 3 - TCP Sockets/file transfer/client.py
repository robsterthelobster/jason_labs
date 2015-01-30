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

port = 842
size = 1024
#Start
sckt = socket.socket()
sckt.connect((serverIP, port))
file = open(param, "rb")
	
while True:
	chunk = file.read(65536)
	if not chunk:
		break  # EOF
	sckt.sendall(chunk)

