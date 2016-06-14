#encoding=utf-8
import os
import commands
import threading

def read_conf(path):
	file=open(path)
	A=[]
	for line in file:
		A.append(line.strip())
	return A

def read_source_dir(ips, s_path, w_df):
	if s_path[-1] != '/':
		s_path += '/'
	path_lists={}
	source_path_nums=0
	for ip in ips:
		command='ssh name@%s ls %s'%(ip, s_path)
		status,output=commands.getstatusoutput(command)
		if status != 0:
			w_df.write(command+'\n')
		path_list_=output.split('\n')
		path_list =[s_path+p+'/' for p in path_list_]
		path_lists[ip]=path_list
		source_path_nums += len(path_list_)
	return path_lists, source_path_nums

def send_dest_command(dest_ips, s_path, path_lists, source_path_nums):
	if s_path[-1] != '/':
		s_path += '/'
	comm_list=[]
	for k , v in path_list.items():
		for v_ in v:
			comm_list.append('scp -r name@%s:%s '%(k, v_))
	if len(comm_list) != source_path_nums:
		print 'nums not equal'
	n = source_path_nums
	m = len(dest_ips)
	a = n/m
	b = n%m
	b_ = 0
	A = [0] * m
	for i in xrange(m):
		if b_ >= b:
			A[i] = a
		else:
			A[i] = a + 1
			b_ += 1
	c = 0
	for i in xrange(m):
		for j in range(c, c + A[i]):
			comm_list[j] += 'name@%s:%s'%(dest_ips[i], s_path)
		c += A[i]
	return comm_list, A

def send_dest(comm_list, w_f):
	for comm in comm_list:
		status, output = commands.getstatusoutput(comm)
		if status != 0:
			w_f.write('status: ' + str(status) + ' failed command: '+ comm + '\n')

def mk_dest_dir(dest_ips, s_path, w_df):
	if s_path[-1] != '/':
		s_path += '/'
	for ip in dest_ips:
		comm = 'ssh name@%s mkdir -p %s'%(ip, s_path)
		status, output = commands.getstatusoutput(comm)
		if status != 0:
			w_df.write('make dest dir failed, command: ' + comm)

if __name__ == '__main__':
	failed_comm_path = 'fail'
	failed_dir_path = 'read_dirs_fail'
	w_f = open(failed_comm_path, 'w')
	w_df = open(failed_dir_path, 'w')
	source_ip_file = 'source'
	dest_ip_file   = 'dest'
	s_path_ = 'path'
	source_ips = read_conf(source_ip_file)
	dest_ips = read_conf(dest_ip_file)
	s_path = read_conf(s_path_)
	if len(s_path) != 2:
		print 's_path:\n /home/name/**/'
		print '/home/name/**/'
	mk_dest_dir(dest_ips, s_path[0], w_df)
	path_lists, nums = read_source_dir(source_ips, s_path[0], w_df)
	comm_list, A = send_dest_command(dest_ips, s_path[0], path_lists, nums)
	threads = []
	print ''
	c = 0
	for i in xrange(len(A)):
		a = threading.Thread(target = send_dest, args = (comm_list[c : c + A[i]], w_f))
		c += A[i]
		a.start()
		a.join()
	mk_dest_dir(dest_ips, s_path[1], w_df)
	path_lists, nums = read_source_dir(source_ips, s_path[1], w_df)
	comm_list, A = send_dest_command(dest_ips, s_path[1], path_lists, nums)
	threads = []
	print ''
	c = 0
	for i in xrange(len(A)):
		a = threading.Thread(target = send_dest, args = (comm_list[c : c + A[i]], w_f))
		c += A[i]
		a.start()
		a.join()


