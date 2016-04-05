from tkinter import *

def create_window(title, msg):
	# Prepara la finestra
	cima = Tk()
	F = Frame(cima)
	F.pack()

	# Rinomina la finestra
	F.master.title(title)

	lCiao = Label(F, text = msg)
	lCiao.pack()

	# Attiva il ciclo
	cima.mainloop()

	return lCiao

def text(msg, F):
	# Aggiungi i widget
	lCiao = Label(F, text = msg)
	lCiao.pack()
	F.master.update_idletasks()

def error(msg, F):
	# Aggiungi i widget
	lCiao = Label(F, text = msg)
	lCiao.pack()

def success(msg, F):
	# Aggiungi i widget
	lCiao = Label(F, text = msg)
	lCiao.pack()