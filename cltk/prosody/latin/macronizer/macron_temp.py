

dict = {}
with open("/Users/Tyler1/GitHub/cltk/cltk/prosody/latin/macronizer/macrons.txt") as file:
    for line in file:
        entry = line.split()
        head = entry[0]
        info = (entry[1], entry[2], entry[3])
        if head not in dict.keys():
            dict.update({head: [info]})
        else:
            dict.get(head).append(info)

#with open("/Users/Tyler1/GitHub/cltk/cltk/prosody/latin/macronizer/macrons.py", 'w') as f:
    f.write('vowel_len_map = {')
    for key, value in dict.items():
        f.write('\'%s\':%s,\n' % (key, value))
    f.write('}')

