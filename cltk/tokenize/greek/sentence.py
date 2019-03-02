""" Code for sentence tokenization: Greek
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
import re
from cltk.tokenize.sentence import BaseSentenceTokenizer, RegexSentenceTokenizer, PunktSentenceTokenizer
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars
#from nltk.metrics.scores import accuracy, precision, recall, f-score

class GreekLanguageVars(PunktLanguageVars):
    # _re_non_word_chars = PunktLanguageVars._re_non_word_chars.replace("'",'')
    sent_end_chars = ('.', ';', '·')


def SentenceTokenizer(tokenizer='regex'):
    if tokenizer=='punkt':
        return GreekPunktSentenceTokenizer()
    if tokenizer=='regex':
        return GreekRegexSentenceTokenizer()


class GreekPunktSentenceTokenizer(PunktSentenceTokenizer):
    """ Base class for sentence tokenization
    """

    def __init__(self, language='latin'):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        PunktSentenceTokenizer.__init__(self, language='greek')
        self.model = self._get_model()
        self.lang_vars = GreekLanguageVars()


class GreekRegexSentenceTokenizer(RegexSentenceTokenizer):
    def __init__(self):
        RegexSentenceTokenizer.__init__(self, language='greek', sent_end_chars=GreekLanguageVars.sent_end_chars)


if __name__ == "__main__":
    from pprint import pprint
    sentences = """ὅλως δ’ ἀντεχόμενοί τινες, ὡς οἴονται, δικαίου τινός (ὁ γὰρ νόμος δίκαιόν τἰ τὴν κατὰ πόλεμον δουλείαν τιθέασι δικαίαν, ἅμα δ’ οὔ φασιν· τήν τε γὰρ ἀρχὴν ἐνδέχεται μὴ δικαίαν εἶναι τῶν πολέμων, καὶ τὸν ἀνάξιον δουλεύειν οὐδαμῶς ἂν φαίη τις δοῦλον εἶναι· εἰ δὲ μή, συμβήσεται τοὺς εὐγενεστάτους εἶναι δοκοῦντας δούλους εἶναι καὶ ἐκ δούλων, ἐὰν συμβῇ πραθῆναι ληφθέντας."""
    tokenizer = SentenceTokenizer(tokenizer='punkt')
    sents = tokenizer.tokenize(sentences)
    print(sents)
    # for i, sent in enumerate(sents, 1):
    #     print(f'{i}: {sent}')
