from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, SOCK_STREAM
#from subprocess import call ## does not work in this case
import os
import commands
<<<<<<< HEAD

PORT_NUMBER = 51236 
SIZE = 1024
=======
import select

import multiprocessing as mp
import threading
#import re				# regular expression

PORT_NUMBER = 51236 
SIZE = 1024
backlog = 4			# the number of connection can have

>>>>>>> 22c6219fbc85756766779abdeff20efc690749ca

hostName = gethostbyname( '192.168.1.3' )

global mySocket

mySocket = socket( AF_INET, SOCK_STREAM )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Listening on port {0}\n".format(PORT_NUMBER))

<<<<<<< HEAD

mySocket.listen(1)
while True:
	print  'waiting for a connection'
	connection, client_address = mySocket.accept()

=======
mySocket.listen(backlog)
"""
while True:
	print  'waiting for a connection'
	connection, client_address = mySocket.accept()
	
>>>>>>> 22c6219fbc85756766779abdeff20efc690749ca
	try:
		print 'connection from', client_address

		while True:
<<<<<<< HEAD
#     		   	(data,addr) = mySocket.recv(SIZE)
=======
#     	   	(data,addr) = mySocket.recv(SIZE)
			print 'wait for a new data'
>>>>>>> 22c6219fbc85756766779abdeff20efc690749ca
			data = connection.recv(SIZE)
		        print data
		#	os.system(data) # work
			#call(data)
<<<<<<< HEAD
	
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
=======
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


"""
# this one for loop version
def aWorker(s):
	if s == mySocket:
		client, address = mySocket.accept()
		input_.append(client)
		print 'A client ' + str(address)
	else:
		data = s.recv(SIZE)
		if data == 'kill_server':
			s.close()
			return	#break
		elif not data:
			return 	#break
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
input_ = [mySocket,]
while True:
	inputReady, outputReady, exceptReady = select.select(input_, [], [])
	# inputReady a list of connections 
	for s in inputReady:
		aWorker(s)

"""

class ClientThread(threading.Thread):
	def __init__(self, ip, port, socket):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket
		print '[+] New thread started for '+ ip + ': ' + str(port)

	def run(self):
		data = self.socket.recv(SIZE)
		if data == 'kill_server':
			self.socket.close()
			return	#break
		elif not data:
			return 	#break
		else:
			print data
			# filter before applying to rippled e.g:  Couldn't create directory monitor on smb://x-gnome-default-workgroup/.
			#data = data.replace("'", "\'")
			#data = data.replace('"', '\"')
			status, output = commands.getstatusoutput(data)
			print status
			print '=============================='
			print output
			self.socket.sendall(output)


while True:
#		
	clientsock, (ip, port) = mySocket.accept()
	print ip
	newthread = ClientThread(ip,port, clientsock)
	while True:
		newthread.run()
#############################################333

	
server.close()
>>>>>>> 22c6219fbc85756766779abdeff20efc690749ca
