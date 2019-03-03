"""Tokenize sentences."""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>','Anoop Kunchukuttan']
__license__ = 'MIT License. See LICENSE.'

import os
import re
import string

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer

from cltk.utils.file_operations import open_pickle

# Part of Latin workaround
class LatinLanguageVars(PunktLanguageVars):
    _re_non_word_chars = PunktLanguageVars._re_non_word_chars.replace("'",'')

PUNCTUATION = {'greek':
                   {'external': ('.', ';'),
                    'internal': (',', '·'),
                    'file': 'greek.pickle', },
               'latin':
                   {'external': ('.', '?', '!', ':'),
                    'internal': (',', ';'),
                    'file': 'latin.pickle', }}

INDIAN_LANGUAGES = ['bengali','hindi','marathi','sanskrit','telugu']

class TokenizeSentence():  # pylint: disable=R0903
    """Tokenize sentences for the language given as argument, e.g.,
    ``TokenizeSentence('greek')``.
    """

    def __init__(self: object, language: str):
        """Lower incoming language name and assemble variables.
        :type language: str
        :param language : Language for sentence tokenization.
        """
        self.language = language.lower()

        # Workaround for Latin—use old API syntax to load new sent tokenizer
        if self.language == 'latin':
            PunktSentenceTokenizer.__init__(self, language='latin')
            self.model = PunktSentenceTokenizer._get_model(self)
            self.lang_vars = LatinLanguageVars()
        elif self.language not in INDIAN_LANGUAGES :
            self.internal_punctuation, self.external_punctuation, self.tokenizer_path = \
                self._setup_language_variables(self.language)


    def _setup_language_variables(self, lang: str):
        """Check for language availability and presence of tokenizer file,
        then read punctuation characters for language and build tokenizer file
        path.
        :param lang: The language argument given to the class.
        :type lang: str
        :rtype (str, str, str)
        """
        assert lang in PUNCTUATION.keys(), \
            'Sentence tokenizer not available for {0} language.'.format(lang)
        internal_punctuation = PUNCTUATION[lang]['internal']
        external_punctuation = PUNCTUATION[lang]['external']
        file = PUNCTUATION[lang]['file']
        rel_path = os.path.join('~/cltk_data',
                                lang,
                                'model/' + lang + '_models_cltk/tokenizers/sentence')  # pylint: disable=C0301
        path = os.path.expanduser(rel_path)
        tokenizer_path = os.path.join(path, file)
        assert os.path.isfile(tokenizer_path), \
            'CLTK linguistics data not found for language {0}'.format(lang)
        return internal_punctuation, external_punctuation, tokenizer_path

    def _setup_tokenizer(self, tokenizer: object):
        """Add tokenizer and punctuation variables.
        :type tokenizer: object
        :param tokenizer : Unpickled tokenizer object.
        :rtype : object
        """
        language_punkt_vars = PunktLanguageVars
        language_punkt_vars.sent_end_chars = self.external_punctuation
        language_punkt_vars.internal_punctuation = self.internal_punctuation
        tokenizer.INCLUDE_ALL_COLLOCS = True
        tokenizer.INCLUDE_ABBREV_COLLOCS = True
        params = tokenizer.get_params()
        return PunktSentenceTokenizer(params)

    def tokenize_sentences(self: object, untokenized_string: str):
        """Tokenize sentences by reading trained tokenizer and invoking
        ``PunktSentenceTokenizer()``.
        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :rtype : list of strings
        """
        # load tokenizer
        assert isinstance(untokenized_string, str), \
            'Incoming argument must be a string.'


        if self.language=='latin':
            tokenizer = open_pickle(self.model)
            if self.lang_vars:
                tokenizer._lang_vars = self.lang_vars
        else:
            tokenizer = open_pickle(self.tokenizer_path)
            tokenizer = self._setup_tokenizer(tokenizer)

        # mk list of tokenized sentences
        if self.language=='latin':
            return tokenizer.tokenize(sentences)
        else:
            tokenized_sentences = []
            for sentence in tokenizer.sentences_from_text(untokenized_string, realign_boundaries=True):  # pylint: disable=C0301
                tokenized_sentences.append(sentence)
            return tokenized_sentences

    def indian_punctuation_tokenize_regex(self: object, untokenized_string: str):
        """A trivial tokenizer which just tokenizes on the punctuation boundaries.
        This also includes punctuation, namely the the purna virama ("|") and
        deergha virama ("॥"), for Indian language scripts.

        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :rtype : list of strings
        """
        modified_punctuations = string.punctuation.replace("|","") # The replace , deletes the ' | ' from the punctuation string provided by the library
        indian_punctuation_pattern = re.compile('(['+modified_punctuations+'\u0964\u0965'+']|\|+)')
        tok_str = indian_punctuation_pattern.sub(r' \1 ',untokenized_string.replace('\t',' '))
        return re.sub(r'[ ]+',u' ',tok_str).strip(' ').split(' ')

    def tokenize(self: object, untokenized_string: str):
        # NLTK's PlaintextCorpusReader needs a function called tokenize
        # in functions used as a parameter for sentence tokenization.
        # So this is an alias for tokenize_sentences().
        if self.language in INDIAN_LANGUAGES:
            return self.indian_punctuation_tokenize_regex(untokenized_string)
        else:
            return self.tokenize_sentences(untokenized_string)

