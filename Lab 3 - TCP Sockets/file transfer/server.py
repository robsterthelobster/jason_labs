import socket

ip = ''
port = 842
size = 1024
password = "meh"
pwGood = None
put = False

serv_sckt = socket.socket()
serv_sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serv_sckt.bind((ip,port))
serv_sckt.listen(1)
print ("Server Start")
conn, addr = serv_sckt.accept()
with open('myTransfer.txt', 'wb') as file_to_write:
    while True:
        data = conn.recv(1024)
        print data
        if not data:
            break
        file_to_write.write(data)
		

#serv_sckt.shutdown(socket.SHUT_RDWR)
serv_sckt.close()
print("Done!")



