import string
import random
import socket
import shutil

####### STRINGHE

# Format string completa text con char per ottenere una stringa di lunghezza length
def format_string(text, length, char):
	l = len(text)
	dif = length - l
	return char * dif + text 

def reformat_string(text):
	return text.strip()

def	write_right_text(text):
	print(str(text).rjust(shutil.get_terminal_size((80, 20))[0] - 5))

def write_daemon_text(host, text):
	write_right_text("\n")
	write_right_text("Daemon connected on " + host)
	write_right_text(text)

def error(text):
	print ("Error:", text)

# Return PktID in string
def random_pktid(length):
   return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(length))

####### SOCKET

def create_socket_server(myHost, port):
	s = None
	for res in socket.getaddrinfo(myHost, format_string(port, LENGTH_PORT, "0"), socket.AF_UNSPEC,socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
	    af, socktype, proto, canonname, sa = res
	    try:
	        s = socket.socket(af, socktype, proto)
	    except socket.error as msg:
	        s = None
	        continue
	    try:
	        s.bind(sa)
	        s.listen(10)
	    except socket.error as msg:
	        s.close()
	        s = None
	        continue
	    break
	return s

def create_socket_client(myHost, port):
	s = None
	for res in socket.getaddrinfo(myHost, format_string(port, LENGTH_PORT, "0"), socket.AF_UNSPEC, socket.SOCK_STREAM):
	    af, socktype, proto, canonname, sa = res
	    try:
	        s = socket.socket(af, socktype, proto)
	    except socket.error as msg:
	        s = None
	        continue
	    try:
	        s.connect(sa)
	    except socket.error as msg:
	        s.close()
	        s = None
	        continue
	    break
	return s

def forward(pk, listNeighbor, s):
	if pk != bytes(const.ERROR_PKT, "ascii"):
		for x in listNeighbor:
			s = func.create_socket_client(x[0], x[1])
			if not(s is None):
				s.sendall(pk)
				s.close()

###### IP

def roll_the_dice(ip):
	return random.choice([ip[0:15], ip[16:55]])

def get_ipv4(ip):
	return ip[0:15]

def get_ipv6(ip):
	return ip[16:55]