import socket

host = socket.gethostbyname('localhost')
port = 3101

client = ('127.0.0.1',1101)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host,port))

img1 = open('servsend.jpg','rb')
i=0
while True:
	pack1 = img1.read(1000)
	if not pack1:
		pack1 = ""
		sock.sendto(pack1,client)
		break
	sock.sendto(pack1,client)
	i = i+1
	print 'sent packet ',i
img1.close()

print 'Server send complete'

img2 = open('servrecv.jpg','wb')
i=0
while True:
	pack2, addr2 = sock.recvfrom(1000)
	if not pack2:
		break
	i = i+1
	print 'received packet ',i
	img2.write(pack2)
img2.close()

print 'Server receive complete'

sock.close()
