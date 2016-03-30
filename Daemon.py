from threading import Thread
import time
import socket
import Constant as const
import Function as func
import Package as pack

class Daemon(Thread):

	# Inizializza il thread, prende in ingresso l'istanza e un valore su cui ciclare
	# Tutti i metodi di una classe prendono l'istanza come prima variabile in ingresso
	# __init__ è un metodo predefinito per creare il costruttore
	def __init__(self, host, listNeighbor, listPkt, listResultQuery, pktID, host46):
		# Costruttore
		Thread.__init__(self)
		self.host = host
		self.host46 = host46
		self.port = const.PORT
		self.listNeighbor = listNeighbor
		self.listPkt = listPkt
		self.listResultQuery = listResultQuery
		self.pktID = pktID

	def run(self):
		# Creazione socket
		s = func.create_socket_server(self.host, self.port)

		if s is None:
			func.write_daemon_text(self.host, 'Error: Daemon could not open socket in upload on ' + self.host)
			sys.exit(1)

		while 1:
			conn, addr = s.accept()
			func.write_daemon_text(self.host, 'Connected by ' + addr[0])
			ricevutoByte = conn.recv(1024)
			if ((not ricevutoByte) || (ricevutoByte[0:4] == const.CODE_LOGO)):
				break
			else:
				if ricevutoByte[0:4] == const.CODE_ANSWER_QUERY:
					# Controlla che il pacchetto non sia arrivato in ritardo tommAsinus
					listResultQuery.append([len(listResultQuery), ricevutoByte[80:112], ricevutoByte[112:], ricevutoByte[20:75], ricevutoByte[75:80]])

				elif ricevutoByte[0:4] == const.CODE_QUERY:
					if func.add_pktid(ricevutoByte[4:20], self.pktID) is False:
						# Inoltro
						pk = pack.forward_query()
						func.forward(pk, listNeighbor, s)

						# Rispondi
						listFileFounded = func.search_file(func.reformat_string(str(ricevutoByte[82:]),"ascii"))
						if len(listFileFounded) != 0:
							for x in listFileFounded:
								pk = pack.answer_query(ricevutoByte[4:20], self.host46, x[0], x[1])
								s = func.create_socket_client(func.roll_the_dice(ricevutoByte[20:75]), ricevutoByte[75:80])
								if s != None:
									s.sendall(pk)
									s.close()

				elif ricevutoByte[0:4] == const.CODE_NEAR:
					if func.add_pktid(ricevutoByte[4:20], self.pktID) is False:
						func.write_daemon_text("Response near request:", ricevutoByte[20:75])
						# Inoltro
						pk = pack.forward_neighbor()
						func.forward(pk, listNeighbor, s)

						# Response neighborhood
						pk = pack.neighbor(self.host46)
						s = func.create_socket_client(func.roll_the_dice(ricevutoByte[20:75]), ricevutoByte[75:80])
						if s != None:
							s.sendall(pk)
							s.close()

				elif ricevutoByte[0:4] == const.CODE_ANSWER_NEAR:
					func.write_daemon_text("Add neighbor:", ricevutoByte[20:75])
					listNeighbor.append([ricevutoByte[20:75], ricevutoByte[75:80]])

			conn.close()



