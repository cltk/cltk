""" Latin word tokenization - handles enclitics and abbreviations."""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Todd Cook <todd.g.cook@gmail.com']
__license__ = 'MIT License.'

import re
from typing import List

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

from cltk.tokenize.latin.params import ABBREVIATIONS
from cltk.tokenize.latin.params import latin_exceptions
from cltk.tokenize.latin.params import latin_replacements as REPLACEMENTS
from cltk.tokenize.latin.sentence import SentenceTokenizer
from cltk.tokenize.latin.params import LatinLanguageVars


class WordTokenizer:
    """Tokenize according to rules specific to a given language."""

    ENCLITICS = ['que', 'n', 'ne', 'ue', 've', 'st']

    EXCEPTIONS = list(set(ENCLITICS + latin_exceptions))

    def __init__(self):
        self.language = 'latin'
        self.punkt_param = PunktParameters()
        self.punkt_param.abbrev_types = set(ABBREVIATIONS)
        self.sent_tokenizer = PunktSentenceTokenizer(self.punkt_param)
        self.word_tokenizer = LatinLanguageVars()

    def tokenize(self, text:str) ->List[str]:
        """
        Tokenizer divides the text into a list of substrings

        :param text: This accepts the string value that needs to be tokenized
        :returns: A list of substrings extracted from the text

        >>> toker = WordTokenizer()
        >>> text = 'atque haec abuterque puerve paterne nihil'
        >>> toker.tokenize(text)
        ['atque', 'haec', 'abuter', '-que', 'puer', '-ve', 'pater', '-ne', 'nihil']

        >>> toker.tokenize('Cicero dixit orationem pro Sex. Roscio')
        ['Cicero', 'dixit', 'orationem', 'pro', 'Sex.', 'Roscio']

        >>> toker.tokenize('Cenavin ego heri in navi in portu Persico?')
        ['Cenavi', '-ne', 'ego', 'heri', 'in', 'navi', 'in', 'portu', 'Persico', '?']

        >>> toker.tokenize('Dic si audes mihi, bellan videtur specie mulier?')
        ['Dic', 'si', 'audes', 'mihi', ',', 'bella', '-ne', 'videtur', 'specie', 'mulier', '?']

        """

        def matchcase(word):
            """helper function From Python Cookbook"""

            def replace(matching):
                text = matching.group()
                if text.isupper():
                    return word.upper()
                elif text.islower():
                    return word.lower()
                elif text[0].isupper():
                    return word.capitalize()
                return word

            return replace

        for replacement in REPLACEMENTS:
            text = re.sub(replacement[0], matchcase(replacement[1]), text, flags=re.IGNORECASE)

        sents = self.sent_tokenizer.tokenize(text)
        tokens = [] # type: List[str]

        for sent in sents:
            temp_tokens = self.word_tokenizer.word_tokenize(sent)
            # Need to check that tokens exist before handling them;
            # needed to make stream.readlines work in PlaintextCorpusReader
            if temp_tokens:
                if temp_tokens[0].endswith('ne'):
                    if temp_tokens[0].lower() not in WordTokenizer.EXCEPTIONS:
                        temp = [temp_tokens[0][:-2], '-ne']
                        temp_tokens = temp + temp_tokens[1:]
                if temp_tokens[-1].endswith('.'):
                    final_word = temp_tokens[-1][:-1]
                    del temp_tokens[-1]
                    temp_tokens += [final_word, '.']

                for token in temp_tokens:
                    tokens.append(token)

        # Break enclitic handling into own function?
        specific_tokens = [] # type: List[str]

        for token in tokens:
            is_enclitic = False
            if token.lower() not in WordTokenizer.EXCEPTIONS:
                for enclitic in WordTokenizer.ENCLITICS:
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
