from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, SOCK_STREAM
#from subprocess import call ## does not work in this case
import os
import commands
import select

import multiprocessing as mp
import threading
#import re				# regular expression

PORT_NUMBER = 51236 
SIZE = 4096
backlog = 4			# the number of connection can have


hostName = gethostbyname( '192.168.1.3' )

global mySocket

mySocket = socket( AF_INET, SOCK_STREAM )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Listening on port {0}\n".format(PORT_NUMBER))

mySocket.listen(backlog)

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
#connection.close()		range(0,len(
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
#while True:
#	inputReady, outputReady, exceptReady = select.select(input_, [], [])
#	# inputReady a list of connections 
#	for s in inputReady:
#		p = Process(target=aWorker, args=s)
#		p.start()

while True:
	c, addr = mySocket.accept()
	thread.start_new_thread(aworker,c)
	print 'tri hoc gioi'
mySocket.close()

"""
class ClientThread(threading.Thread):
	def __init__(self, ip, port, socket):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket
		print '[+] New thread started for '+ ip + ': ' + str(port)

	def run(self):
		self.socket.settimeout(100)
		try:
			while True:
				data = self.socket.recv(SIZE)
				if data == 'kill_server':
					print 'close Connection'
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
					#print status
					print '=============================='
					print output
					self.socket.sendall(output)
		except(self.socket.timeout) as error:
			self.socket.close()

if __name__== '__main__':
	while True:
		try:
			clientsock, (ip, port) = mySocket.accept()
			print ip
			newthread = ClientThread(ip,port, clientsock)
			newthread.start()
		except KeyboardInterrupt:
			break

#	clientsock, (ip, port) = mySocket.accept()
#	print ip
#	newthread2 = ClientThread(ip,port, clientsock)
#	newthread2.start()
#	while True:
#		newthread.run()
#############################################333
	
	server.close()

