"""Process downloaded or local corpora from one format into another.
Some formatting can happen here, or invoke language-specific formatters in
other files.

#TODO: Add generic HTML stripper
#TODO mk class accepting language as argument
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


from cltk.corpus.utils.cltk_logger import logger
import os
import re
import sys


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


def build_phi5_index(index_path_rel = '~/cltk_data/originals/phi5/AUTHTAB.DIR'):
    """Return dict of 362 files in format of {file: author_name}. This has
    been pre-generated and saved at ``~/cltk/corpus/latin/phi5_index.py``.
    TODO: Update this to account for works within each author's file.
    """
    index_path = os.path.expanduser(index_path_rel)
    if not os.path.isfile(index_path):
        logger.info("Failed to locate original PHI5 index at '%s'. Please import PHI5 first." % index_path)
        sys.exit(1)
    with open(index_path, 'rb') as f:
        r = f.read()
        index_all = r.decode('latin-1').split('\xff')[1:-21]
        index = [x for x in index_all if x]
        file_author = {}
        for x in index:
            # file name
            pattern_file = re.compile('LAT[\d].{4}')
            m = pattern_file.match(x)
            file_name = m.group()[:-1] + '.TXT'

            # author name
            author_name = pattern_file.split(x)[-1]
            pattern_author = re.compile('&1|&l|l$|&|1$|\x83')
            author_name = pattern_author.sub('', author_name)
            pattern_comma = re.compile('\x80')
            author_name = pattern_comma.sub(', ', author_name)
            file_author[file_name] = author_name

    return file_author


def build_tlg_index(index_path_rel='~/cltk_data/originals/tlg/AUTHTAB.DIR'):
    """Return dict of 362 files in format of {file: author_name}. This has
    been pre-generated and saved at ``~/cltk/corpus/latin/phi5_index.py``.
    TODO: Update this to account for works within each author's file.
    TODO: merge with phi5 build index
"""
    index_path = os.path.expanduser(index_path_rel)
    with open(index_path, 'rb') as f:
        r = f.read()
        index_all = r.decode('latin-1').split('\xff')[1:-6]  # diff from phi5
        index = [x for x in index_all if x]
        file_author = {}
        for x in index:
            # file name
            pattern_file = re.compile('TLG[\d].{4}')
            m = pattern_file.match(x)
            file_name = m.group()[:-1] + '.TXT'

            # author name
            author_name = pattern_file.split(x)[-1]
            pattern_author = re.compile('&1|&l|l$|&|1$|\x83|\[2|\]2')  # diff from phi5
            author_name = pattern_author.sub('', author_name)
            pattern_comma = re.compile('\x80')
            author_name = pattern_comma.sub(', ', author_name)
            file_author[file_name] = author_name

    return file_author