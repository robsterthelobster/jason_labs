import socket
import os

ip = ''
port = 842
size = 1024

serv_sckt = socket.socket()
serv_sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sckt.bind((ip,port))
serv_sckt.listen(1)
print ("Server Start")
while True:
	c, a = serv_sckt.accept()
	data = c.recv(size)
	if data.decode() == "list":
		files = [f for f in os.listdir('.') if os.path.isfile(f)]
		filenames = ""
		filenames += str(files)[1:-1]
		c.sendall(filenames.encode())
		break
	else:
		print("Not list")
		break

#serv_sckt.shutdown(socket.SHUT_RDWR)
serv_sckt.close()
print("Server Shutdown!")
