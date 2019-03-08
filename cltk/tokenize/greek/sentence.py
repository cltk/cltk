""" Code for sentence tokenization: Greek
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
import re

from cltk.tokenize.sentence import BaseSentenceTokenizer, RegexSentenceTokenizer, PunktSentenceTokenizer
from cltk.utils.file_operations import open_pickle

from nltk.tokenize.punkt import PunktLanguageVars

def SentenceTokenizer(tokenizer='regex'):
    if tokenizer=='punkt':
        return GreekPunktSentenceTokenizer()
    if tokenizer=='regex':
        return GreekRegexSentenceTokenizer()


class GreekLanguageVars(PunktLanguageVars):
    # _re_non_word_chars = PunktLanguageVars._re_non_word_chars.replace("'",'')
    sent_end_chars = ('.', ';', '·')


class GreekPunktSentenceTokenizer(PunktSentenceTokenizer):
    """ PunktSentenceTokenizer trained on Ancient Greek
    """
    models_path = os.path.expanduser('~/cltk_data/greek/model/greek_models_cltk/tokenizers/sentence')
    missing_models_message = "BackoffLatinLemmatizer requires the ```latin_models_cltk``` to be in cltk_data. Please load this corpus."

    def __init__(self: object, language:str = 'latin'):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        PunktSentenceTokenizer.__init__(self, language='greek')
        self.models_path = GreekPunktSentenceTokenizer.models_path

        try:
            self.model =  open_pickle(os.path.join(self.models_path, 'greek_punkt.pickle'))
        except FileNotFoundError as err:
            raise type(err)(GreekPunktSentenceTokenizer.missing_models_message)

        # self.model = self._get_model()
        self.lang_vars = GreekLanguageVars()


class GreekRegexSentenceTokenizer(RegexSentenceTokenizer):
    def __init__(self: object):
        RegexSentenceTokenizer.__init__(self, language='greek', sent_end_chars=GreekLanguageVars.sent_end_chars)


if __name__ == "__main__":
    from pprint import pprint
    sentences = """ὅλως δ’ ἀντεχόμενοί τινες, ὡς οἴονται, δικαίου τινός (ὁ γὰρ νόμος δίκαιόν τἰ τὴν κατὰ πόλεμον δουλείαν τιθέασι δικαίαν, ἅμα δ’ οὔ φασιν· τήν τε γὰρ ἀρχὴν ἐνδέχεται μὴ δικαίαν εἶναι τῶν πολέμων, καὶ τὸν ἀνάξιον δουλεύειν οὐδαμῶς ἂν φαίη τις δοῦλον εἶναι· εἰ δὲ μή, συμβήσεται τοὺς εὐγενεστάτους εἶναι δοκοῦντας δούλους εἶναι καὶ ἐκ δούλων, ἐὰν συμβῇ πραθῆναι ληφθέντας."""
    tokenizer = SentenceTokenizer(tokenizer='regex')
    sents = tokenizer.tokenize(sentences)
    for i, sent in enumerate(sents, 1):
        print(f'{i}: {sent}')
