"""Assembles JSON files of PHI and TLG corpora"""

import json
import logging
import os
import re
import ast
from pprint import pprint
from cltk.corpus.classical_greek.replacer import Replacer

INDEX_DICT_PHI5 = {}
INDEX_DICT_PHI7 = {}
INDEX_DICT_TLG = {}


class Compile(object):
    """Make JSON files out of TLG & PHI disks"""

    def __init__(self, corpora_root='.', project_root='cltk/corpus'):
        """Initializer, optional corpora and project"""
        self.corpora_root = corpora_root
        self.project_root = project_root
        logging.basicConfig(filename='compiler.log',
                            level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def uppercase_files(self):
        """Uppercase corpora file names"""
        corpus_list = ['TLG_E', 'PHI5', 'PHI7']
        for directory in corpus_list:
            corpus_dir = self.corpora_root + '/' + directory
            os.chdir(corpus_dir)
            for filename in os.listdir('.'):
                new = filename.upper()
                os.rename(filename, new)

    def open_index_phi7(self):
        """Creates a dictionary of PHI7 collections and file names."""
        global INDEX_DICT_PHI7
        logging.info('Starting PHI7 index parsing.')
        #phi7_path = self.project_root + '/classical_greek/plaintext/phi_7'
        index = 'AUTHTAB.DIR'
        local_index = self.corpora_root + '/' + 'PHI7/' + index
        try:
            with open(local_index, 'rb') as index_opened:
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
                return INDEX_DICT_PHI7
        except IOError:
            logging.error('Failed to open PHI7 index file AUTHTAB.DIR')

    def dump_txts_phi7(self):
        """reads file and translates to ascii"""
        logging.info('Starting PHI7 corpus compilation.')
        phi7_path = self.project_root + '/classical_greek/plaintext/phi_7'
        self.open_index_phi7()
        phi7_dict = {}
        for file_name in INDEX_DICT_PHI7:
            abbrev = INDEX_DICT_PHI7[file_name]
            files_path = self.corpora_root + '/' + 'PHI7' + '/' \
              + file_name + '.TXT'
            try:
                with open(files_path, 'rb') as txt_opened:
                    txt_read = txt_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    print(txt_ascii)
                    phi7_dict[abbrev] = txt_ascii
            except IOError:
                logging.error('Failed to open PHI7 file %s of author %s',
                              file_name, abbrev)
        json_path = phi7_path + '/' + 'phi7.json'
        try:
            with open(json_path, 'w') as json_opened:
                json_array = json.dumps(phi7_dict)
                json_opened.write(json_array)
        except IOError:
            logging.error('Failed to create and/or write to file phi7.json.')
        logging.info('Finished PHI7 corpus compilation.')

    def dump_txts_phi7_files(self):
        """reads file and translates to ascii"""
        logging.info('Starting PHI7 corpus compilation into files.')
        phi7_path = self.project_root + '/classical_greek/plaintext/phi_7'
        self.open_index_phi7()
        for file_name in INDEX_DICT_PHI7:
            abbrev = INDEX_DICT_PHI7[file_name]
            files_path = self.corpora_root + '/' + 'PHI7' + '/' \
              + file_name + '.TXT'
            try:
                with open(files_path, 'rb') as txt_opened:
                    txt_read = txt_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    file_path = phi7_path + '/' + file_name + '.txt'
                    print(file_path)
                    try:
                        with open(file_path, 'w') as new_file:
                            new_file.write(txt_ascii)
                    except IOError:
                        logging.error('Failed to write to new file %s of \
                        author %s', file_name, abbrev)
            except IOError:
                logging.error('Failed to open PHI7 file %s of author %s', \
                              file_name, abbrev)
                #later delete the authdab-making part dict
        authtab_path = phi7_path + '/' + 'authtab.txt'
        print(authtab_path)
        try:
            with open(authtab_path, 'w') as authtab_opened:
                authtab_opened.write(str(INDEX_DICT_PHI7))
        except IOError:
            logging.error('Failed to create and/or write to file tlg.json.')
        logging.info('Finished PHI7 corpus compilation.')

    def open_index_phi5(self):
        """Creates a dictionary of PHI5 collections and file names."""
        global INDEX_DICT_PHI5
        logging.info('Starting PHI5 index parsing.')
        index = 'AUTHTAB.DIR'
        local_index = self.corpora_root + '/' + 'PHI5/' + index
        try:
            with open(local_index, 'rb') as index_opened:
                index_read = index_opened.read().decode('latin-1')
                index_split = index_read.split('ÿ')[1:-21]
                index_filter = [item for item in index_split if item]
                INDEX_DICT_PHI5 = {}
                for file in index_filter:
                    file_repl = file.replace('\x83l', '')\
                      .replace('', '; ').replace('&1', '')\
                      .replace('&', '')
                    file_split = file_repl.split(' ', 1)
                    label = file_split[0]
                    name = file_split[1]
                    INDEX_DICT_PHI5[label] = name
                logging.info('Finished PHI5 index parsing.')
                return INDEX_DICT_PHI5
        except IOError:
            logging.error('Failed to open PHI5 index file AUTHTAB.DIR')

    def dump_txts_phi5(self):
        """reads file and translates to ascii"""
        logging.info('Starting PHI5 corpus compilation.')
        phi5_path = self.project_root + '/classical_latin/plaintext/phi_5'
        self.open_index_phi5()
        phi5_dict = {}
        for file_name in INDEX_DICT_PHI5:
            abbrev = INDEX_DICT_PHI5[file_name]
            files_path = self.corpora_root + '/' + 'PHI5' + '/' \
              + file_name + '.TXT'
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    phi5_dict[abbrev] = txt_ascii
            except IOError:
                logging.error('Failed to open PHI5 file %s of author %s',
                              file_name, abbrev)
        json_path = phi5_path + '/' + 'phi5.json'
        try:
            with open(json_path, 'w') as phi5_json:
                phi5_json_array = json.dumps(phi5_dict)
                phi5_json.write(phi5_json_array)
        except IOError:
            logging.error('Failed to create and write to file phi5.json.')
        logging.info('Finished PHI5 corpus compilation.')

    def dump_txts_phi5_files(self):
        """reads file and translates to ascii"""
        logging.info('Starting PHI5 corpus compilation.')
        phi5_path = self.project_root + '/classical_latin/plaintext/phi_5'
        self.open_index_phi5()
        for file_name in INDEX_DICT_PHI5:
            abbrev = INDEX_DICT_PHI5[file_name]
            files_path = self.corpora_root + '/' + 'PHI5' + '/' \
              + file_name + '.TXT'
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    file_path = phi5_path + '/' + file_name + '.txt'
                    print(file_path)
                    try:
                        with open(file_path, 'w') as new_file:
                            new_file.write(txt_ascii)
                    except IOError:
                        logging.error('Failed to write to new file %s of \
                        author %s', file_name, abbrev)
            except IOError:
                logging.error('Failed to open PHI5 file %s of author %s', \
                              file_name, abbrev)
        #later delete the authdab-making part dict
        authtab_path = phi5_path + '/' + 'authtab.txt'
        print(authtab_path)
        try:
            with open(authtab_path, 'w') as authtab_opened:
                authtab_opened.write(str(INDEX_DICT_PHI5))
        except IOError:
            logging.error('Failed to create and/or write to file tlg.json.')
        logging.info('Finished PHI5 corpus compilation.')

    def find_phi5_works(self, auth_abbrev):
        """Finds texts within a generator author Unicode .txt file"""
        global WORKS
        logging.info('Starting to find works within a PHI5 author file.')
        phi5_path = self.project_root + '/classical_latin/plaintext/phi_5'
        auth_file = phi5_path + '/' + auth_abbrev + '.txt'
        with open(auth_file) as open_file:
            string = open_file.read()
            title_reg = re.compile('\{1.{1,50}?\}1')
            WORKS = title_reg.findall(string)
            return WORKS

    def write_phi5_auth_works(self):
        """read authtab.txt, read author file, and expand dict
        to include author works
        """
        logging.info('Starting to compile auth-works dict')
        phi5_path = self.project_root + '/classical_latin/plaintext/phi_5'
        authtab_path = phi5_path + '/authtab.txt'
        with open(authtab_path) as file_opened:
            read = file_opened.read()
            dict_read = ast.literal_eval(read)
            auth_work_dict = {}
            for key in dict_read:
                auth_node = {}
                self.find_phi5_works(key)
                auth_name = dict_read[key]
                auth_node['phi5_file'] = key
                auth_node['phi5_name'] = auth_name
                auth_node['works'] = WORKS
                auth_work_dict[auth_name] = auth_node
            file_path = phi5_path + '/' + 'auth_work.txt'
            try:
                with open(file_path, 'w') as new_file:
                    pprint(auth_work_dict, stream=new_file)
            except IOError:
                logging.error('Failed to write to auth_work.txt')
        logging.info('Finished compiling auth-works dict')

    def open_index_tlg(self):
        """Creates a dictionary of TLG collections and file names."""
        global INDEX_DICT_TLG
        logging.info('Starting TLG index parsing.')
        #tlg_e_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        index = 'AUTHTAB.DIR'
        local_index = self.corpora_root + '/' + 'TLG_E/' + index
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
                      .replace('1D', 'D').replace('1L', 'L').replace('', ' ')
                    file_split = file_repl.split(' ', 1)
                    label = file_split[0]
                    name = file_split[1]
                    INDEX_DICT_TLG[label] = name
                logging.info('Finished TLG index parsing.')
                return INDEX_DICT_TLG
        except IOError:
            logging.error('Failed to open TLG index file AUTHTAB.DIR')

    def dump_txts_tlg(self):
        """reads file and translates to ascii"""
        logging.info('Starting TLG corpus compilation.')
        tlg_e_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        self.open_index_tlg()
        tlg_dict = {}
        for file_name in INDEX_DICT_TLG:
            abbrev = INDEX_DICT_TLG[file_name]
            files_path = self.corpora_root + '/' + 'TLG_E' + '/' \
              + file_name + '.TXT'
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    local_replacer = Replacer()
                    new_uni = local_replacer.beta_code(txt_ascii)
                    #print(new_uni)
                    tlg_dict[abbrev] = new_uni
            except IOError:
                logging.error('Failed to open TLG file %s of author %s',
                              file_name, abbrev)
        json_path = tlg_e_path + '/' + 'tlg.json'
        try:
            with open(json_path, 'w') as json_opened:
                json_array = json.dumps(tlg_dict)
                json_opened.write(json_array)
        except IOError:
            logging.error('Failed to create and/or write to file tlg.json.')
        logging.info('Finished TLG corpus compilation.')

    def dump_txts_tlg_files(self):
        """reads file and translates to ascii"""
        logging.info('Starting TLG corpus compilation into files.')
        tlg_e_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        self.open_index_tlg()
        for file_name in INDEX_DICT_TLG:
            abbrev = INDEX_DICT_TLG[file_name]
            files_path = self.corpora_root + '/' + 'TLG_E' + '/' \
              + file_name + '.TXT'
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    local_replacer = Replacer()
                    new_uni = local_replacer.beta_code(txt_ascii)
                    file_path = tlg_e_path + '/' + file_name +\
                       '.txt'
                    print(file_path)
                    try:
                        with open(file_path, 'w') as new_file:
                            new_file.write(new_uni)
                    except IOError:
                        logging.error('Failed to write to new file %s of \
                        author %s', file_name, abbrev)
            except IOError:
                logging.error('Failed to open TLG file %s of author %s',
                              file_name, abbrev)
        #later delete the authdab-making part dict
        authtab_path = tlg_e_path + '/' + 'authtab.txt'
        print(authtab_path)
        try:
            with open(authtab_path, 'w') as authtab_opened:
                authtab_opened.write(str(INDEX_DICT_TLG))
        except IOError:
            logging.error('Failed to create and/or write to file tlg.json.')
        logging.info('Finished TLG corpus compilation.')

    def dump_txts_tlg_idt(self):
        """reads idt files and translates to ascii"""
        logging.info('Starting to read and write TLG .idt files.')
        tlg_e_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        self.open_index_tlg()
        for file_name in INDEX_DICT_TLG:
            abbrev = INDEX_DICT_TLG[file_name]
            files_path = self.corpora_root + '/' + 'TLG_E' + '/' \
              + file_name + '.IDT'
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    file_path = tlg_e_path + '/' + file_name +\
                       '.idt'
                    print(file_path)
                    try:
                        with open(file_path, 'w') as new_file:
                            #print(txt_read)
                            new_file.write(txt_read)
                    except IOError:
                        logging.error('Failed to write to new file %s of \
                        author %s', file_name, abbrev)
            except IOError:
                logging.error('Failed to open TLG file %s of author %s',
                              file_name, abbrev)
        logging.info('Finished TLG .idt compilation.')

    def write_tlg_meta_index(self):
        """Reads and writes the LSTSCDCN.DIR file"""
        logging.info('Starting to read the TLG file LSTSCDCN.DIR.')
        index = 'LSTSCDCN.DIR'
        tlg_e_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        local_index = self.corpora_root + '/' + 'TLG_E/' + index
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

    def find_tlg_works(self, auth_abbrev):
        """Finds texts within a generator author Unicode .txt file"""
        global WORKS
        logging.info('Starting to find works within a TLG author file.')
        tlg_e_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        auth_file = tlg_e_path + '/' + auth_abbrev + '.txt'
        with open(auth_file) as file_opened:
            string = file_opened.read()
            title_reg = re.compile('\{1.{1,50}?\}1')
            WORKS = title_reg.findall(string)
            return WORKS

    def write_tlg_auth_works(self):
        """read authtab.txt, read author file, and expand dict to
        include author works
        """
        logging.info('Starting to compile auth-works dict')
        tlg_e_path = self.project_root + '/classical_greek/plaintext/tlg_e'
        authtab_path = tlg_e_path + '/authtab.txt'
        with open(authtab_path) as file_opened:
            read = file_opened.read()
            dict_read = ast.literal_eval(read)
            auth_work_dict = {}
            for key in dict_read:
                auth_node = {}
                self.find_tlg_works(key)
                auth_name = dict_read[key]
                auth_node['tlg_file'] = key
                auth_node['tlg_name'] = auth_name
                auth_node['works'] = WORKS
                auth_work_dict[auth_name] = auth_node
            file_path = tlg_e_path + '/' + 'auth_work.txt'
            try:
                with open(file_path, 'w') as new_file:
                    pprint(auth_work_dict, stream=new_file)
            except IOError:
                logging.error('Failed to write to auth_work.txt')
        logging.info('Finished compiling auth-works dict')

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
