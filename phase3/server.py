import socket
import base64
import string
import json

i=0

def checksum (data):
        a = base64.b16encode(data)
        b = str.decode(a)
	c = '0'
        d = base64.b16encode(c)
        csum = str.decode(d)
	rang = len(b)
        for i in range(0,rang):
                csum = hex( int(csum,16) + int(b[i],16) )
                i = i+1
	csum = csum[2:]
        return csum

def makepkt(seq,leng,data,csum):
	leng = str.decode(leng)
	seq = str.decode(seq)
	a = base64.b16encode(data)
        data = str.decode(a)
        lst = [seq,leng,data,csum]
        pkt = json.dumps(lst)
        return pkt

def waitack(seq,pkt):
	nxtseq = int(seq)^1
	print "Waiting for ack or Nack"
	ack, addr = sock.recvfrom(4)
	if (str(ack)) == (str(nxtseq)):
		print "Received ACK"
		seq = nxtseq
		udtsend(int(seq))
	else:
		print "Received NACK" 
		sock.sendto(pkt,channel1)
		waitack(seq,pkt)
	return ()
	
def udtsend(seq):
	data = img1.read(1000)
	if not data:
		data = ""
		sock.sendto(data,channel1)
		img1.close()
		print 'Server send complete'
		sock.close()

	else: 
		#print "imgdata= ", data
		csum = checksum(data)
		print "checksum= ",csum
		seq = str(seq)
		print "seqnum= ", seq
		leng = len(data)
		leng = str(leng).zfill(4)
		pkt = makepkt(seq,leng,data,csum)
		print "packet= ",pkt
		sock.sendto(pkt,channel1)
		waitack(seq,pkt)
	return ()
	
host = socket.gethostbyname('localhost')
port = 3101

channel1 = ('127.0.0.1',1103)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host,port))

img1 = open('servsend.jpg','rb')
i = 0
seq = 0
udtsend(seq)


