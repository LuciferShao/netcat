#encoding=utf-8

import argparse
import socket
import threading
import subprocess

def run_command(command):
	command=command.rstrip()
	try:
		output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
	except:
		output="Failed to execute command.\n"
	return output
		
def menu():
	parse=argparse.ArgumentParser("nc tool")
	parse.add_argument("-l","--listen",help="set listen method",action="store_true")
	parse.add_argument("-p","--port",help="set the network port",default=0,type=int)
	parse.add_argument("-t","--target",help="set the target",default="0.0.0.0")
	parse.add_argument("-f","--file",help="please set the file address")
	args=parse.parse_args()
	if args.listen:
		server(args.port,args.target)
	else:
		client(args.port,args.target)

def server(port,host):
	monitor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	monitor.bind((host,port))
	monitor.listen(5)
	
	while True:
		monitor_socket,addr=monitor.accept()
		monitor_thread=threading.Thread(target=client_handler,args=(monitor_socket,))
		monitor_thread.start()

def client_handler(monitor_socket):
	print "ok"
	while True:
		recv_len=1
		response=""
		while recv_len:
			data=monitor_socket.recv(4096)
			response+=data
			if len(data)<4096:
				break
		print response
		result=run_command(response)
		monitor_socket.send(result)		
	
def client(port,host):
	
	conn=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		conn.connect((host,port))
		while True:
			buffer=raw_input(">>")
			conn.send(buffer)
		
			recv_len=1
			response=""
			while recv_len:
				data=conn.recv(4096)
				response+=data
				
				if len(data)<4096:
					break
			print response
	except:
		print "Exiting......."
		conn.close()	
	
if __name__=='__main__':
	menu()
