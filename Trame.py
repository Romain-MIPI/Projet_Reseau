class Ethernet:
    def __init__(self):
        self.dst_mac = None
        self.src_mac = None
        self.type = None

    def decodeEth(self, trame):
        self.dst_mac = trame[:12]
        self.src_mac = trame[12:24]
        self.type = trame[24:]

    def printEth(self):
        print("dst -> ", self.dst_mac)
        print("src -> ", self.src_mac)
        print("type -> ", self.type)

class IPv4:
    def __init__(self):
        self.version = None
        self.hlen = None
        self.ToS = None
        self.len = None
        self.id = None
        self.flags = None
        self.DF = None
        self.MF = None
        self.fragment_offset = None
        self.TTL = None
        self.protocole = None
        self.checksum = None
        self.src_ip = None
        self.dst_ip = None
        self.option = None

    def decodeIPv4(self, trame):
        print(trame)
        self.version = trame[0]
        self.hlen = trame[1]
        self.ToS = trame[2:4]
        self.len = trame[4:8]
        self.id = trame[8:12]
        self.flags = trame[12:16] 
        self.TTL = trame[16:18]
        self.protocole = trame[18:20]
        self.checksum = trame[20:24]
        self.src_ip = trame[24:32]
        self.dst_ip = trame[32:40]
        if self.hlen == '4':
            self.option = None
        else:
            self.option = trame[40:]
        self.offset(self.flags)

    def offset(self, trame):
        tramebin = str(bin(int(trame, 16)))[2:]
        #print(tramebin)
        self.DF = tramebin[0]
        self.MF = tramebin[1]
        self.fragment_offset = tramebin[2:]

    def printIPv4(self):
        print("version -> ", self.version)
        print("hlen -> ", self.hlen)
        print("Tos -> ", self.ToS)
        print("total length -> ", str(int(self.len, base = 16)))
        print("id -> ", self.id)
        print("flags -> ", self.flags)
        print("DF -> ", self.DF,)
        print("MF -> ", self.MF)
        print("fragment offset -> ", self.fragment_offset)
        print("TTL -> ", self.TTL)
        print("protocole -> ", self.protocole)
        print("checksum -> ", self.checksum)
        print("src ip -> ", self.src_ip)
        print("dst ip -> ", self.dst_ip)
        print("option -> ", self.option)

class TCP:
    def __init__(self):
        self.port_src = None
        self.port_dst = None
        self.seq_num = None
        self.ack_num = None
        self.THL = None
        self.URG = None
        self.ACK = None
        self.PSH = None
        self.RST = None
        self.SYN = None
        self.FIN = None
        self.window = None
        self.checksum = None
        self.urgent_pointer = None
        self.option = None
        self.option_type = None
        self.option_length = None
        self.option_value = None
    
    #def decodeTCP(self, trame):