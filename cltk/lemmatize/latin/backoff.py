"""Module for lemmatizing Latin
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

import os
import re
from typing import List, Dict, Tuple, Set, Any, Generator
import reprlib

from cltk.lemmatize.backoff import DefaultLemmatizer, IdentityLemmatizer, DictLemmatizer, RegexpLemmatizer, UnigramLemmatizer
from cltk.lemmatize.latin.latin import latin_sub_patterns, latin_pps, rn_patterns

from cltk.utils.file_operations import open_pickle


class RomanNumeralLemmatizer(RegexpLemmatizer):
    """Lemmatizer for identifying roman numerals in Latin text based on
    regex.
    """
    def __init__(self: object, default: str = None, backoff: object = None):
        """
        RomanNumeralLemmatizer
        :type default: str
        :param default: Default replacement for lemma; 'NUM' in given pattern
        """
        regexps = [
            (r'(?=^[MDCLXVUI]+$)(?=^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|IU|V?I{0,3}|U?I{0,3})$)', 'NUM'),
            (r'(?=^[mdclxvui]+$)(?=^m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|iu|v?i{0,3}|u?i{0,3})$)', 'NUM')
            ]
        RegexpLemmatizer.__init__(self, regexps, backoff)
        self._regexs = [(re.compile(regexp), pattern,) for regexp, pattern in regexps]
        self.default = default

    def choose_tag(self: object, tokens: List[str], index: int, history: List[str]):
        """Use regular expressions for rules-based lemmatizing based on word endings;
        tokens are matched for patterns with the base kept as a group; an word ending
        replacement is added to the (base) group.
        :rtype: str
        :type tokens: list
        :param tokens: List of tokens to be lemmatized
        :type index: int
        :param index: Int with current token
        :type history: list
        :param history: List with tokens that have already been lemmatized; NOT USED
        """
        for pattern, replace in self._regexs:
            if re.search(pattern, tokens[index]):
                if self.default:
                    return self.default
                else:
                    return replace

    def __repr__(self: object):
        return f'<{type(self).__name__}: CLTK Roman Numeral Patterns>'

class BackoffLatinLemmatizer(object):
    """Suggested backoff chain; includes at least on of each
    type of major sequential backoff class from backoff.py

    ### Putting it all together
    ### BETA Version of the Backoff Lemmatizer AKA BackoffLatinLemmatizer
    ### For comparison, there is also a TrainLemmatizer that replicates the
    ###    original Latin lemmatizer from cltk.stem
    """

    models_path = os.path.normpath(get_cltk_data_dir() + '/latin/model/latin_models_cltk/lemmata/backoff')

    def __init__(self: object, train: List[list] = None, seed: int = 3, verbose: bool = False):
        self.models_path = BackoffLatinLemmatizer.models_path

        missing_models_message = "BackoffLatinLemmatizer requires the ```latin_models_cltk``` to be in cltk_data. Please load this corpus."

        try:
            self.train =  open_pickle(os.path.join(self.models_path, 'latin_pos_lemmatized_sents.pickle'))
            self.LATIN_OLD_MODEL =  open_pickle(os.path.join(self.models_path, 'latin_lemmata_cltk.pickle'))
            self.LATIN_MODEL =  open_pickle(os.path.join(self.models_path, 'latin_model.pickle'))
        except FileNotFoundError as err:
            raise type(err)(missing_models_message)

        self.latin_sub_patterns = latin_sub_patterns # Move to latin_models_cltk

        self.seed = seed
        self.VERBOSE=verbose

        def _randomize_data(train: List[list], seed: int):
            import random
            random.seed(seed)
            random.shuffle(train)
            pos_train_sents = train[:4000]
            lem_train_sents = [[(item[0], item[1]) for item in sent] for sent in train]
            train_sents = lem_train_sents[:4000]
            test_sents = lem_train_sents[4000:5000]

            return pos_train_sents, train_sents, test_sents

        self.pos_train_sents, self.train_sents, self.test_sents = _randomize_data(self.train, self.seed)
        self._define_lemmatizer()

    def _define_lemmatizer(self: object):
        # Suggested backoff chain--should be tested for optimal order
        self.backoff0 = None
        self.backoff1 = IdentityLemmatizer(verbose=self.VERBOSE)
        self.backoff2 = DictLemmatizer(lemmas=self.LATIN_OLD_MODEL, source='Morpheus Lemmas', backoff=self.backoff1, verbose=self.VERBOSE)
        self.backoff3 = RegexpLemmatizer(self.latin_sub_patterns, source='CLTK Latin Regex Patterns', backoff=self.backoff2, verbose=self.VERBOSE)
        self.backoff4 = UnigramLemmatizer(self.train_sents, source='CLTK Sentence Training Data', backoff=self.backoff3, verbose=self.VERBOSE)
        self.backoff5 = DictLemmatizer(lemmas=self.LATIN_MODEL, source='Latin Model', backoff=self.backoff4, verbose=self.VERBOSE)
        self.lemmatizer = self.backoff5

    def lemmatize(self: object, tokens: List[str]):
        lemmas = self.lemmatizer.lemmatize(tokens)
        return lemmas

    def evaluate(self: object):
        if self.VERBOSE:
            raise AssertionError("evaluate() method only works when verbose: bool = False")
        return self.lemmatizer.evaluate(self.test_sents)

    def __repr__(self: object):
        return f'<BackoffLatinLemmatizer v0.2>'

if __name__ == '__main__':

    from pprint import pprint
    l1 = DefaultLemmatizer('UNK', verbose=True)
    l2 = DictLemmatizer(lemmas={'arma': 'arma', 'uirum': 'uir'}, backoff=l1, verbose=True)
    l3 = UnigramLemmatizer(train=[[('cano', 'cano'), ('.', 'punc')],], backoff=l2, verbose=True)
    l4 = RegexpLemmatizer(regexps=[('(.)tat(is|i|em|e|es|um|ibus)$', r'\1tas'),], backoff=l3, verbose=True)
    lemmas = l4.lemmatize('arma uirum -que cano nobilitatis .'.split())
    pprint(lemmas)

    # [('arma', 'arma', <UnigramLemmatizer: [[('res', 'res'), ...], ...]>),
    # ('uirum', 'uir', <UnigramLemmatizer: [[('res', 'res'), ...], ...]>),
    # ('-que', '-que', <DictLemmatizer: {'!': 'punc', ...}>),
    # ('cano', 'cano', <DictLemmatizer: {'-nam': 'nam', ...}>),
    # ('nobilitatis',
    # 'nobilitas',
    # <RegexpLemmatizer: [('(bil)(is|i|e...es|ium|ibus)$', '\\1is'), ...]>),
    # ('.', 'punc', <DictLemmatizer: {'!': 'punc', ...}>)]

    print('\n')

    bll = BackoffLatinLemmatizer(seed=5, verbose=False)
    lemmas = bll.lemmatize('arma uirum -que cano nobilitatis .'.split())
    pprint(lemmas)

    # [('arma', 'arma', <UnigramLemmatizer: CLTK Sentence Training Data>),
    # ('uirum', 'uir', <UnigramLemmatizer: CLTK Sentence Training Data>),
    # ('-que', '-que', <DictLemmatizer: Latin Model>),
    # ('cano', 'cano', <DictLemmatizer: Morpheus Lemmas>),
    # ('nobilitatis', 'nobilitas', <RegexpLemmatizer: CLTK Latin Regex Patterns>),
    # ('.', 'punc', <DictLemmatizer: Latin Model>)]

    rn = RomanNumeralLemmatizer()
    print(rn.lemmatize(['MMCI']))
