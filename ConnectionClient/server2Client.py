from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, SOCK_STREAM
#from subprocess import call ## does not work in this case
import os
import commands
import select
#import re				# regular expression

PORT_NUMBER = 51236 
SIZE = 1024
backlog = 10			# the number of connection can have


hostName = gethostbyname( '192.168.1.3' )

mySocket = socket( AF_INET, SOCK_STREAM )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Test server listening on port {0}\n".format(PORT_NUMBER))

mySocket.listen(backlog)
input_ = [mySocket,]
"""
while True:
	print  'waiting for a connection'
	connection, client_address = mySocket.accept()
	
	try:
		print 'connection from', client_address

		while True:
#     	   	(data,addr) = mySocket.recv(SIZE)
			print 'wait for a new data'
			data = connection.recv(SIZE)
		        print data
		#	os.system(data) # work
			#call(data)
			if data == 'kill_server':
				connection.close()
				break
#				sys.exit()
			elif not data:
				break
			else:
				status, output = commands.getstatusoutput(data)
				print status
				print '=============================='
				print output
				connection.sendall(output)
					
#			if data == 'exit':
#				sys.ext()
	finally:
		print 'complete 1 connection'
#connection.close()		
"""
#(data,addr) = mySocket.recvfrom(SIZE)
#print data
#sys.ext()

while True:
	inputReady, outputReady, exceptReady = select.select(input_, [], [])
	
	# inputReady a list of connections 
	for s in inputReady:
		if s == mySocket:
			client, address = mySocket.accept()
			input_.append(client)
			print 'new client ' + str(address)
		else:
			data = s.recv(SIZE)
			if data == 'kill_server':
				s.close()
				break
			elif not data:
				break
			else:
				print data
				# filter before applying to rippled e.g:  Couldn't create directory monitor on smb://x-gnome-default-workgroup/.
				#data = data.replace("'", "\'")
				#data = data.replace('"', '\"')
				status, output = commands.getstatusoutput(data)
				print status
				print '=============================='
				print output
				s.sendall(output)
server.close()
