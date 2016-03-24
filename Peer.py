import Function as func
import Costant as const
import Package as pack
import Daemon as daemon
import Neighbor as near

def updateNeighbor(host):
	pk = pack.neighbor(host)
	while True:
		print ("Peer Vicino:")
		nGroup = input("Numero del gruppo: ")
		nElement = input("Numero dell'elemento del gruppo: ")
		hostN = func.roll_the_dice("172.030." + func.format_string(nGroup, LENGTH_SECTION_IPV4, "0") + "." + func.format_string(nElement, LENGTH_SECTION_IPV4, "0") + "|fc00:0000:0000:0000:0000:0000:" + func.format_string(nGroup, LENGTH_SECTION_IPV6, "0") + ":" + func.format_string(nElement, LENGTH_SECTION_IPV6, "0"))
		s = func.create_socket_client(host, const.PORT);
		if s is None:
			print func.error("\nErrore nella scelta del primo peer vicino, scegline un altro.")
		else:
			s.sendall(bytes(pk, "ascii"))
			s.close()
			break

def search(host, query):
	pk = pack.query(host, query)
	listNeighbor = near.get_neighbor()
	if len(listNeighbor) is 0:
		print func.error("Nessun vicino presente, crea prima una rete virtuale")
	else:
		i = 0
		for x in listNeighbor:
			s = func.create_socket_client(x[0], x[1]);
			if s is None:
				print func.error("\nPeer vicino non attivo:", x[0])
			else:
				s.sendall(bytes(pk, "ascii"))
				s.close()
				i = i + 1
				break
	if i is 0:
		print func.error("Nessun peer vicino attivo")
	else:
		print ("\n\nLista file disponibili: \n")
		print("ID\tFILE\t\tIP")




####### INIZIO CLIENT #######
nGroup = input("Inserire il numero del gruppo: ")
nElement = input("Inserire il numero dell'elemento del gruppo: ")
host = "172.030." + func.format_string(nGroup, LENGTH_SECTION_IPV4, "0") + "." + func.format_string(nElement, LENGTH_SECTION_IPV4, "0") + "|fc00:0000:0000:0000:0000:0000:" + func.format_string(nGroup, LENGTH_SECTION_IPV6, "0") + ":" + func.format_string(nElement, LENGTH_SECTION_IPV6, "0")

print ("IP:", host)

# Menù di interazione
while True:
	choice = input("\n\nScegli azione:\nupdate - Update Neighborhood\nsearch - Search File\nquit - Quit\n\nScelta: ")

	if (choice == "update"):
		updateNeighbor(host)

	elif (choice == "search"):
		query = input("\n\nInserisci il nome del file da cercare: ")
		search(host, query)

	elif (choice == "quit"):
		#
		break

	else:
		error("Wrong Choice!")
