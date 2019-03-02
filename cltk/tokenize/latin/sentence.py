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


if __name__ == "__main__":
    sentences = """Sed hoc primum sentio, nisi in bonis amicitiam esse non posse; neque id ad vivum reseco, ut illi qui haec subtilius disserunt, fortasse vere, sed ad communem utilitatem parum; negant enim quemquam esse virum bonum nisi sapientem. Sit ita sane; sed eam sapientiam interpretantur quam adhuc mortalis nemo est consecutus, nos autem ea quae sunt in usu vitaque communi, non ea quae finguntur aut optantur, spectare debemus. Numquam ego dicam C. Fabricium, M'. Curium, Ti. Coruncanium, quos sapientes nostri maiores iudicabant, ad istorum normam fuisse sapientes. Quare sibi habeant sapientiae nomen et invidiosum et obscurum; concedant ut viri boni fuerint. Ne id quidem facient, negabunt id nisi sapienti posse concedi."""

    tokenizer = SentenceTokenizer()
    sents = tokenizer.tokenize(sentences)
    for i, sent in enumerate(sents, 1):
        print(f'{i}: {sent}')
