""" Code for sentence tokenization: Sanskrit
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
import re

from cltk.tokenize.sentence import BaseSentenceTokenizer, BaseRegexSentenceTokenizer
from cltk.tokenize.sanskrit.params import SanskritLanguageVars

from nltk.tokenize.punkt import PunktLanguageVars

def SentenceTokenizer(tokenizer: str = 'regex'):
    if tokenizer=='regex':
        return GreekRegexSentenceTokenizer()


class SanskritRegexSentenceTokenizer(BaseRegexSentenceTokenizer):
    """ RegexSentenceTokenizer for Sanskrit
    """
    def __init__(self: object):
        super().__init__(language='sanskrit',
            sent_end_chars=SanskritLanguageVars.sent_end_chars)


if __name__ == '__main__':
    text = """श्री भगवानुवाच भूय एव महाबाहो श्रृणु मे परमं वचः। यत्तेऽहं प्रीयमाणाय वक्ष्यामि हितकाम्यया।।
न मे विदुः सुरगणाः प्रभवं न महर्षयः। अहमादिर्हि देवानां महर्षीणां च सर्वशः।।
यो मामजमनादिं च वेत्ति लोकमहेश्वरम्। असम्मूढः स मर्त्येषु सर्वपापैः प्रमुच्यते।।
बुद्धिर्ज्ञानमसंमोहः क्षमा सत्यं दमः शमः। सुखं दुःखं भवोऽभावो भयं चाभयमेव च।।"""

    t = SanskritRegexSentenceTokenizer()
    sents = t.tokenize(text)
    for i, sent in enumerate(sents, 1):
        print(f'{i}: {sent}')
