"""Code for sentences tokenization: Greek.

Sentence tokenization for Ancient Greek is available using a regular-expression based tokenizer.

>>> from cltk.sentence.grc import GreekRegexSentenceTokenizer
>>> from cltk.languages.example_texts import get_example_text
>>> splitter = GreekRegexSentenceTokenizer()
>>> sentences = splitter.tokenize(get_example_text("grc"))
>>> sentences[:2]
['ὅτι μὲν ὑμεῖς, ὦ ἄνδρες Ἀθηναῖοι, πεπόνθατε ὑπὸ τῶν ἐμῶν κατηγόρων, οὐκ οἶδα: ἐγὼ δ᾽ οὖν καὶ αὐτὸς ὑπ᾽ αὐτῶν ὀλίγου ἐμαυτοῦ ἐπελαθόμην, οὕτω πιθανῶς ἔλεγον.', 'καίτοι ἀληθές γε ὡς ἔπος εἰπεῖν οὐδὲν εἰρήκασιν.']
>>> len(sentences)
9
"""

__author__ = ["Patrick J. Burns <patrick@diyclassics.org>"]


from cltk.sentence.sentence import RegexSentenceTokenizer

sent_end_chars = [".", ";", "·"]


class GreekRegexSentenceTokenizer(RegexSentenceTokenizer):
    """``RegexSentenceTokenizer`` for Ancient Greek."""

    def __init__(self: object):
        super().__init__(language="greek", sent_end_chars=sent_end_chars)
