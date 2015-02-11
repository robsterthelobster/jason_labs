import socket
import sys

#Format: client.py (serverip) (password) (command) (param)
serverIP = sys.argv[1]
inputPW  = sys.argv[2]
command  = sys.argv[3]
param    = "[None]"
if len(sys.argv) == 5:
	param = sys.argv[4]

port = 8888
size = 1024
#Start
sckt = socket.socket()
sckt.connect((serverIP, port))
#Try password
sckt.sendall(inputPW.encode())
print("Sending password...")
data = sckt.recv(size)
data = data.decode()
if data != "True":
	sckt.close()
	print("Password invalid!")
else:
	print("Password accepted.")
	print("Sending command: " + command)
	if command == "list":
		sckt.sendall(command.encode())
		data = sckt.recv(size)
		data = data.decode()
		print("Data recieved:")
		files = data.split(", ")
		for file in files:
			print(file)
		print("Done!")

	elif command == "get":
		sckt.sendall(command.encode())
		data = sckt.recv(size)
		print("Server: " + data.decode())
		sckt.sendall(param.encode())
		data = sckt.recv(size)
		if data.decode() == "true":
			with open(param, 'wb') as file_to_write:
				while True:
					data = sckt.recv(size)
					#print("Client: " + str(data))
					if not data:
						break
					file_to_write.write(data)
			print("Done!")
		else:
			print("File [" + param + "] does not exist")
		
	elif command == "put":
		try:
			file = open(param, "rb")
			sckt.sendall(command.encode())
			data = sckt.recv(size)
			print("Server: " + data.decode())
			sckt.sendall(param.encode())
		
			while True:
				chunk = file.read(65536)
				if not chunk:
					break  # EOF
				sckt.sendall(chunk)
				
			print("Done!")
			file.close()
		except FileNotFoundError:
			print("File [" + param + "] does not exist")
			
	elif command == "delete":
		sckt.sendall(command.encode())
		data = sckt.recv(size)
		print("Server: " + data.decode())
		sckt.sendall(param.encode())
		data = sckt.recv(size)
		if data.decode() == "false":
			print("File [" + param + "] does not exist")
			
		print("Done!")
	
	elif command == "end":
		sckt.sendall(command.encode())
		
	else:
		print(command + " is a invalid command")
	sckt.shutdown(socket.SHUT_RDWR)
	sckt.close()