# -*- coding: utf-8 -*-


def parse(argv):
    dic = {}
    prev_i = ""
    for i in argv:
        if i.startswith("-") or i.startswith("--"):
            dic[i] = ""
            prev_i = i
        else:
            dic[prev_i] = i
            
        
    return dic
    