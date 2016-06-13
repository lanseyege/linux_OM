#encoding=utf-8

import os,struct,sys,ConfigParser
from socket import *
path_list=[]
ips=[]
all_path=[]
def read_conf(config_file):
	cf = ConfigParser.ConfigParser()
	cf.read(config_file)
	ip = cf.get('ip','ip')
	ips = ip.split(',')
	port = cf.get('port','port')
	ports = port.split(',')
	for a in ips:
		print a+' '
	for a in ports:
		print a+' '
	all_p=cf.get('path','path')
	all_path=all_p.split(',')
def read_path(path):
	if path[-1] != '/':
		path +='/'
	if os.path.isdir(path):
		path_list=os.listdir(path)
	path_list=[path+p+'/' for p in path_list]
def send_file():
	n=len(path_list)
	m=len(ips)
	a=n/m
	b=n%m
	b_=0
	A=[0]*m
	B=set{}
	for i in xrange(m):
		if b_>= b:
			A[i]=a
		else:
			A[i]=a+1
			b_ +=1
	c=0
	for i in xrange(m):
		B[ips[i]]=path_list[c:c+A[i]]
		c+=A[i]
	for ip in ips:
		ADDR={ip,80000}
		BUFSIZE=102400
		sendSock=socket(AF_INET,SOCK_STREAM)
		sendSock.connect(ADDR)
		for path in B[ip]:
			filelist=os.listdir(path)
			for filename in filelist:
				filename=path+filename			
				FILEINFO_SIZE=struct.calcsize('128s32sI8s')
				fhead=struct.pack('128s11I',filename,0,0,0,0,0,0,0,0,os.stat(filename).st_size,0,0)
				sendSock.send(fhead)
				fp=open(filename,'rb')
				while 1:
					filedata=fp.read(BUFSIZE)
					if not filedata:
						break
					sendSock.send(filedata)
				fp.close()
		fhead=struct.pack('128s11I','over',0,0,0,0,0,0,0,0,0,0,0)
		sendSock.send(fhead)							
		sendSock.close()

if__name__=='__main__':
	config_file=sys.argv[0]
	send_conf(config_file)
	read_path(all_path[0])
	send_file()
	read_path(all_path[1])
	send_file()



