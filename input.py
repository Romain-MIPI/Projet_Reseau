from Trame import *

def decode_trame(file):
    fichier = open(file, "r")
    str_trame = ""
    offset = ""
    trame = ""
    for ligne in fichier.readlines():
        if ligne != '\n':
            tab = ligne.split('   ')
            offset = tab[0]
            trame = tab[1]
            if offset == "0000":
                if str_trame != "":
                    print(str_trame)
                    eth = Ethernet()
                    eth.decodeEth(str_trame[:28])
                    print(str_trame[:28])
                    eth.printEth()

                    ip = IPv4()
                    fin_ip = (28+(2*int(str_trame[29])*4))
                    print(str_trame[28:fin_ip])
                    ip.decodeIPv4(str_trame[28:fin_ip])
                    ip.printIPv4()
                    str_trame = trame.rstrip('\n').replace(" ", "")
                else :
                    str_trame += trame.rstrip('\n').replace(" ", "")
            else:
                str_trame += trame.rstrip('\n').replace(" ", "")
    print(str_trame)
    print(str_trame[:28])
    eth = Ethernet()
    eth.decodeEth(str_trame[:28])
    eth.printEth()

    ip = IPv4()
    print("hlen = ", int(str_trame[29])*4)
    fin_ip = (28+(2*int(str_trame[29]))*4)
    print(fin_ip)
    print(str_trame[28:fin_ip])
    ip.decodeIPv4(str_trame[28:fin_ip])
    ip.printIPv4()

decode_trame("TCP.txt")