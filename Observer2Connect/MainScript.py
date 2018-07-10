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
#!/usr/bin/env python
##########################################################
#		Lib
###########################################################
import sys
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import difflib, sys

import os
from shutil import copyfile
import time
##########################################################3
# accoun Tri
#./rippled submit sh1LrEHjJyMGi9JLUHeyvKKAGSuRL '{"Account" : "rBor3Awo22JCTB21gJejAyHZhQBXq7c29N", "TransactionType" : "LogTransaction", "TransactionContent" :  "tri dep trai"}'

# create a list of copy files of original files
# Take the last modfication of files
# create a list of connection
def initClient(path):
	listFiles = ['/var/log/syslog']
	for ifile in range(0,len(listFiles)):
		aFile = listFiles[ifile]

		# take the last modification
		mtime = os.path.getmtime(aFile)

		# create a list of coppy files
		if len(aFile.split('/')) > 1:
			newName = aFile.split('/')
			newName[-1] = 'Ori_'+newName[-1]
			#fileName = '/'.join(newName)
			fileName = path + newName[-1]
		else:
			fileName = 'Ori_'+aFile
		copyfile(aFile, fileName)
		print fileName
		innerList = [fileName, aFile, mtime, 0]
		Files.append(innerList)

	# create a list of connections
	for iconn in range(0, len(SERVER_IP)):
		# connect to the server
		mySocket = socket( AF_INET, SOCK_STREAM)
		mySocket.connect((SERVER_IP[iconn],PORT_NUMBER))
		conn.append(mySocket)

# compare 2 files 
# connect to server
# add new data for Ori_file
def compare_connectServer(file1, file2):
	#take the first connection
#	for con in range(0, len(conn)):
#		mySocket = conn[con]

	# read two files
	with open(file1,'r') as f1, open(file2,'r') as f2:
		# take the difference between two files
		diff = difflib.ndiff(f1.readlines(),f2.readlines()) 
	
		# for the all file with difference
		for line in diff:
#        if line.startswith('-'):
#            sys.stdout.write(line)
#        elif line.startswith('+'):
#            sys.stdout.write('\t\t'+line)
			
			# the '+' at the begining of the line is the difference of 2 files
			if line.startswith('+'):
				line = line[2:len(line)-1]
				sys.stdout.write(line)
				
				# filtering special character in content of the line
				# the result should be \'' or \"" in command line
				modifiedLine = line.replace('"', '\"\"')
				modifiedLine = modifiedLine.replace("'", "\'\'")
				print modifiedLine
				# create msg to update to TCP/IP server for starting a transaction
				msg = '../cmake-build-debug/./rippled submit ' + secretAcc + ' \'{"Account" : "' + accID + '", "TransactionType" : "LogTransaction", "TransactionContent" :  "' + "[" +file1 + "] " + modifiedLine + '"}\''
				#print msg
				print msg
				print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))
				starConnection(msg)
				# write the new update to a backup File
				with open(file1, "a") as text_file:
					text_file.write(line + '\n')

def starConnection(msg):
	# start connecting to server
	for iSoc in conn:
		try:
			#mySocket.sendall(msg)
			iSoc.sendall(msg)
			"""
		received = 0
		expected = len(msg)
		while received < expected:
			data = mySocket.recv(SIZE)
			print '===================================================='
			print data
			received += len(data)
			if len(data) > 0:
				break
			"""
		finally:
			print '####################### Finish a line ###########################'


def check_updating():
	for ifile in range(0, len(Files)):
		temp = Files[ifile]
		checkMTIME = os.path.getmtime(temp[1])
		if checkMTIME > temp[2]:
			# update the modified time
			Files[ifile][2] = checkMTIME
			# update 1 meaning that it was modified
			Files[ifile][3] = 1 
def closeConnection():
	for iconn in range(0, len(conn)):
		conn[iconn].sendall('kill_server')
		print 'connection close'	
		conn[iconn].close()
		
def main():
	# info of Account/home/lab298a/Public/TriThesis/BCLog-master/my_modified_rippled/Observer2Connect/
	global secretAcc 
	secretAcc = 'sh1LrEHjJyMGi9JLUHeyvKKAGSuRL'
	global accID
	accID = 'rBor3Awo22JCTB21gJejAyHZhQBXq7c29N'


	global SIZE
	SIZE = 4096

	# info of Server
	global SERVER_IP
	SERVER_IP = []
	SERVER_IP.append('192.168.1.3')
	SERVER_IP.append('192.168.1.1')
	
	global PORT_NUMBER	# default port
	PORT_NUMBER = 51236
	global conn
	conn = []	
	
	# info of files need to be checked
	global Files
	Files = []
	
	# initialize to prepare	
	initClient('/home/lab298a/Public/TriThesis/BCLog-master/my_modified_rippled/Observer2Connect/')

#	nextRound = 1
	
	while True:
		try:
			# check update the updating of clients
			for ifile in range(0, len(Files)):
				temp = Files[ifile]
				#print temp[1]
				checkMTIME = os.path.getmtime(temp[1])
				if checkMTIME > temp[2]:
					# update the modified time
					Files[ifile][2] = checkMTIME
					# update 1 meaning that it was modified
					Files[ifile][3] = 1 
					# execute compare and connect to server
					compare_connectServer(Files[ifile][0], Files[ifile][1])
				#time.sleep(1)
		except KeyboardInterrupt:
			for iS in conn:
				iS.sendall('kill_server')
			break
	closeConnection()


if __name__ == '__main__':

	print("Start a Client")
	
	main()

#	secretAcc = 'sh1LrEHjJyMGi9JLUHeyvKKAGSuRL'
#	accID = 'rBor3Awo22JCTB21gJejAyHZhQBXq7c29N'


#	SERVER_IP   = '192.168.1.3'
#	PORT_NUMBER = 51236
#	SIZE = 1024
	
