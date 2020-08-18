"""Sentence tokenization for Sanskrit.

>>> from cltk.sentence.san import SanskritRegexSentenceTokenizer
>>> from cltk.languages.example_texts import get_example_text
>>> splitter = SanskritRegexSentenceTokenizer()
>>> sentences = splitter.tokenize(get_example_text("san"))
>>> sentences[1]
'तेन त्यक्तेन भुञ्जीथा मा गृधः कस्य स्विद्धनम् ॥'
>>> len(sentences)
12
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]
__license__ = "MIT License."


import string

from nltk.tokenize.punkt import PunktLanguageVars

from cltk.sentence.sentence import RegexSentenceTokenizer


class SanskritLanguageVars(PunktLanguageVars):
    sent_end_chars = ["\u0964", "\u0965", "\|", "\|\|"]


class SanskritRegexSentenceTokenizer(RegexSentenceTokenizer):
    """RegexSentenceTokenizer for Sanskrit."""

    def __init__(self: object):
        super().__init__(
            language="sanskrit", sent_end_chars=SanskritLanguageVars.sent_end_chars
        )
