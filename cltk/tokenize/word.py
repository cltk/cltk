"""Language-specific word tokenizers. Primary purpose is to handle enclitics."""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Natasha Voake <natashavoake@gmail.com>',
              'Clément Besnier <clemsciences@gmail.com>',
              'Andrew Deloucas <adeloucas@g.harvard.edu>']
# Author info for Arabic?

__license__ = 'MIT License. See LICENSE.'

import re

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

from nltk.tokenize.treebank import TreebankWordTokenizer

import cltk.corpus.arabic.utils.pyarabic.araby as araby
from cltk.tokenize.latin.sentence import LatinPunktSentenceTokenizer
from cltk.tokenize.greek.sentence import GreekRegexSentenceTokenizer
from cltk.tokenize.middle_english.params import MiddleEnglishTokenizerPatterns
from cltk.tokenize.middle_high_german.params import MiddleHighGermanTokenizerPatterns
from cltk.tokenize.old_norse.params import OldNorseTokenizerPatterns
from cltk.tokenize.old_french.params import OldFrenchTokenizerPatterns

class WordTokenizer:  # pylint: disable=too-few-public-methods
    """Tokenize according to rules specific to a given language."""

    def __init__(self, language):
        """Take language as argument to the class. Check availability and
        setup class variables."""
        self.language = language
        self.available_languages = ['akkadian',
                                    'arabic',
                                    'french', # deprecate
                                    'greek',
                                    'latin',
                                    'middle_english',
                                    'middle_french',
                                    'middle_high_german',
                                    'old_french',
                                    'old_norse',
                                    'sanskrit'
                                    ]
        assert self.language in self.available_languages, \
            "Specific tokenizer not available for '{0}'. Only available for: '{1}'.".format(self.language,  # pylint: disable=line-too-long
            self.available_languages)  # pylint: disable=line-too-long

    def tokenize(self, string):
        """Tokenize incoming string."""
        if self.language == 'akkadian':
            tokens = tokenize_akkadian_words(string)
        elif self.language == 'arabic':
            tokenizer = BaseArabyWordTokenizer('arabic')
            tokens = tokenizer.tokenize(string)
        elif self.language == 'french':
            tokenizer = BaseRegexWordTokenizer('old_french', OldFrenchTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'greek':
            tokenizer = BasePunktWordTokenizer('greek', GreekRegexSentenceTokenizer)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'latin':
            # Add deprecation warning to use cltk.tokenize.latin.word
            # Enclitic support removed from this tokenizer
            tokenizer = TreebankWordTokenizer()
            tokens = tokenizer.tokenize(string)
        elif self.language == 'old_norse':
            tokenizer = BaseRegexWordTokenizer('old_norse', OldNorseTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'middle_english':
            tokenizer = BaseRegexWordTokenizer('middle_english', MiddleEnglishTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'middle_french':
            tokenizer = BaseRegexWordTokenizer('old_french', OldFrenchTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'middle_high_german':
            tokenizer = BaseRegexWordTokenizer('middle_high_german', MiddleHighGermanTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'old_french':
            tokenizer = BaseRegexWordTokenizer('old_french', OldFrenchTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        else:
            tokenizer = TreebankWordTokenizer
            tokens = tokenizer.tokenize(string)
        return tokens

    def tokenize_sign(self, word):
        """This is for tokenizing cuneiform signs."""
        if self.language == 'akkadian':
            sign_tokens = tokenize_akkadian_signs(word)
        else:
            sign_tokens = 'Language must be written using cuneiform.'

        return sign_tokens

def tokenize_akkadian_words(line):
    """
    Operates on a single line of text, returns all words in the line as a
    tuple in a list.

    input: "1. isz-pur-ram a-na"
    output: [("isz-pur-ram", "akkadian"), ("a-na", "akkadian")]

    :param: line: text string
    :return: list of tuples: (word, language)
    """
    beginning_underscore = "_[^_]+(?!_)$"
    # only match a string if it has a beginning underscore anywhere
    ending_underscore = "^(?<!_)[^_]+_"
    # only match a string if it has an ending underscore anywhere
    two_underscores = "_[^_]+_"
    # only match a string if it has two underscores

    words = line.split()
    # split the line on spaces ignoring the first split (which is the
    # line number)
    language = "akkadian"
    output_words = []
    for word in words:
        if re.search(two_underscores, word):
            # If the string has two underscores in it then the word is
            # in Sumerian while the neighboring words are in Akkadian.
            output_words.append((word, "sumerian"))
        elif re.search(beginning_underscore, word):
            # If the word has an initial underscore somewhere
            # but no other underscores than we're starting a block
            # of Sumerian.
            language = "sumerian"
            output_words.append((word, language))
        elif re.search(ending_underscore, word):
            # If the word has an ending underscore somewhere
            # but not other underscores than we're ending a block
            # of Sumerian.
            output_words.append((word, language))
            language = "akkadian"
        else:
            # If there are no underscore than we are continuing
            # whatever language we're currently in.
            output_words.append((word, language))
    return output_words


def tokenize_akkadian_signs(word):
    """
    Takes tuple (word, language) and splits the word up into individual
    sign tuples (sign, language) in a list.

    input: ("{gisz}isz-pur-ram", "akkadian")
    output: [("gisz", "determinative"), ("isz", "akkadian"),
    ("pur", "akkadian"), ("ram", "akkadian")]

    :param: tuple created by word_tokenizer2
    :return: list of tuples: (sign, function or language)
    """
    word_signs = []
    sign = ''
    language = word[1]
    determinative = False
    for char in word[0]:
        if determinative is True:
            if char == '}':
                determinative = False
                if len(sign) > 0:  # pylint: disable=len-as-condition
                    word_signs.append((sign, 'determinative'))
                sign = ''
                language = word[1]
                continue
            else:
                sign += char
                continue
        else:
            if language == 'akkadian':
                if char == '{':
                    if len(sign) > 0:  # pylint: disable=len-as-condition
                        word_signs.append((sign, language))
                    sign = ''
                    determinative = True
                    continue
                elif char == '_':
                    if len(sign) > 0:  # pylint: disable=len-as-condition
                        word_signs.append((sign, language))
                    sign = ''
                    language = 'sumerian'
                    continue
                elif char == '-':
                    if len(sign) > 0:  # pylint: disable=len-as-condition
                        word_signs.append((sign, language))
                    sign = ''
                    language = word[1] # or default word[1]?
                    continue
                else:
                    sign += char
            elif language == 'sumerian':
                if char == '{':
                    if len(sign) > 0:  # pylint: disable=len-as-condition
                        word_signs.append((sign, language))
                    sign = ''
                    determinative = True
                    continue
                elif char == '_':
                    if len(sign) > 0:  # pylint: disable=len-as-condition
                        word_signs.append((sign, language))
                    sign = ''
                    language = word[1]
                    continue
                elif char == '-':
                    if len(sign) > 0:  # pylint: disable=len-as-condition
                        word_signs.append((sign, language))
                    sign = ''
                    language = word[1]
                    continue
                else:
                    sign += char
    if len(sign) > 0:
        word_signs.append((sign, language))

    return word_signs


class BaseWordTokenizer:
    """ Base class for word tokenization"""

    def __init__(self, language: str = None):
        """
        :param language : language for word tokenization
        :type language: str
        """
        if language:
            self.language = language.lower()

    def tokenize(self, text: str, model: object = None):
        """
        Replace in subclasses
        """
        pass


class BasePunktWordTokenizer(BaseWordTokenizer):
    """Base class for punkt word tokenization"""

    def __init__(self, language: str = None, sent_tokenizer:object = None):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language = language
        super().__init__(language=self.language)
        if sent_tokenizer:
            self.sent_tokenizer = sent_tokenizer()
        else:
            punkt_param = PunktParameters()
            self.sent_tokenizer = PunktSentenceTokenizer(punkt_param)

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        sents = self.sent_tokenizer.tokenize(text)
        tokenizer = TreebankWordTokenizer()
        return [item for sublist in tokenizer.tokenize_sents(sents) for item in sublist]


class BaseRegexWordTokenizer(BaseWordTokenizer):
    """Base class for punkt word tokenization"""

    def __init__(self, language:str = None, patterns:list = []):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language = language
        self.patterns = patterns
        super().__init__(language=self.language)

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        for pattern in self.patterns:
            text = re.sub(pattern[0], pattern[1], text)
        return text.split()


class BaseArabyWordTokenizer(BaseWordTokenizer):
    """Base class for Araby word tokenization"""

    def __init__(self, language:str = None, patterns:list = []):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language = language
        self.patterns = patterns
        super().__init__(language=self.language)

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        return araby.tokenize(text)
