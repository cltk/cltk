""" Latin word tokenization - handles enclitics and abbreviations."""

__author__ = [
    "Patrick J. Burns <patrick@diyclassics.org>",
    "Todd Cook <todd.g.cook@gmail.com",
]
__license__ = "MIT License."

import re
from typing import List, Tuple

from nltk.tokenize.punkt import PunktLanguageVars, PunktParameters

from cltk.sentence.lat import LatinPunktSentenceTokenizer
from cltk.tokenizers.lat.params import ABBREVIATIONS, latin_exceptions
from cltk.tokenizers.lat.params import latin_replacements as REPLACEMENTS
from cltk.tokenizers.word import WordTokenizer


class LatinLanguageVars(PunktLanguageVars):
    _re_non_word_chars = PunktLanguageVars()._re_non_word_chars.replace("'", "")


class LatinWordTokenizer(WordTokenizer):
    """Tokenize according to rules specific to a given language."""

    ENCLITICS = ["que", "n", "ne", "ue", "ve", "st"]

    EXCEPTIONS = list(set(ENCLITICS + latin_exceptions))

    def __init__(self):
        self.punkt_param = PunktParameters()
        self.punkt_param.abbrev_types = set(ABBREVIATIONS)
        self.sent_tokenizer = LatinPunktSentenceTokenizer()
        self.word_tokenizer = LatinLanguageVars()

    def tokenize(
        self,
        text: str,
        replacements: List[Tuple[str, str]] = REPLACEMENTS,
        enclitics_exceptions: List[str] = EXCEPTIONS,
        enclitics: List[str] = ENCLITICS,
    ) -> List[str]:
        """
        Tokenizer divides the text into a list of substrings

        :param text: This accepts the string value that needs to be tokenized
        :param replacements: List of replacements to apply to tokens such as "mecum" -> ["cum", "me"]
        :param enclitics_exceptions: List of words that look likes they end with an enclitic but are not.
        :param enclitics: List of enclitics to check for in tokenization

        :returns: A list of substrings extracted from the text

        >>> toker = LatinWordTokenizer()
        >>> text = 'atque haec abuterque puerve paterne nihil'
        >>> toker.tokenize(text)
        ['atque', 'haec', 'abuter', '-que', 'puer', '-ve', 'pater', '-ne', 'nihil']

        >>> toker.tokenize('Cicero dixit orationem pro Sex. Roscio')
        ['Cicero', 'dixit', 'orationem', 'pro', 'Sex.', 'Roscio']

        >>> toker.tokenize('nihilne te nocturnum praesidium Palati')
        ['nihil', '-ne', 'te', 'nocturnum', 'praesidium', 'Palati']

        >>> toker.tokenize('Cenavin ego heri in navi in portu Persico?')
        ['Cenavi', '-ne', 'ego', 'heri', 'in', 'navi', 'in', 'portu', 'Persico', '?']

        >>> toker.tokenize('Dic si audes mihi, bellan videtur specie mulier?')
        ['Dic', 'si', 'audes', 'mihi', ',', 'bella', '-ne', 'videtur', 'specie', 'mulier', '?']

        >>> toker.tokenize("mecum")
        ['cum', 'me']

        You can specify how replacements are made using replacements

        >>> toker.tokenize("mecum", replacements=[(r"mecum", "me cum")])
        ['me', 'cum']

        Or change enclitics and enclitics exception:
        >>> toker.tokenize("atque haec abuterque puerve paterne nihil", enclitics=["que"])
        ['atque', 'haec', 'abuter', '-que', 'puerve', 'paterne', 'nihil']

        >>> toker.tokenize("atque haec abuterque puerve paterne nihil", enclitics=["que", "ve", "ne"],
        ...    enclitics_exceptions=('paterne', 'atque'))
        ['atque', 'haec', 'abuter', '-que', 'puer', '-ve', 'paterne', 'nihil']

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

        for replacement in replacements:
            text = re.sub(
                replacement[0], matchcase(replacement[1]), text, flags=re.IGNORECASE
            )

        sents = self.sent_tokenizer.tokenize(text)
        tokens = []  # type: List[str]

        for sent in sents:
            temp_tokens = self.word_tokenizer.word_tokenize(sent)
            # Need to check that tokens exist before handling them;
            # needed to make stream.readlines work in PlaintextCorpusReader
            if temp_tokens:
                if temp_tokens[0].endswith("ne"):
                    if temp_tokens[0].lower() not in enclitics_exceptions:
                        temp = [temp_tokens[0][:-2], "-ne"]
                        temp_tokens = temp + temp_tokens[1:]
                if temp_tokens[-1].endswith("."):
                    final_word = temp_tokens[-1][:-1]
                    del temp_tokens[-1]
                    temp_tokens += [final_word, "."]

                for token in temp_tokens:
                    tokens.append(token)

        # Break enclitic handling into own function?
        specific_tokens = []  # type: List[str]

        for token in tokens:
            is_enclitic = False
            if token.lower() not in enclitics_exceptions:
                for enclitic in enclitics:
                    if token.endswith(enclitic):
                        if enclitic == "n":
                            specific_tokens += [token[: -len(enclitic)]] + ["-ne"]
                        elif enclitic == "st":
                            if token.endswith("ust"):
                                specific_tokens += [token[: -len(enclitic) + 1]] + [
                                    "est"
                                ]
                            else:
                                specific_tokens += [token[: -len(enclitic)]] + ["est"]
                        else:
                            specific_tokens += [token]
                        is_enclitic = True
                        break
            if not is_enclitic:
                specific_tokens.append(token)

        # collapse abbreviations
        abbrev_idx = []
        for idx, token in enumerate(specific_tokens):
            if token.lower() in self.punkt_param.abbrev_types:
                abbrev_idx.append(idx)
        for val in reversed(abbrev_idx):
            if val + 1 < len(specific_tokens) and specific_tokens[val + 1] == ".":
                specific_tokens[val] = specific_tokens[val] + "."
                specific_tokens[val + 1] = ""
        specific_tokens = [tmp for tmp in specific_tokens if tmp]
        return specific_tokens

    @staticmethod
    def compute_indices(text: str, tokens):
        indices = []
        for i, token in enumerate(tokens):
            if 1 <= i:
                current_index = indices[-1] + len(tokens[i - 1])
                if token == "-ne":
                    indices.append(current_index + text[current_index:].find(token[1:]))
                else:
                    indices.append(current_index + text[current_index:].find(token))
            else:
                indices.append(text.find(token))
        return indices
