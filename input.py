#print(int("ff", base = 16))

def decode_trame(file):
    fichier = open(file, "r")
    string = fichier.read()
    list_trame = string.split("   ")
    for trame in list_trame:
        print("trame : " + trame)
        traiter_trame(trame)

def traiter_trame(trame):
    mac_dst = trame[0:17].replace(" ", ":")
    mac_src = trame[18:35].replace(" ", ":")
    print("src : " + mac_src)
    print("dst : " + mac_dst)
    trame_type = trame[36:41].replace(" ", "")
    version = trame[42]
    hlen = trame[43]
    if trame_type == "0800":
        print("type : IPv" + version + " (0x" + trame_type + ")")
    else :
        print("version = " + version)
    print("header length : " + str(int(hlen, base=16)*4) + " bytes (" + hlen + ")")


decode_trame("trame.txt")