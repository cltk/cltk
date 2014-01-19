"""Assembles JSON files of PHI and TLG corpora"""

import json
import logging
import os
import re
from cltk.replacer import Replacer


INDEX_DICT_PHI5 = {}
INDEX_DICT_PHI7 = {}
INDEX_DICT_TLG = {}


class Compile(object):
    """Make JSON files out of TLG & PHI disks"""

    def __init__(self, corpora_root='.', project_root='.'):
        """Initializer, optional corpora and project"""
        self.corpora_root = corpora_root
        self.project_root = project_root
        local_project_save = self.project_root + '/' \
          + 'cltk.log'
        #clear_log()
        logging.basicConfig(filename=local_project_save,
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
        local_project_save = self.project_root + '/' + 'phi7.json'
        try:
            with open(local_project_save, 'w') as json_opened:
                json_array = json.dumps(phi7_dict)
                json_opened.write(json_array)
        except IOError:
            logging.error('Failed to create and/or write to file phi7.json.')
        self.confirm_json_present('PHI7')
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
        local_project_save = self.project_root + '/' + 'phi5.json'
        try:
            with open(local_project_save, 'w') as phi5_json:
                phi5_json_array = json.dumps(phi5_dict)
                phi5_json.write(phi5_json_array)
        except IOError:
            logging.error('Failed to create and write to file phi5.json.')
        self.confirm_json_present('PHI5')
        logging.info('Finished PHI5 corpus compilation.')

    def open_index_tlg(self):
        """Creates a dictionary of TLG collections and file names."""
        global INDEX_DICT_TLG
        logging.info('Starting TLG index parsing.')
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
        self.open_index_tlg()
        for file_name in INDEX_DICT_TLG:
            tlg_dict = {}
            abbrev = INDEX_DICT_TLG[file_name]
            files_path = self.corpora_root + '/' + 'TLG_E' + '/' \
              + file_name + '.TXT'
            try:
                with open(files_path, 'rb') as index_opened:
                    txt_read = index_opened.read().decode('latin-1')
                    txt_ascii = remove_non_ascii(txt_read)
                    r = Replacer()
                    new_uni = r.beta_code(txt_ascii)
                    tlg_dict[abbrev] = new_uni
                    local_project_save = self.project_root + '/' + 'tlg.json'
                    loaded_json = {}
                    try:
                        with open(local_project_save, 'r') as tlg_json:
                            loaded_json = json.load(tlg_json)
                    except ValueError:
                        print("ValueError, no JSON")
                        pass
                    loaded_json.update(tlg_dict)
                    with open(local_project_save, 'w') as tlg_json:
                        json.dump(loaded_json, tlg_json)
                        print("Wrote json with .dump().")
                        '''
                        a_dict = {'new_key': 'new_value'}
                        with open('test.json') as f:
                            data = json.load(f)
                        data.update(a_dict)
                        with open('test.json', 'w') as f:
                            json.dump(data, f)
                        '''
                        #tlg_json_array = json.dumps(tlg_dict)
                        #tlg_json.write(tlg_json_array)
            except IOError:
                logging.error('Failed to open TLG file %s of author %s',
                              file_name, abbrev)
        self.confirm_json_present('TLG_E')
        logging.info('Finished TLG corpus compilation.')

    def confirm_json_present(self, directory):
        """Checks that the JSON file is in fact present and opens OK"""
        logging.info('Confirming JSON file saved.')
        if directory == 'PHI7':
            present = os.path.isfile(self.project_root + '/' + 'phi7.json')
        elif directory == 'PHI5':
            present = os.path.isfile(self.project_root + '/' + 'phi5.json')
        elif directory == 'TLG_E':
            present = os.path.isfile(self.project_root + '/' + 'tlg.json')
        if present is True:
            logging.info('%s JSON file is present.', directory)
        else:
            logging.error('%s JSON file is not present.', directory)

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
