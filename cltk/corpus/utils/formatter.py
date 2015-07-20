"""Process downloaded or local corpora from one format into another.
Some formatting can happen here, or invoke language-specific formatters in
other files.

TODO: Add function to build all tlg/phi files from the index
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'

from builtins import bytes
from cltk.corpus.greek.tlg_index import TLG_INDEX
from cltk.corpus.greek.tlg_index import TLG_WORKS_INDEX
from cltk.corpus.latin.phi5_index import PHI5_INDEX
from cltk.corpus.latin.phi5_index import PHI5_WORKS_INDEX
from cltk.utils.cltk_logger import logger
import os
import re


# research how to build regex values for re.compile() from this dict
TLG_PHI_REPLACEMENTS = {
    'newline_hyphen': '-\n',
    'newline': '\n',  # you probably want to substitute this with an empty space ' '
    'within_pointed_brackets': '\{.+?\}',
    'chevrons': '«|»',
    'ellipsis': ' ... ',
    'latin_09': '[a-zA-Z0-9]',
    'within_parentheses': '\(.+?\)',
    'pointed_brackets': '\<|\>',
    'curled_single_quotes': '‘|’',
    'underscore': '_',
}


def remove_non_ascii(input_string):
    """remove non-ascii: http://stackoverflow.com/a/1342373"""
    no_ascii = "".join(i for i in input_string if ord(i) < 128)
    return no_ascii


def tlg_plaintext_cleanup(text, rm_punctuation=False, rm_periods=False):
    """Remove and substitute post-processing for Greek TLG text.
    TODO: Surely more junk to pull out. Please submit bugs!
    TODO: \{.+?\}|\(.+?\) always working?
    TODO: This is a rather slow now, help in speeding up welcome.
    """
    remove_comp = re.compile(r'-\n|«|»|<|>|\.\.\.|‘|’|_|\{.+?\}|\(.+?\)|[a-zA-Z0-9]')
    text = remove_comp.sub('', text)

    new_text = None
    if rm_punctuation:
        new_text = ''
        punctuation = [',', '·', ':', '"', "'", '?', '-', '!', '*', '[', ']', '{', '}']
        if rm_periods:
            punctuation += ['.', ';']
        for char in text:
            # second try at rming some punctuation; merge with above regex
            if char in punctuation:
                pass
            else:
                new_text += char
    if new_text:
        text = new_text

    # replace line breaks w/ space
    replace_comp = re.compile(r'\n')
    text = replace_comp.sub(' ', text)

    comp_space = re.compile(r'\s+')
    text = comp_space.sub(' ', text)

    return text


def phi5_plaintext_cleanup(text, rm_punctuation=False, rm_periods=False):
    """Remove and substitute post-processing for Greek PHI5 text.
    TODO: Surely more junk to pull out. Please submit bugs!
    TODO: This is a rather slow now, help in speeding up welcome.
    """
    # This works OK, doesn't get some
    # Note: rming all characters between {} and ()
    remove_comp = re.compile(r'-\n|«|»|\<|\>|\.\.\.|‘|’|_|\{.+?\}|\(.+?\)|[0-9]')
    text = remove_comp.sub('', text)

    new_text = None
    if rm_punctuation:
        new_text = ''
        punctuation = [',', ';', ':', '"', "'", '?', '-', '!', '*', '[', ']', '{', '}']
        if rm_periods:
            punctuation += ['.']
        for char in text:
            # rm acute combining acute accents made by TLGU
            # Could be caught by regex, tried and failed, not sure why
            if bytes(char, 'utf-8') == b'\xcc\x81':
                pass
            # second try at rming some punctuation; merge with above regex
            elif char in punctuation:
                pass
            else:
                new_text += char
    if new_text:
        text = new_text

    # replace line breaks w/ space
    replace_comp = re.compile(r'\n')
    text = replace_comp.sub(' ', text)

    comp_space = re.compile(r'\s+')
    text = comp_space.sub(' ', text)

    return text


def assemble_tlg_author_filepaths():
    """Reads TLG index and builds a list of absolute filepaths."""
    plaintext_dir_rel = '~/cltk_data/greek/text/tlg/plaintext/'
    plaintext_dir = os.path.expanduser(plaintext_dir_rel)
    filepaths = [os.path.join(plaintext_dir, x + '.TXT') for x in TLG_INDEX]
    return filepaths


def assemble_phi5_author_filepaths():
    """Reads PHI5 index and builds a list of absolute filepaths.
    """
    plaintext_dir_rel = '~/cltk_data/latin/text/phi5/plaintext/'
    plaintext_dir = os.path.expanduser(plaintext_dir_rel)
    filepaths = [os.path.join(plaintext_dir, x + '.TXT') for x in PHI5_INDEX]
    return filepaths


def assemble_tlg_works_filepaths():
    """Reads TLG index and builds a list of absolute filepaths."""
    plaintext_dir_rel = '~/cltk_data/greek/text/tlg/individual_works/'
    plaintext_dir = os.path.expanduser(plaintext_dir_rel)
    all_filepaths = []
    for author_code in TLG_WORKS_INDEX:
        author_data = TLG_WORKS_INDEX[author_code]
        works = author_data['works']
        for work in works:
            f = os.path.join(plaintext_dir, author_code + '.TXT' + '-' + work + '.txt')
            all_filepaths.append(f)
    return all_filepaths


def assemble_phi5_works_filepaths():
    """Reads PHI5 index and builds a list of absolute filepaths."""
    plaintext_dir_rel = '~/cltk_data/latin/text/phi5/individual_works/'
    plaintext_dir = os.path.expanduser(plaintext_dir_rel)
    all_filepaths = []
    for author_code in PHI5_WORKS_INDEX:
        author_data = PHI5_WORKS_INDEX[author_code]
        works = author_data['works']
        for work in works:
            f = os.path.join(plaintext_dir, author_code + '.TXT' + '-' + work + '.txt')
            all_filepaths.append(f)
    return all_filepaths

if __name__ == '__main__':
    pass
