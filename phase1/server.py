import socket

host = socket.gethostbyname('localhost')
port = 3101

client = ('127.0.0.1', 1101)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host,port))

img1 = open('servsend.jpg', 'rb')
data1 = img1.read(6000)
sock.sendto(data1, client)
img1.close()
	

data2, addr2 = sock.recvfrom(6000)
img2 = open('servrecv.jpg', 'wb')
img2.write(data2)
img2.close()

sock.close()
