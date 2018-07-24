"""Tokenize lines."""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Andrew Deloucas <adeloucas@g.harvard.edu>']
__license__ = 'MIT License. See LICENSE.'

import re


class LineTokenizer():
    """Tokenize text by line; designed for study of poetry."""
    
    
    def __init__(self, language):
        """Lower incoming language name and assemble variables.
        :type language: str
        :param language : Language for sentence tokenization.
        """
        self.language = language.lower() # Keep in case there winds up being a need for language-specific line tokenization

    def tokenize(self: object, untokenized_string: str, include_blanks=False):
        """Tokenize lines by '\n'.
        :type untokenized_string: str
        :param untokenized_string: A string containing one of more sentences.
        :param include_blanks: Boolean; If True, blanks will be preserved by "" in returned list of strings; Default is False.
        :rtype : list of strings
        """
        
        # load tokenizer
        assert isinstance(untokenized_string, str), 'Incoming argument must be a string.'

        # make list of tokenized sentences
        if include_blanks:
            tokenized_lines = untokenized_string.splitlines()
        else:
            tokenized_lines = [line for line in untokenized_string.splitlines() if line != '']
        return tokenized_lines

class Akkadian_LineTokenizer(object):
    """
    The tokenizer has the option of preserving damage marked by CDLI.
    ATF-format signs denoting damage and their meaning:
        # = Signs which are damaged
        [] = Signs which are completely broken away
        x = Signs which cannot be identified
        n = Numbers which cannot be identified
        ! = Indicates uncertainty of reading
        ? = Indicates correction
        * = Indicates a collated reading

    Likewise, the tokenizer has the option of preserving metadata stored in
    the ATF file.

    For in depth reading on ATF-formatting for CDLI and ORACC:
        Oracc ATF Primer = http://oracc.museum.upenn.edu/doc/help/editinginatf/
        primer/index.html
        ATF Structure = http://oracc.museum.upenn.edu/doc/help/editinginatf/
        primer/structuretutorial/index.html
        ATF Inline = http://oracc.museum.upenn.edu/doc/help/editinginatf/
        primer/inlinetutorial/index.html
    """
    def __init__(self, preserve_damage=False):
        """
        :param preserve_damage: turns on or off damage markers in text.
        """
        self.damage = preserve_damage

    def string_tokenizer(self, untokenized_string: str, include_blanks=False):
        """
        This function is based off CLTK's line tokenizer. Use this for strings
        rather than .txt files.

        input: '20. u2-sza-bi-la-kum\n1. a-na ia-as2-ma-ah-{d}iszkur#\n2.
        qi2-bi2-ma\n3. um-ma {d}utu-szi-{d}iszkur\n'
        output:['20. u2-sza-bi-la-kum', '1. a-na ia-as2-ma-ah-{d}iszkur#',
        '2. qi2-bi2-ma']

        :param untokenized_string: string
        :param include_blanks: instances of empty lines
        :return: lines as strings in list
        """
        line_output = []
        assert isinstance(untokenized_string, str), \
            'Incoming argument must be a string.'
        if include_blanks:
            tokenized_lines = untokenized_string.splitlines()
        else:
            tokenized_lines = [line for line in untokenized_string.splitlines()
                               if line != r'\\n']
        for line in tokenized_lines:
            # Strip out damage characters
            if not self.damage:  # Add 'xn' -- missing sign or number?
                line = ''.join(c for c in line if c not in "#[]?!*")
                re.match(r'^\d*\.|\d\'\.', line)
                line_output.append(line.rstrip())
        return line_output

    def line_tokenizer(self, text):
        """
        From a .txt file, outputs lines as string in list.

        input:  21. u2-wa-a-ru at-ta e2-kal2-la-ka _e2_-ka wu-e-er
                22. ... u2-ul szi-...
                23. ... x ...
        output:['21. u2-wa-a-ru at-ta e2-kal2-la-ka _e2_-ka wu-e-er',
                '22. ... u2-ul szi-...',
                '23. ... x ...',]

        :param: .txt file containing untokenized string
        :return: lines as strings in list
        """
        line_output = []

        with open(text, mode='r+', encoding='utf8') as file:
            lines = file.readlines()
            assert isinstance(text, str), 'Incoming argument must be a string.'
        for line in lines:
            # Strip out damage characters
            if not self.damage:  # Add 'xn' -- missing sign or number?
                line = ''.join(c for c in line if c not in "#[]?!*")
                re.match(r'^\d*\.|\d\'\.', line)
                line_output.append(line.rstrip())
        return line_output
