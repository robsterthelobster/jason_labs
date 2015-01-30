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
			serv_sckt.close()
	if pwGood == "True":
		data = c.recv(size)
		data = data.decode()
		print(data)
		
		if data == "list":
			files = [f for f in os.listdir('.') if os.path.isfile(f)]
			filenames = ""
			filenames += str(files)[1:-1]
			c.sendall(filenames.encode()) 

		elif data == "get":
			print("get")
		elif data == "put":
			print("put")
		elif data == "delete":
			print("delete")
		else:
			print("Invalid command")
			
		break

#serv_sckt.shutdown(socket.SHUT_RDWR)
serv_sckt.close()
print("Done!")