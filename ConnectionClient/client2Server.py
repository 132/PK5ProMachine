import sys
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM


SERVER_IP   = '192.168.1.3'
PORT_NUMBER = 51236
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

#mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket = socket( AF_INET, SOCK_STREAM)
"""
while True:
        mySocket.sendto('ls -l',(SERVER_IP,PORT_NUMBER))
"""
#mySocket.sendto('ls -l',(SERVER_IP,PORT_NUMBER))

mySocket.connect((SERVER_IP,PORT_NUMBER))
#id = 0
#while True:
#print id
try:
#	mySocket.sendto('../cmake-build-debug/./rippled submit sh1LrEHjJyMGi9JLUHeyvKKAGSuRL \'{"Account" : "rBor3Awo22JCTB21gJejAyHZhQBXq7c29N", "TransactionType" : "LogTransaction", "TransactionContent" :  "tri dep trai"}\'',(SERVER_IP,PORT_NUMBER))
	msg = '../cmake-build-debug/./rippled submit sh1LrEHjJyMGi9JLUHeyvKKAGSuRL \'{"Account" : "rBor3Awo22JCTB21gJejAyHZhQBXq7c29N", "TransactionType" : "LogTransaction", "TransactionContent" :  "tri dep trai"}\''
	mySocket.sendall(msg)
	print msg
	received = 0
	expected = len(msg)
	while received < expected:
		print 'wait for response'
		data = mySocket.recv(SIZE)
		received += len(data)
		print 'received "%s"' %data
		if len(data) > 0:
			break
finally:
	print 'closing socket'
	
mySocket.close()	
sys.exit()
