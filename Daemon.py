from threading import Thread
from random import randint
import time
import socket
import Constant as const
import Function as func

class Daemon(Thread):

	# Inizializza il thread, prende in ingresso l'istanza e un valore su cui ciclare
	# Tutti i metodi di una classe prendono l'istanza come prima variabile in ingresso
	# __init__ è un metodo predefinito per creare il costruttore
	def __init__(self, host):
		# Costruttore
		Thread.__init__(self)
		self.host = host
		self.port = const.PORT
		self.alive = True

	# Funzione per stopppare il Thread
	def stop(self):
		self.alive = False

	def run(self):
		# Creazione socket
		s = func.create_socket_server(self.host, self.port)

		if s is None:
			write_daemon_text(myHost, 'Error: Daemon could not open socket in upload on ' + myHost)
			sys.exit(1)

		while 1:
			conn, addr = s.accept()
			# write_daemon_text(myHost, 'Connected by ' + addr[0])
			ricevutoByte = conn.recv(1024)
			if not ricevutoByte:
				break
			if ricevutoByte == "LOGOUT":
				break
			md5 = ricevutoByte[4:36]
			fileName = searchName(md5)
			upload(fileName, conn, myHost)
			conn.close()



