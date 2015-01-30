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
num = int(str(data.decode()))
i = 0
while i < num:
	data = sckt.recv(size)
	temp = str(data.decode())
	print("File[" + str(i) + "]: " + temp)
	i += 1
sckt.close()
