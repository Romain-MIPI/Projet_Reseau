from Trame import *
import string

def decode_trame(file):
    fichier = open(file, "r")
    str_trame = ""
    offset = ""
    offset_total = 0
    trame = ""
    list_trame = []
    for ligne in fichier.readlines():
        if ligne != '\n':
            tab = ligne.split('   ')
            offset = tab[0]
            trame = tab[1].rstrip('\n').replace(" ", "")
            if check_ascii(trame): # si la trame contient bien que des hex
                if offset == "0000": # si c'est un début d'un trame
                    if str_trame != "": # si ce n'est la premiere trame
                        #traitement trame
                        #print(str_trame)
                        eth = Ethernet()
                        eth.decodeEth(str_trame[:28])
                        #print(str_trame[:28])
                        #eth.printEth()

                        ip = IPv4()
                        fin_ip = (28+(2*int(str_trame[29], base = 16)*4))
                        #print(str_trame[28:fin_ip])
                        ip.decodeIPv4(str_trame[28:fin_ip])
                        #ip.printIPv4()

                        tcp = TCP()
                        fin_tcp = fin_ip+(2*int(str_trame[fin_ip+24], base = 16)*4)
                        #print(str_trame[fin_ip:fin_tcp])
                        tcp.decodeTCP(str_trame[fin_ip:fin_tcp])
                        #tcp.printTPC()

                        http = HTTP()
                        http.decodeHTTP(str_trame[fin_tcp:])
                        #http.printHTTP()

                        t = Trame()
                        t.setEth(eth)
                        t.setIP(ip)
                        t.setTCP(tcp)
                        t.setHTTP(http)
                        list_trame.append(t)

                        #lecture trame suivant
                        str_trame = trame
                        offset_total = 0
                    else :
                        # lecture premiere trame
                        str_trame = trame
                else:
                    # offset n'est pas 0000 donc on continue de lire
                    str_trame += trame
                if int(offset, base = 16) != offset_total:
                    print("offset non compatible avec la trame")
                    exit()
                else:
                    offset_total += int(len(trame)/2)
            else:
                print(trame)
                print("trame non compatible")
                exit()
            
    #traitement derniere trame
    if int(offset, base = 16) != int(offset_total - len(trame)/2): # - len(trame)/2 pour qu'il compte pas les octets de la derniere ligne
        print("offset non compatible avec la trame")
        exit()
    else:
        offset_total += int(len(trame)/2)

        #print(str_trame)
        #print(str_trame[:28])
        eth = Ethernet()
        eth.decodeEth(str_trame[:28])
        #eth.printEth()

        ip = IPv4()
        #print("hlen = ", int(str_trame[29], base = 16)*4)
        fin_ip = (28+(2*int(str_trame[29], base = 16))*4)
        #print(fin_ip)
        #print(str_trame[28:fin_ip])
        ip.decodeIPv4(str_trame[28:fin_ip])
        #ip.printIPv4()

        tcp = TCP()
        #print(str_trame[fin_ip+24])
        fin_tcp = fin_ip+(2*int(str_trame[fin_ip+24], base = 16)*4)
        #print(str_trame[fin_ip:fin_tcp])
        tcp.decodeTCP(str_trame[fin_ip:fin_tcp])
        #tcp.printTPC()

        http = HTTP()
        http.decodeHTTP(str_trame[fin_tcp:])
        #http.printHTTP()

        t = Trame()
        t.setEth(eth)
        t.setIP(ip)
        t.setTCP(tcp)
        t.setHTTP(http)
        list_trame.append(t)

    return list_trame

def check_ascii(str):
    for c in str:
        if c not in string.hexdigits: # si c n'est pas un hex
            return False
    return True

list_trame = decode_trame("TCP_2.txt")
for trame in list_trame:
    trame.eth.printEth()
    trame.ip.printIPv4()
    trame.tcp.printTPC()
    trame.http.printHTTP()
