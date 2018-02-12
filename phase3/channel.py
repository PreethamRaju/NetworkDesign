import socket
import base64
import string
import json
import sys
import random

def noloss():
	while True:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((host,serport))
		pkt, addr = sock.recvfrom(2029)
		sock.close()
		if not pkt:
			data = ""
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.bind((host,cliport))
			sock.sendto(pkt,client)
			print 'Channel send complete'
			sock.close()
			sys.exit()
		else:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)			
			sock.bind((host,cliport))
			sock.sendto(pkt,client)
			pkt, addr = sock.recvfrom(4)
			sock.close()
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.bind((host,serport))
			sock.sendto(pkt,server)
			sock.close()
	return()

def removepkt(pkt,garble):
	lst = json.loads(pkt)
	lst = str(lst)
	#print "lst",lst
	seq = lst[3]
	leng = lst[9:13]
	leng = int(leng)
	print "length",leng
	if garble == 1:
		d = ''.join(random.choice('0123456789ABCDEF') for i in range(2000))
		d = str.encode(d)
	elif garble == 0:
		d = lst[18:(2*leng+18)]
		#print "recvdata",d
		d = str.encode(d)
	data = base64.b16decode(d)
	recvcsum = lst[(2*leng+23):(2*leng+27)]
	leng = str(leng).zfill(4)
	return (seq,leng,data,recvcsum)


def makepkt(seq,leng,data,recvcsum):
	leng = str.decode(leng)
	seq = str.decode(seq)
	a = base64.b16encode(data)
        data = str.decode(a)
        lst = [seq,leng,data,recvcsum]
        pkt = json.dumps(lst)
        return pkt


def datagarb(garble,pkt,pktsent,pktcorr):
	if garble == 1:
		pktsent = pktsent+1
		pktcorr = pktcorr+1

	elif garble == 0:
		pktsent = pktsent+1

	(seq,leng,data,recvcsum) = removepkt(pkt,garble)
	pkt = makepkt(seq,leng,data,recvcsum)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host,cliport))
	sock.sendto(pkt,client)
	print "Sent packet to client"
	pkt, addr = sock.recvfrom(4)
	print "received paket from client"
	sock.close()
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host,serport))
	sock.sendto(pkt,server)
	print "sent packet to server"
	sock.close()
	return (pktsent,pktcorr)

pktsent = 0
pktcorr = 0
garble = 0

def dataloss(pktsent,pktcorr,dataper):
	if (pktsent):
		prop = (float(pktcorr)/float(pktsent))*100
		prop = float("{0:.2f}".format(prop))
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host,serport))
	pkt, addr = sock.recvfrom(2029)
	sock.close()
	if not pkt:
		data = ""
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((host,cliport))
		sock.sendto(pkt,client)
		print "Channel loss = ", prop
		print 'Channel send complete'
		sock.close()
		sys.exit()
	else:
		print "Received Pkt from server"
		if pktsent == 0:
			garble = 0
		elif (prop < float(dataper)):
			print "prop", prop
			garble = 1
		else:
			print "prop", prop
			garble = 0
		(pktsent,pktcorr) = datagarb(garble,pkt,pktsent,pktcorr)
	dataloss(pktsent,pktcorr,dataper)
	return ()


def ackgarb(garble,pkt,pktsent,pktcorr):
	if garble == 1:
		pkt = int(pkt)^1
		pktsent = pktsent+1
		pktcorr = pktcorr+1
	else:
		pktsent = pktsent+1
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host,serport))
	sock.sendto(str(pkt),server)
	sock.close()
	print "Sent pkt to Server:",str(pkt)
	return (pktsent,pktcorr)

def ackloss(pktsent,pktcorr,ackper):
	if (pktsent):
		prop = (float(pktcorr)/float(pktsent))*100
		prop = float("{0:.2f}".format(prop))
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((host,serport))
	pkt, addr = sock.recvfrom(2029)
	sock.close()
	if not pkt:
		data = ""
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((host,cliport))
		sock.sendto(pkt,client)
		print "pktsent:", pktsent
		print "pktcorrupted:", pktcorr
		print "Channel loss = ", prop 
		print 'Channel send complete'	
		sock.close()
		sys.exit()
	else:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((host,cliport))
		sock.sendto(pkt,client)
		pkt, addr = sock.recvfrom(4)
		sock.close()
		print "Received Pkt from Client:", pkt
		if pktsent == 0:
			garble = 0
		elif (prop < float(ackper)):
			print "prop", prop
			garble = 1
		else:
			print "prop", prop
			garble = 0
		(pktsent,pktcorr) = ackgarb(garble,pkt,pktsent,pktcorr)
	ackloss(pktsent,pktcorr,ackper)
	return()		
	

host = socket.gethostbyname('localhost')
serport = 1103
cliport = 1993

client = ('127.0.0.1',1101)
server = ('127.0.0.1',3101)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print "Option-1: Input '1' for No Loss or Bit Error, '0' otherwise"
print "Option-2: Input 'ACK error percentage' for ACK packet bit-error, '0' otherwise"
print "Option-3: Input 'Data error percentage' for Data packet bit-error"

rel = raw_input("Option-1: ")
ackper = raw_input("Option-2: ")
dataper = raw_input("Option-3: ")

pktsent = 0
pktcorr = 0
garble = 0

if rel == '1':
	noloss()
elif ackper == '0':
	print "Channel set for data loss"
	dataloss(pktsent,pktcorr,dataper)
else:
	print "Channel set for ack loss"
	ackloss(pktsent,pktcorr,ackper)
	



