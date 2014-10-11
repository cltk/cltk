import bs4
from cltk.corpus_api.greek.beta_to_unicode import Replacer



class TEIDoc(object):
    def __init__(self, path):
        self.path = path
        self.beta_replacer = Replacer()

    @property
    def soup(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            xml_data = f.read()
        return bs4.BeautifulSoup(xml_data)

    @property
    def struct_tags(self):
        struct_info = self.soup.find('encodingdesc')
        structs = struct_info.find_all('refsdecl')
        return [c.attrs.values() for s in structs
                for c in s.contents
                if c.name]

    def tags(self, text_only=False):
        if text_only:
            tags = self.soup.find('text').find_all(True)
        else:
            tags = self.soup.find_all(True)
        tag_names = [x.name for x in tags if x.name]
        return list(set(tag_names))


class TXTDoc(object):
    def __init__(self, path):
        self.path = path
        self.beta_replacer = Replacer()
