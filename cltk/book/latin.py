"""CLTK 'book', i.e. demo texts modelled after the nltk.book function."""

__author__ = 'Patrick J. Burns <patrick@diyclassics.org>'
__license__ = 'MIT License. See LICENSE.'

from nltk.text import Text

from cltk.corpus.latin.readers import get_latin_library_reader


class LatinSetup(object):
    def __init__(self):
        print("*** Introductory Examples for testing CLTK Latin ***")
        print("Loading text1, ..., text3 and sent1, ..., sent3")
        print("Type the name of the text or sentence to view it, e.g. Latin.text1 or Latin.sent2.")
        print("Type: 'Latin.texts()' or 'Latin.sents()' to list the materials.")

        latinlibrary = get_latin_library_reader()

        text1_source = [file for file in latinlibrary.fileids() if 'cicero/cat' in file]
        self.text1 = Text(latinlibrary.words(text1_source), name='Cicero, In Catilinam')
        print("Latin.text1:", self.text1.name)

        text2_source = [file for file in latinlibrary.fileids() if 'sen/seneca.ep' in file]
        self.text2 = Text(latinlibrary.words(text2_source), name='Seneca, Epistulae Morales')
        print("Latin.text2:", self.text2.name)

        self.text3 = Text(latinlibrary.words('bible/genesis.txt'), name='Biblia Sacra, Genesis')
        print("Latin.text3:", self.text3.name)

        # 4 ???
        # print("text4:", self.text4.name)

        self.sent1 = ['Quo', 'usque', 'tandem', 'abutere', ',', 'Catilina', ',', 'patientia', 'nostra', '?']
        self.sent2 = ['Ita', 'fac', ',', 'mi', 'Lucili', ':', 'vindica', 'te', 'tibi,', 'et', 'tempus', 'quod', 'adhuc',
                      'aut', 'auferebatur', 'aut', 'subripiebatur', 'aut', 'excidebat', 'collige', 'et', 'serva', '.']
        self.sent3 = ['In', 'principio', 'creavit', 'Deus', 'caelum', 'et', 'terram', '.']

    def texts(self):
        print("Latin.text1:", self.text1.name)
        print("Latin.text2:", self.text2.name)
        print("Latin.text3:", self.text3.name)
        # print("text4:", self.text4.name)

    def sents(self):
        print("Latin.sent1:", " ".join(self.sent1))
        print("Latin.sent2:", " ".join(self.sent2))
        print("Latin.sent3:", " ".join(self.sent3))
        # print("sent4:", " ".join(self.sent4))


if __name__ == '__main__':
    latinlibrary = get_latin_library_reader()
    print(latinlibrary)

    l = LatinSetup()
    l.texts()
    l.sents()


