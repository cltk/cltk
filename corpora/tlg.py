# encoding: utf-8
"""TLG Greek texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import os
import re
import bs4
import json
import requests
import subprocess
from cltk.corpus import LocalCorpus, TXTDoc


class TLG(LocalCorpus):
    def __init__(self, path):
        self.name = 'tlg'
        self.path = path
        LocalCorpus.__init__(self, self.name, self.path)
        self.tlgu = TLGU()

    def retrieve(self):
        return self.retrieve(location=self.path)

    def compile(self):
        """Reads original Beta Code files and converts to Unicode files

        """
        self.logger.info('Starting TLG corpus compilation into files.')
        for file_name, abbrev in self.authors.items():
            orig_file = file_name + '.TXT'
            orig_path = os.path.join(self.original_texts, orig_file)
            #try:
            compiled_file = file_name + '.txt'
            compiled_path = os.path.join(self.compiled_texts,
                                         compiled_file)
            # Use `tlgu` utility to compile to Unicode text
            self.tlgu.run(orig_path, compiled_path,
                          opts=['-X', '-b'])
            msg = 'Compiled {} to : {}'.format(file_name, compiled_path)
            self.logger.info(msg)
            #except IOError:
            #    msg = 'Failed to compile {}'.format(file_name)
            #    self.logger.error(msg)

    @property
    def metadata(self):
        return self._property('meta_index.json', self.index_meta)

    @property
    def authors(self):
        return self._property('authors_index.json', self.index_authors)

    @property
    def works(self):
        return self._property('works_index.json', self.index_works)

    def index_works(self, path):
        self.logger.info('Starting TLG works index parsing.')
        works_dict = {}
        for file_name, auth_name in self.authors.items():
            d = {}
            d['tlg_file'] = file_name
            d['tlg_name'] = auth_name
            d['works'] = self._get_author_titles(file_name)
            works_dict[auth_name] = d
        output_path = os.path.join(self.compiled_texts, 'works_index.json')
        try:
            with open(output_path, 'w') as file:
                file.write(json.dumps(works_dict,
                                      sort_keys=True,
                                      indent=2,
                                      separators=(',', ': ')))
            return works_dict
        except IOError:
            msg = "Failed to write TLG's `works_index.json`"
            self.logger.error(msg)

    def _get_author_titles(self, auth_abbrev):
        """Reads a converted TLG file and returns a list of header titles
        within it
        """
        author_file = auth_abbrev + '.txt'
        author_path = os.path.join(self.compiled_texts, author_file)
        with open(author_path, 'r', encoding='utf-8') as file:
            data = file.read()
        title_re = re.compile('\{1.{1,50}?\}1')
        return title_re.findall(data)

    def index_meta(self, path):
        """Reads TLG's `LSTSCDCN.DIR` and writes a JSON dict
        to `meta_index.json` in the CLTK's corpus directory.

        """
        splitter = lambda x: x.split('ÿ')[2:-3]
        
        def to_dict(item):
            rg_key = re.compile('^[AUT|AWN|BIB|DAT|LIS]{3}?.{5}?')
            m_key = rg_key.findall(item)
            m_value = rg_key.split(item)
            if m_key and m_value:
                return m_key[0], m_value[1]
            else:
                return None

        return self._indexer('LSTSCDCN.DIR', path, splitter, to_dict)

    def index_authors(self, path):
        """Reads TLG's `AUTHTAB.DIR` and writes a JSON dict
        to `author_index.json` in the CLTK's corpus directory.

        """
        splitter = lambda x: x.split('ÿ')[1:-7]

        def to_dict(item):
            item_repl = item.replace(' &1', ' ').replace('&', '') \
                            .replace(' 1', ' ').replace('-1', '-')\
                            .replace('[2', '[').replace(']2', ']')\
                            .replace('1Z', '').replace('1P', 'P') \
                            .replace('1D', 'D').replace('1L', 'L')\
                            .replace('Â€', ' ')
            item_split = item_repl.split(' ', 1)
            return item_split[0], item_split[1]

        return self._indexer('AUTHTAB.DIR', path, splitter, to_dict)

    


class TLGU(object):
    def __init__(self):
        self.name = 'tlgu'
        self.url = 'http://tlgu.carmen.gr'

    @property
    def exe(self):
        find_exe = ['mdfind', 'kMDItemFSName=tlgu',
                    'kMDItemContentType=public.unix-executable']
        c_path = subprocess.check_output(find_exe)
        exe_paths = c_path.split(b'\n')
        if len(exe_paths) > 0:
            return exe_paths[0]
        else:
            self.compile()
            return self.exe

    def compile(self):
        if subprocess.check_output(['which', 'gcc']):
            find_c = ['mdfind', 'kMDItemFSName=tlgu.c']
            c_path = subprocess.check_output(find_c)
            c_path = c_path.strip()
            if c_path:
                # If running in a Virtual Env,
                # it should create the executable file
                # at `[venv]/lib/python3.4/site-packages/cltk/tlgu`
                compile_c = ['gcc', c_path, '-o', 'tlgu']
                subprocess.check_output(compile_c)
            else:
                self.download()
                self.compile()
        else:
            raise Error('Cannot compile `tlgu` without `gcc`!')

    def run(self, input_path, output_path, opts=[]):
        convert_tlg = [self.exe]
        if opts != []:
            convert_tlg.extend(opts)
        convert_tlg.extend([input_path, output_path])
        return subprocess.call(convert_tlg)

    def download(self):
        zip_url = self._get_zip_url()
        #Download zip to temp file
        #Unpack to temp dir
        #Compile

    def _get_zip_url(self):
        r = requests.get(self.url)
        soup = bs4.BeautifulSoup(r.text)
        download = soup.find('a', {'href': re.compile('.zip')}).get('href')
        return '/'.join([self.url, download])

    


class TLGDoc(TXTDoc):
    def __init__(self, path):
        self.path = path
        TXTDoc.__init__(self, self.path)

print(TLG('~').compile())
