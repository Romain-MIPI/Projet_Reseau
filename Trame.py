class Trame:
    def __init__(self):
        self.eth = None
        self.ip = None
        self.tcp = None
        self.http = None

    def setEth(self, eth):
        self.eth = eth

    def setIP(self, ip):
        self.ip = ip

    def setTCP(self, tcp):
        self.tcp = tcp

    def setHTTP(self, http):
        self.http = http

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
        print("dst ->", self.dst_mac)
        print("src ->", self.src_mac)
        print("type ->", self.type)

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
        if self.hlen == '5':
            self.option = None
        else:
            self.option = trame[40:]
        self.offset(self.flags)

    def offset(self, trame):
        tramebin = str(bin(int(trame, 16)))[2:]
        nb_zeros = 16 - len(tramebin)
        while nb_zeros != 0:
            tramebin = "0" + tramebin
            nb_zeros -= 1
        self.DF = tramebin[1]
        self.MF = tramebin[2]
        self.fragment_offset = tramebin[3:]

    def printIPv4(self):
        print("version ->", self.version)
        print("hlen ->", int(self.hlen, base = 16)*4, "bytes (", self.hlen, ")")
        print("Tos ->", self.ToS)
        print("total length ->", str(int(self.len, base = 16)))
        print("id ->", self.id)
        print("flags ->", self.flags)
        print("DF ->", self.DF,)
        print("MF ->", self.MF)
        print("fragment offset ->", self.fragment_offset)
        print("TTL ->", int(self.TTL, base = 16))
        print("protocole ->", self.protocole)
        print("checksum ->", self.checksum)
        print("src ip ->", self.src_ip)
        print("dst ip ->", self.dst_ip)
        print("option ->", self.option)

class TCP:
    def __init__(self):
        self.port_src = None
        self.port_dst = None
        self.seq_num = None
        self.ack_num = None
        self.THL = None
        self.flags = None
        self.URG = None
        self.ACK = None
        self.PSH = None
        self.RST = None
        self.SYN = None
        self.FIN = None
        self.window = None
        self.checksum = None
        self.urgent_pointer = None
        self.option = []
    
    def decodeTCP(self, trame):
        self.port_src = trame[:4]
        self.port_dst = trame[4:8]
        self.seq_num = trame[8:16]
        self.ack_num = trame[16:24]
        self.THL = trame[24]
        self.flags = trame[25:28]
        self.window = trame[28:32]
        self.checksum = trame[32:36]
        self.urgent_pointer = trame[36:40]
        if self.THL == '5':
            self.option = None
        else:
            self.setoptions(trame[40:])
        self.setflags(self.flags)

    def setflags(self, trame):
        tramebin = str(bin(int(trame, 16)))[2:]
        nb_zeros = 6 - len(tramebin)
        while nb_zeros != 0:
            tramebin = "0" + tramebin
            nb_zeros -= 1
        self.URG = tramebin[0]
        self.ACK = tramebin[1]
        self.PSH = tramebin[2]
        self.RST = tramebin[3]
        self.SYN = tramebin[4]
        self.FIN = tramebin[5]

    def setoptions(self, trame):
        i = 0
        len_op = len(trame)
        while i <= len_op -1:
            if trame[i:i+2] == '00' or trame[i:i+2] == '01':
                self.option.append((trame[i:i+2], None, None))
                i += 2
            else:
                option_length = trame[i+2:i+4]
                print((int(option_length, base = 16)//2))
                if trame[i:i+2] == '08':
                    len_value = 2*int(option_length, base = 16) - 4
                    print(len_value)
                    self.option.append((trame[i:i+2], option_length, (trame[i+4:i+4+(len_value//2)], trame[i+4+(len_value//2):])))
                else:
                    if 2*int(option_length, base = 16) - 4 == 0:
                        self.option.append((trame[i:i+2], option_length, None))
                    else:
                        self.option.append((trame[i:i+2], option_length, trame[i+4:i+4+(2*int(option_length, base = 16) - 4)]))
                i += 4+2*int(option_length, base = 16) - 4



    def printTPC(self):
        print("port src ->", int(self.port_src, base = 16))
        print("port dst ->", int(self.port_dst, base = 16))
        print("sequence number ->", int(self.seq_num, base = 16))
        print("acknowledgment number ->", int(self.ack_num, base = 16))
        print("THL ->", int(self.THL, base = 16)*4, "bytes (", self.THL, ")")
        print("flags ->", self.flags)
        print("URG ->", self.URG)
        print("ACK ->", self.ACK)
        print("PSH ->", self.PSH)
        print("RST ->", self.RST)
        print("SYN ->", self.SYN)
        print("FIN ->", self.FIN)
        print("Window ->", int(self.window, base = 16))
        print("checksum ->", self.checksum)
        print("urgent pointer ->", self.urgent_pointer)
        print("option ->", self.option)

class HTTP:
    def __init__(self):
        self.string = None

    def decodeHTTP(self, string):
        self.string = bytes.fromhex(string).decode("ASCII").rstrip('\n')

    def printHTTP(self):
        print("------------------------------------------------------------\n")
        print(self.string)
        print("------------------------------------------------------------")