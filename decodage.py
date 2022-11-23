#print(int("ff", base = 16))

def decode_trame(file):
    fichier = open(file, "r")
    string = fichier.read()
    list_trame = string.split("   ")
    for trame in list_trame:
        print("trame : " + trame)

def traiter_trame(trame):
    mac_dst = trame[0:17].replace(" ", ":")
    mac_src = trame[18:35].replace(" ", ":")
    print("src : " + mac_src)
    print("dst : " + mac_dst)


decode_trame("trame.txt")