from threading import Thread
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
			func.write_daemon_text(myHost, 'Error: Daemon could not open socket in upload on ' + myHost)
			sys.exit(1)

		while 1:
			conn, addr = s.accept()
			func.write_daemon_text(myHost, 'Connected by ' + addr[0])
			ricevutoByte = conn.recv(1024)
			if not ricevutoByte:
				break
			if ricevutoByte[0:4] == const.CODE_LOGO:
				break
			if ricevutoByte[0:4] == const.CODE_QUERY:

			elif ricevutoByte[0:4] == const.CODE_NEAR:

			conn.close()



