"""Tokenize lines."""

__author__ = [
    "Patrick J. Burns <patrick@diyclassics.org>",
    "Andrew Deloucas <adeloucas@g.harvard.edu>",
]
__license__ = "MIT License. See LICENSE."


class LineTokenizer:
    """Tokenize text by line; designed for study of poetry."""

    def __init__(self, language):
        """Lower incoming language name and assemble variables.
        :type language: str
        :param language : Language for sentences tokenization.
        """
        self.language = (
            language.lower()
        )  # Keep in case there winds up being a need for language-specific line tokenization

    def tokenize(self: object, untokenized_string: str, include_blanks=False):
        """Tokenize lines by '\n'.

        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :param include_blanks: Boolean; If True, blanks will be preserved by "" in returned list of strings; Default is False.
        :rtype : list of strings
        """

        # load tokenizer
        assert isinstance(
            untokenized_string, str
        ), "Incoming argument must be a string."

        # make list of tokenized sentences
        if include_blanks:
            tokenized_lines = untokenized_string.splitlines()
        else:
            tokenized_lines = [
                line for line in untokenized_string.splitlines() if line != ""
            ]
        return tokenized_lines
