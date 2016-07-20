"""
Script for making a python dictionary, called vowel_len_map, in macrons.py
"""

import os
import re

def macronize(word):
    rep = {
        "a_": "ā",
        "e_": "ē",
        "i_": "ī",
        "o_": "ō",
        "u_": "ū"
    }
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    macronized = pattern.sub(lambda m: rep[re.escape(m.group(0))], word)
    return macronized

def correct_tag(tag):
    rep = {
        "v-prppnn-": "t-prppnn-",
        "v-prppmn-": "t-prppmn-",
        "v-srppmn-": "t-srppmn-",
        "v-srppfn-": "t-srppfn-",
        "v-prppma-": "t-prppma-",
        "v-srppnn-": "t-srppnn-",
        "v-srppfb-": "t-srppfb-",
        "v-spgpng-": "t-spgpng-",
        "v-sfpama-": "t-sfpama-",
        "v-prppfb-": "t-prppfb-",
        "v-spdana-": "t-spdana-",
        "v-spgpma-": "t-spgpma-",
        "v-srppnb-": "t-srppnb-",
        "v-spgpnb-": "t-spgpnb-",
        "v-prppmb-": "t-prppmb-",
        "m-p---fn-": "m--------",
        "m-p---fa-": "m--------",
        "m-p---fm-": "m--------",
        "m-p---mn-": "m--------",
    }
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    tag = pattern.sub(lambda m: rep[re.escape(m.group(0))], tag)
    return tag

def clean():
    os.remove("/Users/Tyler1/GitHub/cltk/cltk/prosody/latin/macronizer/macrons.py")

def create_dict():
    macrons = {}

    with open("/Users/Tyler1/GitHub/cltk/cltk/prosody/latin/macronizer/macrons.txt") as file:
        for line in file:
            entry = line.split()
            head = entry[0]
            macronized = macronize(entry[3])
            info = (correct_tag(entry[1]), entry[2], macronized)
            if head not in macrons.keys():
                macrons.update({head: [info]})
            else:
                macrons.get(head).append(info)
    return macrons

def write_dict():
    with open("/Users/Tyler1/GitHub/cltk/cltk/prosody/latin/macronizer/macrons.py", 'w+') as file:
        file.write('vowel_len_map = {')
        for key, value in create_dict().items():
            file.write('\'%s\':%s,\n' % (key, value))
        file.write('}')

clean()
write_dict()

