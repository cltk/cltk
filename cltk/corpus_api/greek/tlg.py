# encoding: utf-8
"""TLG Greek texts class"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import os
import re
import json
from cltk.wrappers.wrapper import TLGU
from cltk.corpora.corpus import Corpus

METADATA_KEYS = {
    'key': 'key',
    'nam': 'name',
    'epi': 'genre',
    'geo': 'geographical_adj',
    'dat': 'date',
    'vid': 'cf',            # ??
    'wrk': 'work',
    'cla': 'classification',
    'xmt': 'format',        # ??
    'typ': 'type',
    'wct': 'word_count',
    'cit': 'citation_structure',
    'tit': 'title',
    'pub': 'publisher',
    'pla': 'publication_place',
    'pyr': 'publication_year',
    'ryr': 'republication_year',
    'rpl': 'republication_place',
    'rpu': 'republication_publisher',
    'pag': 'pages',
    'edr': 'editor',
    'brk': 'broken',        # ??
    'ser': '',              # ??
    'srt': 'short_title',   # ??
    'crf': '',              # ??
    'syn': 'synonym',
    'gen': 'genre',         # relation to `epi`??
    'ref': 'reference'      # ??
}


class TLG(Corpus):
    def __init__(self, path):
        self.name = 'tlg'
        self.path = path
        Corpus.__init__(self, self.name)
        self.tlgu = TLGU()

    def retrieve(self):
        return self.copy_contents()

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

    # TODO
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

    def index_metadata(self):
        # Search `DOCCAN2.TXT` canon metadata file.
        orig_index = os.path.join(self.original_texts, 'DOCCAN2.TXT')
        # Use `tlgu` to convert to ASCII
        new_index = self.tlgu.convert(orig_index, 'full', True, False)
        keys = re.findall(r"\t([a-z]{3})", new_index)
        return set(keys) # 110283 vs 28
        # Split text lines into list
        #index_lines = new_index.split('\n')
        # Split each line into sections
        #index_sections = [x.split("\t")
        #                  for x in index_lines]
        #doccan_re = r"^\.\.(.+?)\.(.+?)\.(.+?)\s+?([a-z]{3})\s{1}(.+?)$"
        #re.findall(doccan_re, searchText)
        return index_sections

    def index_lists(self):
        """Reads TLG's `LSTSCDCN.DIR` and writes a JSON dict
        to `meta_index.json` in the CLTK's corpus directory.

        """
        orig_index = os.path.join(self.original_texts, 'LSTSCDCN.DIR')
        # Use `tlgu` to convert to ASCII
        new_index = self.tlgu.convert(orig_index, 'plain', True, False)
        # Split text lines into list
        index_lines = new_index.split('\n')
        # Split each line into sections
        index_sections = [re.split(r"(?<=[A-Z])([A-Z])(?=[a-z])", x)
                          for x in index_lines]
        # Rejoin split character with following text
        index_dict = {}
        for data in index_sections:
            if len(data) == 3:
                rejoined = ''.join([data[1], data[2]])
                index_dict[data[0]] = rejoined
            else:
                if data[0] and data != ['*END']:
                    desc = re.split('\x01b|\x016|\x01\x14', data[0])
                    index_dict[desc[0]] = desc[1]
        return index_dict

    def index_authors(self):
        """Reads TLG's `AUTHTAB.DIR` and writes a JSON dict
        to `author_index.json` in the CLTK's corpus directory.

        """
        orig_index = os.path.join(self.original_texts, 'AUTHTAB.DIR')
        # Use `tlgu` to convert to ASCII
        new_index = self.tlgu.convert(orig_index, 'full', True, False)
        # Split text lines into list
        index_lines = new_index.split('\n')
        # Split each line into sections
        index_sections = [re.split('\t|(?<=\d)\s', x)[1:] for x in index_lines]
        # Factor out abbreviations
        index_dict = {}
        for i, data in enumerate(index_sections):
            # if only one item, that item is abbrv of previous item
            if len(data) == 1:
                abbrv = '(' + data[0] + ')'
                previous = index_sections[(i - 1)]
                added_abbrv = ' '.join([previous[-1], abbrv])
                index_dict[previous[0]] = added_abbrv
            else:
                try:
                    index_dict[data[0]] = data[1]
                except IndexError:
                    pass
        return index_dict

t = TLG('~').index_metadata()
#print(json.dumps(t[:10]))
print(t)
