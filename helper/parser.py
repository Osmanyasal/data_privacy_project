# -*- coding: utf-8 -*-

from helper.anonymization import AnonymizationTypes 

def parse(argv):
    dic = {
        "is_tabular":True, ## default
        "dgh_folder":"./test/iris/DGHs",
        "dataset":"./test/iris/Iris.csv",
        #"testset":None,
        "data_propotion":None,
        "test_propotion":None,
        "ml_methods":"all", ## 
        "anonymization":AnonymizationTypes.get_type("all"), ## clustering, bottomup, kanonymity, random, DP
        "start_k":3, ## default
        "end_k":5, ## default
        "start_sens":None,
        "end_sens":None,
        "start_eps":None,
        "end_eps":None,
        "number":None,
        "seed":0
        }
    prev_i = ""
    is_first = True
    for i in argv:
        if is_first:
            is_first = False
        elif i[2:] in dic.keys():
            prev_i = i[2:]   #.replace("--","")
        else:
            if prev_i == "anonymization":
                dic[prev_i] = [AnonymizationTypes.get_type(i)]
            elif prev_i == "is_tabular":
                dic[prev_i] = i.lower().capitalize() == "True"
            elif prev_i.endswith("_k") or  prev_i == "number":
                dic[prev_i] = int(i)
            elif prev_i.endswith("_eps") or prev_i.endswith("_sens"):
                dic[prev_i] = float(i)
            else:
                dic[prev_i] = i
    return dic


#print(parse("--is_tabular False --end_k 321 --anonymization random".split()))