"""Assembles JSON files of PHI and TLG corpora"""

import ast
import logging
import os
from pprint import pprint
import re
import shutil
import site
import sys

from cltk.corpus.classical_greek.replacer import Replacer


INDEX_DICT_PHI5 = {}
INDEX_DICT_PHI7 = {}
INDEX_DICT_TLG = {}


class Compile(object):
    """Make JSON files out of TLG & PHI disks"""

    def __init__(self):
        """Initializer, optional corpora and project"""
        self.cltk_bin_path = os.path.join(site.getsitepackages()[0], 'cltk')
        #make local CLTK dirs
        default_cltk_local = '~/cltk_local'
        cltk_local = os.path.expanduser(default_cltk_local)
        if os.path.isdir(cltk_local) is True:
            pass
        else:
            os.mkdir(cltk_local)
        self.orig_files_dir = os.path.join(cltk_local, 'originals')
        if os.path.isdir(self.orig_files_dir) is True:
            pass
        else:
            os.mkdir(self.orig_files_dir)
        self.compiled_files_dir = os.path.join(cltk_local, 'compiled')
        if os.path.isdir(self.compiled_files_dir) is True:
            pass
        else:
            os.mkdir(self.compiled_files_dir)
        logging.basicConfig(filename='compiler.log',
                            level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def import_corpora(self, corpus_name, corpus_location):
        if corpus_name == 'tlg':
            orig_files_dir_tlg = os.path.join(self.orig_files_dir, 'tlg')
            if os.path.isdir(orig_files_dir_tlg) is True:
                pass
            else:
                os.mkdir(orig_files_dir_tlg)
            copy_dir_contents(corpus_location, orig_files_dir_tlg)
        elif corpus_name == 'phi7':
            orig_files_dir_phi7 = os.path.join(self.orig_files_dir, 'phi7')
            if os.path.isdir(orig_files_dir_phi7) is True:
                pass
            else:
                os.mkdir(orig_files_dir_phi7)
            copy_dir_contents(corpus_location, orig_files_dir_phi7)
        elif corpus_name == 'phi5':
            orig_files_dir_phi5 = os.path.join(self.orig_files_dir, 'phi5')
            if os.path.isdir(orig_files_dir_phi5) is True:
                pass
            else:
                os.mkdir(orig_files_dir_phi5)
            copy_dir_contents(corpus_location, orig_files_dir_phi5)
        else:
            logging.error('Unrecognized corpus name. Choose one of the following: "tlg", "phi7", "phi5".')

    def read_tlg_index_file_author(self):
        """Reads CLTK's index_file_author.txt for TLG."""
        global tlg_index
        logging.info('Starting TLG index_file_author.txt read.')
        compiled_files_dir_tlg_index = os.path.join(self.compiled_files_dir, 'tlg', 'index_file_author.txt')
        try:
            with open(compiled_files_dir_tlg_index, 'r') as index_opened:
                tlg_index = index_opened.read()
                tlg_index = ast.literal_eval(tlg_index)
                return tlg_index
        except IOError:
            logging.error('Failed to open TLG index file index_file_author.txt.')

    def make_tlg_index_file_author(self):
        """Reads TLG's AUTHTAB.DIR and writes a dict (index_file_author.txt) to the CLTK's corpus directory."""
        logging.info('Starting TLG index parsing.')
        orig_files_dir_tlg_index = os.path.join(self.orig_files_dir, 'tlg', 'AUTHTAB.DIR')
        compiled_files_dir_tlg = os.path.join(self.compiled_files_dir, 'tlg')
        try:
            with open(orig_files_dir_tlg_index, 'rb') as index_opened:
                index_read = index_opened.read().decode('latin-1')
                index_split = index_read.split('ÿ')[1:-7]
                index_filter = [item for item in index_split if item]
                INDEX_DICT_TLG = {}
                for file in index_filter:
                    file_repl = file.replace(' &1', ' ').replace('&', '')\
                        .replace(' 1', ' ').replace('-1', '-').replace('[2', '[')\
                        .replace(']2', ']').replace('1Z', '').replace('1P', 'P')\
                        .replace('1D', 'D').replace('1L', 'L').replace('Â€', ' ')
                    file_split = file_repl.split(' ', 1)
                    label = file_split[0]
                    name = file_split[1]
                    INDEX_DICT_TLG[label] = name
                logging.info('Finished TLG index parsing.')
                logging.info('Starting writing TLG index_file_author.txt.')
                authtab_path = compiled_files_dir_tlg + '/' + 'index_file_author.txt'
                try:
                    with open(authtab_path, 'w') as authtab_opened:
                        authtab_opened.write(str(INDEX_DICT_TLG))
                        logging.info('Finished writing TLG index_file_author.txt.')
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
                    file_path = os.path.join(compiled_files_dir_tlg, file_name_txt_uni)
                    try:
                        with open(file_path, 'w') as new_file:
                            new_file.write(new_uni)
                    except IOError:
                        logging.error('Failed to write to new file %s of author %s', file_name, abbrev)
                logging.info('Finished TLG corpus compilation to %s', file_path)
            except IOError:
                logging.error('Failed to open TLG file %s of author %s', file_name, abbrev)
        self.make_tlg_meta_index()
        self.make_tlg_index_auth_works()

    def read_tlg_author_work_titles(self, auth_abbrev):
        """Reads a converted TLG file and returns a list of header titles within it"""
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
        """read index_file_author.txt, read author file, and expand dict to include author works, index_author_works.txt"""
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
        orig_files_dir_tlg_index_meta = os.path.join(self.orig_files_dir, 'tlg', 'LSTSCDCN.DIR')
        compiled_files_dir_tlg_meta = os.path.join(self.compiled_files_dir, 'tlg', 'index_meta.txt')
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
        compiled_files_dir_phi7_index = os.path.join(self.compiled_files_dir, 'phi7', 'index_file_author.txt')
        try:
            with open(compiled_files_dir_phi7_index, 'r') as index_opened:
                phi7_index = index_opened.read()
                phi7_index = ast.literal_eval(phi7_index)
                return phi7_index
        except IOError:
            logging.error('Failed to open PHI7 index file index_file_author.txt.')

    #not tested
    def make_phi7_index_file_author(self):
        """Reads phi7's AUTHTAB.DIR and writes a dict (index_file_author.txt) to the CLTK's corpus directory."""
        logging.info('Starting phi7 index parsing.')
        orig_files_dir_phi7_index = os.path.join(self.orig_files_dir, 'phi7', 'AUTHTAB.DIR')
        compiled_files_dir_phi7 = os.path.join(self.compiled_files_dir, 'phi7')
        try:
            with open(orig_files_dir_phi7_index, 'rb') as index_opened:
                index_read = index_opened.read().decode('latin-1')
                index_split = index_read.split('ÿ')[2:-9]
                index_filter = [item for item in index_split if item]
                INDEX_DICT_PHI7 = {}
                for file in index_filter:
                    file_repl = file.replace('l', '').replace('g', '')\
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
                compiled_files_dir_phi7_authtab = os.path.join(compiled_files_dir_phi7, 'index_file_author.txt')
                try:
                    with open(compiled_files_dir_phi7_authtab, 'w') as authtab_opened:
                        authtab_opened.write(str(INDEX_DICT_PHI7))
                        logging.info('Finished writing PHI7 index_file_author.txt.')
                except IOError:
                    logging.error('Failed to write PHI7 index_file_author.txt.')
        except IOError:
            logging.error('Failed to open PHI7 index file AUTHTAB.DIR')

    #not tested
    def read_phi7_index_file_author(self):
        """Reads CLTK's index_file_author.txt for PHI7."""
        global phi7_index
        logging.info('Starting phi7 index_file_author.txt read.')
        compiled_files_dir_phi7_index = os.path.join(self.compiled_files_dir, 'phi7', 'index_file_author.txt')
        try:
            with open(compiled_files_dir_phi7_index, 'r') as index_opened:
                phi7_index = index_opened.read()
                phi7_index = ast.literal_eval(phi7_index)
                return phi7_index
        except IOError:
            logging.error('Failed to open PHI7 index file index_file_author.txt.')

    def read_phi7_author_work_titles(self, auth_abbrev):
        """Reads a converted phi7 file and returns a list of header titles within it"""
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
        """read index_file_author.txt, read author file, and expand dict to include author works, index_author_works.txt"""
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

    #add smart parsing of beta code tags
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
                    #local_replacer = Replacer()
                    #new_uni = local_replacer.beta_code(txt_ascii)
                    file_name_txt_uni = file_name + '.txt'
                    file_path = os.path.join(compiled_files_dir_phi7, file_name_txt_uni)
                    try:
                        with open(file_path, 'w') as new_file:
                            new_file.write(txt_ascii)
                    except IOError:
                        logging.error('Failed to write to new file %s of author %s', file_name, abbrev)
                logging.info('Finished PHI7 corpus compilation to %s', file_path)
            except IOError:
                logging.error('Failed to open PHI7 file %s of author %s', file_name, abbrev)
        self.make_phi7_index_auth_works()


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
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dest)