""" Code for sentence tokenization: Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
from cltk.tokenize.sentence import BaseSentenceTokenizer, PunktSentenceTokenizer
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars

# Need to think about the best way to evaluate sentence tokenizers
#from nltk.metrics.scores import accuracy, precision, recall, f-score

class LatinLanguageVars(PunktLanguageVars):
    _re_non_word_chars = PunktLanguageVars._re_non_word_chars.replace("'",'')


def SentenceTokenizer(tokenizer='punkt'):
    if tokenizer=='punkt':
        return LatinPunktSentenceTokenizer()


class LatinPunktSentenceTokenizer(PunktSentenceTokenizer):
    """ Base class for sentence tokenization
    """

    def __init__(self, language='latin'):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        PunktSentenceTokenizer.__init__(self, language='latin')
        self.model = self._get_model()
        self.lang_vars = LatinLanguageVars()


class GreekRegexSentenceTokenizer(RegexSentenceTokenizer):
    def __init__(self):
        RegexSentenceTokenizer.__init__(self, language='greek', sent_end_chars=GreekLanguageVars.sent_end_chars)


    # def tokenize(self, text, model=None, lang_vars=self.lang_vars):
    #     """
    #     Method for tokenizing sentences. This method
    #     should be overridden by subclasses of SentenceTokenizer.
    #     """
    #     if not self.model:
    #         model = self.model
    #
    #     tokenizer = open_pickle(self.model)
    #     tokenizer._lang_vars = LatinLanguageVars()
    #
    #     return tokenizer.tokenize(text)


    # def _get_model(self):
    #     # Can this be simplified?
    #     model_file = '{}_punkt.pickle'.format(self.language)
    #     model_path = os.path.join('~/cltk_data',
    #                             self.language,
    #                             'model/' + self.language + '_models_cltk/tokenizers/sentence')  # pylint: disable=C0301
    #     model_path = os.path.expanduser(model_path)
    #     model_path = os.path.join(model_path, model_file)
    #     assert os.path.isfile(model_path), \
    #         'Please download sentence tokenization model for {}.'.format(self.language)
    #     return model_path


if __name__ == "__main__":
    sentences = """Sed hoc primum sentio, nisi in bonis amicitiam esse non posse; neque id ad vivum reseco, ut illi qui haec subtilius disserunt, fortasse vere, sed ad communem utilitatem parum; negant enim quemquam esse virum bonum nisi sapientem. Sit ita sane; sed eam sapientiam interpretantur quam adhuc mortalis nemo est consecutus, nos autem ea quae sunt in usu vitaque communi, non ea quae finguntur aut optantur, spectare debemus. Numquam ego dicam C. Fabricium, M'. Curium, Ti. Coruncanium, quos sapientes nostri maiores iudicabant, ad istorum normam fuisse sapientes. Quare sibi habeant sapientiae nomen et invidiosum et obscurum; concedant ut viri boni fuerint. Ne id quidem facient, negabunt id nisi sapienti posse concedi."""

    tokenizer = SentenceTokenizer()
    sents = tokenizer.tokenize(sentences)
    for i, sent in enumerate(sents, 1):
        print(f'{i}: {sent}')
