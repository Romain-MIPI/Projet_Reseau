import eel
import os
import re
import input



path = os.path.abspath(os.path.join(os.curdir, 'web'))
print(path)
eel.init(path)

list_trame = input.decode_trame("./Trame/TCP_2.txt") + input.decode_trame("./Trame/TCP.txt")

@eel.expose
def load_data(filters):
    #filters: 

    #call backend functions
    ip = [["1.23.34", "jkj"], ["xfs", "klj"]]

    return ip

@eel.expose
def double():
    #if "i" not in vars():
    j = eel.load_a()()
    return 2*j



@eel.expose
def validate_filter():
    filter = eel.check_if_filter()()
    if filter == 0:
        return 1
    if sort_filter(split_filter(filter)) == 0:
        return 0
    else: 
        return 1

@eel.expose
def filter_output():
    i = eel.pass_i()()
    if i >= len(list_trame):
        return "end_of_list"
    trame = list_trame[i]
    filter = eel.check_if_filter()()
   
    if filter == 0:
        return dict_from_trame(trame)
    else:
       
        f = sort_filter(split_filter(filter)) 
        d = dict_from_trame(trame)
        for couche in d.keys():
            if f[couche] == {"*":"*"}: 
                for i in range(len(d[couche].keys())):
                    if d[couche][list(d[couche].keys())[i]] is None: 
                        print("first out")
                        return 0
            else:          
                for specifier in f[couche].keys(): 
                    if f[couche] == {}: 
                            pass
                    
                    else: 
                            if specifier not in d[couche].keys():
                                print("second out")
                                return 0

                            if (re.search("src", specifier) is not None) or (re.search("dst", specifier) is not None): #specifier == src/dst: if filter is ip, then src and dst must exist 
                                for i in f[couche][specifier]:
                                    if re.search("both", i) is not None:
                                        if ("both"+d[couche]['src'][0] == i) or ("both" + d[couche]['dst'][0] == i):
                                            pass
                                        else:
                                            print("third out")
                                            return 0
                                    else: 
                                        if i not in d[couche][specifier]:
                                            print("six out")
                                            return 0
                                    
                            else: 
                                if d[couche][specifier] not in f[couche][specifier]:
                                    print("fourth out")
                                    return 0
                      
        print("-------------------\nAfter filter: ", d) 
        return d
        
    
def dict_from_trame(trame):
    c = Modify_Data()
    def get_tcp_types():
        print(trame.tcp.option_value)
        res = []
        ref = ["URG", "ACK", "PSH", "RST", "SYN", "FIN"]
        calls = [trame.tcp.URG, trame.tcp.ACK, trame.tcp.PSH, trame.tcp.RST, trame.tcp.SYN, trame.tcp.FIN]
        for i in range(len(ref)):
            if int(calls[i]) == 1:
                res.append(ref[i])
        return res
    d = {"ip":{
            "src":[c.ip_to_str(trame.ip.dst_ip)],
            "dst":[c.ip_to_str(trame.ip.src_ip)]
            }, 
        "tcp":{
            "src":[str(int(trame.tcp.port_dst, base=16))],
            "dst":[str(int(trame.tcp.port_src, base=16))],
            "seq_num":[str(int(trame.tcp.seq_num, base=16))],
            "ack_num":[str(int(trame.tcp.ack_num, base = 16))],
            "type":[get_tcp_types()]
            },
        "http":{
            
            "comm":[trame.http.string]
            },
        }
    
    return d

 
    



class Modify_Data:
    #Used to modify datatypes to get the output type

    def ip_to_str(self, input):
        output = ""
        for i in range(0, len(input), 2):
            if i != 0: 
                output += "."
            output += str(int(input[i:i+2], base= 16))
        return output


def split_filter(filterstring):
    def rem(input):
        if input == "": 
            return None 
        return input
        
    filter = []
    if re.search("&&", filterstring) is not None:
        fc = filterstring.split("&&")
    else: 
        fc = [filterstring]
    for f in fc:
        couche = None
        specifier = None
        valeur = None
        if re.search("==", f) is None:
            couche = f.strip()
        else: 
            f_split = f.split("==")
            if ("" == f_split[0].strip()) or ("" == f_split[1].strip()) or (len(f_split) > 2): 
                return 0

            if re.search(r"\.", f_split[0]) is None:
                couche = f_split[0].strip()
            else: 
                if ("" == f_split[0].strip()) or ("" == f_split[1].strip()) or (len(f_split) > 2): 
                    return 0
                f_split_split = f_split[0].split(".")
                couche = f_split_split[0].strip()
                specifier = f_split_split[1].strip()
            valeur = f_split[1].strip()
        filter.append((rem(couche), rem(specifier), rem(valeur)))
    return filter

def sort_filter(filter):

    filtres = {"ip":{}, "tcp":{}, "http":{}}

    ref_vals = {"ip": ["dst", "src"], 
                "tcp": ["dst", "src"],
                "http": []}

    def sous_filtre(kw, f):
        if f[1] is None:
            if f[2] is None: # - -
                filtres[kw]["*"] = "*"
            else: # - X
                if "*" in filtres[kw].keys(): 
                    del filtres[kw]["*"]
                for i in ref_vals[kw]: 
                    if i in filtres[kw]:
                        
                        filtres[kw][i].append("both" + f[2])
                    else:
                        filtres[kw][i] = ["both" + f[2]]
        elif f[1] is not None:
            if f[2] is None: 
                return 0 # X -
            else: # X X
                if "*" in filtres[kw].keys(): 
                    del filtres[kw]["*"]
                if f[1] in filtres[kw]:
                        filtres[kw][f[1]].append(f[2])
                else:
                    filtres[kw][f[1]] = [f[2]]
        return 1

    
    if filter == 0: 
        return 0
    if len(filter) == 0: 
        return 0
    for seul_filtre in filter:
        try:
            c = sous_filtre(seul_filtre[0], seul_filtre)
        except KeyError:
            return 0
        if c == 0: 
            return 0
    return filtres


@eel.expose
def save_to_file(): 
    count = eel.pass_file_count()()
    data = eel.pass_output_strings()()
    data_split = data.split("_end_of_line,")
    print(data_split)
    for i in range(len(data_split)): 
        pass
        data_split[i] = data_split[i].replace("_end_of_line", "")
    with open('output' + str(count), 'w') as fw:
        for i in data_split:
            fw.write(i)
            fw.write("\n\n\n")

    












eel.start("index.html", mode = "default")
