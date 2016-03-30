import Function as func
import Costant as const
import Package as pack
import Daemon as daemon
import Neighbor as near

# Crea il pacchetto "NEAR.PKTID.IP4|IP6.PORTA.", inserisco manualmente un elemento della rete, se va bene invio il pacchetto, else ne provo un altro.
def updateNeighbor(myHost):
	pk = pack.neighbor(myHost)
	while True:
		print ("Peer Vicino:")
		nGroup = input("Numero del gruppo: ")
		nElement = input("Numero dell'elemento del gruppo: ")
		hostN = func.roll_the_dice("172.030." + func.format_string(nGroup, LENGTH_SECTION_IPV4, "0") + "." + func.format_string(nElement, LENGTH_SECTION_IPV4, "0") + "|fc00:0000:0000:0000:0000:0000:" + func.format_string(nGroup, LENGTH_SECTION_IPV6, "0") + ":" + func.format_string(nElement, LENGTH_SECTION_IPV6, "0"))
		s = func.create_socket_client(hostN, const.PORT);
		if s is None:
			print func.error("\nErrore nella scelta del primo peer vicino, scegline un altro.")
		else:
			s.sendall(pk)
			s.close()
			break

def search(myHost, query, listNeighbor):
	pk = pack.query(myHost, query)
	if len(listNeighbor) is 0:
		print func.error("Nessun vicino presente, crea prima una rete virtuale")
	else:
		i = 0
		for x in listNeighbor:
			s = func.create_socket_client(x[0], x[1]);
			if s is None:
				print func.error("\nPeer vicino non attivo:", x[0])
			else:
				s.sendall(pk)
				s.close()
				i = i + 1
	if i is 0:
		print func.error("Nessun peer vicino attivo")
	else:
		print ("\n\nScegli file da quelli disponibili (0 per uscire): \n")
		choose = input("ID\tFILE\t\tIP")
		# Da fare
		stopSearch(myHost)
		if choose != 0:
			download(listResultQuery[choose - 1])

# Funzione di download
def download(selectFile):	

	print ("Il file selezionato ha questi parametri: ", selectFile)

	md5 = selectFile[1]
	nomeFile = selectFile[2]
	ip = selectFile[3]
	port = selectFile[4]

	# Con probabilità 0.5 invio su IPv4, else IPv6
	ip = roll_the_dice(ip.decode("ascii"))
	print(ip)

	# Mi connetto al peer

	sP = func.create_socket_client(ip, port)
	if sP is None:
	    print ('Error: could not open socket in download')
	else:
		pack = pack.dl(md5)
		sP.sendall(pack)
		ricevutoHeader = sP.recv(10)
		nChunk = int(ricevutoHeader[4:10])

		print(ricevutoHeader)

		ricevutoByte = b''

		i = 0
		
		while i != nChunk:
			ricevutoLen = sP.recv(5)
			print(ricevutoLen)
			while (len(ricevutoLen) < 5):
				ricevutoLen = ricevutoLen + sP.recv(5 - int(ricevutoLen))
			buff = sP.recv(int(ricevutoLen))
			while(len(buff) < int(ricevutoLen)):
				buff = buff + sP.recv(int(ricevutoLen) - len(buff))
			ricevutoByte = ricevutoByte + buff
			print(len(buff), buff)
			i = i + 1

		sP.close()

		print ("Il numero di chunk è: ", nChunk)
		
		# Salvare il file data
		open((const.FILE_COND + nomeFile.decode("ascii")),'wb').write(ricevutoByte)

def logout(ip):
	i = 0
	pk = pack.logout()
	s = func.create_socket_client(func.get_ipv4(ip), const.PORT);
	if s is None:
		print func.error("\nErrore nella chiusura del demone:", func.get_ipv4(ip))
	else:
		s.sendall(pk)
		s.close()
		i = i + 1
	s = func.create_socket_client(func.get_ipv6(ip), const.PORT);
	if s is None:
		print func.error("\nErrore nella chiusura del demone:", func.get_ipv6(ip))
	else:
		s.sendall(pk)
		s.close()
		i = i + 1
	if i is 2:
		print ("Logout eseguito con successo.")

####### VARIABILI 

listNeighbor = []	
listPkt = []
listResultQuery = []	
pktID = []	

####### INIZIO CLIENT #######
nGroup = input("Inserire il numero del gruppo: ")
nElement = input("Inserire il numero dell'elemento del gruppo: ")
host = "172.030." + func.format_string(nGroup, LENGTH_SECTION_IPV4, "0") + "." + func.format_string(nElement, LENGTH_SECTION_IPV4, "0") + "|fc00:0000:0000:0000:0000:0000:" + func.format_string(nGroup, LENGTH_SECTION_IPV6, "0") + ":" + func.format_string(nElement, LENGTH_SECTION_IPV6, "0")

print ("IP:", host)

####### DEMONI

daemonThreadv4 = daemon.Daemon(func.get_ipv4(host), listNeighbor, listPkt, listResultQuery, pktID)
daemonThreadv6 = daemon.Daemon(func.get_ipv6(host), listNeighbor, listPkt, listResultQuery, pktID)
daemonThreadv4.setName("Thread ipv4")
daemonThreadv6.setName("Thread ipv6")
daemonThreadv4.start()	
daemonThreadv6.start()

# Menù di interazione
while True:
	choice = input("\n\nScegli azione:\nupdate - Update Neighborhood\nsearch - Search File\nquit - Quit\n\nScelta: ")

	if (choice == "update"):
		updateNeighbor(host)

	elif (choice == "search"):
		query = input("\n\nInserisci il nome del file da cercare: ")
		while(len(query) > const.LENGTH_QUERY):
			print("Siamo spiacenti ma accettiamo massimo 20 caratteri.")
			query = input("\n\nInserisci il nome del file da cercare: ")
		search(host, query, listNeighbor)

	elif (choice == "quit"):
		logout(host)
		daemonThreadv4.join()
		daemonThreadv6.join()
		break

	else:
		error("Wrong Choice!")