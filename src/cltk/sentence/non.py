"""Code for sentences tokenization: Old Norse.

Sentence tokenization for Old Norse is available using a regular-expression based tokenizer.

>>> from cltk.sentence.non import OldNorseRegexSentenceTokenizer
>>> from cltk.languages.example_texts import get_example_text
>>> splitter = OldNorseRegexSentenceTokenizer()
>>> sentences = splitter.tokenize(get_example_text("non"))
>>> sentences[:2]
['Gylfi konungr réð þar löndum er nú heitir Svíþjóð.', 'Frá honum er þat sagt at hann gaf einni farandi konu at launum skemmtunar sinnar eitt plógsland í ríki sínu þat er fjórir öxn drægi upp dag ok nótt.']
>>> len(sentences)
7
"""

__author__ = ["Clément Besnier <clem@clementbesnier.fr>"]


from cltk.sentence.sentence import RegexSentenceTokenizer

sent_end_chars = [".", "!", "?"]


class OldNorseRegexSentenceTokenizer(RegexSentenceTokenizer):
    """``RegexSentenceTokenizer`` for Old Norse."""

    def __init__(self: object):
        super().__init__(language="non", sent_end_chars=sent_end_chars)
