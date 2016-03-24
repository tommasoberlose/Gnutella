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

###### IP

def roll_the_dice(ip):
	return random.choice([ip[0:15], ip[16:55]])
