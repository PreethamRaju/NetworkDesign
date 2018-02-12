import socket

host = '127.0.0.1'
port = 1101

server = ('127.0.0.1',3101)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((host,port))

img1 = open('clirecv.jpg','wb')
i = 0
while True:
	pack1, addr1 = sock.recvfrom(1000)
	if not pack1:
		break
	i = i+1
	print 'received packet',i
	img1.write(pack1)
img1.close()

print 'client receive complete'

img2 = open('clisend.jpg','rb')
i = 0
while True:
	pack2 = img2.read(1000)
	if not pack2:
		pack2 = ""
		sock.sendto(pack2,server)
		break
	sock.sendto(pack2,server)
	i = i+1
	print 'sent packet ',i
img2.close()

sock.close()

