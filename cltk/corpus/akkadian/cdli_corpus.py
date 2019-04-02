"""
The Importer feature sets up the ability to work with cuneiform text(s)
one-on-one, whether it is the Code of Hammurabi, a collection of texts such as
ARM01, or whatever your research desires.

This cdli_corpus module is for working with text files having already been read
by file_importer. The file_lines required by CDLICorpus are taken from prior
use of FileImport(text_file).read_file().

e.g.:
    # FileImport takes a txt file and reads it; this becomes file_lines.
        text_path = os.path.join('texts', 'ARM01_texts.txt')
        f_i = FileImport(text_path)
        f_i.read_file()
        ARM01 = f_i.file_lines
    # CDLICorpus takes file_lines and uses it to work:
        cdli = CDLICorpus()
        cdli.parse_file(ARM01)
        cdli.print_catalog()

The output of CDLICorpus will be able to further utilized by the feature
ATFConverter and its subsequent classes: Tokenizer, ATFConverter, Lemmatizer,
and PPrint.
"""

import re

__author__ = ['Andrew Deloucas <ADeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'


class CDLICorpus(object):
    """
    Takes file_lines, prepares and organizes data.
    """

    def __init__(self):
        """
        Empty.
        """
        self.chunks = []
        self.catalog = {}

    def parse_file(self, file_lines):
        """
        Parses lines of file into a dictionary of texts.
        :param file_lines: file_importer.file_lines
        :return: Each text as the form:
            Pnum: {'metadata': List of lines of metadata,
                   'pnum': P-number,
                   'edition': Bibliographic edition,
                   'raw_text': Raw lines of ATF text,
                   'transliteration': lines of transliteration,
                   'normalization': lines of normalization (if present),
                   'translation': lines of translation (if present)}
        """
        # separate the file into chunks of text
        chunks, chunk = [], []
        # check to see what format the corpus is in, we assume that the headers are the same for all
        # texts in the file... (maybe not safe?)
        if re.match('Primary publication:', file_lines[0]):
            header = re.compile('Primary publication:')
        else:
            header = re.compile(r'&?P\d{6}')
        for line in file_lines:
            if header.match(line):
                if len(chunk) > 0:  # pylint: disable=len-as-condition
                    chunks.append(chunk)
                chunk = [line]
            else:
                if len(line) > 0:  # pylint: disable=len-as-condition
                    chunk.append(line)
        chunks.append(chunk)
        self.chunks = chunks
        # create a rich catalog from the chunks
        re_translit = re.compile(r'(\d+\'?\.) ?(.*)')
        re_normaliz = re.compile(r'(#tr\.ts:) ?(.*)')
        re_translat = re.compile(r'(#tr\.en:) ?(.*)')
        for chunk in self.chunks:
            text = chunk
            if chunk[0].startswith('Primary publication:'):
                # we've got full metadata, add additional parsing later
                metadata = chunk[:25]
                text = chunk[26:]
            else:  # no metadata
                metadata = []
            pnum = ''.join([c for c in text[0].split('=')[0] if c != '&']).rstrip()
            edition = text[0].split('=')[1].lstrip()
            text = text[3:]
            translit = []
            normaliz = []
            translat = []
            for line in text:
                if re.match(r'\d+\'?\.', line):
                    translit.append(re_translit.match(line).groups()[1])
                if line.startswith('#tr.ts:'):
                    normaliz.append(re_normaliz.match(line).groups()[1])
                if line.startswith('#tr.en:'):
                    translat.append(re_translat.match(line).groups()[1])
            self.catalog[pnum] = {'metadata': metadata,
                                  'pnum': pnum,
                                  'edition': edition,
                                  'raw_text': text,
                                  'transliteration': translit,
                                  'normalization': normaliz,
                                  'translation': translat}

    def toc(self):
        """
        Returns a rich list of texts in the catalog.
        """
        output = []
        for key in sorted(self.catalog.keys()):
            edition = self.catalog[key]['edition']
            length = len(self.catalog[key]['transliteration'])
            output.append(
                "Pnum: {key}, Edition: {edition}, length: {length} line(s)".format(
                    key=key, edition=edition, length=length))
        return output

    def list_pnums(self):
        """
        Lists all Pnums in the catalog.
        """
        return sorted([key for key in self.catalog])

    def list_editions(self):
        """
        Lists all text editions in the catalog.
        """
        return sorted([self.catalog[key]['edition'] for key in self.catalog])

    def print_catalog(self, catalog_filter=[]):
        """
        Prints out a catalog of all the texts in the corpus.  Can be filtered by passing
        a list of keys you want present in the texts.
        :param: catalog_filter = If you wish to sort the list, use the keys pnum,
        edition, metadata, transliteration, normalization, or translation.
        """
        keys = sorted(self.catalog.keys())
        if len(catalog_filter) > 0:  # pylint: disable=len-as-condition
            valid = []
            for key in keys:
                for f in catalog_filter:
                    if len(self.catalog[key][f]) > 0:  # pylint: disable=len-as-condition
                        valid.append(key)
            keys = valid
        for key in keys:
            print(f"Pnum: {self.catalog[key]['pnum']}")
            print(f"Edition: {self.catalog[key]['edition']}")
            print(f"Metadata: {len(self.catalog[key]['metadata']) > 0}")
            print(f"Transliteration: {len(self.catalog[key]['transliteration']) > 0}")
            print(f"Normalization: {len(self.catalog[key]['normalization']) > 0}")
            print(f"Translation: {len(self.catalog[key]['translation']) > 0}")
            print()