### Code below for consideration as new structure for modules; code above legacy?

# """ Code for sentence tokenization
# """
#
# __author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
# __license__ = 'MIT License.'


from abc import abstractmethod

#from nltk.metrics.scores import accuracy, precision, recall, f-score
#from cltk.utils.cltk_logger import logger

class BaseSentenceTokenizer(object):
    """ Base class for sentence tokenization
    """

    def __init__(self, language=None):
        """ Initialize stoplist builder with option for language specific parameters
        :param language : language for sentence tokenization
        :type language: str
        """
        if language:
            self.language = language.lower()


    @abstractmethod
    def tokenize(self, text):
        """
        Method for tokenizing sentences. This method
        should be overridden by subclasses of SentenceTokenizer.
        """

class PunktSentenceTokenizer(BaseSentenceTokenizer):
    """Base class for punkt sentence tokenization
    """
    def __init__(self, language=None):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language=language
        BaseSentenceTokenizer.__init__(self, language=self.language)
        if language:
            self.model = PunktSentenceTokenizer._get_model(self)


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


    def tokenize(self, text, model=None, lang_vars=None):
        """
        Method for tokenizing sentences. This method
        should be overridden by subclasses of SentenceTokenizer.
        """
        if not self.model:
            model = self.model

        tokenizer = open_pickle(self.model)
        if self.lang_vars:
            tokenizer._lang_vars = self.lang_vars

        return tokenizer.tokenize(text)


class RegexSentenceTokenizer(BaseSentenceTokenizer):
    """ Base class for regex sentence tokenization
    """

    def __init__(self, language=None, sent_end_chars=[]):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        BaseSentenceTokenizer.__init__(self, language)
        # self.model = self._get_model()
        if sent_end_chars:
            self.sent_end_chars = '\\'+'|\\'.join(sent_end_chars)
            self.pattern = rf'(?<!\w\.\w.)(?<!\w\w\.)(?<={self.sent_end_chars})\s'
        else:
            raise Exception


    def tokenize(self, text):
        """
        Method for tokenizing Greek sentences with regular expressions.
        """
        sentences = re.split(self.pattern, text)
        return sentences

## Think more about how this will work
#    def evaluate(self, gold):
#        """
#        following http://www.nltk.org/_modules/nltk/tag/api.html#TaggerI.evaluate
#        Score the accuracy of the tokenizer against the gold standard.
#        Strip the tags from the gold standard text, retokenize it using
#        the tokenizer, then compute the accuracy, precision, recall, and f-score.
#
#        :type gold: list(list(tuple(str, str)))
#        :param gold: The list of tagged sentences to score the tagger on.
#        :rtype: float
#        """
#
#        tokenized_sents = self.tag_sents(untag(sent) for sent in gold)
#        gold_tokens = list(chain(*gold))
#        test_tokens = list(chain(*tagged_sents))
#        return accuracy(gold_tokens, test_tokens)


if __name__ == "__main__":
    sentences = """Sed hoc primum sentio, nisi in bonis amicitiam esse non posse; neque id ad vivum reseco, ut illi qui haec subtilius disserunt, fortasse vere, sed ad communem utilitatem parum; negant enim quemquam esse virum bonum nisi sapientem. Sit ita sane; sed eam sapientiam interpretantur quam adhuc mortalis nemo est consecutus, nos autem ea quae sunt in usu vitaque communi, non ea quae finguntur aut optantur, spectare debemus. Numquam ego dicam C. Fabricium, M'. Curium, Ti. Coruncanium, quos sapientes nostri maiores iudicabant, ad istorum normam fuisse sapientes. Quare sibi habeant sapientiae nomen et invidiosum et obscurum; concedant ut viri boni fuerint. Ne id quidem facient, negabunt id nisi sapienti posse concedi."""

    tokenizer = TokenizeSentence('latin')
    sents = tokenizer.tokenize(sentences)
    for i, sent in enumerate(sents, 1):
        print(f'{i}: {sent}')
