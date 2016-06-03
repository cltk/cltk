"""Language-specific word tokenizers. Primary purpose is to handle enclitics.
"""

import re

#from nltk.tokenize.punkt import PunktLanguageVars
from nltk.tokenize import word_tokenize


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

        if self.language == 'latin':
            from cltk.tokenize.latin_exceptions import latin_exceptions
            self.enclitics = ['que', 'n', 'ne', 'ue', 've', 'st']

            self.exceptions = self.enclitics
            self.exceptions = list(set(self.exceptions + latin_exceptions))


    def tokenize(self, string):
        """Tokenize incoming string."""

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

#       punkt = PunktLanguageVars()
        generic_tokens = word_tokenize(string)

        specific_tokens = []
        for generic_token in generic_tokens:
            is_enclitic = False
            if generic_token.lower() not in self.exceptions:
                for enclitic in self.enclitics:
                    if generic_token.endswith(enclitic):
                        if enclitic == 'n':
                                specific_tokens += [generic_token[:-len(enclitic)]] + ['-ne']
                        elif enclitic == 'st':
                            if generic_token.endswith('ust'):
                                specific_tokens += [generic_token[:-len(enclitic)+1]] + ['est']
                            else:
                                specific_tokens += [generic_token[:-len(enclitic)]] + ['est']
                        else:
                            specific_tokens += [generic_token[:-len(enclitic)]] + ['-' + enclitic]
                        is_enclitic = True
                        break
            if not is_enclitic:
                specific_tokens.append(generic_token)
        return specific_tokens

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
