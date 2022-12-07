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
                        t = Trame()

                        #print(str_trame)
                        c2 = Ethernet()
                        c2.decodeEth(str_trame[:28])
                        #print(str_trame[:28])
                        #c2.printEth()
                        t.setC2(c2)

                        if c2.type == "0806": # si c'est un ARP
                            c3 = ARP()
                            c3.decodeARP(str_trame[28:])
                            t.setC3(c3)

                        if c2.type == "0800": # si c'est un IPv4
                            c3 = IPv4()
                            fin_ip = (28+(2*int(str_trame[29], base = 16)*4))
                            #print(str_trame[28:fin_ip])
                            c3.decodeIPv4(str_trame[28:fin_ip])
                            #c3.printIPv4()
                            t.setC3(c3)

                            if c3.protocole == "01": # si c'est un ICMP
                                c3_2 = ICMP()
                                c3_2.decodeICMP(str_trame[fin_ip:])
                                t.setC4(c3_2)

                            if c3.protocole == "06": # si c'est un TCP
                                c4 = TCP()
                                fin_tcp = fin_ip+(2*int(str_trame[fin_ip+24], base = 16)*4)
                                #print(str_trame[fin_ip:fin_tcp])
                                c4.decodeTCP(str_trame[fin_ip:fin_tcp])
                                #c4.printTPC()
                                t.setC4(c4)

                                if c4.port_dst == "0050" and str_trame[fin_tcp:] != "": # si c'est un HTTP
                                    c7 = HTTP()
                                    c7.decodeHTTP(str_trame[fin_tcp:])
                                    #c7.printHTTP()
                                    t.setC7(c7)

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
    #if int(offset, base = 16) != int(offset_total - len(trame)/2): # - len(trame)/2 pour qu'il compte pas les octets de la derniere ligne
        #print("offset non compatible avec la trame")
        #exit()
    #else:
        #offset_total += int(len(trame)/2)

    t = Trame()

    c2 = Ethernet()
    c2.decodeEth(str_trame[:28])
    #print(str_trame[:28])
    #c2.printEth()
    t.setC2(c2)

    if c2.type == "0806": # si c'est un ARP
        c3 = ARP()
        c3.decodeARP(str_trame[28:])
        t.setC3(c3)

    if c2.type == "0800": # si c'est un IPv4
        c3 = IPv4()
        fin_ip = (28+(2*int(str_trame[29], base = 16)*4))
        #print(str_trame[28:fin_ip])
        c3.decodeIPv4(str_trame[28:fin_ip])
        #c3.printIPv4()
        t.setC3(c3)

        if c3.protocole == "01": # si c'est un ICMP
            c3_2 = ICMP()
            c3_2.decodeICMP(str_trame[fin_ip:])
            t.setC4(c3_2)

        if c3.protocole == "06": # si c'est un TCP
            c4 = TCP()
            fin_tcp = fin_ip+(2*int(str_trame[fin_ip+24], base = 16)*4)
            #print(str_trame[fin_ip:fin_tcp])
            c4.decodeTCP(str_trame[fin_ip:fin_tcp])
            #c4.printTPC()
            t.setC4(c4)

            if c4.port_dst == "0050" and str_trame[fin_tcp:] != "": # si c'est un HTTP
                print("ici : ", str_trame[fin_tcp:], "fin")
                c7 = HTTP()
                c7.decodeHTTP(str_trame[fin_tcp:])
                #c7.printHTTP()
                t.setC7(c7)

    list_trame.append(t)

    return list_trame

def check_ascii(str):
    for c in str:
        if c not in string.hexdigits: # si c n'est pas un hex
            return False
    return True

#list_trame = decode_trame("TCP.txt")
#list_trame = decode_trame("TCP_2.txt")
#list_trame = decode_trame("ICMP.txt")
#list_trame = decode_trame("ARP.txt")
#for trame in list_trame:
#    trame.printTrame()
