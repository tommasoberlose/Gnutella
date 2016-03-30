from threading import Thread
import time
import sys
import socket
import Constant as const
import Function as func
import Package as pack

class Daemon(Thread):

	# Inizializza il thread, prende in ingresso l'istanza e un valore su cui ciclare
	# Tutti i metodi di una classe prendono l'istanza come prima variabile in ingresso
	# __init__ è un metodo predefinito per creare il costruttore
	def __init__(self, host, listNeighbor, listPkt, listResultQuery, host46):
		# Costruttore
		Thread.__init__(self)
		self.host = host
		self.host46 = host46
		self.port = const.PORT
		self.listNeighbor = listNeighbor
		self.listPkt = listPkt
		self.listResultQuery = listResultQuery

	def run(self):
		# Creazione socket
		s = func.create_socket_server(self.host, self.port)

		if s is None:
			func.write_daemon_text(self.host, 'Error: Daemon could not open socket in upload on ' + self.host)
			sys.exit(1)

		while 1:

			conn, addr = s.accept()
			func.write_daemon_text(self.host, 'connected by ' + addr[0])
			ricevutoByte = conn.recv(1024)
			print(ricevutoByte)
			if not ricevutoByte:
				print("Pacchetto errato")
				break
			elif (str(ricevutoByte[0:4], "ascii") == const.CODE_LOGO):
				break
			else:
				if str(ricevutoByte[0:4], "ascii") == const.CODE_ANSWER_QUERY:
					func.write_daemon_text(self.host, "ANSWER QUERY")
					if func.check_query(ricevutoByte[4:20]):
						# Controlla che il pacchetto non sia arrivato in ritardo tommAsinus
						listResultQuery.append([len(listResultQuery), ricevutoByte[80:112], ricevutoByte[112:], ricevutoByte[20:75], ricevutoByte[75:80]])
						print(len(listResultQuery) + "\t" + ricevutoByte[112:] + "\t" + str(ricevutoByte[20:75],"ascii"))
					else: 
						func.write_right_text(self.host, "Pacchetto di risposta ad una query arrivato tardi")

				elif str(ricevutoByte[0:4], "ascii") == const.CODE_QUERY:
					func.write_daemon_text(self.host, "QUERY")
					if func.add_pktid(ricevutoByte[4:20], self.listPkt) is True:
						# Inoltro
						pk = pack.forward_query()
						func.forward(pk, self.listNeighbor)

						# Rispondi
						listFileFounded = func.search_file(func.reformat_string(str(ricevutoByte[82:]),"ascii"))
						if len(listFileFounded) != 0:
							for x in listFileFounded:
								pk = pack.answer_query(ricevutoByte[4:20], self.host46, x[0], x[1])
								sC = func.create_socket_client(func.roll_the_dice(ricevutoByte[20:75]), ricevutoByte[75:80])
								if sC != None:
									sC.sendall(pk)
									sC.close()
					else:
						func.write_daemon_text(self.host, "Pacchetto già ricevuto")

				elif str(ricevutoByte[0:4], "ascii") == const.CODE_NEAR:
					func.write_daemon_text(self.host, "NEAR")
					if func.add_pktid(ricevutoByte[4:20], self.listPkt) is True:
						func.write_daemon_text(self.host, "Response near request:" + str(ricevutoByte[20:75], "ascii"))
						# Inoltro
						pk = pack.forward_neighbor(ricevutoByte)
						func.forward(pk, self.listNeighbor)

						# Response neighborhood
						pk = pack.answer_neighbor(ricevutoByte[4:20], self.host46)
						sC = func.create_socket_client(func.roll_the_dice(ricevutoByte[20:75]), ricevutoByte[75:80])
						if sC != None:
							sC.sendall(pk)
							sC.close()
					else:
						func.write_daemon_text(self.host, "Pacchetto già ricevuto")

				elif str(ricevutoByte[0:4], "ascii") == const.CODE_ANSWER_NEAR:
					func.write_daemon_text(self.host, "ANSWER NEAR")
					func.write_daemon_text(self.host, "Add neighbor:" + str(ricevutoByte[20:75], "ascii"))
					self.listNeighbor.append([ricevutoByte[20:75], ricevutoByte[75:80]])

			conn.close()



