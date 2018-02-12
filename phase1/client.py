import socket

host = '127.0.0.1'
port = 1101

server = ('127.0.0.1', 3101)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host,port))
	
data1, addr1 = sock.recvfrom(6000)
img1 = open('clirecv.jpg', 'wb')
img1.write(data1)
img1.close()

img2 = open('clisend.jpg', 'rb')
data2 = img2.read(6000)
sock.sendto(data2, server)
img2.close()
	
sock.close()
