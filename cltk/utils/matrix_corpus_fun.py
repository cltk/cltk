"""`matrix_corpus_fun.py` -  useful functions for performing operations on a corpus in matrix form;
that is: a list wrapping a list of strings, with each sublist being a sentence. Typically:
[["word", "word", "word"] # one sentence
 , ["word", "word", "word"] # another sentence
 # etc
 ]
"""

import logging
import re
from collections import Counter

from cltk.stem.latin.j_v import JVReplacer
from cltk.prosody.latin.string_utils import punctuation_for_spaces_dict, remove_punctuation_dict
from cltk.prosody.latin.scansion_constants import ScansionConstants

__author__ = ['Todd Cook <todd.g.cook@gmail.com>']
__license__ = 'MIT License'

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())


def drop_all_caps(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:
    >>> drop_all_caps(drop_arabic_numeric ([['Catullus'], ['C.', 'VALERIVS', 'CATVLLVS'],['1','2', '2b', '3' ],['I.', 'ad', 'Cornelium'],['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum', '?']]))
    [['Catullus'], [], [], ['ad', 'Cornelium'], ['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum']]
     """
    return [[word
             for word in sentence
             if re.match('.[a-z]', word)]
            for sentence in X]


def drop_arabic_numeric(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:

    >>> drop_arabic_numeric([['Catullus'], ['C.', 'VALERIVS', 'CATVLLVS'],['1','2', '2b', '3' ],['I.', 'ad', 'Cornelium'],['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum', '?']])
    [['Catullus'], ['C.', 'VALERIVS', 'CATVLLVS'], [], ['I.', 'ad', 'Cornelium'], ['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum', '?']]
    """
    return [[word
             for word in sentence
             if not re.match('[0-9]+([a-z]+)?', word)]
            for sentence in X]


def drop_empty_lists(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:

    >>> drop_empty_lists([['Catullus'], [], [], ['I.', 'ad', 'Cornelium'], ['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum', '?']])
    [['Catullus'], ['I.', 'ad', 'Cornelium'], ['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum', '?']]
    """
    return [sentence for sentence in X if sentence]


def drop_non_lower(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:

    >>> drop_non_lower([['Catullus'], ['C.', 'VALERIVS', 'CATVLLVS'],['1','2', '2b', '3' ],['I.', 'ad', 'Cornelium'],['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum', '?']])
    [['Catullus'], [], ['2b'], ['ad', 'Cornelium'], ['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum']]
    """
    return [[word
             for word in sentence
             if word.upper() != word]
            for sentence in X]


def clean_latin_text(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:
    >>> clean_latin_text([['Catullus'], ['C.', 'VALERIVS', 'CATVLLVS'],['1','2', '2b', '3' ],['I.', 'ad', 'Cornelium'],['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum', '?']])
    [['ad'], ['dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum']]
    """
    return drop_empty_lists(drop_probable_entities(
        drop_all_caps(drop_arabic_numeric(drop_non_lower((X))))))


def drop_probable_entities(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:
    >>> drop_empty_lists(drop_arabic_numeric(drop_probable_entities([['Catullus'], ['C.', 'VALERIVS', 'CATVLLVS'],['1','2', '2b', '3' ],['I.', 'ad', 'Cornelium'],['Cui', 'dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum', '?']])))
    [['ad'], ['dono', 'lepidum', 'novum', 'libellum', 'arida', 'modo', 'pumice', 'expolitum', '?']]
    """
    return [[word
             for word in sentence
             if word[0].lower() == word[0]]
            for sentence in X]


def jv_transform(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    >>> jv_transform([['venio', 'jacet'], ['julius', 'caesar']])
    [['uenio', 'iacet'], ['iulius', 'caesar']]
    """
    jvreplacer = JVReplacer()
    return [[jvreplacer.replace(word)
             for word in sentence]
            for sentence in X]


def drop_enclitics(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return: The matrix cleaned of enclitics
    >>> drop_enclitics([['arma', 'virum', '-que', 'cano']])
    [['arma', 'virum', 'cano']]
    """
    return [[word
             for word in sentence
             if not word.startswith('-')]
            for sentence in X]


def drop_short_sentences(X, min_len=2):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:
    >>> drop_short_sentences([['ita', 'vero'], ['quid', 'est', 'veritas'], ['vir', 'qui', 'adest']])
    [['quid', 'est', 'veritas'], ['vir', 'qui', 'adest']]
    """
    return [sentence for sentence in X if len(sentence) > min_len]


def drop_empty_strings(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:
    >>> drop_empty_strings([['', '', 'quid', 'est', 'veritas'], ['vir', 'qui', 'adest']])
    [['quid', 'est', 'veritas'], ['vir', 'qui', 'adest']]
    """
    return [[word
             for word in sentence
             if len(word) > 0]
            for sentence in X]


def drop_edge_punct(word):
    """
    Remove edge punctuation.
    :param word: a single string
    >>> drop_edge_punct("'fieri")
    'fieri'
    >>> drop_edge_punct('sedes.')
    'sedes'
    """
    if not word:
        return word
    try:
        if not word[0].isalpha():
            word = word[1:]
        if not word[-1].isalpha():
            word = word[:-1]
    except:
        pass
    return word


def profile_chars(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return: A Counter dictionary of character frequencies
    >>> from collections import Counter
    >>> result = profile_chars([['the', 'quick', 'brown'],['how', 'now', 'cow']])
    >>> result == Counter({'o': 4, 'w': 4, 'h': 2, 'c': 2, 'n': 2, 't': 1, 'e': 1, 'q': 1, 'u': 1, 'i': 1, 'k': 1, 'b': 1, 'r': 1})
    True
    """
    char_counter = Counter()
    for sentence in X:
        for word in sentence:
            for car in word:
                char_counter.update({car: 1})
    return char_counter


def split_camel(word):
    """
    Separate any words joined in Camel case fashion using a single space.
    >>> split_camel('esseCarthaginienses')
    'esse Carthaginienses'
    >>> split_camel('urbemCertimam')
    'urbem Certimam'
    """
    m = re.match('[a-z]+[A-Z][a-z]', word)
    if m:
        _, end = m.span()
        return word[:end - 2] + ' ' + word[end - 2:]
    return word


def separate_camel_cases(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:
    >>> separate_camel_cases([['amo', 'urbemRomam']])
    [['amo', 'urbem Romam']]
    """
    return [[split_camel(word)
             for word in sentence]
            for sentence in X]


def demacronize(X):
    """
    Transform macronized vowels into normal vowels
    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return: X
    >>> demacronize([['ōdī', 'et', 'amō',]])
    [['odi', 'et', 'amo']]
    """
    scansion = ScansionConstants()
    accent_dropper = str.maketrans(scansion.ACCENTED_VOWELS, scansion.VOWELS)
    return [[word.translate(accent_dropper)
             for word in sentence]
            for sentence in X]


def drop_all_punctuation(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:
    >>> drop_all_punctuation ([["I'm","ok!","Oh","%&*()[]{}!? Fine!"]])
    [['Im', 'ok', 'Oh', 'Fine']]
    """
    punct_spaces = remove_punctuation_dict()
    return [[drop_punctuation(word, transformation_table=punct_spaces)
             for word in sentence]
            for sentence in X]


def splice_hyphenated_word(word):
    """

    :param word:
    :return:
    >>> splice_hyphenated_word('fortis-eum')
    'fortis eum'
    >>> splice_hyphenated_word('prorogabatur—P')
    'prorogabatur P'
    """
    # return word.replace('-', ' ')
    hyphen_codes = [45, 8212]
    hyphens = [chr(val) for val in hyphen_codes]
    return re.sub('[{}]'.format(''.join(hyphens)), ' ', word)


def splice_hyphens(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:

    >>> splice_hyphens([['iam', 'fortis-eum'], ['ita', 'vero']])
    [['iam', 'fortis eum'], ['ita', 'vero']]
    """
    return [[splice_hyphenated_word(word)
             for word in sentence]
            for sentence in X]


def drop_punctuation(word, transformation_table=None):
    """

    :param word:
    :return:
    >>> drop_punctuation('~fudge')
    'fudge'
    """
    word = re.sub('[+~]', ' ', word)
    if transformation_table:
        word = word.translate(transformation_table)
    word = re.sub('\s+', ' ', word)
    word = word.strip()
    return word


def divide_separate_words(X):
    """
    As part of processing, some words obviously need to be separated.
    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:
    >>> divide_separate_words([['ita vero'], ['quid', 'est', 'veritas']])
    [['ita', 'vero'], ['quid', 'est', 'veritas']]
    """
    new_X = []
    for sentence in X:
        data_row = []
        for word in sentence:
            if ' ' in word:
                data_row += word.split()
            else:
                data_row.append(word)
        new_X.append(data_row)
    return new_X


def drop_fringe_punctuation(X):
    """
    Drop punctuation that occurs on the edges of words.
    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    >>> drop_fringe_punctuation([['this' , 'is', 'cool!'], ["'But", 'so', 'is', 'this'] ])
    [['this', 'is', 'cool'], ['But', 'so', 'is', 'this']]
    """
    return [[drop_edge_punct(word)
             for word in sentence]
            for sentence in X]


def drop_editorial(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return: matrix cleaned of individual strings with \<[A-Za-z]+\>

    >>> drop_editorial([['quid','est', 'ver<it>as'], ['vir', 'qui', 'adest']])
    [['quid', 'est', 'veras'], ['vir', 'qui', 'adest']]
    """
    return [[re.sub("\<[A-Za-z]+\>", '', word)
             for word in sentence]
            for sentence in X]


def accept_editorial(X):
    """

    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return: matrix with editorial suggestions accepted

    >>> accept_editorial([['quid','est', 'ver<it>as'], ['vir', 'qui', 'adest']])
    [['quid', 'est', 'veritas'], ['vir', 'qui', 'adest']]
    """
    return [[re.sub('\>', '', re.sub('\<', '', word))
             for word in sentence]
            for sentence in X]


def distinct_words(X):
    """
    Diagnostic function
    :param X:
    :return:
    >>> dl = distinct_words([['the', 'quick', 'brown'], ['here', 'lies', 'the', 'fox']])
    >>> sorted(dl)
    ['brown', 'fox', 'here', 'lies', 'quick', 'the']
    """
    return set([word
                for sentence in X
                for word in sentence])


def distinct_letters(X):
    """
    Diagnostic function
    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :return:
    >>> dl = distinct_letters([['the', 'quick', 'brown'],['how', 'now', 'cow']])
    >>> sorted(dl)
    ['b', 'c', 'e', 'h', 'i', 'k', 'n', 'o', 'q', 'r', 't', 'u', 'w']
    """
    return set([letter
                for sentence in X
                for word in sentence
                for letter in word])


def word_for_char(X, character):
    """
    Diagnostic function, collect the words where a character appears
    :param X: a data matrix: a list wrapping a list of strings, with each sublist being a sentence.
    :param character:
    :return:
    >>> word_for_char( [['the', 'quick', 'brown'],['how', 'now', 'cow']], 'n')
    ['brown', 'now']
    """
    return [word
            for sentence in X
            for word in sentence
            if character in word]
