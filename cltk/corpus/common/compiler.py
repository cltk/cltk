"""Assembles JSON files of PHI and TLG corpora"""

import ast
import logging
import os
from pprint import pprint
import re
import shutil
import sys

from cltk.corpus.classical_greek.replacer import Replacer


INDEX_DICT_PHI5 = {}
INDEX_DICT_PHI7 = {}
INDEX_DICT_TLG = {}


class Compile(object):
    """Make JSON files out of TLG & PHI disks"""

    def __init__(self):
        """Initializer, optional corpora and project"""
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
            #convert_tlg_txt() #change to look always in ~/cltk_local/originals
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
        tlg_index_path = self.project_root + '/classical_greek/plaintext/tlg_e/index_file_author.txt'
        try:
            with open(tlg_index_path, 'r') as index_opened:
                tlg_index = index_opened.read()
                tlg_index = ast.literal_eval(tlg_index)
                #!!!
                print(self.cltk_local)
                print(self.project_root)
                print(self.cltk_root)
                return tlg_index
        except IOError:
            logging.error('Failed to open TLG index file index_file_author.txt.')

    def make_tlg_index_file_author(self):
        """Reads TLG's AUTHTAB.DIR and writes a dict (index_file_author.txt) to the CLTK's corpus directory."""
        logging.info('Starting TLG index parsing.')
        cltk_tlg_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        index = 'AUTHTAB.DIR'
        local_index = self.cltk_local + '/' + 'TLG_E/' + index
        try:
            with open(local_index, 'rb') as index_opened:
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
                authtab_path = cltk_tlg_path + '/' + 'index_file_author.txt'
                try:
                    with open(authtab_path, 'w') as authtab_opened:
                        authtab_opened.write(str(INDEX_DICT_TLG))
                        logging.info('Finished writing TLG index_file_author.txt.')
                except IOError:
                    logging.error('Failed to write TLG index_file_author.txt.')
        except IOError:
            logging.error('Failed to open TLG index file AUTHTAB.DIR')

    def convert_tlg_txt(self):
        """Reads original Beta Code files and converts to Unicode files"""
        logging.info('Starting TLG corpus compilation into files.')
        tlg_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        self.read_tlg_index_file_author()
        for file_name in tlg_index:
            abbrev = tlg_index[file_name]
            files_path = self.cltk_local + '/TLG_E/' + file_name + '.TXT'
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    local_replacer = Replacer()
                    new_uni = local_replacer.beta_code(txt_ascii)
                    file_path = tlg_path + '/' + file_name + '.txt'
                    try:
                        with open(file_path, 'w') as new_file:
                            new_file.write(new_uni)
                    except IOError:
                        logging.error('Failed to write to new file %s of author %s', file_name, abbrev)
                logging.info('Finished TLG corpus compilation.')
            except IOError:
                logging.error('Failed to open TLG file %s of author %s', file_name, abbrev)

    def read_tlg_author_work_titles(self, auth_abbrev):
        """Reads a converted TLG file and returns a list of header titles within it"""
        global WORKS
        logging.info('Starting to find works within a TLG author file.')
        tlg_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        auth_file = tlg_path + '/' + auth_abbrev + '.txt'
        with open(auth_file) as file_opened:
            string = file_opened.read()
            title_reg = re.compile('\{1.{1,50}?\}1')
            WORKS = title_reg.findall(string)
            return WORKS

    def write_tlg_index_auth_works(self):
        """read index_file_author.txt, read author file, and expand dict to include author works, index_author_works.txt"""
        logging.info('Starting to compile TLG auth_works.txt.')
        tlg_path = self.project_root + '/classical_greek/plaintext/tlg_e'
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
            print(auth_node)
        file_path = tlg_path + '/' + 'index_author_works.txt'
        print(auth_work_dict)
        try:
            with open(file_path, 'w') as new_file:
                pprint(auth_work_dict, stream=new_file)
        except IOError:
            logging.error('Failed to write to index_auth_work.txt')
        logging.info('Finished compiling TLG index_auth_works.txt.')

    def write_tlg_meta_index(self):
        """Reads and writes the LSTSCDCN.DIR file"""
        logging.info('Starting to read the TLG file LSTSCDCN.DIR.')
        index = 'LSTSCDCN.DIR'
        tlg_e_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        local_index = self.cltk_local + '/' + 'TLG_E/' + index
        meta_list_dict = {}
        try:
            with open(local_index, 'rb') as index_opened:
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
                file_path = tlg_e_path + '/' + 'meta_list.txt'
                try:
                    with open(file_path, 'w') as new_file:
                        new_file.write(str(meta_list_dict))
                except IOError:
                    logging.error('Failed to write to meta_list.txt file \
                    of TLG')
        except IOError:
            logging.error('Failed to open TLG index file LSTSCDCN.DIR')

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