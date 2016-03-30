import Constant as const
import Function as func

def query(ip, query):
	pk_id = func.random_pktid(const.LENGTH_PKTID)
	port = func.format_string(const.PORT, const.LENGTH_PORT, "0")
	step = func.format_string(const.TTL, const.LENGTH_TTL, "0")
	query = func.format_string(query, const.LENGTH_QUERY, " ")
	pack = bytes(const.CODE_QUERY, "ascii") + bytes(pk_id, "ascii") + bytes(ip, "ascii") + bytes(port, "ascii") + bytes(step, "ascii") + bytes(query, "ascii")
	return pack

def forward_query(pack):
	step = modify_ttl(pack[80:82])
	if step != 0:
		step = func.format_string(str(step), const.LENGTH_TTL, "0")
		pack = pack[0:80] + bytes(step, "ascii") + pack[82:]
		return pack
	else: 
		return bytes(const.ERROR_PKT, "ascii")

def neighbor(ip):
	pk_id = func.random_pktid(const.LENGTH_PKTID)
	port = func.format_string(const.PORT, const.LENGTH_PORT, "0")
	step = func.format_string(const.TTL, const.LENGTH_TTL, "0")
	pack = bytes(const.CODE_NEAR, "ascii") + bytes(pk_id, "ascii") + bytes(ip, "ascii") + bytes(port, "ascii") + bytes(step, "ascii")
	return pack


def forward_neighbor(pack):
	step = modify_ttl(pack[80:82])
	if step != 0:
		step = func.format_string(str(step), const.LENGTH_TTL, "0")
		pack = pack[0:80] + bytes(step, "ascii")
		return pack
	else: 
		return bytes(const.ERROR_PKT, "ascii")

def dl(md5):
	pack = bytes(const.CODE_DOWNLOAD, "ascii") + bytes(md5, "ascii")
	return pack

def answer_query(pktID, ip, md5, fileName):
	port = func.format_string(const.PORT, const.LENGTH_PORT, "0")
	fileName = func.format_string(fileName, const.LENGTH_FILENAME, " ")
	return bytes(const.CODE_ANSWER_QUERY, "ascii") + pktID + bytes(ip, "ascii") + bytes(port, "ascii") + md5 + bytes(fileName, "ascii")

def answer_neighbor(pktID, ip):
	port = func.format_string(const.PORT, const.LENGTH_PORT, "0")
	return bytes(const.CODE_ANSWER_NEAR, "ascii") + pktID + bytes(ip, "ascii") + bytes(port, "ascii")

def modify_ttl(step):
	step = int(step)
	step = step - 1
	return step

def logout():
	return bytes(const.CODE_LOGO, "ascii")