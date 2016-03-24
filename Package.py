import Constant as const
import Function as func

def query(ip, query):
	pk_id = func.random_pktid(const.LENGTH_PKTID)
	port = func.format_string(const.PORT, const.LENGTH_PORT, "0")
	step = func.format_string(const.TTL, const.LENGTH_TTL, "0")
	query = func.format_string(query, const.LENGTH_QUERY, " ")
	pack = bytes(const.CODE_QUERY, "ascii") + bytes(pk_id, "ascii") + bytes(ip, "ascii") + bytes(port, "ascii") + bytes(step, "ascii") + bytes(query, "ascii")

def forward(pack):
	step = pack[79:81]
	if step != 0:
		step = modify_ttl(step)
		pack = bytes(const.CODE_QUERY, "ascii") + bytes(pk_id, "ascii") + bytes(ip, "ascii") + bytes(port, "ascii") + bytes(step, "ascii") + bytes(query, "ascii")
		return pack
	else: 
		return const.ERROR_PKT

def neighbor(ip):
	pk_id = func.random_pktid(const.LENGTH_PKTID)
	step = func.format_string(const.TTL, const.LENGTH_TTL, "0")
	pack = bytes(const.CODE_NEAR, "ascii") + bytes(pk_id, "ascii") + bytes(ip, "ascii") + bytes(func.format_string(const.PORT, const.LENGTH_PORT, "0"), "ascii") + bytes(step, "ascii")
	return pack

def dl(md5):
	pack = bytes(const.CODE_DOWNLOAD, "ascii") + bytes(md5, "ascii")
	return pack



def modify_ttl(step):
	step = int.from_bytes(step, byteorder='big')
	step = step - 1
	return step