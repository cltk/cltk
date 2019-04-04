"""Language-specific word tokenizers. Primary purpose is to handle enclitics."""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Natasha Voake <natashavoake@gmail.com>',
              'Clément Besnier <clemsciences@gmail.com>',
              'Andrew Deloucas <adeloucas@g.harvard.edu>']
# Author info for Arabic?

__license__ = 'MIT License. See LICENSE.'

import re

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

import cltk.corpus.arabic.utils.pyarabic.araby as araby
from cltk.tokenize.latin.word import *

class WordTokenizer:  # pylint: disable=too-few-public-methods
    """Tokenize according to rules specific to a given language."""

    def __init__(self, language):
        """Take language as argument to the class. Check availability and
        setup class variables."""
        self.language = language
        self.available_languages = ['akkadian',
                                    'arabic',
                                    'french',
                                    'greek',
                                    'latin',
                                    'old_norse',
                                    'middle_english',
                                    'middle_high_german']
        assert self.language in self.available_languages, \
            "Specific tokenizer not available for '{0}'. Only available for: '{1}'.".format(self.language,  # pylint: disable=line-too-long
            self.available_languages)  # pylint: disable=line-too-long
        # ^^^ Necessary? since we have an 'else' in `tokenize`

    def tokenize(self, string):
        """Tokenize incoming string."""

        if self.language == 'akkadian':
            tokens = tokenize_akkadian_words(string)
        elif self.language == 'arabic':
            tokens = tokenize_arabic_words(string)
        elif self.language == 'french':
            tokens = tokenize_french_words(string)
        elif self.language == 'greek':
            tokens = tokenize_greek_words(string)
        elif self.language == 'latin':
            tokenizer = LatinPunktWordTokenizer()
            tokens = tokenizer.tokenize(string)
        elif self.language == 'old_norse':
            tokens = tokenize_old_norse_words(string)
        elif self.language == 'middle_english':
            tokens = tokenize_middle_english_words(string)
        elif self.language == 'middle_high_german':
            tokens = tokenize_middle_high_german_words(string)
        else:
            tokens = nltk_tokenize_words(string)

        return tokens

    def tokenize_sign(self, word):
        """This is for tokenizing cuneiform signs."""
        if self.language == 'akkadian':
            sign_tokens = tokenize_akkadian_signs(word)
        else:
            sign_tokens = 'Language must be written using cuneiform.'

        return sign_tokens


def nltk_tokenize_words(string, attached_period=False, language=None):
    """Wrap NLTK's tokenizer PunktLanguageVars(), but make final period
    its own token.

    >>> nltk_tokenize_words("Sentence 1. Sentence 2.")
    ['Sentence', '1', '.', 'Sentence', '2', '.']

    >>> #Optionally keep the NLTK's output:

    >>> nltk_tokenize_words("Sentence 1. Sentence 2.", attached_period=True)
    ['Sentence', '1.', 'Sentence', '2.']

    TODO: Run some tests to determine whether there is a large penalty for
    re-calling PunktLanguageVars() for each use of this function. If so, this
    will need to become a class, perhaps inheriting from the PunktLanguageVars
    object. Maybe integrate with WordTokenizer.
    """
    assert isinstance(string, str), "Incoming string must be type str."
    if language == 'sanskrit':
        periods = ['.', '।','॥']
    else:
        periods = ['.']
    punkt = PunktLanguageVars()
    tokens = punkt.word_tokenize(string)
    if attached_period:
        return tokens
    new_tokens = []
    for word in tokens:
        for char in periods:
            if word.endswith(char):
                new_tokens.append(word[:-1])
                new_tokens.append(char)
                break
        else:
            new_tokens.append(word)
    return new_tokens


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


def tokenize_arabic_words(text):

    """
        Tokenize text into words
        @param text: the input text.
        @type text: unicode.
        @return: list of words.
        @rtype: list.
    """
    specific_tokens = []
    if not text:
        return specific_tokens
    else:
        specific_tokens = araby.tokenize(text)
        return specific_tokens


