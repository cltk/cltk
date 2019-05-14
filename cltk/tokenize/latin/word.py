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
    """
    PunktSentenceTokenizer trained on Latin
    """
    def __init__(self: object, language:str = 'latin', sent_tokenizer=SentenceTokenizer):
        """
        :param language : language for word tokenization
        :type language: str
        """
        super().__init__(language='latin')
        self.sent_tokenizer = sent_tokenizer()
        self._latin_replacements = latin_replacements

    def tokenize(self, text: str, split_enclitics:list = ['ne', 'n', 'que', 've', 'ue', 'st'],
                                  split_words:list = []):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        if self._latin_replacements:
            split_words = self._latin_replacements

        if split_words:
            text = self._replace_patterns(text, split_words)
        sents = self.sent_tokenizer.tokenize(text)
        if split_enclitics:
            sents = self._split_enclitics(sents, split_enclitics)
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

        enclitics_ = [enc for enc in enclitics if enc is not 'ne' and enc is not 'n']
        if len(enclitics_) > 1:
            if "que" in enclitics_ and 'ue' in enclitics_:
                enclitics_.remove('que')
                enclitics_.remove('ue')
                enclitics_.append('q?ue')
            enclitics_string = "|".join(enclitics_)
            enc_compile = re.compile(r'\b(?<!~)(\w+?)(%s)[%s]?\b'%(enclitics_string, re.escape(string.punctuation)))

        sent_tokens_ = []
        for sent in sents:
            for word in latin_exceptions:
                sent = re.sub(rf'\b{word}\b', self._matchcase(rf'~{word}~'), sent, flags=re.IGNORECASE)
            sent = " ".join(filter(None, ne_compile.split(sent)))
            sent = " ".join(filter(None, enc_compile.split(sent)))
            for enclitic in enclitics:
                if enclitic == 'st':
                    sent = sent.replace('u st ', 'us st ')
                    sent = re.sub(rf'[^%s]\b{enclitic}\b'%(exclude_flag), f' e{enclitic}', sent)
                elif enclitic == 'n':
                    sent = re.sub(rf'[^%s]\b{enclitic}\b'%(exclude_flag), f' -{enclitic}e', sent)
                else:
                    sent = re.sub(rf'[^%s]\b{enclitic}\b'%(exclude_flag), f' -{enclitic}', sent)
            sent = sent.replace('~','')
            sent_tokens_.append(" ".join(sent.split()))
        return sent_tokens_

    def _matchcase(self, word):
        # From Python Cookbook, p. 47
        def replace(m):
            text = m.group()
            if text.isupper():
                return word.upper()
            elif text.islower():
                return word.lower()
            elif text[0].isupper():
                return word.title()
            else:
                return word
        return replace

    def _replace_patterns(self, text: str, patterns: list):
        for pattern in patterns:
            text = re.sub(pattern[0], self._matchcase(pattern[1]), text, flags=re.IGNORECASE)
        return text
