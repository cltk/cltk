"""Process downloaded or local corpora from one format into another.
Some formatting can happen here, or invoke language-specific formatters in
other files.

#TODO: Add generic HTML stripper
#TODO mk class accepting language as argument
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


# from cltk.corpus.greek.tlgu import tlgu
import re


def remove_non_ascii(input_string):
    """remove non-ascii: http://stackoverflow.com/a/1342373"""
    no_ascii = "".join(i for i in input_string if ord(i) < 128)
    return no_ascii


def cleanup_tlg_txt(tlg_str):
    """"Remove all non–Greek characters from a TLG corpus."""
    # fix beta code transliteration problems
    tlg_str = re.sub(r'ι\+', 'ϊ', tlg_str)
    tlg_str = re.sub(r'ί\+', 'ΐ', tlg_str)
    tlg_str = re.sub(r'\\.', '.', tlg_str)
    # fix tlg markup
    tlg_str = re.sub(r'@1 \{1.+?\}1 @', '', tlg_str)  # rm book titles
    tlg_str = re.sub(r'\[.+?\]', '', tlg_str)  # rm words in square brackets
    tlg_str = re.sub(r'[0-9]', '', tlg_str)
    tlg_str = re.sub(r'@|%|\x00', '', tlg_str)
    tlg_str = re.sub('—', ' — ', tlg_str)
    return tlg_str
