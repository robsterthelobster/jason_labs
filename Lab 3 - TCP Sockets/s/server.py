import socket
import os

ip = ''
port = 842
size = 1024
password = "meh"
pwGood = None

serv_sckt = socket.socket()
serv_sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sckt.bind((ip,port))
serv_sckt.listen(1)
print ("Server Start")
while True:
	c, a = serv_sckt.accept()
	data = c.recv(size)
	if data and pwGood == None:
		#print("Data: " + data.decode())
		if data.decode() == password:
			pwGood = "True"
			c.sendall(pwGood.encode())
		else:
			pwGood = "False"
			c.sendall(pwGood.encode())
	if pwGood == "True":
		data = c.recv(size)
		command = data.decode()
		
		if command == "list":
			path = os.getcwd() + "\\public"
			files = os.listdir(path)
			filenames = ""
			for i in range(len(files)):
				if os.path.isfile(path+"\\"+str(files[i])):
					filenames += str(files[i])
					if i != len(files) - 1:
						filenames += ", "
			c.sendall(filenames.encode())
				
		elif command == "get":
			data = c.recv(size)
			filename = data.decode()
			try:
				file = open(filename, "rb")
				c.sendall("true".encode())
				while True:
					chunk = file.read(65536)
					if not chunk:
						c.sendall("end".encode())
						break
					c.sendall(chunk)
			except FileNotFoundError:
				c.sendall("false".encode())
				
		elif command == "put":
			data = c.recv(size)
			filename = data.decode()
			with open(filename, 'wb') as file_to_write:
				while True:
					data = c.recv(size)
					if not data:
						break
					file_to_write.write(data)
			
		elif command == "delete":
			data = c.recv(size)
			try:
				os.remove(data.decode())
				c.sendall("true".encode())
			except FileNotFoundError:
				c.sendall("false".encode())
				
		elif command == "end":
			break;
		
		else:
			print("Invalid command")
			
	data = None
	pwGood = None

serv_sckt.close()