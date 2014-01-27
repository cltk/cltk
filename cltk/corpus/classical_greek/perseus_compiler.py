import os
import re
import bleach
from cltk.corpus.classical_greek.replacer import Replacer

root = os.getcwd()
perseus_root = root + '/plaintext/perseus_greek/'
#print(perseus_root)
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
                #print(unicode_converted)
                unicode_root = root + '/plaintext/perseus_unicode/'
                unic_pres = os.path.isdir(unicode_root)
                if unic_pres is True:
                    pass
                else:
                    os.mkdir(unicode_root)
                author_path = unicode_root + author
                author_path_pres = os.path.isdir(author_path)
                if author_path_pres is True:
                    pass
                else:
                    os.mkdir(author_path)
                gk_file_txt = os.path.splitext(gk_file)[0] + '.txt'
                uni_write = author_path + '/' + gk_file_txt
                print(uni_write)
                with open(uni_write, 'w') as uni_write:
                    uni_write.write(unicode_converted)
