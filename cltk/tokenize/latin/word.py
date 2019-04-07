""" Code for word tokenization: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import re

from nltk.tokenize.treebank import TreebankWordTokenizer

from cltk.tokenize.word import BasePunktWordTokenizer
from cltk.tokenize.latin.params import ABBREVIATIONS, latin_exceptions, latin_replacements
from cltk.tokenize.latin.sentence import SentenceTokenizer

def WordTokenizer():
    return LatinPunktWordTokenizer()

class LatinPunktWordTokenizer(BasePunktWordTokenizer):
    """ PunktSentenceTokenizer trained on Latin
    """

    def __init__(self: object, language:str = 'latin', sent_tokenizer=SentenceTokenizer):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        super().__init__(language='latin')
        self.sent_tokenizer = sent_tokenizer()

    def tokenize(self, text: str, split_enclitics:list = ['ne', 'n', 'que', 've', 'ue', 'st'], split_words:bool = True):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        if split_words:
            text = self._replace_patterns(text, latin_replacements)
        sents = self.sent_tokenizer.tokenize(text)
        if split_enclitics:
            sents = self._split_enclitics(sents, split_enclitics)
        # print(sents)
        tokenizer = TreebankWordTokenizer()
        return [item for sublist in tokenizer.tokenize_sents(sents) for item in sublist]

    def _split_enclitics(self:object, sents:list, enclitics: list):
        import string
        exclude_flag = '~'
        if 'ne' in enclitics and 'n' in enclitics:
            ne_compile = re.compile(r'^\b(\w+?)([n]e?)[%s]?\b'%re.escape(string.punctuation))
        elif 'ne' in enclitics:
            ne_compile = re.compile(r'^\b(\w+?)(ne)[%s]?\b'%re.escape(string.punctuation))
        elif 'n' in enclitics:
            ne_compile = re.compile(r'^\b(\w+?)(n)[%s]?\b'%re.escape(string.punctuation))

        enclitics = [enc for enc in enclitics if enc is not 'ne' and enc is not 'n']
        if len(enclitics) > 1:
            if "que" in enclitics and 'ue' in enclitics:
                enclitics.remove('que')
                enclitics.remove('ue')
                enclitics.append('q?ue')
            enclitics_ = "|".join(enclitics)
            print(enclitics_)
            enc_compile = re.compile(r'[^%s]\b(\w+?)(%s)[%s]?\b'%(exclude_flag, enclitics_, re.escape(string.punctuation)))

        sent_tokens_ = []
        for sent in sents:
            for word in latin_exceptions:
                sent = sent.replace(f' {word} ', f' ~{word}~ ')
            sent = " ".join(filter(None, ne_compile.split(sent)))
            sent = " ".join(filter(None, enc_compile.split(sent)))
            sent = sent.replace('~', '')
            sent_tokens_.append(sent)
        return sent_tokens_

    def _matchcase(self, word):
        # From Python Cookbook
        def replace(m):
            text = m.group()
            if text.isupper():
                return word.upper()
            elif text.islower():
                return word.lower()
            elif text[0].isupper():
                return word.capitalize()
            else:
                return word
        return replace

    def _replace_patterns(self, text: str, patterns: list):
        for pattern in patterns:
            text = re.sub(pattern[0], self._matchcase(pattern[1]), text, flags=re.IGNORECASE)
        return text

if __name__ == '__main__':
    text = """Hocne verumst, totane teque ferri, Cynthia, Roma, quoque et nonve ignotaue vivere nequitia?"""
    w = LatinPunktWordTokenizer()
    tokens = w.tokenize(text)
    for i, token in enumerate(tokens, 1):
        print(f'{i}: {token}')
    pass
