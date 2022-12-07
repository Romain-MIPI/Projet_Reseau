class Trame:
    def __init__(self):
        self.c2 = None
        self.c3 = None
        self.c4 = None
        self.c7 = None

    def setC2(self, c2):
        self.c2 = c2

    def setC3(self, c3):
        self.c3 = c3

    def setC4(self, c4):
        self.c4 = c4

    def setC7(self, c7):
        self.c7 = c7

    def printTrame(self):
        if isinstance(self.c2, Ethernet):
            self.c2.printEth()
        if isinstance(self.c3, ARP):
            self.c3.printARP()
        elif isinstance(self.c3, IPv4):
            self.c3.printIPv4()
        if isinstance(self.c4, ICMP):
            self.c4.printICMP()
        elif isinstance(self.c4, TCP):
            self.c4.printTPC()
        if isinstance(self.c7, HTTP):
            self.c7.printHTTP()

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
        print("-------------------------Ethernet---------------------------")
        dst = self.dst_mac[0:2]
        src = self.src_mac[0:2]
        for i in range(2, len(self.dst_mac)):
            if i%2 == 0:
                dst += ":"
                src += ":"
            dst += self.dst_mac[i]
            src += self.src_mac[i]
        print("dst ->", dst)
        print("src ->", src)
        if self.type == "0800":
            print("type ->", self.type, "(IPv4)")
        elif self.type == "0806":
            print("type ->", self.type, "(ARP)")
        else:
            print("type ->", self.type)
        print("------------------------------------------------------------\n")

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
        print("----------------------------IPv4----------------------------")
        print("version ->", self.version)
        print("hlen ->", int(self.hlen, base = 16)*4, "bytes (", self.hlen, ")")
        print("Tos ->", self.ToS)
        print("total length ->", str(int(self.len, base = 16)))
        print("id ->", self.id, "(", int(self.id, base = 16), ")")
        print("flags ->", self.flags)
        print("DF ->", self.DF,)
        print("MF ->", self.MF)
        print("fragment offset ->", self.fragment_offset)
        print("TTL ->", int(self.TTL, base = 16))
        if self.protocole == "01":
            print("protocole ->", self.protocole, "(ICMP)")
        elif self.protocole == "06":
            print("protocole ->", self.protocole, "(TCP)")
        elif self.protocole == "11":
            print("protocole ->", self.protocole, "(UDP)")
        print("checksum ->", self.checksum)
        src = str(int(self.src_ip[0:2], base = 16))
        dst = str(int(self.dst_ip[0:2], base = 16))
        stock_src = ""
        stock_dst = ""
        for i in range(2, len(self.dst_ip)):
            if i%2 == 0:
                if not (stock_src == "" and stock_dst == ""):
                    src = src + "." + str(int(stock_src, base = 16))
                    dst = dst + "." + str(int(stock_dst, base = 16))
                    stock_src = ""
                    stock_dst = ""
            stock_src += self.src_ip[i]
            stock_dst += self.dst_ip[i]
        src = src + "." + str(int(stock_src, base = 16))
        dst = dst + "." + str(int(stock_dst, base = 16))
        print("src ip ->", src)
        print("dst ip ->", dst)
        print("option ->", self.option)
        print("------------------------------------------------------------\n")

class ARP:
    def __init__(self):
        self.HType = None
        self.PType = None
        self.HAddLen = None
        self.PAddLen = None
        self.OpCode = None
        self.SenderHAdd = None
        self.SenderPAdd = None
        self.TargetHAdd = None
        self.TargetPAdd = None

    def decodeARP(self, trame):
        self.HType = trame[:4]
        self.PType = trame[4:8]
        self.HAddLen = trame[8:10]
        self.PAddLen = trame[10:12]
        self.OpCode = trame[12:16]
        self.SenderHAdd = trame[16:28]
        self.SenderPAdd = trame[28:36]
        self.TargetHAdd = trame[36:48]
        self.TargetPAdd = trame[48:]

    def printARP(self):
        print("------------------------------ARP---------------------------")
        if self.HType == "0001":
            print("Hardware type -> Ethernet (", self.HType, ")")
        else:
            print("Hardware type ->", self.HType)
        if self.PType == "0800":
            print("Protocole type -> IPv4 (", self.PType, ")")
        else:
            print("Protocole type ->", self.PType)
        print("Hardware Address Length ->", self.HAddLen)
        print("Protocol Address Length ->", self.PAddLen)
        if self.OpCode == "0001":
            print("OpCode -> ", "Request (", self.OpCode, ")")
        else:
            print("OpCode -> ", "Reply (", self.OpCode, ")")
        senderH = self.SenderHAdd[0:2]
        targetH = self.TargetHAdd[0:2]
        for i in range(2, len(self.SenderHAdd)):
            if i%2 == 0:
                senderH += ":"
                targetH += ":"
            senderH += self.SenderHAdd[i]
            targetH += self.TargetHAdd[i]
        senderP = str(int(self.SenderPAdd[0:2], base = 16))
        targetP = str(int(self.TargetPAdd[0:2], base = 16))
        stock_sender = ""
        stock_target = ""
        for i in range(2, len(self.SenderPAdd)):
            if i%2 == 0:
                if not (stock_sender == "" and stock_target == ""):
                    senderP = senderP + "." + str(int(stock_sender, base = 16))
                    targetP = targetP + "." + str(int(stock_target, base = 16))
                    stock_sender = ""
                    stock_target = ""
            stock_sender += self.SenderPAdd[i]
            stock_target += self.TargetPAdd[i]
        senderP = senderP + "." + str(int(stock_sender, base = 16))
        targetP = targetP + "." + str(int(stock_target, base = 16))
        print("Sender Mac Address ->", senderH)
        print("Sender IP Address ->", senderP)
        print("Target Mac Address ->", targetH)
        print("Target IP Address ->", targetP)
        print("------------------------------------------------------------\n")

class ICMP:
    def __init__(self):
        self.type = None
        self.code = None
        self.checksum = None
        self.id = None
        self.seqNum = None
        self.timestamp = None
        self.data = None

    def decodeICMP(self, trame):
        # reconnaît que des types echo request et echo reply
        self.type = trame[:2]
        self.code = trame[2:4]
        self.checksum = trame[4:8]
        self.id = trame[8:12]
        self.seqNum = trame[12:16]
        self.timestamp = trame[16:32]
        self.data = trame[32:]

    def printICMP(self):
        print("-----------------------------ICMP---------------------------")
        if self.type == "08":
            print("type -> ", self.type, "(Echo (ping) request)")
        if self.type == "00":
            print("type -> ", self.type, "(Echo (ping) reply)")
        print("code -> ", self.code)
        print("checksum -> ", self.checksum)
        print("id -> ", self.id, "(", str(int(self.id, base = 16)), ")")
        print("sequence number -> ", self.seqNum)
        print("timestamp -> ", self.timestamp)
        print("data -> ", self.data)
        print("------------------------------------------------------------\n")

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
        print("---------------------------TCP------------------------------")
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
        print("------------------------------------------------------------\n")

class HTTP:
    def __init__(self):
        self.string = None

    def decodeHTTP(self, string):
        self.string = bytes.fromhex(string).decode("ASCII").rstrip('\n')

    def printHTTP(self):
        if self.string != None:
            print("-----------------------------HTTP---------------------------")
            print(self.string)
            print("------------------------------------------------------------\n")