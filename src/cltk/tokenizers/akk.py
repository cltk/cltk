""" Code for word tokenization: Akkadian
"""

__author__ = [
    "Andrew Deloucas <adeloucas@g.harvard.edu>",
    "Patrick J. Burns <patrick@diyclassics.org>",
]
__license__ = "MIT License."

import re

from cltk.tokenizers.word import WordTokenizer


class AkkadianWordTokenizer(WordTokenizer):
    """
    Akkadian word and cuneiform tokenizer.
    """

    def tokenize(self, text: str):
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

        words = text.split()
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

    def tokenize_sign(self, word: str):
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
        sign = ""
        language = word[1]
        determinative = False
        for char in word[0]:
            if determinative is True:
                if char == "}":
                    determinative = False
                    if len(sign) > 0:  # pylint: disable=len-as-condition
                        word_signs.append((sign, "determinative"))
                    sign = ""
                    language = word[1]
                    continue
                else:
                    sign += char
                    continue
            else:
                if language == "akkadian":
                    if char == "{":
                        if len(sign) > 0:  # pylint: disable=len-as-condition
                            word_signs.append((sign, language))
                        sign = ""
                        determinative = True
                        continue
                    elif char == "_":
                        if len(sign) > 0:  # pylint: disable=len-as-condition
                            word_signs.append((sign, language))
                        sign = ""
                        language = "sumerian"
                        continue
                    elif char == "-":
                        if len(sign) > 0:  # pylint: disable=len-as-condition
                            word_signs.append((sign, language))
                        sign = ""
                        language = word[1]  # or default word[1]?
                        continue
                    else:
                        sign += char
                elif language == "sumerian":
                    if char == "{":
                        if len(sign) > 0:  # pylint: disable=len-as-condition
                            word_signs.append((sign, language))
                        sign = ""
                        determinative = True
                        continue
                    elif char == "_":
                        if len(sign) > 0:  # pylint: disable=len-as-condition
                            word_signs.append((sign, language))
                        sign = ""
                        language = word[1]
                        continue
                    elif char == "-":
                        if len(sign) > 0:  # pylint: disable=len-as-condition
                            word_signs.append((sign, language))
                        sign = ""
                        language = word[1]
                        continue
                    else:
                        sign += char
        if len(sign) > 0:
            word_signs.append((sign, language))

        return word_signs

    @staticmethod
    def compute_indices(text: str, tokens):
        indices = []
        for i, token in enumerate(tokens):
            if 1 <= i:
                current_index = indices[-1] + len(tokens[i - 1][0])
                indices.append(current_index + text[current_index:].find(token[0]))
            else:
                indices.append(text.find(token[0]))
        return indices
