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

                        c2 = Ethernet()
                        c2.decodeEth(str_trame[:28])
                        t.setC2(c2)

                        if c2.type == "0806": # si c'est un ARP
                            c3 = ARP()
                            c3.decodeARP(str_trame[28:])
                            t.setC3(c3)

                        elif c2.type == "0800": # si c'est un IPv4
                            c3 = IPv4()
                            fin_ip = (28+(2*int(str_trame[29], base = 16)*4))
                            c3.decodeIPv4(str_trame[28:fin_ip])
                            t.setC3(c3)

                            if c3.protocole == "01": # si c'est un ICMP
                                c3_2 = ICMP()
                                c3_2.decodeICMP(str_trame[fin_ip:])
                                t.setC4(c3_2)

                            elif c3.protocole == "06": # si c'est un TCP
                                c4 = TCP()
                                fin_tcp = fin_ip + (2*int(str_trame[fin_ip+24], base = 16)*4)
                                c4.decodeTCP(str_trame[fin_ip:fin_tcp])
                                t.setC4(c4)

                                if c4.port_dst == "0050" and str_trame[fin_tcp:] != "": # si c'est un HTTP non vide
                                    c7 = HTTP()
                                    c7.decodeHTTP(str_trame[fin_tcp:])
                                    #c7.printHTTP()
                                    t.setC7(c7)

                                elif c4.port_dst == "0016": # si c'est un ssh
                                    print("ssh n'est pas traitable encore")

                                else:
                                    print("protocole non traitable")
                            
                            elif c3.protocole == "11": # si c'est un UDP
                                c4 = UDP()
                                fin_udp = fin_ip + 16
                                c4.decodeUDP(str_trame[fin_ip:fin_udp])
                                t.setC4(c4)

                                if c4.port_dst == "0050" and str_trame[fin_tcp:] != "": # si c'est un HTTP non vide
                                    c7 = HTTP()
                                    c7.decodeHTTP(str_trame[fin_tcp:])
                                    t.setC7(c7)

                                elif c4.port_dst == "0016": # si c'est un ssh
                                    print("ssh n'est pas traitable encore")
                                
                                elif c4.port_dst == "0035": # si c'est un dns
                                    print("dns n'est pas traitable encore")

                                elif c4.port_dst == "0043" or c4.port_dst == "0044": # si c'est un dhcp
                                    print("dhcp n'est pas encore traitable")

                                else:
                                    print("couche 7 : non traitable")

                            else:
                                print("couche 4 : protocole non traitable")
                            
                        else:
                            print("couche 3 : type de trame non traitable")

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

                # vérification offset
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
    t = Trame()

    c2 = Ethernet()
    c2.decodeEth(str_trame[:28])
    t.setC2(c2)

    if c2.type == "0806": # si c'est un ARP
        c3 = ARP()
        c3.decodeARP(str_trame[28:])
        t.setC3(c3)

    elif c2.type == "0800": # si c'est un IPv4
        c3 = IPv4()
        fin_ip = (28+(2*int(str_trame[29], base = 16)*4))
        c3.decodeIPv4(str_trame[28:fin_ip])
        t.setC3(c3)

        if c3.protocole == "01": # si c'est un ICMP
            c3_2 = ICMP()
            c3_2.decodeICMP(str_trame[fin_ip:])
            t.setC4(c3_2)

        elif c3.protocole == "06": # si c'est un TCP
            c4 = TCP()
            fin_tcp = fin_ip + (2*int(str_trame[fin_ip+24], base = 16)*4)
            c4.decodeTCP(str_trame[fin_ip:fin_tcp])
            t.setC4(c4)

            if c4.port_dst == "0050" and str_trame[fin_tcp:] != "": # si c'est un HTTP non vide
                c7 = HTTP()
                c7.decodeHTTP(str_trame[fin_tcp:])
                #c7.printHTTP()
                t.setC7(c7)

            elif c4.port_dst == "0016": # si c'est un ssh
                print("ssh n'est pas traitable encore")

            else:
                print("protocole non traitable")
        
        elif c3.protocole == "11": # si c'est un UDP
            c4 = UDP()
            fin_udp = fin_ip + 16
            c4.decodeUDP(str_trame[fin_ip:fin_udp])
            t.setC4(c4)

            if c4.port_dst == "0050" and str_trame[fin_tcp:] != "": # si c'est un HTTP non vide
                c7 = HTTP()
                c7.decodeHTTP(str_trame[fin_tcp:])
                t.setC7(c7)

            elif c4.port_dst == "0016": # si c'est un ssh
                print("ssh n'est pas traitable encore")
            
            elif c4.port_dst == "0035": # si c'est un dns
                print("dns n'est pas traitable encore")

            elif c4.port_dst == "0043" or c4.port_dst == "0044": # si c'est un dhcp
                print("dhcp n'est pas encore traitable")

            else:
                print("couche 7 : non traitable")

        else:
            print("couche 4 : protocole non traitable")
        
    else:
        print("couche 3 : type de trame non traitable")

    list_trame.append(t)

    return list_trame

def check_ascii(str):
    for c in str:
        if c not in string.hexdigits: # si c n'est pas un hex
            return False
    return True

#list_trame = decode_trame("./Trame/TCP.txt")
#list_trame = decode_trame("./Trame/TCP_2.txt")
#list_trame = decode_trame("./Trame/ICMP.txt")
#list_trame = decode_trame("./Trame/ARP.txt")
list_trame = decode_trame("./Trame/UDP.txt")
for trame in list_trame:
    trame.printTrame()