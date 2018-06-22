from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, SOCK_STREAM
#from subprocess import call ## does not work in this case
import os
import commands

PORT_NUMBER = 51236 
SIZE = 1024

hostName = gethostbyname( '192.168.1.3' )

mySocket = socket( AF_INET, SOCK_STREAM )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Test server listening on port {0}\n".format(PORT_NUMBER))


mySocket.listen(1)
while True:
	print  'waiting for a connection'
	connection, client_address = mySocket.accept()

	try:
		print 'connection from', client_address

		while True:
#     		   	(data,addr) = mySocket.recv(SIZE)
			data = connection.recv(SIZE)
		        print data
		#	os.system(data) # work
			#call(data)
	
			status, output = commands.getstatusoutput(data)

			print status
			print '=============================='
			print output
		
			connection.sendall(output)
			break	
#			if data == 'exit':
#				sys.ext()
	finally:
		connection.close()		

#(data,addr) = mySocket.recvfrom(SIZE)
#print data
#sys.ext()
