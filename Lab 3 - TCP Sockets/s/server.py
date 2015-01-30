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
		data = data.decode()
		
		if data == "list":
			files = [f for f in os.listdir('.') if os.path.isfile(f)]
			filenames = ""
			filenames += str(files)[1:-1]
			c.sendall(filenames.encode()) 

		elif data == "get":
			data = c.recv(1024)
			file = open(data.decode(), "rb")
			
			while True:
				chunk = file.read(65536)
				if not chunk:
					break
				c.sendall(chunk)
			
		elif data == "put":
			data = c.recv(1024)
			filename = data.decode()
			with open(filename, 'wb') as file_to_write:
				while True:
					data = c.recv(1024)
					if not data:
						break
					file_to_write.write(data)
			
		elif data == "delete":
			data = c.recv(1024)
			os.remove(data.decode())
			
		else:
			print("Invalid command")
			
	data = None
	pwGood = None
	
#serv_sckt.shutdown(socket.SHUT_RDWR)
serv_sckt.close()
print("Done!")