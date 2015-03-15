"""Process downloaded or local corpora from one format into another.
Some formatting can happen here, or invoke language-specific formatters in
other files.

#TODO: Add generic HTML stripper
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


from cltk.corpus.greek.tlg_indices import TLG_INDEX
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
    tlg_str = re.sub(r'ι|\+', 'ϊ', tlg_str)
    tlg_str = re.sub(r'ί\+', 'ΐ', tlg_str)
    tlg_str = re.sub(r'\\.', '.', tlg_str)
    # fix tlg markup
    tlg_str = re.sub(r'@1 \{1.+?\}1 @', '', tlg_str)  # rm book titles
    tlg_str = re.sub(r'\[.+?\]', '', tlg_str)  # rm words in square brackets
    tlg_str = re.sub(r'[0-9]', '', tlg_str)
    tlg_str = re.sub(r'@|%|\x00', '', tlg_str)
    tlg_str = re.sub('—', ' — ', tlg_str)
    return tlg_str


def build_corpus_index(corpus, authtab_path=None):
    """Build index for TLG or PHI5. ``authtab_path`` for testing only.
    TODO: Add a test flag argument and rm authtab_path
    :param corpus:
    :return: dict
    """
    if corpus == 'tlg':
        if not authtab_path:
            authtab_path = '~/cltk_data/originals/tlg/AUTHTAB.DIR'
        slice_start = 1
        slice_end = -6
        file_name_match = 'TLG[\d].{4}'
        pattern_author_regex = '&1|&l|l$|&|1$|\x83|\[2|\]2'
    elif corpus == 'phi5':
        if not authtab_path:
            authtab_path = '~/cltk_data/originals/phi5/AUTHTAB.DIR'
        slice_start = 1
        slice_end = -21
        file_name_match = 'LAT[\d].{4}'
        pattern_author_regex = '&1|&l|l$|&|1$|\x83'
    else:
        logger.warning("Corpus {0} not available. Choose from 'tlg' or 'phi5'.".format(corpus))
        sys.exit(1)
    index_path = os.path.expanduser(authtab_path)
    if not os.path.isfile(index_path):
        logger.info("Failed to locate original {0} index at '{1}'. Please import first.".format(corpus, index_path))
        sys.exit(1)
    with open(index_path, 'rb') as f:
        r = f.read()
    index_all = r.decode('latin-1').split('\xff')[slice_start:slice_end]
    index = [x for x in index_all if x]
    file_author = {}
    for x in index:
        # file name
        pattern_file = re.compile(file_name_match)
        m = pattern_file.match(x)
        file_name = m.group()[:-1]# + '.TXT'

        # author name
        author_name = pattern_file.split(x)[-1]
        pattern_author = re.compile(pattern_author_regex)
        author_name = pattern_author.sub('', author_name)
        pattern_comma = re.compile('\x80')
        author_name = pattern_comma.sub(', ', author_name)
        file_author[file_name] = author_name

    return file_author


def index_from_files():
    """This uses the TLG author index and makes  new index including the file
    names of TLG works. The TLGU().make_individual_works() must be run first
    to create the files to look for.
    TODO: Remove this once a good TLG index has been finalized.
    """
    path_rel = '~/cltk_data/greek/text/tlg/individual_works/'
    path = os.path.expanduser(path_rel)
    individual_works = os.listdir(path)
    new_dict = {}
    for author_code in TLG_INDEX:
        author_name = TLG_INDEX[author_code[:7]]
        works = []
        comp = re.compile(author_code + r'.*')
        for y in individual_works:
            match = comp.match(y)
            if match:
                work = match.group()[8:-4]
                works.append(work)
        new_dict[author_code] = {'name': author_name, 'works': works}
    return new_dict
