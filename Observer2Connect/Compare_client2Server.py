"""
while True:
        mySocket.sendto('ls -l',(SERVER_IP,PORT_NUMBER))
"""
"""
#mySocket.sendto('ls -l',(SERVER_IP,PORT_NUMBER))

mySocket.connect((SERVER_IP,PORT_NUMBER))
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
"""

import sys
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import difflib, sys
from time import sleep
# accoun Tri
#./rippled submit sh1LrEHjJyMGi9JLUHeyvKKAGSuRL '{"Account" : "rBor3Awo22JCTB21gJejAyHZhQBXq7c29N", "TransactionType" : "LogTransaction", "TransactionContent" :  "tri dep trai"}'

secretAcc = 'sh1LrEHjJyMGi9JLUHeyvKKAGSuRL'
accID = 'rBor3Awo22JCTB21gJejAyHZhQBXq7c29N'

SERVER_IP   = '192.168.1.3'
PORT_NUMBER = 51236
SIZE = 1024

mySocket = socket( AF_INET, SOCK_STREAM)
mySocket.connect((SERVER_IP,PORT_NUMBER))

with open('f1.txt','r') as f1, open('f2.txt','r') as f2:
	diff = difflib.ndiff(f1.readlines(),f2.readlines())    
	for line in diff:
#        if line.startswith('-'):
#            sys.stdout.write(line)
#        elif line.startswith('+'):
#            sys.stdout.write('\t\t'+line)  
		if line.startswith('+'):
			line = line[2:len(line)-1]
			sys.stdout.write(line)
			msg = '../cmake-build-debug/./rippled submit ' + secretAcc + ' \'{"Account" : "' + accID + '", "TransactionType" : "LogTransaction", "TransactionContent" :  "' + line + '"}\''
			print msg
			try:
				print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))
				print msg
				mySocket.sendall(msg)
				received = 0
				expected = len(msg)
				print 'already sent msg'		
				while received < expected:
					#print 'wait for response'
					data = mySocket.recv(SIZE)
					print data
					received += len(data)
			#print 'len(data): ' + str(len(data))
			#print 'received "%s"' %data
					if len(data) > 0:
						break
			finally:
				print 'abc'
				sleep(1)
		print 'next line'
	mySocket.sendall('kill_server')
print 'connection close'	
mySocket.close()

