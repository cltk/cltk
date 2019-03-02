""" Code for sentence tokenization: Greek
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
import re
from cltk.tokenize.sentence import BaseSentenceTokenizer, RegexSentenceTokenizer
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

class GreekPunktSentenceTokenizer(BaseSentenceTokenizer):
    """ Base class for sentence tokenization
    """

    def __init__(self):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        BaseSentenceTokenizer.__init__(self, 'greek')
        self.model = self._get_model()


    def tokenize(self, text, model=None):
        """
        Method for tokenizing sentences. This method
        should be overridden by subclasses of SentenceTokenizer.
        """
        if not self.model:
            model = self.model

        tokenizer = open_pickle(self.model)
        tokenizer._lang_vars = GreekLanguageVars()
        print(tokenizer._lang_vars.sent_end_chars)

        return tokenizer.tokenize(text)


    def _get_model(self):
        # Can this be simplified?
        model_file = '{}_punkt.pickle'.format(self.language)
        model_path = os.path.join('~/cltk_data',
                                self.language,
                                'model/' + self.language + '_models_cltk/tokenizers/sentence')  # pylint: disable=C0301
        model_path = os.path.expanduser(model_path)
        model_path = os.path.join(model_path, model_file)
        assert os.path.isfile(model_path), \
            'Please download sentence tokenization model for {}.'.format(self.language)
        return model_path


# class GreekRegexSentenceTokenizer(BaseSentenceTokenizer):
#     """ Base class for sentence tokenization
#     """
#
#     def __init__(self):
#         """
#         :param language : language for sentence tokenization
#         :type language: str
#         """
#         BaseSentenceTokenizer.__init__(self, 'greek')
#         # self.model = self._get_model()
#
#
#     def tokenize(self, text, model=None):
#         """
#         Method for tokenizing Greek sentences with regular expressions.
#         """
#         sent_end_chars = '\\'+'|\\'.join(GreekLanguageVars.sent_end_chars)
#         sentences = re.split(rf'(?<!\w\.\w.)(?<!\w\w\.)(?<={sent_end_chars})\s', text)
#         return sentences

class GreekRegexSentenceTokenizer(RegexSentenceTokenizer):
    def __init__(self):
        RegexSentenceTokenizer.__init__(self, language='greek', sent_end_chars=GreekLanguageVars.sent_end_chars)


if __name__ == "__main__":
    from pprint import pprint
    sentences = """ὅλως δ’ ἀντεχόμενοί τινες, ὡς οἴονται, δικαίου τινός (ὁ γὰρ νόμος δίκαιόν τἰ τὴν κατὰ πόλεμον δουλείαν τιθέασι δικαίαν, ἅμα δ’ οὔ φασιν· τήν τε γὰρ ἀρχὴν ἐνδέχεται μὴ δικαίαν εἶναι τῶν πολέμων, καὶ τὸν ἀνάξιον δουλεύειν οὐδαμῶς ἂν φαίη τις δοῦλον εἶναι· εἰ δὲ μή, συμβήσεται τοὺς εὐγενεστάτους εἶναι δοκοῦντας δούλους εἶναι καὶ ἐκ δούλων, ἐὰν συμβῇ πραθῆναι ληφθέντας."""
    tokenizer = SentenceTokenizer(tokenizer='regex')
    sents = tokenizer.tokenize(sentences)
    for i, sent in enumerate(sents, 1):
        print(f'{i}: {sent}')
