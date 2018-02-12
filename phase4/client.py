import socket
import base64
import string
import json
import sys

i=0

def checksum (leng,data):
        a = base64.b16encode(data)
        b = str.decode(a)
	c = '0'
        d = base64.b16encode(c)
        csum = str.decode(d)
	rang = len(b)
	for i in range(0,rang):
                csum = hex( int(csum,16) + int(b[i],16) )
                i = i+1
	compcsum = csum[2:]
        return compcsum

def removepkt(pkt):
	lst = json.loads(pkt)
	lst = str(lst)
	#print "lst",lst
	seq = lst[3]
	leng = lst[9:13]
	leng = int(leng)
	print "length",leng
	d = lst[18:(2*leng+18)]
	#print "recvdata",d
	d = str.encode(d)
	data = base64.b16decode(d)
	recvcsum = lst[(2*leng+23):(2*leng+27)]
	return (seq,leng,data,recvcsum)

def check(expseq,seq,compcsum,recvcsum,data):
	if (str(expseq)==str(seq))&(str(compcsum)==str(recvcsum)):
		print 'recvseq= ',seq
		#print 'recvdata= ',data
		print 'recvcsum=',recvcsum
		print 'compcsum=',compcsum
		#i = i+1
		#print 'received packet',i
		img.write(data)
		expseq = int(seq)^1
		sock.sendto(str(expseq),channel2)
		print "Sent ACK"
		rdtrcv(expseq)
	else:
		sock.sendto(str(expseq),channel2)
		print "Sent NACK"
		rdtrcv(expseq)
	return ()

def rdtrcv(expseq):
	pkt, addr = sock.recvfrom(2029)
	if not pkt:
		print "client receive complete"
		img.close()
		sock.close()
		sys.exit()
	else:
		print "recvpkt= ",pkt
		(seq,leng,data,recvcsum) = removepkt(pkt)
		compcsum = checksum(leng,data)
		check(expseq,seq,compcsum,recvcsum,data)
	return ()


host = '127.0.0.1'
port = 1101

channel2 = ('127.0.0.1',1993)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((host,port))

img = open('clirecv.jpg','wb')
i = 0
expseq = 0
rdtrcv(expseq)




