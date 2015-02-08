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


def build_corpus_index(corpus, authtab_path=None):
    """Build index for TLG or PHI5. ``authtab_path`` for testing only.
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
        logger.warning("Corpus %s not available. Choose from 'tlg' or 'phi5'." % corpus)
        sys.exit(1)
    index_path = os.path.expanduser(authtab_path)
    if not os.path.isfile(index_path):
        logger.info("Failed to locate original %s index at '%s'. Please import first." % (corpus, index_path))
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
        file_name = m.group()[:-1] + '.TXT'

        # author name
        author_name = pattern_file.split(x)[-1]
        pattern_author = re.compile(pattern_author_regex)
        author_name = pattern_author.sub('', author_name)
        pattern_comma = re.compile('\x80')
        author_name = pattern_comma.sub(', ', author_name)
        file_author[file_name] = author_name

    return file_author

def make_tlg_work_dict(author_dict):
    """ Lots to do here still. Pare characters around formats and clean all junk characters.
    :param author_dict:
    :return:
    """
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)

    final_dict = {}
    for file, author in file_index.items():
        a_id = {'id:': file[:-4]}
        idt_file = file[:-4] + '.IDT'
        author_index_path = os.path.join(orig_dir_path, idt_file)
        with open(author_index_path, 'rb') as a_ind_f:
            a_ind = a_ind_f.read()
        lat_list = a_ind.decode('latin-1').split('ÿ')
        ascii_list = [remove_non_ascii(x) for x in lat_list]

        works_list = []
        author_works = {}
        for possible_title in ascii_list:
            title_parts = possible_title.split('\x10', maxsplit=1)
            title_parts = [x for x in title_parts if x]
            for part in title_parts:
                try:
                    title_format = part.split('\x11', maxsplit=1)
                    title = title_format[0]
                    format = title_format[1]
                    author_works[title] = format
                    works_list.append(author_works)
                except:
                    pass
        author_vals = {'works': works_list, 'id': file[:-4]}
        final_dict[author] = author_vals
    #print(len(final_dict))  # 1777 this is missing ~100 files; find why
    return final_dict


if __name__ == '__main__':
    file_index = build_corpus_index('tlg')
    x = make_tlg_work_dict(file_index)
    print(x)


