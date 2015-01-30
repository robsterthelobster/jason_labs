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
size = 1042
#Start
sckt = socket.socket()
sckt.connect((serverIP, port))
#Try password
sckt.sendall(inputPW.encode())
data = sckt.recv(size)
data = data.decode()
print("Data: " + data)
if data != "True":
	sckt.close()
	print("Password invalid!")
else:
	print("Success!")
	print(command)
	if command == "list":
		sckt.sendall(command.encode())
		data = sckt.recv(size)
		data = data.decode()
		files = data.split()
		for file in files:
			print(file)

	elif command == "get":
		print(command)
	elif command == "put":
		print(command)
		sckt.sendall(command)
		file = open(param, "rb")
	
		while True:
			chunk = file.read(65536)
			if not chunk:
				break  # EOF
			sckt.sendall(chunk)
	elif command == "delete":
		print(command)
	else:
		print("Invalid command")

	sckt.close()