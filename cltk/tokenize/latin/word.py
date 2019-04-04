""" Code for word tokenization: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
import re

from nltk.tokenize.treebank import TreebankWordTokenizer

from cltk.tokenize.word import BasePunktWordTokenizer
from cltk.tokenize.latin.params import ABBREVIATIONS, latin_exceptions, latin_replacements
from cltk.tokenize.latin.sentence import SentenceTokenizer

def WordTokenizer():
    return LatinPunktSentenceTokenizer()


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

    def tokenize(self, text: str, split_enclitics:bool = True, split_words:bool = True):
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
            sents = self._split_enclitics(sents)
        print(sents)
        tokenizer = TreebankWordTokenizer()
        return [item for sublist in tokenizer.tokenize_sents(sents) for item in sublist]

    def _split_enclitics(self:object, sents:list):
        sent_tokens_ = []
        for sent in sents:
            sent_tokens = sent.split()
            tokens_ = []
            if sent_tokens[0].endswith('ne') and sent_tokens[0] not in latin_exceptions:
                tokens_.extend([sent_tokens[0][:-2], '-ne'])
            elif sent_tokens[0].endswith('n') and sent_tokens[0] not in latin_exceptions:
                tokens_.extend([sent_tokens[0][:-1], '-ne'])
            else:
                for token in sent_tokens:
                    if token.endswith('que') and token not in latin_exceptions:
                        tokens_.extend([token[:-3], '-que'])
                    elif token.endswith('ve') and token not in latin_exceptions:
                        tokens_.extend([token[:-2], '-ve'])
                    elif token.endswith('ue') and token not in latin_exceptions:
                        tokens_.extend([token[:-2], '-ue'])
                    elif token.endswith('ust') and token not in latin_exceptions:
                        tokens_.extend([token[:-1], 'est'])
                    elif token.endswith('st') and token not in latin_exceptions:
                        tokens_.extend([token[:-2], 'est'])
                    else:
                        tokens_.append(token)
                sent_tokens_.append(" ".join(tokens_))
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
    text = """Haec si tecum, ita verumst ut dixi, patria loquatur, nonne impetrare debeat, etiamsi vim adhibere non possit? Quid, quod tu te ipse in custodiam dedisti, quod vitandae suspicionis causa ad M'. Lepidum te habitare velle dixisti? A quo non receptus etiam ad me venire ausus es atque, ut domi meae te adservarem, rogasti. Cum a me quoque id responsum tulisses, me nullo modo posse isdem parietibus tuto esse tecum, qui magno in periculo essem, quod isdem moenibus contineremur, ad Q. Metellum praetorem venisti. A quo repudiatus ad sodalem tuum, virum optumum, M. Metellum, demigrasti; quem tu videlicet et ad custodiendum diligentissimum et ad suspicandum sagacissimum et ad vindicandum fortissimum fore putasti. Sed quam longe videtur a carcere atque a vinculis abesse debere, qui se ipse iam dignum custodia iudicarit! """
    w = LatinPunktWordTokenizer()
    tokens = w.tokenize(text)
    for i, token in enumerate(tokens, 1):
        print(f'{i}: {token}')
    pass