def tokenize_french_words(string):
    assert isinstance(string, str), "Incoming string must be type str."

    # normalize apostrophes

    text = re.sub(r"’", r"'", string)

    # Dealing with punctuation
    text = re.sub(r"\'", r"' ", text)
    text = re.sub("(?<=.)(?=[.!?)(\";:,«»\-])", " ", text)

    results = str.split(text)
    return (results)


def tokenize_greek_words(text):
    """
    Tokenizer divides the string into a list of substrings. This is a placeholder
    function that returns the default NLTK word tokenizer until
    Greek-specific options are added.

    Example:
    >>> text = 'Θουκυδίδης Ἀθηναῖος ξυνέγραψε τὸν πόλεμον τῶν Πελοποννησίων καὶ Ἀθηναίων,'
    >>> tokenize_greek_words(text)
    ['Θουκυδίδης', 'Ἀθηναῖος', 'ξυνέγραψε', 'τὸν', 'πόλεμον', 'τῶν', 'Πελοποννησίων', 'καὶ', 'Ἀθηναίων', ',']

    :param string: This accepts the string value that needs to be tokenized
    :returns: A list of substrings extracted from the string
    """

    return nltk_tokenize_words(text) # Simplest implementation to start


def tokenize_old_norse_words(text):
    """

    :param text: a text or a sentence
    :return:
    """
    assert isinstance(text, str)

    # punctuation
    text = re.sub(r"\'", r"' ", text)
    text = re.sub("(?<=.)(?=[.!?)(\";:,«»\-])", " ", text)

    # TODO dealing with merges between verbs at the second person of the present tense and þú
    # -> -tu, -ðu, -du, -u : question

    # TODO dealing with merges between verbs and sik -> st : middle voice

    results = str.split(text)
    return results

def tokenize_middle_english_words(text):
    """Tokenizes ME text:

    >>> tokenize_middle_english_words("And then,   went   I  fastyr!")
    ['And', 'then', ',', 'went', 'I', 'fastyr', '!']

    """

    assert isinstance(text, str)

    text = re.sub(r'\n', r' ', text)
    text = re.sub(r'(?<=.)(?=[\.\";\,\:\-\[\]\(\)!&?])',r' ', text)
    text = re.sub(r'(?<=[\.\";\-\,\:\[\]\(\)!&?])(?=.)',r' ', text)
    text = re.sub(r'\s+',r' ', text)
    text = str.split(text)

    return text

def tokenize_middle_high_german_words(text):
    """Tokenizes MHG text"""

    assert isinstance(text, str)
    # As far as I know, hyphens were never used for compounds, so the tokenizer treats all hyphens as line-breaks
    text = re.sub(r'-\n',r'-', text)
    text = re.sub(r'\n', r' ', text)
    text = re.sub(r'(?<=.)(?=[\.\";\,\:\[\]\(\)!&?])',r' ', text)
    text = re.sub(r'(?<=[\.\";\,\:\[\]\(\)!&?])(?=.)',r' ', text)
    text = re.sub(r'\s+',r' ', text)
    text = str.split(text)

    return text

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
    """Base class for punkt sentence tokenization"""

    missing_models_message = "BasePunktWordTokenizer requires a language model."

    def __init__(self, language: str = None, sent_tokenizer:object = None, lang_vars: object = None):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language = language
        # self.lang_vars = lang_vars
        super().__init__(language=self.language)
        if sent_tokenizer:
            self.sent_tokenizer = sent_tokenizer
        else:
            punkt_param = PunktParameters()
            self.sent_tokenizer = PunktSentenceTokenizer(punkt_param)

    def tokenize(self, text: str, model: object = None):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        tokenizer = PunktLanguageVars()
        return tokenizer.word_tokenize(text)

if __name__ == '__main__':
    w = WordTokenizer('latin')
    tokens = w.tokenize('arma virumque cano')
    print(tokens)
    pass
