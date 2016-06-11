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

def clean():
    os.remove("/Users/Tyler1/GitHub/cltk/cltk/prosody/latin/macronizer/macrons.py")

def create_dict():
    macrons = {}

    with open("/Users/Tyler1/GitHub/cltk/cltk/prosody/latin/macronizer/macrons.txt") as file:
        for line in file:
            entry = line.split()
            head = entry[0]
            macronized = macronize(entry[3])
            info = (entry[1], entry[2], macronized)
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

