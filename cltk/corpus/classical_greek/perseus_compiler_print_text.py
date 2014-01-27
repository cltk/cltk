import os
import re
import bleach
from cltk.corpus.classical_greek.replacer import Replacer

root = os.getcwd()
perseus_root = root + '/plaintext/perseus_greek/'
authors = os.listdir(perseus_root)

for author in authors:
    texts = os.listdir(perseus_root + author + '/opensource')
    for text in texts:
        text_match = re.match(r'.*_gk.xml', text)
        if text_match:
            gk_file = text_match.group()
            txt_file = perseus_root + author + '/opensource/' + gk_file
            with open(txt_file) as gk:
                html = gk.read()
                beta_code = bleach.clean(html, strip=True).upper()
                a_replacer = Replacer()
                unicode_converted = a_replacer.beta_code(beta_code)
                print(unicode_converted)
