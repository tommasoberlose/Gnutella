import Constant as const
import time

def add_pktid(list_pkt, pktid, time):
	i = 0
	for lista in list_pkt:
		if pktid == list_pkt[i][0]:
			return false
		i = i + 1
	add_list = [pktid, time]
	list_pkt.append(add_list)
	return list_pkt

def clear_pktid(list_pkt, nowtime):
	i = 0
	for i in list_pkt:
		time = list_pkt[i][1]
		diff = nowtime - time
		if diff => 300:
			del list_pkt[i]
		i = i + 1
	return list_pkt


	####### sincronizzazione tra add e clear nei thread

