#encoding=utf-8
import os,struct,sys,ConfigParser
from socket import *

ADDR=('127.0.0.1', 80000)
BUFSIZE=102400
FILEINFO_SIZE=struct.calcsize('128s32sI8s')

def server():
	recvSock=socket(AF_INET,SOCK_STREAM)
	recvSock.bind(ADDR)
	recvSock.listen(True)
	while True:
		conn, addr = recvSock.accept()
		print 'connect...',addr
		while True:
			fhead=conn.recv(FILEINFO_SIZE)
			filename,temp,filesize=struct.unpack('128s32sI8s',fhead)
			filename=filename.strip('\00')
			if filename == 'over':
				break
			path=filename[0:filename.rfind('/')]
			if not os.path.isdir(path):
				os.makedirs(path)
			print filename
			fp=open(filename,'wb')
			restsize=filesize
			while 1:
				if restsize > BUFSIZE:
					filedata=conn.recv(BUFSIZE)
				else:
					filedata=conn.recv(restsize)
				if not filedata:
					break
				fp.write(filedata)
				restsize=restsize-len(filedata)
				if restsize==0:
					break
			fp.close()
		conn.close()
	recvSock.close()

if __name__=='__main__':
	server()



