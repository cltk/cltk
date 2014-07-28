"""Assembles corpora into ~/cltk_data"""

import ast
import logging
import os
from pprint import pprint
import re
import requests
from requests_toolbelt import SSLAdapter
import shutil
import site
import ssl
from urllib.parse import urlsplit

from cltk.corpus.classical_greek.beta_to_unicode import Replacer

# these can be deleted, I think
INDEX_DICT_PHI5 = {}
INDEX_DICT_PHI7 = {}
INDEX_DICT_TLG = {}


class Compile(object):  # pylint: disable=R0904
    """Copy or download files out of TLG & PHI disks"""
    def __init__(self):
        """Initializer, makes ~/cltk_data dirs"""
        self.cltk_bin_path = os.path.join(site.getsitepackages()[0], 'cltk')
        # make local CLTK dirs
        default_cltk_data = '~/cltk_data'
        cltk_data = os.path.expanduser(default_cltk_data)
        if os.path.isdir(cltk_data) is True:
            pass
        else:
            os.mkdir(cltk_data)
        self.orig_files_dir = os.path.join(cltk_data, 'originals')
        if os.path.isdir(self.orig_files_dir) is True:
            pass
        else:
            os.mkdir(self.orig_files_dir)
        self.compiled_files_dir = os.path.join(cltk_data, 'compiled')
        if os.path.isdir(self.compiled_files_dir) is True:
            pass
        else:
            os.mkdir(self.compiled_files_dir)
        log_path = os.path.join(cltk_data, 'cltk.log')
        logging.basicConfig(filename=log_path,
                            level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def import_corpus(self, corpus_name, corpus_location=None):
        """Main method. Copies or downloads corpora, moves to originals,
        then compiled
        """
        if corpus_name == 'tlg':
            orig_files_dir_tlg = os.path.join(self.orig_files_dir, 'tlg')
            if os.path.isdir(orig_files_dir_tlg) is True:
                pass
            else:
                os.mkdir(orig_files_dir_tlg)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_tlg)
            copy_dir_contents(corpus_location, orig_files_dir_tlg)
            self.compile_tlg_txt()
        elif corpus_name == 'phi7':
            orig_files_dir_phi7 = os.path.join(self.orig_files_dir, 'phi7')
            if os.path.isdir(orig_files_dir_phi7) is True:
                pass
            else:
                os.mkdir(orig_files_dir_phi7)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_phi7)
            copy_dir_contents(corpus_location, orig_files_dir_phi7)
            self.compile_phi7_txt()
        elif corpus_name == 'phi5':
            orig_files_dir_phi5 = os.path.join(self.orig_files_dir, 'phi5')
            if os.path.isdir(orig_files_dir_phi5) is True:
                pass
            else:
                os.mkdir(orig_files_dir_phi5)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_phi5)
            copy_dir_contents(corpus_location, orig_files_dir_phi5)
            self.compile_phi5_txt()
        elif corpus_name == 'latin_library':
            orig_files_dir_latin_library = os.path.join(self.orig_files_dir,
                                                        'latin_library')
            if os.path.isdir(orig_files_dir_latin_library) is True:
                pass
            else:
                os.mkdir(orig_files_dir_latin_library)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_latin_library)
            self.get_latin_library_tar()
        elif corpus_name == 'perseus_latin':
            orig_files_dir_perseus_latin = os.path.join(self.orig_files_dir,
                                                        'perseus_latin')
            if os.path.isdir(orig_files_dir_perseus_latin) is True:
                pass
            else:
                os.mkdir(orig_files_dir_perseus_latin)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_perseus_latin)
            self.get_perseus_latin_tar()
        elif corpus_name == 'perseus_greek':
            orig_files_dir_perseus_greek = os.path.join(self.orig_files_dir,
                                                        'perseus_greek')
            if os.path.isdir(orig_files_dir_perseus_greek) is True:
                pass
            else:
                os.mkdir(orig_files_dir_perseus_greek)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_perseus_greek)
            self.get_perseus_greek_tar()
        elif corpus_name == 'lacus_curtius_latin':
            orig_files_dir_lacus_curtius_latin = \
                os.path.join(self.orig_files_dir, 'lacus_curtius_latin')
            if os.path.isdir(orig_files_dir_lacus_curtius_latin) is True:
                pass
            else:
                os.mkdir(orig_files_dir_lacus_curtius_latin)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_lacus_curtius_latin)
            self.get_lacus_curtius_latin_tar()
        elif corpus_name == 'treebank_perseus_greek':
            orig_files_dir_treebank_perseus_greek = \
                os.path.join(self.orig_files_dir, 'treebank_perseus_greek')
            if os.path.isdir(orig_files_dir_treebank_perseus_greek) is True:
                pass
            else:
                os.mkdir(orig_files_dir_treebank_perseus_greek)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_treebank_perseus_greek)
            self.get_treebank_perseus_greek_tar()
        elif corpus_name == 'treebank_perseus_latin':
            orig_files_dir_treebank_perseus_latin = \
                os.path.join(self.orig_files_dir, 'treebank_perseus_latin')
            if os.path.isdir(orig_files_dir_treebank_perseus_latin) is True:
                pass
            else:
                os.mkdir(orig_files_dir_treebank_perseus_latin)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_treebank_perseus_latin)
            self.get_treebank_perseus_latin_tar()
        elif corpus_name == 'pos_latin':
            orig_files_dir_pos_latin = os.path.join(self.orig_files_dir,
                                                    'pos_latin')
            if os.path.isdir(orig_files_dir_pos_latin) is True:
                pass
            else:
                os.mkdir(orig_files_dir_pos_latin)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_pos_latin)
            self.get_pos_latin_tar()
        elif corpus_name == 'sentence_tokens_latin':
            orig_files_dir_tokens_latin = os.path.join(self.orig_files_dir,
                                                       'sentence_tokens_latin')
            if os.path.isdir(orig_files_dir_tokens_latin) is True:
                pass
            else:
                os.mkdir(orig_files_dir_tokens_latin)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_tokens_latin)
            self.get_sentence_tokens_latin_tar()
        elif corpus_name == 'sentence_tokens_greek':
            orig_files_dir_tokens_greek = os.path.join(self.orig_files_dir,
                                                       'sentence_tokens_greek')
            if os.path.isdir(orig_files_dir_tokens_greek) is True:
                pass
            else:
                os.mkdir(orig_files_dir_tokens_greek)
                logging.info('Made new directory "%s" at "%s"', corpus_name,
                             orig_files_dir_tokens_greek)
            self.get_sentence_tokens_greek_tar()
        else:
            logging.error('Unrecognized corpus name. Choose one of the '
                          'following: "tlg", "phi7", "phi5", "latin_library", '
                          '"perseus_latin", "perseus_greek", '
                          '"lacus_curtius_latin".')

    def read_tlg_index_file_author(self):
        """Reads CLTK's index_file_author.txt for TLG."""
        global tlg_index
        logging.info('Starting TLG index_file_author.txt read.')
        compiled_files_dir_tlg_index = \
            os.path.join(self.compiled_files_dir, 'tlg',
                         'index_file_author.txt')
        try:
            with open(compiled_files_dir_tlg_index, 'r') as index_opened:
                tlg_index = index_opened.read()
                tlg_index = ast.literal_eval(tlg_index)
                return tlg_index
        except IOError:
            logging.error('Failed to open TLG index file '
                          'index_file_author.txt.')

    def make_tlg_index_file_author(self):
        """Reads TLG's AUTHTAB.DIR and writes a dict (index_file_author.txt)
        to the CLTK's corpus directory.
        """
        logging.info('Starting TLG index parsing.')
        orig_files_dir_tlg_index = os.path.join(self.orig_files_dir, 'tlg',
                                                'AUTHTAB.DIR')
        compiled_files_dir_tlg = os.path.join(self.compiled_files_dir, 'tlg')
        try:
            with open(orig_files_dir_tlg_index, 'rb') as index_opened:
                index_read = index_opened.read().decode('latin-1')
                index_split = index_read.split('ÿ')[1:-7]
                index_filter = [item for item in index_split if item]
                INDEX_DICT_TLG = {}
                for file in index_filter:
                    file_repl = file.replace(' &1', ' ').replace('&', '') \
                        .replace(' 1', ' ').replace('-1', '-')\
                        .replace('[2', '[').replace(']2', ']')\
                        .replace('1Z', '').replace('1P', 'P') \
                        .replace('1D', 'D').replace('1L', 'L')\
                        .replace('Â€', ' ')
                    file_split = file_repl.split(' ', 1)
                    label = file_split[0]
                    name = file_split[1]
                    INDEX_DICT_TLG[label] = name
                logging.info('Finished TLG index parsing.')
                logging.info('Starting writing TLG index_file_author.txt.')
                authtab_path = \
                    compiled_files_dir_tlg + '/' + 'index_file_author.txt'
                try:
                    with open(authtab_path, 'w') as authtab_opened:
                        authtab_opened.write(str(INDEX_DICT_TLG))
                        logging.info('Finished writing TLG '
                                     'index_file_author.txt.')
                except IOError:
                    logging.error('Failed to write TLG index_file_author.txt.')
        except IOError:
            logging.error('Failed to open TLG index file AUTHTAB.DIR')

    def compile_tlg_txt(self):
        """Reads original Beta Code files and converts to Unicode files"""
        logging.info('Starting TLG corpus compilation into files.')
        compiled_files_dir_tlg = os.path.join(self.compiled_files_dir, 'tlg')
        if os.path.isdir(compiled_files_dir_tlg) is True:
            pass
        else:
            os.mkdir(compiled_files_dir_tlg)
        self.make_tlg_index_file_author()
        self.read_tlg_index_file_author()
        for file_name in tlg_index:
            abbrev = tlg_index[file_name]
            orig_files_dir_tlg = os.path.join(self.orig_files_dir, 'tlg')
            file_name_txt = file_name + '.TXT'
            files_path = os.path.join(orig_files_dir_tlg, file_name_txt)
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    local_replacer = Replacer()
                    new_uni = local_replacer.beta_code(txt_ascii)
                    file_name_txt_uni = file_name + '.txt'
                    file_path = os.path.join(compiled_files_dir_tlg,
                                             file_name_txt_uni)
                    try:
                        with open(file_path, 'w') as new_file:
                            new_file.write(new_uni)
                    except IOError:
                        logging.error('Failed to write to new file %s of '
                                      'author %s', file_name, abbrev)
                logging.info('Finished TLG corpus compilation to %s',
                             file_path)
            except IOError:
                logging.error('Failed to open TLG file %s of author %s',
                              file_name, abbrev)
        self.make_tlg_meta_index()
        self.make_tlg_index_auth_works()

    def read_tlg_author_work_titles(self, auth_abbrev):
        """Reads a converted TLG file and returns a list of header titles
        within it
        """
        global WORKS
        logging.info('Starting to find works within a TLG author file.')
        compiled_files_dir_tlg = os.path.join(self.compiled_files_dir, 'tlg')
        auth_file = compiled_files_dir_tlg + '/' + auth_abbrev + '.txt'
        with open(auth_file) as file_opened:
            string = file_opened.read()
            title_reg = re.compile('\{1.{1,50}?\}1')
            WORKS = title_reg.findall(string)
            return WORKS

    def make_tlg_index_auth_works(self):
        """read index_file_author.txt, read author file, and expand dict to
        include author works, index_author_works.txt
        """
        logging.info('Starting to compile TLG auth_works.txt.')
        orig_files_dir_tlg_index = os.path.join(self.orig_files_dir, 'tlg')
        compiled_files_dir_tlg = os.path.join(self.compiled_files_dir, 'tlg')
        self.read_tlg_index_file_author()
        auth_work_dict = {}
        for file_name in tlg_index:
            auth_node = {}
            self.read_tlg_author_work_titles(file_name)
            auth_name = tlg_index[file_name]
            auth_node['tlg_file'] = file_name
            auth_node['tlg_name'] = auth_name
            auth_node['works'] = WORKS
            auth_work_dict[auth_name] = auth_node
        file_path = compiled_files_dir_tlg + '/' + 'index_author_works.txt'
        try:
            with open(file_path, 'w') as new_file:
                pprint(auth_work_dict, stream=new_file)
        except IOError:
            logging.error('Failed to write to index_auth_work.txt')
        logging.info('Finished compiling TLG index_auth_works.txt.')

    def make_tlg_meta_index(self):
        """Reads and writes the LSTSCDCN.DIR file"""
        logging.info('Starting to read the TLG file LSTSCDCN.DIR.')
        orig_files_dir_tlg_index_meta = os.path.join(self.orig_files_dir,
                                                     'tlg', 'LSTSCDCN.DIR')
        compiled_files_dir_tlg_meta = os.path.join(self.compiled_files_dir,
                                                   'tlg', 'index_meta.txt')
        meta_list_dict = {}
        try:
            with open(orig_files_dir_tlg_index_meta, 'rb') as index_opened:
                index_read = index_opened.read().decode('latin-1')
                index_split = index_read.split('ÿ')[2:-3]
                index_filter = [item for item in index_split if item]
                for file in index_filter:
                    rg_key = re.compile('^[AUT|AWN|BIB|DAT|LIS]{3}?.{5}?')
                    m_key = rg_key.findall(file)
                    m_value = rg_key.split(file)
                    if not m_key:
                        pass
                    else:
                        if not m_value:
                            pass
                        else:
                            meta_list_dict[m_key[0]] = m_value[1]
                file_path = compiled_files_dir_tlg_meta
                try:
                    with open(file_path, 'w') as new_file:
                        new_file.write(str(meta_list_dict))
                except IOError:
                    logging.error('Failed to write to meta_list.txt file \
                    of TLG')
        except IOError:
            logging.error('Failed to open TLG index file LSTSCDCN.DIR')

    def read_phi7_index_file_author(self):
        """Reads CLTK's index_file_author.txt for phi7."""
        global phi7_index
        logging.info('Starting PHI7 index_file_author.txt read.')
        compiled_files_dir_phi7_index = \
            os.path.join(self.compiled_files_dir, 'phi7',
                         'index_file_author.txt')
        try:
            with open(compiled_files_dir_phi7_index, 'r') as index_opened:
                phi7_index = index_opened.read()
                phi7_index = ast.literal_eval(phi7_index)
                return phi7_index
        except IOError:
            logging.error('Failed to open PHI7 index file '
                          'index_file_author.txt.')

    def make_phi7_index_file_author(self):
        """Reads phi7's AUTHTAB.DIR and writes a dict (index_file_author.txt)
        to the CLTK's corpus directory.
        """
        logging.info('Starting phi7 index parsing.')
        orig_files_dir_phi7_index = os.path.join(self.orig_files_dir, 'phi7',
                                                 'AUTHTAB.DIR')
        compiled_files_dir_phi7 = os.path.join(self.compiled_files_dir, 'phi7')
        try:
            with open(orig_files_dir_phi7_index, 'rb') as index_opened:
                index_read = index_opened.read().decode('latin-1')
                index_split = index_read.split('ÿ')[2:-9]
                index_filter = [item for item in index_split if item]
                INDEX_DICT_PHI7 = {}
                for file in index_filter:
                    file_repl = file.replace('l', '').replace('g', '') \
                        .replace('h', '').replace('>', '').replace(']]', ']')
                    pattern = '.*Library.*|.*Inscriptions .*|.*Bibliography.*'
                    match = re.search(pattern, file_repl)
                    if match:
                        pass
                    else:
                        split = file_repl.split(' ', 1)
                        number = split[0]
                        name = split[1]
                        INDEX_DICT_PHI7[number] = name
                logging.info('Finished PHI7 index parsing.')
                logging.info('Starting writing PHI7 index_file_author.txt.')
                compiled_files_dir_phi7_authtab = \
                    os.path.join(compiled_files_dir_phi7,
                                 'index_file_author.txt')
                try:
                    with open(compiled_files_dir_phi7_authtab, 'w') as \
                            authtab_opened:
                        authtab_opened.write(str(INDEX_DICT_PHI7))
                        logging.info('Finished writing PHI7 '
                                     'index_file_author.txt.')
                except IOError:
                    logging.error('Failed to write PHI7 '
                                  'index_file_author.txt.')
        except IOError:
            logging.error('Failed to open PHI7 index file AUTHTAB.DIR')

    def read_phi7_index_file_author(self):
        """Reads CLTK's index_file_author.txt for PHI7."""
        global phi7_index
        logging.info('Starting phi7 index_file_author.txt read.')
        compiled_files_dir_phi7_index = \
            os.path.join(self.compiled_files_dir, 'phi7',
                         'index_file_author.txt')
        try:
            with open(compiled_files_dir_phi7_index, 'r') as index_opened:
                phi7_index = index_opened.read()
                phi7_index = ast.literal_eval(phi7_index)
                return phi7_index
        except IOError:
            logging.error('Failed to open PHI7 index file '
                          'index_file_author.txt.')

    def read_phi7_author_work_titles(self, auth_abbrev):
        """Reads a converted phi7 file and returns a list of header titles
        within it
        """
        global WORKS
        logging.info('Starting to find works within a PHI7 author file.')
        compiled_files_dir_phi7 = os.path.join(self.compiled_files_dir, 'phi7')
        auth_file = compiled_files_dir_phi7 + '/' + auth_abbrev + '.txt'
        with open(auth_file) as file_opened:
            string = file_opened.read()
            title_reg = re.compile('\{1.{1,50}?\}1')
            WORKS = title_reg.findall(string)
            return WORKS

    def make_phi7_index_auth_works(self):
        """read index_file_author.txt, read author file, and expand dict to
        include author works, index_author_works.txt
        """
        logging.info('Starting to compile PHI7 auth_works.txt.')
        orig_files_dir_phi7_index = os.path.join(self.orig_files_dir, 'phi7')
        compiled_files_dir_phi7 = os.path.join(self.compiled_files_dir, 'phi7')
        self.read_phi7_index_file_author()
        auth_work_dict = {}
        for file_name in phi7_index:
            auth_node = {}
            self.read_phi7_author_work_titles(file_name)
            auth_name = phi7_index[file_name]
            auth_node['phi7_file'] = file_name
            auth_node['phi7_name'] = auth_name
            auth_node['works'] = WORKS
            auth_work_dict[auth_name] = auth_node
        file_path = compiled_files_dir_phi7 + '/' + 'index_author_works.txt'
        try:
            with open(file_path, 'w') as new_file:
                pprint(auth_work_dict, stream=new_file)
        except IOError:
            logging.error('Failed to write to index_auth_work.txt')
        logging.info('Finished compiling PHI7 index_auth_works.txt.')

    # add smart parsing of beta code tags
    def compile_phi7_txt(self):
        """Reads original Beta Code files and converts to Unicode files"""
        logging.info('Starting PHI7 corpus compilation into files.')
        compiled_files_dir_phi7 = os.path.join(self.compiled_files_dir, 'phi7')
        if os.path.isdir(compiled_files_dir_phi7) is True:
            pass
        else:
            os.mkdir(compiled_files_dir_phi7)
        self.make_phi7_index_file_author()
        self.read_phi7_index_file_author()
        for file_name in phi7_index:
            abbrev = phi7_index[file_name]
            orig_files_dir_phi7 = os.path.join(self.orig_files_dir, 'phi7')
            file_name_txt = file_name + '.TXT'
            files_path = os.path.join(orig_files_dir_phi7, file_name_txt)
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    # local_replacer = Replacer()
                    # new_uni = local_replacer.beta_code(txt_ascii)
                    file_name_txt_uni = file_name + '.txt'
                    file_path = os.path.join(compiled_files_dir_phi7,
                                             file_name_txt_uni)
                    try:
                        with open(file_path, 'w') as new_file:
                            new_file.write(txt_ascii)
                    except IOError:
                        logging.error('Failed to write to new file %s of '
                                      'author %s', file_name, abbrev)
                logging.info('Finished PHI7 corpus compilation to %s',
                             file_path)
            except IOError:
                logging.error('Failed to open PHI7 file %s of author %s',
                              file_name, abbrev)
        self.make_phi7_index_auth_works()

    def read_phi5_index_file_author(self):
        """Reads CLTK's index_file_author.txt for phi5."""
        global phi5_index
        logging.info('Starting PHI5 index_file_author.txt read.')
        compiled_files_dir_phi5_index = \
            os.path.join(self.compiled_files_dir, 'phi5',
                         'index_file_author.txt')
        try:
            with open(compiled_files_dir_phi5_index, 'r') as index_opened:
                phi5_index = index_opened.read()
                phi5_index = ast.literal_eval(phi5_index)
                return phi5_index
        except IOError:
            logging.error('Failed to open PHI5 index file '
                          'index_file_author.txt.')

    def make_phi5_index_file_author(self):
        """Reads phi5's AUTHTAB.DIR and writes a dict (index_file_author.txt)
        to the CLTK's corpus directory.
        """
        logging.info('Starting phi5 index parsing.')
        orig_files_dir_phi5_index = os.path.join(self.orig_files_dir, 'phi5',
                                                 'AUTHTAB.DIR')
        compiled_files_dir_phi5 = os.path.join(self.compiled_files_dir, 'phi5')
        try:
            with open(orig_files_dir_phi5_index, 'rb') as index_opened:
                index_read = index_opened.read().decode('latin-1')
                index_split = index_read.split('ÿ')[1:-21]
                index_filter = [item for item in index_split if item]
                INDEX_DICT_PHI5 = {}
                for file in index_filter:
                    file_repl = file.replace('\x83l', '') \
                        .replace('Â€', '; ').replace('&1', '') \
                        .replace('&', '').replace('\x80', '; ')
                    split = file_repl.split(' ', 1)
                    number = split[0]
                    name = split[1]
                    INDEX_DICT_PHI5[number] = name
                logging.info('Finished PHI5 index parsing.')
                logging.info('Starting writing PHI5 index_file_author.txt.')
                compiled_files_dir_phi5_authtab = \
                    os.path.join(compiled_files_dir_phi5,
                                 'index_file_author.txt')
                try:
                    with open(compiled_files_dir_phi5_authtab, 'w') as \
                            authtab_opened:
                        authtab_opened.write(str(INDEX_DICT_PHI5))
                        logging.info('Finished writing PHI5 '
                                     'index_file_author.txt.')
                except IOError:
                    logging.error('Failed to write PHI5 '
                                  'index_file_author.txt.')
        except IOError:
            logging.error('Failed to open PHI5 index file AUTHTAB.DIR')

    def read_phi5_author_work_titles(self, auth_abbrev):
        """Reads a converted phi5 file and returns a list of header titles
        within it
        """
        global WORKS
        logging.info('Starting to find works within a PHI5 author file.')
        compiled_files_dir_phi5 = os.path.join(self.compiled_files_dir, 'phi5')
        auth_file = compiled_files_dir_phi5 + '/' + auth_abbrev + '.txt'
        with open(auth_file) as file_opened:
            string = file_opened.read()
            title_reg = re.compile('\{1.{1,50}?\}1')
            WORKS = title_reg.findall(string)
            return WORKS

    def make_phi5_index_auth_works(self):
        """read index_file_author.txt, read author file, and expand dict to
        include author works, index_author_works.txt
        """
        logging.info('Starting to compile PHI5 auth_works.txt.')
        compiled_files_dir_phi5 = os.path.join(self.compiled_files_dir, 'phi5')
        self.read_phi5_index_file_author()
        auth_work_dict = {}
        for file_name in phi5_index:
            auth_node = {}
            self.read_phi5_author_work_titles(file_name)
            auth_name = phi5_index[file_name]
            auth_node['phi5_file'] = file_name
            auth_node['phi5_name'] = auth_name
            auth_node['works'] = WORKS
            auth_work_dict[auth_name] = auth_node
        file_path = compiled_files_dir_phi5 + '/' + 'index_author_works.txt'
        try:
            with open(file_path, 'w') as new_file:
                pprint(auth_work_dict, stream=new_file)
        except IOError:
            logging.error('Failed to write to index_auth_work.txt')
        logging.info('Finished compiling PHI5 index_auth_works.txt.')

    def compile_phi5_txt(self):
        """Reads original Beta Code files and converts to Unicode files
        todo: #add smart parsing of beta code tags
        """
        logging.info('Starting PHI5 corpus compilation into files.')
        compiled_files_dir_phi5 = os.path.join(self.compiled_files_dir, 'phi5')
        if os.path.isdir(compiled_files_dir_phi5) is True:
            pass
        else:
            os.mkdir(compiled_files_dir_phi5)
        self.make_phi5_index_file_author()
        self.read_phi5_index_file_author()
        for file_name in phi5_index:
            abbrev = phi5_index[file_name]
            orig_files_dir_phi5 = os.path.join(self.orig_files_dir, 'phi5')
            file_name_txt = file_name + '.TXT'
            files_path = os.path.join(orig_files_dir_phi5, file_name_txt)
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    # local_replacer = Replacer()
                    # new_uni = local_replacer.beta_code(txt_ascii)
                    file_name_txt_uni = file_name + '.txt'
                    file_path = os.path.join(compiled_files_dir_phi5,
                                             file_name_txt_uni)
                    try:
                        with open(file_path, 'w') as new_file:
                            new_file.write(txt_ascii)
                    except IOError:
                        logging.error('Failed to write to new file %s of '
                                      'author %s', file_name, abbrev)
                logging.info('Finished PHI5 corpus compilation to %s',
                             file_path)
            except IOError:
                logging.error('Failed to open PHI5 file %s of author %s',
                              file_name, abbrev)
        self.make_phi5_index_auth_works()

    def get_latin_library_tar(self):
        """Fetch Latin Library corpus"""
        orig_files_dir_latin_library = \
            os.path.join(self.orig_files_dir, 'latin_library')
        ll_url = 'https://raw.githubusercontent.com/kylepjohnson/' \
                 'corpus_latin_library/master/latin_library.tar.gz'
        session = requests.Session()
        session.mount(ll_url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        ll_tar = session.get(ll_url, stream=True)
        latin_library_file_name = urlsplit(ll_url).path.split('/')[-1]
        latin_library_file_path = \
            os.path.join(orig_files_dir_latin_library, latin_library_file_name)
        try:
            with open(latin_library_file_path, 'wb') as new_file:
                new_file.write(ll_tar.content)
                logging.info('Finished writing %s.', latin_library_file_name)
        except IOError:
            logging.error('Failed to write file %s', latin_library_file_name)
        try:
            shutil.unpack_archive(latin_library_file_path,
                                  self.compiled_files_dir)
            logging.info('Finished unpacking %s', latin_library_file_name)
        except IOError:
            logging.info('Failed to unpack %s.', latin_library_file_name)

    def get_perseus_latin_tar(self):
        """Fetch Perseus Latin corpus"""
        orig_files_dir_perseus_latin = os.path.join(self.orig_files_dir,
                                                    'perseus_latin')
        pl_url = 'https://raw.githubusercontent.com/kylepjohnson/' \
                 'corpus_perseus_latin/master/perseus_latin.tar.gz'
        session = requests.Session()
        session.mount(pl_url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        ll_tar = session.get(pl_url, stream=True)
        perseus_latin_file_name = urlsplit(pl_url).path.split('/')[-1]
        perseus_latin_file_path = \
            os.path.join(orig_files_dir_perseus_latin, perseus_latin_file_name)
        try:
            with open(perseus_latin_file_path, 'wb') as new_file:
                new_file.write(ll_tar.content)
                logging.info('Finished writing %s.', perseus_latin_file_name)
        except IOError:
            logging.error('Failed to write file %s', perseus_latin_file_name)
        try:
            shutil.unpack_archive(perseus_latin_file_path,
                                  self.compiled_files_dir)
            logging.info('Finished unpacking %s', perseus_latin_file_name)
        except IOError:
            logging.info('Failed to unpack %s.', perseus_latin_file_name)

    def get_lacus_curtius_latin_tar(self):
        """Fetch lacus_curtius_latin_tar"""
        orig_files_dir_lacus_curtius_latin = \
            os.path.join(self.orig_files_dir, 'lacus_curtius_latin')
        lc_url = 'https://raw.githubusercontent.com/kylepjohnson/' \
                 'corpus_lacus_curtius_latin/master/lacus_curtius.tar.gz'
        session = requests.Session()
        session.mount(lc_url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        ll_tar = session.get(lc_url, stream=True)
        lacus_curtius_latin_file_name = urlsplit(lc_url).path.split('/')[-1]
        lacus_curtius_latin_file_path = \
            os.path.join(orig_files_dir_lacus_curtius_latin,
                         lacus_curtius_latin_file_name)
        try:
            with open(lacus_curtius_latin_file_path, 'wb') as new_file:
                new_file.write(ll_tar.content)
                logging.info('Finished writing %s.',
                             lacus_curtius_latin_file_name)
        except IOError:
            logging.error('Failed to write file %s',
                          lacus_curtius_latin_file_name)
        try:
            shutil.unpack_archive(lacus_curtius_latin_file_path,
                                  self.compiled_files_dir)
            logging.info('Finished unpacking %s',
                         lacus_curtius_latin_file_name)
        except IOError:
            logging.info('Failed to unpack %s.', lacus_curtius_latin_file_name)

    def get_perseus_greek_tar(self):
        """Fetch Perseus Greek corpus"""
        orig_files_dir_perseus_greek = os.path.join(self.orig_files_dir,
                                                    'perseus_greek')
        pg_url = 'https://raw.githubusercontent.com/kylepjohnson/' \
                 'corpus_perseus_greek/master/perseus_greek.tar.gz'
        session = requests.Session()
        session.mount(pg_url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        pg_tar = session.get(pg_url, stream=True)
        perseus_greek_file_name = urlsplit(pg_url).path.split('/')[-1]
        perseus_greek_file_path = os.path.join(orig_files_dir_perseus_greek,
                                               perseus_greek_file_name)
        try:
            with open(perseus_greek_file_path, 'wb') as new_file:
                new_file.write(pg_tar.content)
                logging.info('Finished writing %s.', perseus_greek_file_name)
        except IOError:
            logging.error('Failed to write file %s', perseus_greek_file_name)
        try:
            shutil.unpack_archive(perseus_greek_file_path,
                                  self.compiled_files_dir)
            logging.info('Finished unpacking %s', perseus_greek_file_name)
        except IOError:
            logging.info('Failed to unpack %s.', perseus_greek_file_name)

    def get_treebank_perseus_greek_tar(self):
        """Fetch Perseus's Greek part-of-speech treebank"""
        orig_files_dir_treebank_perseus_greek = \
            os.path.join(self.orig_files_dir, 'treebank_perseus_greek')
        pg_url = 'https://raw.githubusercontent.com/kylepjohnson/' \
                 'treebank_perseus_greek/master/treebank_perseus_greek.tar.gz'
        session = requests.Session()
        session.mount(pg_url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        pg_tar = session.get(pg_url, stream=True)
        treebank_perseus_greek_file_name = urlsplit(pg_url).path.split('/')[-1]
        treebank_perseus_greek_file_path = \
            os.path.join(orig_files_dir_treebank_perseus_greek,
                         treebank_perseus_greek_file_name)
        try:
            with open(treebank_perseus_greek_file_path, 'wb') as new_file:
                new_file.write(pg_tar.content)
                logging.info('Finished writing %s.',
                             treebank_perseus_greek_file_name)
        except IOError:
            logging.error('Failed to write file %s',
                          treebank_perseus_greek_file_name)
        try:
            shutil.unpack_archive(treebank_perseus_greek_file_path,
                                  self.compiled_files_dir)
            logging.info('Finished unpacking %s',
                         treebank_perseus_greek_file_name)
        except IOError:
            logging.info('Failed to unpack %s.',
                         treebank_perseus_greek_file_name)

    def get_treebank_perseus_latin_tar(self):
        """Fetch Persus's Latin treebank files"""
        orig_files_dir_treebank_perseus_latin = \
            os.path.join(self.orig_files_dir, 'treebank_perseus_latin')
        pg_url = 'https://raw.githubusercontent.com/kylepjohnson/' \
                 'treebank_perseus_latin/master/treebank_perseus_latin.tar.gz'
        session = requests.Session()
        session.mount(pg_url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        pg_tar = session.get(pg_url, stream=True)
        treebank_perseus_latin_file_name = urlsplit(pg_url).path.split('/')[-1]
        treebank_perseus_latin_file_path = \
            os.path.join(orig_files_dir_treebank_perseus_latin,
                         treebank_perseus_latin_file_name)
        try:
            with open(treebank_perseus_latin_file_path, 'wb') as new_file:
                new_file.write(pg_tar.content)
                logging.info('Finished writing %s.',
                             treebank_perseus_latin_file_name)
        except IOError:
            logging.error('Failed to write file %s',
                          treebank_perseus_latin_file_name)
        try:
            shutil.unpack_archive(treebank_perseus_latin_file_path,
                                  self.compiled_files_dir)
            logging.info('Finished unpacking %s',
                         treebank_perseus_latin_file_name)
        except IOError:
            logging.info('Failed to unpack %s.',
                         treebank_perseus_latin_file_name)

    def get_pos_latin_tar(self):
        """Fetch Latin part-of-speech files"""
        orig_files_dir_pos_latin = os.path.join(self.orig_files_dir,
                                                'pos_latin')
        pg_url = 'https://raw.githubusercontent.com/kylepjohnson/pos_latin/' \
                 'master/pos_latin.tar.gz'
        session = requests.Session()
        session.mount(pg_url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        pg_tar = session.get(pg_url, stream=True)
        pos_latin_file_name = urlsplit(pg_url).path.split('/')[-1]
        pos_latin_file_path = os.path.join(orig_files_dir_pos_latin,
                                           pos_latin_file_name)
        try:
            with open(pos_latin_file_path, 'wb') as new_file:
                new_file.write(pg_tar.content)
                logging.info('Finished writing %s.', pos_latin_file_name)
        except IOError:
            logging.error('Failed to write file %s', pos_latin_file_name)
        try:
            shutil.unpack_archive(pos_latin_file_path, self.compiled_files_dir)
            logging.info('Finished unpacking %s', pos_latin_file_name)
        except IOError:
            logging.info('Failed to unpack %s.', pos_latin_file_name)

    def get_sentence_tokens_latin_tar(self):
        """Fetch algorithm for Latin sentence tokenization"""
        orig_files_dir_tokens_latin = \
            os.path.join(self.orig_files_dir, 'sentence_tokens_latin')
        # make compiled files dir for tokens_latin
        compiled_files_dir_tokens_latin = \
            os.path.join(self.compiled_files_dir, 'sentence_tokens_latin')
        if os.path.isdir(compiled_files_dir_tokens_latin) is True:
            pass
        else:
            os.mkdir(compiled_files_dir_tokens_latin)
        pg_url = 'https://raw.githubusercontent.com/kylepjohnson/' \
                 'cltk_latin_sentence_tokenizer/master/latin.tar.gz'
        session = requests.Session()
        session.mount(pg_url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        pg_tar = session.get(pg_url, stream=True)
        tokens_latin_file_name = urlsplit(pg_url).path.split('/')[-1]
        tokens_latin_file_path = os.path.join(orig_files_dir_tokens_latin,
                                              tokens_latin_file_name)
        try:
            with open(tokens_latin_file_path, 'wb') as new_file:
                new_file.write(pg_tar.content)
                logging.info('Finished writing %s.', tokens_latin_file_name)
                try:
                    shutil.unpack_archive(tokens_latin_file_path,
                                          compiled_files_dir_tokens_latin)
                    logging.info('Finished unpacking %s.',
                                 tokens_latin_file_name)
                except IOError:
                    logging.info('Failed to unpack %s.',
                                 tokens_latin_file_name)
        except IOError:
            logging.error('Failed to write file %s', tokens_latin_file_name)


    def get_sentence_tokens_greek_tar(self):
        """Fetch algorithm for Greek sentence tokenization"""
        orig_files_dir_tokens_greek = \
            os.path.join(self.orig_files_dir, 'sentence_tokens_greek')
        # make compiled files dir for tokens_greek
        compiled_files_dir_tokens_greek = \
            os.path.join(self.compiled_files_dir, 'sentence_tokens_greek')
        if os.path.isdir(compiled_files_dir_tokens_greek) is True:
            pass
        else:
            os.mkdir(compiled_files_dir_tokens_greek)
        pg_url = 'https://raw.githubusercontent.com/kylepjohnson/' \
                 'cltk_greek_sentence_tokenizer/master/greek.tar.gz'
        session = requests.Session()
        session.mount(pg_url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        pg_tar = session.get(pg_url, stream=True)
        tokens_greek_file_name = urlsplit(pg_url).path.split('/')[-1]
        tokens_greek_file_path = os.path.join(orig_files_dir_tokens_greek,
                                              tokens_greek_file_name)
        try:
            with open(tokens_greek_file_path, 'wb') as new_file:
                new_file.write(pg_tar.content)
                logging.info('Finished writing %s.', tokens_greek_file_name)
                try:
                    shutil.unpack_archive(tokens_greek_file_path,
                                          compiled_files_dir_tokens_greek)
                    logging.info('Finished unpacking %s.',
                                 tokens_greek_file_name)
                except IOError:
                    logging.info('Failed to unpack %s.',
                                 tokens_greek_file_name)
        except IOError:
            logging.error('Failed to write file %s', tokens_greek_file_name)


def remove_non_ascii(input_string):
    """remove non-ascii: http://stackoverflow.com/a/1342373"""
    return "".join(i for i in input_string if ord(i) < 128)


def clear_log():
    """Truncates log"""
    try:
        with open('classics_corpus_compiler.log', 'w'):
            logging.info('Cleared log if present.')
    except IOError:
        logging.error('Failed to clear log.')


def copy_dir_contents(src, dest):
    """Copy contents of one directory to another"""
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest)
