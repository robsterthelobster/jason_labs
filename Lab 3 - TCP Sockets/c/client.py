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
		data = sckt.recv(size)
		if data.decode() == "true":
			with open(param, 'wb') as file_to_write:
				while True:
					data = sckt.recv(size)
					temp = data.decode()
					if temp == "end":
						break
					file_to_write.write(data)
		else:
			print("File [" + param + "] does not exist")
		
	elif command == "put":
		try:
			file = open(param, "rb")
			sckt.sendall(command.encode())
			sckt.sendall(param.encode())
		
			while True:
				chunk = file.read(65536)
				if not chunk:
					break  # EOF
				sckt.sendall(chunk)
				
		except FileNotFoundError:
			print("File [" + param + "] does not exist")
			
	elif command == "delete":
		sckt.sendall(command.encode())
		sckt.sendall(param.encode())
		data = sckt.recv(size)
		if data.decode() == "false":
			print("File [" + param + "] does not exist")
	
	elif command == "end":
		sckt.sendall(command.encode())
		
	else:
		print(command + " is a invalid command")

	sckt.close()