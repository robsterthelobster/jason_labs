import socket
import os

ip = ''
port = 80
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
		
		path = os.getcwd() + "\\public"
		if command == "list":
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
				file = open(path+"\\" + filename, "rb")
				c.sendall("true".encode())
				while True:
					chunk = file.read(65536)
					#print("Server: " + str(chunk))
					if not chunk:
						break
					c.sendall(chunk)
				file.close()
			except FileNotFoundError:
				c.sendall("false".encode())
				
		elif command == "put":
			data = c.recv(size)
			filename = data.decode()
			with open(path+"\\"+filename, 'wb') as file_to_write:
				while True:
					data = c.recv(size)
					if not data:
						break
					file_to_write.write(data)
			
		elif command == "delete":
			data = c.recv(size)
			try:
				os.remove(path + "\\" + data.decode())
				c.sendall("true".encode())
			except FileNotFoundError:
				c.sendall("false".encode())
				
		elif command == "end":
			break;
		
		else:
			print("Invalid command")
	
	c.close()
	data = None
	pwGood = None
serv_sckt.shutdown(socket.SHUT_RDWR)
serv_sckt.close()