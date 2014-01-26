import os
import re

root = os.getcwd()

perseus_root = root + '/plaintext/perseus_greek/'

authors = os.listdir(perseus_root)

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

for author in authors:
    texts = os.listdir(perseus_root + author + '/opensource')
    for text in texts:
        text_match = re.match(r'.*_gk.xml', text)
        if text_match:
            gk_file = text_match.group()
            txt_file = perseus_root + author + '/opensource/' + gk_file
            with open(txt_file) as gk:
                html = gk.read()
                print(strip_tags(html))
