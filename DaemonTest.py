from threading import Thread
from random import randint
import time

class Daemon(Thread):

	# Inizializza il thread, prende in ingresso l'istanza e un valore su cui ciclare
	# Tutti i metodi di una classe prendono l'istanza come prima variabile in ingresso
	# __init__ è un metodo predefinito per creare il costruttore
	def __init__(self, val, list):
		# Costruttore
		Thread.__init__(self)
		self.val = val
		self.alive = True
		self.list = list

	def run(self):
		for i in range(1, self.val):
			if self.alive == False:
				print("Thread %s stoppato." % self.getName())
				break
			self.list.append(1)
			print(list)
			print('Value %d in thread %s' % (i, self.getName()))

			# Dorme per un tempo casuale, 1 ~ 5 secondi, ritorna N <= 5 e => 1
			secondsToSleep = randint(1, 5)
			print('%s sleeping for %d seconds...' % (self.getName(), secondsToSleep))
			time.sleep(secondsToSleep)

	def stop(self):
		self.alive = False

# Run following code when the program starts
if __name__ == '__main__':
	list = 1
	# Declare objects of MyThread class
	myThreadOb1 = Daemon(4, list)
	myThreadOb1.setName('Thread 1')

	myThreadOb2 = Daemon(4, list)
	myThreadOb2.setName('Thread 2')

	# Start running the threads!
	myThreadOb1.start()
	myThreadOb2.start()

	stop = input("q per stoppare i thread: ")

	if stop == "q":
		myThreadOb1.stop()
		myThreadOb2.stop()

	# Wait for the threads to finish...
	myThreadOb1.join()
	myThreadOb2.join()

	list = list

	print('Main Terminating...')

	print(list)