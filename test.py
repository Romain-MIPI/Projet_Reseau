import re

def read_trame(path="trame.txt"):
    f = open(path, "rb")
    raw_data = b""
    for line in f.readlines():
        raw_data += line
    raw_data_decoded = raw_data.decode('utf8')

    global trame_dict
    trame_dict = {}
    count = 0
    trame = []
    if re.search("\r\n", raw_data_decoded) is not None:
        input = raw_data_decoded.split("\r\n")
    else: 
        input = raw_data_decoded.split("\n")

    for i in input:
        if i != "":
            j = i.split("   ")
            k = j[0].split("  ")
            
            try:
                index = int(k[0], 16)
                data = k[1]
                if index == 0: 
                    if trame != []:
                        trame_dict[count] = trame
                        count += 1
                    trame = []
                [trame.append(i[j]) for i in data.split(" ") for j in [0,1]]
            except(ValueError):
                print("Error ignored")
    return trame_dict

def bytes_to_mac_adress(bytestring):
    return ":".join(["" + str(bytestring[i])+str(bytestring[i+1]) if i < len(bytestring)-1 or len(bytestring)%2 == 0 else "" + str(bytestring[i]) for i in range(0, len(bytestring), 2)])

read_trame()
src = trame_dict[2][0:12]
print(bytes_to_mac_adress(src))