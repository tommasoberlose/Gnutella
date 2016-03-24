import Function as func
import Costant as const

global listNeighbor = list()

# Mi connetto a una directory, inserire porta 3000
nGroup = input("Inserire il numero del gruppo: ")
nElement = input("Inserire il numero dell'elemento del gruppo: ")
host = func.roll_the_dice("172.030." + func.format_string(nGroup, LENGTH_SECTION_IPV4, "0") + "." + func.format_string(nElement, LENGTH_SECTION_IPV4, "0") + "|fc00:0000:0000:0000:0000:0000:" + func.format_string(nGroup, LENGTH_SECTION_IPV6, "0") + ":" + func.format_string(nElement, LENGTH_SECTION_IPV6, "0"))

print ("IP:", host)

# Menù di interazione
while True:
	choice = input("\n\nScegli azione:\nupdate - Update Neighborhood\nsearch - Search File\nquit - Quit\n\nScelta: ")

	if (choice == "update"):
		listNeighbor = updateNeighbor(host, listNeighbor)

	elif (choice == "search"):
		query = input("\n\nInserisci il nome del file da cercare: ")
		search(query)

	elif (choice == "quit"):
		#
		break

	else:
		error("Wrong Choice!")
