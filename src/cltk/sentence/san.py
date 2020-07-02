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


from cltk.sentence.sentence import BaseRegexSentenceTokenizer
from cltk.tokenizers.san import SanskritLanguageVars


class SanskritRegexSentenceTokenizer(BaseRegexSentenceTokenizer):
    """RegexSentenceTokenizer for Sanskrit."""

    def __init__(self: object):
        super().__init__(
            language="sanskrit", sent_end_chars=SanskritLanguageVars.sent_end_chars
        )
