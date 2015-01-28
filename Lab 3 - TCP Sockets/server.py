import socket

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
		else:
			pwGood = "False"
			c.sendall(pwGood.encode())
			serv_sckt.close()
	if pwGood == "True":
		print("Good")
		c.sendall(pwGood.encode())
		break

#serv_sckt.shutdown(socket.SHUT_RDWR)
serv_sckt.close()
print("Done!")



