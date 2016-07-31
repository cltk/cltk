"""Language-specific word tokenizers. Primary purpose is to handle enclitics.
"""

import re

from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters


__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>']
__license__ = 'MIT License. See LICENSE.'

class WordTokenizer:  # pylint: disable=too-few-public-methods
    """Tokenize according to rules specific to a given language."""

    def __init__(self, language):
        """Take language as argument to the class. Check availability and
        setup class variables."""
        self.language = language
        self.available_languages = ['latin']
        assert self.language in self.available_languages, \
            "Specific tokenizer not available for '{0}'. Only available for: '{1}'.".format(self.language,  # pylint: disable=line-too-long
                                                                                            self.available_languages)  # pylint: disable=line-too-long


    def tokenize(self, string):
        """Tokenize incoming string."""

        if self.language == 'latin':
            tokens = tokenize_latin_words(string)
        else:
            tokens = nltk_tokenize_words(string)

        return tokens


def nltk_tokenize_words(string, attached_period=False, language=None):
    """Wrap NLTK's tokenizer PunktLanguageVars(), but make final period
    its own token.
    >>> nltk_punkt("Sentence 1. Sentence 2.")
    >>> ['Sentence', 'one', '.', 'Sentence', 'two', '.']
    Optionally keep the NLTK's output:
    >>> nltk_punkt("Sentence 1. Sentence 2.", attached_period=True)
    >>> ['Sentence', 'one.', 'Sentence', 'two.']
    TODO: Run some tests to determine whether there is a large penalty for
    re-calling PunktLanguageVars() for each use of this function. If so, this
    will need to become a class, perhaps inheriting from the PunktLanguageVars
    object. Maybe integrate with WordTokenizer.
    """
    assert isinstance(string, str), "Incoming string must be type str."
    if language=='sanskrit':
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

def tokenize_latin_words(string):
    from cltk.tokenize.latin_exceptions import latin_exceptions

    assert isinstance(string, str), "Incoming string must be type str."

    def matchcase(word):
        # From Python Cookbook
        def replace(m):
            text = m.group()
            if text.isupper():
                return word.upper()
            elif text.islower():
                return word.lower()
            elif text[0].isupper():
                return word.capitalize()
            else:
                return word

        return replace

    replacements = [(r'mecum', 'cum me'),
                    (r'tecum', 'cum te'),
                    (r'secum', 'cum se'),
                    (r'nobiscum', 'cum nobis'),
                    (r'vobiscum', 'cum vobis'),
                    (r'quocum', 'cum quo'),
                    (r'quacum', 'cum qua'),
                    (r'quicum', 'cum qui'),
                    (r'quibuscum', 'cum quibus'),
                    (r'sodes', 'si audes'),
                    (r'satin', 'satis ne'),
                    (r'scin', 'scis ne'),
                    (r'sultis', 'si vultis'),
                    (r'similist', 'similis est'),
                    (r'qualist', 'qualis est')
                    ]

    for replacement in replacements:
        string = re.sub(replacement[0], matchcase(replacement[1]), string, flags=re.IGNORECASE)


    punkt_param = PunktParameters()
    abbreviations = ['c', 'l', 'm', 'p', 'q', 't', 'ti', 'sex', 'a', 'd', 'cn', 'sp', "m'", 'ser', 'ap', 'n', 'v', 'k', 'mam', 'post', 'f', 'oct', 'opet', 'paul', 'pro', 'sert', 'st', 'sta', 'v', 'vol', 'vop']
    punkt_param.abbrev_types = set(abbreviations)
    sent_tokenizer = PunktSentenceTokenizer(punkt_param)

    word_tokenizer = PunktLanguageVars()
    sents = sent_tokenizer.tokenize(string)

    enclitics = ['que', 'n', 'ue', 've', 'st']
    exceptions = enclitics
    exceptions = list(set(exceptions + latin_exceptions))

    tokens = []

    for sent in sents:
        temp_tokens = word_tokenizer.word_tokenize(sent)
        if temp_tokens[0].endswith('ne'):
            if temp_tokens[0].lower() not in exceptions:
                temp = [temp_tokens[0][:-2], '-ne']
                temp_tokens = temp + temp_tokens[1:]

        if temp_tokens[-1].endswith('.'):
            final_word = temp_tokens[-1][:-1]
            del temp_tokens[-1]
            temp_tokens += [final_word, '.']

        for token in temp_tokens:
            tokens.append(token)

    # Break enclitic handling into own function?
    specific_tokens = []

    for token in tokens:
        is_enclitic = False
        if token.lower() not in exceptions:
            for enclitic in enclitics:
                if token.endswith(enclitic):
                    if enclitic == 'n':
                        specific_tokens += [token[:-len(enclitic)]] + ['-ne']
                    elif enclitic == 'st':
                        if token.endswith('ust'):
                            specific_tokens += [token[:-len(enclitic) + 1]] + ['est']
                        else:
                            specific_tokens += [token[:-len(enclitic)]] + ['est']
                    else:
                        specific_tokens += [token[:-len(enclitic)]] + ['-' + enclitic]
                    is_enclitic = True
                    break
        if not is_enclitic:
            specific_tokens.append(token)

    return specific_tokens
