""" Code for word tokenization: Sanskrit
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Anoop Kunchukuttan']
__license__ = 'MIT License.'

import string
import re

from cltk.tokenize.word import BaseRegexWordTokenizer

def WordTokenizer():
    return SanskritRegexSentenceTokenizer()


class SanskritRegexSentenceTokenizer(BaseRegexWordTokenizer):
    """
    """

    def __init__(self: object, language:str = 'sanskrit', patterns=None):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.patterns = patterns
        super().__init__(language=language, patterns=self.patterns)

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        modified_punctuations = string.punctuation.replace("|", "")
        indian_punctuation_pattern = re.compile('([' + modified_punctuations + '\u0964\u0965' + ']|\|+)')
        tok_str = indian_punctuation_pattern.sub(r' \1 ', text.replace('\t', ' '))
        return re.sub(r'[ ]+', u' ', tok_str).strip(' ').split(' ')

if __name__ == "__main__":
    text = text = "श्री भगवानुवाच पश्य मे पार्थ रूपाणि शतशोऽथ सहस्रशः। नानाविधानि दिव्यानि नानावर्णाकृतीनि च।।"
    t = SanskritRegexSentenceTokenizer()
    tokens = t.tokenize(text)
    for i, token in enumerate(tokens, 1):
        print(f'{i}: {token}')
