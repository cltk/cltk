# encoding: utf-8
"""The `corpus` class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import os
import ssl
import bs4
import json
import shutil
import requests
from urllib.parse import urlsplit
from requests_toolbelt import SSLAdapter
from cltk.corpora.classical_greek.beta_to_unicode import Replacer

from cltk.main import CLTK


class Corpus(object):
    def __init__(self, name):
        # Initialize class of specified corpus
        self.name = name
        self.location = None
        self.cltk = CLTK()
        self.logger = self.cltk.logger

    @property
    def compiled_texts(self):
        compiled_texts = os.path.join(self.cltk.compiled_dir, self.name)
        return self.cltk.resolve_path(compiled_texts)

    @property
    def original_texts(self):
        original_texts = os.path.join(self.cltk.originals_dir, self.name)
        return self.cltk.resolve_path(original_texts)

    def retrieve(self, location=None, url=None):
        if location is None and url is not None:
            self.get_tar(url)
        elif url is None and location is not None:
            self.copy_contents(location)

    def get_tar(self, url):
        # Initiate HTTP session
        session = requests.Session()
        session.mount(url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        pg_tar = session.get(url, stream=True)
        # Prepare local file
        file_name = urlsplit(url).path.split('/')[-1]
        file_path = os.path.join(self.original_texts, file_name)
        # Write tar data to file in originals dir
        self._write_tar(pg_tar, file_path)
        # Unpack tar data in compiled dir
        self._unpack_tar(file_path)

    def copy_contents(self, location):
        """Copy contents of one directory to another"""
        for file_name in os.listdir(location):
            full_file_name = os.path.join(location, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, self.original_texts)

    def prettify_all(self):
        prettified = os.path.join(self.compiled_texts, '.prettified')
        if os.path.exists(prettified):
            return True
        else:
            for name, folders, files in os.walk(self.compiled_texts):
                for fname in files:
                    if fname.endswith('xml'):
                        path = os.path.join(name, fname)
                        soup = TEIDoc(path).soup
                        pretty_soup = soup.prettify()
                        with open(path, 'w', encoding='utf-8') as file:
                            file.write(pretty_soup)
            with open(prettified, 'w', encoding='utf-8') as file:
                file.write('All documents now prettified.')
            return True
        # On run on 2013 MBA: 202.8s, 266.0s, 276.5s

    def tei_tags(self):
        text_tags = os.path.join(self.compiled_texts, 'tei_tags_index.json')
        try:
            with open(text_tags, 'r') as file:
                tag_index = json.load(file)
        except FileNotFoundError:
            tag_index = {}
            for name, folders, files in os.walk(self.compiled_texts):
                for fname in files:
                    if fname.endswith('xml'):
                        path = os.path.join(name, fname)
                        tags = TEIDoc(path).tags()
                        tag_index[fname] = tags
            with open(text_tags, 'w', encoding='utf-8') as f:
                f.write(json.dumps(tag_index,
                                   sort_keys=True,
                                   indent=2,
                                   separators=(',', ': '))
                        )
        return tag_index

    def _write_tar(self, tar, path):
        try:
            with open(path, 'wb') as file:
                file.write(tar.content)
            msg = 'Wrote tar file to : {}'.format(path)
            self.cltk.logger.info(msg)
        except IOError:
            msg = 'Failed to write tar file to : {}'.format(path)
            self.cltk.logger.error(msg)

    def _unpack_tar(self, tar_path):
        try:
            shutil.unpack_archive(tar_path,
                                  self.cltk.compiled_dir)
            msg = 'Unpacked tar to : {}'.format(tar_path)
            self.cltk.logger.info(msg)
        except IOError:
            msg = 'Failed to unpack tar to : {}'.format(tar_path)
            self.cltk.logger.error(msg)

    def remove_non_ascii(self, input_string):
        """remove non-ascii: http://stackoverflow.com/a/1342373"""
        return "".join(i for i in input_string if ord(i) < 128)


class TEIDoc(object):
    def __init__(self, path):
        self.path = path
        self.beta_replacer = Replacer()

    @property
    def soup(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            xml_data = f.read()
        return bs4.BeautifulSoup(xml_data)

    @property
    def struct_tags(self):
        struct_info = self.soup.find('encodingdesc')
        structs = struct_info.find_all('refsdecl')
        return [c.attrs.values() for s in structs
                for c in s.contents
                if c.name]

    def tags(self, text_only=False):
        if text_only:
            tags = self.soup.find('text').find_all(True)
        else:
            tags = self.soup.find_all(True)
        tag_names = [x.name for x in tags if x.name]
        return list(set(tag_names))
