import socket
import sys

#Format: client.py (serverip) (password) (command) (param)
serverIP = "localhost"
command  = "list"
param    = "test2.txt"

port = 842
size = 1042
#Start
sckt = socket.socket()
sckt.connect((serverIP, port))
sckt.sendall(command.encode())
print("Sending...")
data = sckt.recv(size)
data = data.decode()
files = data.split()
for file in files:
	print(file)
sckt.close()
