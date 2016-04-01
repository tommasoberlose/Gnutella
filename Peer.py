import Function as func
import Constant as const
import Package as pack
import Daemon as daemon

# Crea il pacchetto "NEAR.PKTID.IP4|IP6.PORTA.", inserisco manualmente un elemento della rete, se va bene invio il pacchetto, else ne provo un altro.
def updateNeighbor(myHost):
	pk = pack.neighbor(myHost)
	while True:
		print ("Peer Vicino:")
		nGroup = input("Numero del gruppo: ")
		nElement = input("Numero dell'elemento del gruppo: ")
		nPort = input("Inserire la porta su cui il vicino è in ascolto: ")
		hostN = func.roll_the_dice("172.030." + func.format_string(nGroup, const.LENGTH_SECTION_IPV4, "0") + 
																"." + func.format_string(nElement, const.LENGTH_SECTION_IPV4, "0") + 
																"|fc00:0000:0000:0000:0000:0000:" + func.format_string(nGroup, const.LENGTH_SECTION_IPV6, "0") + 
																":" + func.format_string(nElement, const.LENGTH_SECTION_IPV6, "0"))
		s = func.create_socket_client(hostN, nPort);
		if s is None:
			func.error("Errore nella scelta del primo peer vicino, scegline un altro.")
		else:
			s.sendall(pk)
			s.close()
			break

def search(myHost, query, listNeighbor, listPkt):
	pk = pack.query(myHost, query)
	if len(listNeighbor) is 0:
		func.error("Nessun vicino presente, crea prima una rete virtuale")
	else:
		func.add_pktid(pk[4:20], listPkt)
		i = 0
		for x in listNeighbor:
			s = func.create_socket_client(func.roll_the_dice(x[0]), x[1]);
			if s is None:
				func.error("\nPeer vicino non attivo:" + str(x[0], "ascii"))
			else:
				s.sendall(pk)
				s.close()
				i = i + 1
	if i is 0:
		func.error("Nessun peer vicino attivo")
	else:
		print("\n\nScegli file da quelli disponibili (0 per uscire): \n")
		choose = int(input("ID\tFILE\t\tIP\n"))
		# Da fare
		#stopSearch(myHost)
		if choose != 0:
			download(listResultQuery[choose - 1])
			func.remove_pktid(pk, listPkt)
			#listResultQuery = []
	

# Funzione di download
def download(selectFile):	

	print ("Il file selezionato ha questi parametri: ", selectFile)

	md5 = selectFile[1]
	nomeFile = selectFile[2].decode("ascii").strip()
	ip = selectFile[3]
	port = selectFile[4]

	# Con probabilità 0.5 invio su IPv4, else IPv6
	ip = func.roll_the_dice(ip.decode("ascii"))
	print(ip)

	# Mi connetto al peer

	sP = func.create_socket_client(ip, port)
	if sP is None:
	    print ('Error: could not open socket in download')
	else:
		pk = pack.dl(md5)
		print("Send:", pk)
		sP.sendall(pk)

		nChunk = int(sP.recv(const.LENGTH_HEADER)[4:10])
					
		ricevutoByte = b''

		i = 0
		
		while i != nChunk:
			ricevutoLen = sP.recv(const.LENGTH_NCHUNK)
			print(ricevutoLen)
			while (len(ricevutoLen) < const.LENGTH_NCHUNK):
				ricevutoLen = ricevutoLen + sP.recv(const.LENGTH_NCHUNK - int(ricevutoLen))
			buff = sP.recv(int(ricevutoLen))
			while(len(buff) < int(ricevutoLen)):
				buff = buff + sP.recv(int(ricevutoLen) - len(buff))
			ricevutoByte = ricevutoByte + buff
			print(len(buff), buff)
			i = i + 1

		sP.close()

		print ("Il numero di chunk è: ", nChunk)
		
		# Salvare il file data
		open((const.FILE_COND + nomeFile),'wb').write(ricevutoByte)

def logout(ip):
	i = 0
	pk = pack.logout()
	s = func.create_socket_client(func.get_ipv4(ip), const.PORT);
	if s is None:
		func.error("Errore nella chiusura del demone:" + func.get_ipv4(ip))
	else:
		s.sendall(pk)
		s.close()
		i = i + 1
	s = func.create_socket_client(func.get_ipv6(ip), const.PORT);
	if s is None:
		func.error("Errore nella chiusura del demone:" + func.get_ipv6(ip))
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

####### INIZIO CLIENT #######
nGroup = input("Inserire il numero del gruppo: ")
nElement = input("Inserire il numero dell'elemento del gruppo: ")
host = ("172.030." + func.format_string(nGroup, const.LENGTH_SECTION_IPV4, "0") + 
				"." + func.format_string(nElement, const.LENGTH_SECTION_IPV4, "0") + 
				"|fc00:0000:0000:0000:0000:0000:" + func.format_string(nGroup, const.LENGTH_SECTION_IPV6, "0") + 
				":" + func.format_string(nElement, const.LENGTH_SECTION_IPV6, "0"))

print ("IP:", host)

####### DEMONI

daemonThreadv4 = daemon.Daemon(func.get_ipv4(host), listNeighbor, listPkt, listResultQuery, host)
daemonThreadv6 = daemon.Daemon(func.get_ipv6(host), listNeighbor, listPkt, listResultQuery, host)
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
		search(host, query, listNeighbor, listPkt)

	elif (choice == "quit"):
		logout(host)
		daemonThreadv4.join()
		daemonThreadv6.join()
		break

	else:
		func.error("Wrong Choice!")