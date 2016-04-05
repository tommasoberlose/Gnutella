import Function as func
import Package as pack
import Constant as const
import Interface as ui
import hashlib
from tkinter import *

"""print("TEST FUNC")

print ("Format String: ", func.format_string("ciao", 10, " "));
print ("Random Pktid: ", func.random_pktid(const.LENGTH_PKTID))
print ("Reformat String: ", func.reformat_string("       ciao"))


print("\nTEST PACK")
print("PACK QUERY:", pack.query("172.030.001.004|fc00:0000:0000:0000:0000:0000:0001:0004", "ricerca"))
print("PACK FORWARD QUERY:", pack.forward_query(pack.query("172.030.001.004|fc00:0000:0000:0000:0000:0000:0001:0004", "ricerca")))
print("PACK NEAR:", pack.neighbor("172.030.001.004|fc00:0000:0000:0000:0000:0000:0001:0004"))
print("PACK FORWARD NEAR:", pack.forward_neighbor(pack.neighbor("172.030.001.004|fc00:0000:0000:0000:0000:0000:0001:0004")))
md5 = hashlib.md5(open(const.FILE_COND + "puppies.jpg",'rb').read()).hexdigest()
print("PACK ANSWER QUERY:", pack.answer_query(bytes(func.random_pktid(const.LENGTH_PKTID), "ascii"), "172.030.001.004|fc00:0000:0000:0000:0000:0000:0001:0004", bytes(md5, "ascii"), "File.py"))
print("PACK DOWLOAD:", pack.dl(md5))
print("PACK LOGOUT", pack.logout())"""

lCiao = ui.create_window("Thread 1", "Stocazzo")
lCiao.configure(text = "Dai pur")
