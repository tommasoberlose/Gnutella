#funzione di ricerca file all'interno della cartella FileCondivisi
import os
import sys
import string
import hashlib
import Constant as const

def search(query):
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
			######gestire gli errori
			error("file_not_exists")

	print(file_found_list)
	return file_found_list

query = input("Inserisci il nome del file da cercare: ")
search(query)
