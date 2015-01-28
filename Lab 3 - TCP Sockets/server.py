import socket

ip = ''
port = 842
size = 1024
password = "meh"

serv_sckt = socket.socket()
serv_sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sckt.bind((ip,port))
serv_sckt.listen(1)
c, a = serv_sckt.accept()
while True:
	data = c.recv(size)
	print(data)
	if not data:
		break
serv_socket.shutdown(socket.SHUT_RDWR)
serv_socket.close()



