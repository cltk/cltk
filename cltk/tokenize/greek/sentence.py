""" Code for sentence tokenization: Greek
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License.'

import os.path
from cltk.tokenize.sentence import BaseSentenceTokenizer
from cltk.utils.file_operations import open_pickle
from nltk.tokenize.punkt import PunktLanguageVars
#from nltk.metrics.scores import accuracy, precision, recall, f-score


class GreekLanguageVars(PunktLanguageVars):
    # _re_non_word_chars = PunktLanguageVars._re_non_word_chars.replace("'",'')
    pass

class SentenceTokenizer(BaseSentenceTokenizer):
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
        tokenizer._lang_vars = LatinLanguageVars()

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


if __name__ == "__main__":
    sentences = """ὅτι μὲν τοίνυν εἰσὶ φύσει τινὲς οἱ μὲν ἐλεύθεροι οἱ δὲ δοῦλοι, φανερόν, οἷς καὶ συμφέρει τὸ δουλεύειν καὶ δίκαιόν ἐστιν."""
    tokenizer = SentenceTokenizer()
    sents = tokenizer.tokenize(sentences)
    print(sents)
