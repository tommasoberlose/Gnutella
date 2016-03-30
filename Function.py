import string
import random
import socket
import shutil
import os
import sys
import hashlib
import time
import Constant as const
import Function as func

####### STRINGHE

# Format string completa text con char per ottenere una stringa di lunghezza length
# Tested, fondamentale che il text passato sia stringa e la length un numero.
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
	write_right_text("Daemon on " + host + ": " + text)

def error(text):
	print ("Error:", text)

# Return PktID in string 
# Tested
def random_pktid(length):
   return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(length))

####### SOCKET

def create_socket_server(myHost, port):
	s = None
	if len(myHost) < 55:
		for res in socket.getaddrinfo(myHost, int(port), socket.AF_UNSPEC,socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
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
	else:
		func.error("Errore dimensione IP.")
	return s

def create_socket_client(myHost, port):
	s = None
	if len(myHost) < 55:
		for res in socket.getaddrinfo(myHost, int(port), socket.AF_UNSPEC, socket.SOCK_STREAM):
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
	else:
		func.error("Errore dimensione IP.")
	return s

def forward(pk, listNeighbor, s):
	if pk != bytes(const.ERROR_PKT, "ascii"):
		for x in listNeighbor:
			s = func.create_socket_client(func.roll_the_dice(x[0]), x[1])
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


###### SEARCH FILE

#funzione di ricerca file all'interno della cartella FileCondivisi
def search_file(query):
	file_list = []
	file_found_list = []
	file_list = os.listdir(const.FILE_COND)
	for file in file_list:
		if query in file:
			if not file.endswith('~'):
				md5File = hashlib.md5(open(const.FILE_COND + file,'rb').read()).hexdigest()
				file_found = [md5File, file]
				file_found_list.append(file_found)
		else:
			func.error("File not exists")

	print(file_found_list)
	return file_found_list

def add_pktid(list_pkt, pktid):
	list_pkt = clear_pktid(list_pkt)
	for lista in list_pkt:
		if pktid == lista[0]:
			return False
	pkTime = time.time() * 1000
	add_list = [pktid, pkTime]
	list_pkt.append(add_list)
	return list_pkt

def clear_pktid(list_pkt):
	for i in list_pkt:
		pkTime = i[1]
		nowtime = time.time() * 1000
		diff = nowtime - pkTime
		if diff >= 300000:
			del i
	return list_pkt