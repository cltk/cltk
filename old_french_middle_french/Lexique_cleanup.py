from __future__ import print_function
#encoding: utf-8

import re
import os, sys


with open('lexiquedelancienfrancais.txt', 'r') as in_file:
       stripped = (line.strip() for line in in_file)
## removes additional commas
       for stripped in stripped:
              entry, PoS, definition_sce = stripped.split(',', 2)
              definition = definition_sce.replace(',','')
## adds lemma number for non-pre-existing lemma numbers
              if not entry[0].isdigit():
                  entry = " ".join(("1.", entry))
              entry = entry.replace('1.','1.,')
              entry = entry.replace('2.', '2.,')
              entry = entry.replace('3.', '3.,')
              entry = entry.replace('*', '')

              entries = (entry, PoS, definition)
              output = ",".join(entries)
              with open("lex.txt", "a") as text_file:
                  text_file.write(output +"\n")
                  text_file.close()
              print(output)






