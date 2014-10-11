# encoding: utf-8
"""The `corpus` class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import os
import ssl
import json
import shutil
import requests
from urllib.parse import urlsplit
from requests_toolbelt import SSLAdapter

from cltk.corpus_api.common.corpora_attributes import CORPORA
from cltk import CLTK


class CorpusError(Exception):
    """Error with Corpus.
    """


class Corpus(object):
    def __init__(self, name):
        # Initialize class of specified corpus
        self.name = name
        # Initialize emptry properties
        self._languages = None
        self._retrieval = None
        self._font_encoding = None
        self._file_encoding = None
        self._markup = None
        # Initialize global vars
        self.cltk = CLTK()
        self.logger = self.cltk.logger
        self.attributes = CORPORA.get(self.name, None)

## Attribute Properties ---------------------------------------------------

    @property
    def languages(self):
        if self._languages:
            return self._languages
        elif self.attributes:
            return self.attributes['languages']
        else:
            raise CorpusError("You haven't set `languages` yet.")

    @languages.setter
    def languages(self, value):
        self._languages = value

    @property
    def retrieval(self):
        if self._retrieval:
            return self._retrieval
        elif self.attributes:
            return self.attributes['retrieval']
        else:
            raise CorpusError("You haven't set `retrieval` yet.")

    @retrieval.setter
    def retrieval(self, value):
        self._retrieval = value

    @property
    def font_encoding(self):
        if self._font_encoding:
            return self._font_encoding
        elif self.attributes:
            return self.attributes['font_encoding']
        else:
            raise CorpusError("You haven't set `font_encoding` yet.")

    @font_encoding.setter
    def font_encoding(self, value):
        self._font_encoding = value

    @property
    def file_encoding(self):
        if self._file_encoding:
            return self._file_encoding
        elif self.attributes:
            return self.attributes['file_encoding']
        else:
            raise CorpusError("You haven't set `file_encoding` yet.")

    @file_encoding.setter
    def file_encoding(self, value):
        self._file_encoding = value

    @property
    def markup(self):
        if self._markup:
            return self._markup
        elif self.attributes:
            return self.attributes['markup']
        else:
            raise CorpusError("You haven't set `markup` yet.")

    @markup.setter
    def markup(self, value):
        self._markup = value

## Directory Properties ---------------------------------------------------

    @property
    def compiled_texts(self):
        compiled_texts = os.path.join(self.cltk.compiled_dir, self.name)
        return self.cltk.resolve_path(compiled_texts)

    @property
    def original_texts(self):
        original_texts = os.path.join(self.cltk.originals_dir, self.name)
        return self.cltk.resolve_path(original_texts)

## Retrieval code paths ---------------------------------------------------

    def retrieve(self, location):
        """Retrieve corpus data from `location` and
        move into the corpus' `/originals` directory within
        the CLTK's `/cltk_data` directory.

        :param location: location of corpus data.
                         Either file path or URL.
        :type location: ``unicode``

        """
        if self.retrieval == 'local':
            self._retrieve_local(location)
        elif self.retrieval == 'remote':
            self._retrieve_remote(location)

    def _retrieve_local(self, path):
        """Copy corpus data from `path` to `/originals` directory.

        :param path: file path of corpus data
        :type path: ``unicode``

        """
        for file_name in os.listdir(path):
            full_file_name = os.path.join(path, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, self.original_texts)

    def _retrieve_remote(self, url):
        """Download corpus data from `url` and
        move into to `/originals` directory.

        :param url: URL of corpus data
        :type url: ``unicode``

        """
        # Initiate HTTP session
        session = requests.Session()
        session.mount(url, SSLAdapter(ssl.PROTOCOL_TLSv1))
        remote_data = session.get(url, stream=True)
        # Prepare local file
        file_name = urlsplit(url).path.split('/')[-1]
        file_path = os.path.join(self.original_texts, file_name)
        # Write tar data to file in originals dir
        self._write_tar(remote_data, file_path)

    def _write_tar(self, tar, path):
        try:
            with open(path, 'wb') as file:
                file.write(tar.content)
            msg = 'Wrote tar file to : {}'.format(path)
            self.logger.info(msg)
        except IOError:
            msg = 'Failed to write tar file to : {}'.format(path)
            self.logger.error(msg)

## Compiling code paths ---------------------------------------------------

    def compile(self):
        if self.file_encoding == 'latin-1':
            self._compile_binary()
        elif self.file_encoding == 'utf-8':
            self._compile_unicode()

    # TODO: fix `tglu` calls
    def _compile_binary(self):
        msg = 'Starting `{}` corpus compilation'.format(self.name)
        self.logger.info(msg)
        for file_name, abbrev in self.authors.items():
            orig_file = '.'.join([file_name, 'TXT'])
            orig_path = os.path.join(self.original_texts, orig_file)
            try:
                compiled_file = '.'.join([file_name, 'txt'])
                compiled_path = os.path.join(self.compiled_texts,
                                             compiled_file)
                # Use `tlgu` utility to compile to Unicode text
                self.tlgu.run(orig_path, compiled_path,
                              opts=['-X', '-b'])
                msg = 'Compiled {} to : {}'.format(file_name, compiled_path)
                self.logger.info(msg)
            except IOError:
                msg = 'Failed to compile {}'.format(file_name)
                self.logger.error(msg)

    # TODO: what is the argument here?
    def _compile_unicode(self):
        if self.retrieval == 'remote':
            self._unpack_tar(file_path)

    def _unpack_tar(self, tar_path):
        try:
            shutil.unpack_archive(tar_path,
                                  self.cltk.compiled_dir)
            msg = 'Unpacked tar to : {}'.format(tar_path)
            self.logger.info(msg)
        except IOError:
            msg = 'Failed to unpack tar to : {}'.format(tar_path)
            self.logger.error(msg)

    def remove_non_ascii(self, input_string):
        """remove non-ascii: http://stackoverflow.com/a/1342373"""
        return "".join(i for i in input_string if ord(i) < 128)



### Helper Methods

    def _property(self, json_file, index_func):
        path = os.path.join(self.compiled_texts, json_file)
        if os.path.exists(path):
            with open(path, 'r') as file:
                property_index = json.load(file)
        else:
            property_index = index_func(path)
        return property_index

    def _indexer(self, input_file, output_path, splitter_func, to_dict_func):
        output_file = os.path.basename(output_path)
        type = ' '.join([self.name.upper(), output_file.split('_')[0]])
        self.logger.info('Starting {} index parsing.'.format(type))
        orig_index = os.path.join(self.original_texts, input_file)
        try:
            with open(orig_index, 'rb') as file:
                index_read = file.read().decode('latin-1')
            index_split = splitter_func(index_read)
            index_filtered = (item for item in index_split if item)
            index_dict = {}
            for file in index_filtered:
                dict = to_dict_func(file)
                if dict:
                    key, val = dict
                    index_dict[key] = val
            self.logger.info('Finished {} index parsing.'.format(type))
            msg = 'Writing `{}` to : {}'.format(output_file, output_path)
            self.logger.info(msg)
            try:
                with open(output_path, 'w') as file:
                    file.write(json.dumps(index_dict,
                                          sort_keys=True,
                                          indent=2,
                                          separators=(',', ': ')))
                return index_dict
            except IOError:
                msg = "Failed to write `{}`".format(output_file)
                self.logger.error(msg)
        except IOError:
            msg = "Failed to open `{}` index file".format(input_file)
            self.logger.error(msg)
