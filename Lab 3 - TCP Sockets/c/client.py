import socket
import sys

#Format: client.py (serverip) (password) (command) (param)
serverIP = sys.argv[1]
inputPW  = sys.argv[2]
command  = sys.argv[3]
param    = "[None]"
if len(sys.argv) == 5:
	param = sys.argv[4]

port = 842
size = 1042
#Start
sckt = socket.socket()
sckt.connect((serverIP, port))
#Try password
sckt.sendall(inputPW.encode())
data = sckt.recv(size)
data = data.decode()
if data != "True":
	sckt.close()
	print("Password invalid!")
else:
	if command == "list":
		sckt.sendall(command.encode())
		data = sckt.recv(size)
		data = data.decode()
		files = data.split()
		for file in files:
			print(file)

	elif command == "get":
		sckt.sendall(command.encode())
		sckt.sendall(param.encode())
		
		with open(param, 'wb') as file_to_write:
			while True:
				data = sckt.recv(1024)
				if not data:
					break
				file_to_write.write(data)
		
	elif command == "put":
		sckt.sendall(command.encode())
		sckt.sendall(param.encode())
		file = open(param, "rb")
	
		while True:
			chunk = file.read(65536)
			if not chunk:
				break  # EOF
			sckt.sendall(chunk)
			
	elif command == "delete":
		sckt.sendall(command.encode())
		sckt.sendall(param.encode())
		
	else:
		print("Invalid command")

	sckt.close()