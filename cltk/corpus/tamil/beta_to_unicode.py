"""Converts legacy encodings into Unicode."""

import regex

__author__ = ['DilshanAbeysinghe', 'Kyle P. Johnson <kyle@kyle-p-johnson.com>', ]

VOWELS = [
    # Perseus-style head words
    # CAPS smooth
    (r'\*\)A', 'அ'),
    (r'\*\)E', 'ஆ'),
    (r'\*\)H', 'இ'),
    (r'\*\)I', 'ஈ'),
    (r'\*\)O', 'உ'),
    (r'\*\)W', 'ஊ'),
    # CAPS rough
    (r'\*\(A', 'எ'),
    (r'\*\(E', 'ஏ'),
    (r'\*\(H', 'ஐ'),
    (r'\*\(I', 'ஒ'),
    (r'\*\(O', 'ஓ'),
    (r'\*\(R', 'ஔ')
]

CONSTANTS= [
    (r'I\+', 'க்'),
    (r'I\\\+', 'ங்'),
    (r'I/\+', 'ச்'),
    # Add a second entry for out-of-order betacode
    (r'I\+/', 'ஞ்'),
    (r'I=\+', 'ட்'),
    (r'U\+', 'ண்'),
    (r'U\\\+', 'த்'),
    (r'U/\+', 'ந்'),
    (r'U=\+', 'ப்'),
    (r'A\'', 'ம்'),
    (r'I\'', 'ய்'),
    (r'U\'', 'ர்'),
    (r'A&', 'ல்'),
    (r'I&', 'வ்'),
    (r'U&', 'ழ்'),
    (r'R\)', 'ள்'),
    (r'R\(', 'ற்'),
    (r'A\)\|', 'ன்')
]

GRANTHA_CONSONANTS = [
    (r':', 'ஜ்'),
    (r'\.', 'ஶ்'),
    (r',', 'ஷ்'),
    (r';', 'ஸ்'),
    (r'\'', 'ஹ்'),
    (r'-', 'க்ஷ்')
]


class Replacer(object):  # pylint: disable=R0903
    """Replace Beta Code with Unicode."""
    def __init__(self, pattern1=None, pattern2=None, pattern3=None):
        if pattern1 is None:
            pattern1 = VOWELS
        if pattern2 is None:
            pattern2 = CONSTANTS
        if pattern3 is None:
            pattern3 = GRANTHA_CONSONANTS
        self.pattern1 = \
            [(regex.compile(beta_regex, flags=regex.VERSION1), repl)
             for (beta_regex, repl) in pattern1]
        self.pattern2 = \
            [(regex.compile(beta_regex, flags=regex.VERSION1), repl)
             for (beta_regex, repl) in pattern2]
        self.pattern3 = \
            [(regex.compile(beta_regex, flags=regex.VERSION1), repl)
             for (beta_regex, repl) in pattern3]

    def beta_code(self, text):
        """Replace method. Note: regex.subn() returns a tuple (new_string,
        number_of_subs_made).
        """
        text = text.replace('-', '')
        for (pattern, repl) in self.pattern1:
            text = pattern.subn(repl, text)[0]
        for (pattern, repl) in self.pattern2:
            text = pattern.subn(repl, text)[0]
        # remove third run, if punct list not used
        for (pattern, repl) in self.pattern3:
            text = pattern.subn(repl, text)[0]
return text