"""
The Importer feature sets up the ability to work with cuneiform text(s)
one-on-one, whether it is the Code of Hammurabi, a collection of Akkadian texts
such as ARM01, or whatever your research desires.

This cdli_corpus module is for working with text files having already been read
by file_importer. The file_lines required by CDLICorpus are taken from prior
use of FileImport(text_file).read_file().

e.g.:
    # FileImport takes a txt file and reads it; this becomes file_lines.
        text_path = os.path.join('Akkadian_test_texts', 'ARM01_texts.txt')
        f_i = FileImport(text_path)
        f_i.read_file()
        ARM01 = f_i.file_lines
    # CDLICorpus takes file_lines and uses it to work:
        cdli = CDLICorpus(ARM01)
        cdli.chunk_text()
        cdli.ingest()
        cdli.print_text_by_cdli_number('&P254202')

The output of CDLICorpus will be able to further utilized by the feature
ATFConverter and its subsequent classes: Tokenizer, ATFConverter, Lemmatizer,
and Pretty Print.
"""

import re

__author__ = ['Andrew Deloucas <adeloucas@g.harvard.com>']
__license__ = 'MIT License. See LICENSE.'


class CDLICorpus(object):
    """
    Takes file_lines, prepares and organizes data.
    """
    def __init__(self):
        """
        Empty.
        """
        self.texts = []

    def _chunk_text(self, file_lines, only_normalization=False):
        """
        Splits up a text whenever a break is found in file_lines. Only
        Normalization separates out texts that contain normalized lines in
        the CDLI corpus.
        :return: Disparate texts.
        """
        texts, text = [], []
        if re.match('Primary publication:', file_lines[0]):
            for line in file_lines:
                if line.strip() == '':
                    if len(text) > 0:   # pylint: disable =len-as-condition
                        texts.append(text)
                    text = []
                else:
                    text.append(line.rstrip())
            texts.append(text)
        else:
            for line in file_lines:
                if re.match(r'&?P\d{6}', line):
                    if len(text) > 0:  # pylint: disable =len-as-condition
                        texts.append(text)
                    text = [line]
                else:
                    text.append(line)
            texts.append(text)
        if only_normalization:
            norm_texts = []
            for text in texts:
                norm = False
                norm_text = [text[0]]
                for line in text[1:]:
                    if line.startswith('#tr.ts'):
                        norm = True
                        norm_text.append(line)
                if norm:
                    norm_texts.append(norm_text)
            texts = norm_texts
        return texts

    def _find_cdli_number(self, file_lines):
        """
        Finds CDLI Number (ex: &P254202, P254203) in file_lines & lists it.
        :return: List of CDLI Numbers found in file_lines.
        """
        header, output = [], []
        for text in self._chunk_text(file_lines):
            for lines in text:
                if re.match(r'^&P\d.*$', lines):
                    header.append(lines)
                elif re.match(r'^P\d.*$', lines):
                    header.append(lines)
        for string in header:
            if len(string) > 1:
                split_string = string.split('=')
                cdli_num = split_string[0].rstrip()
                output.append(cdli_num)
        return output

    def _find_edition(self, file_lines):
        """
        Finds edition info (ex: ARM 01, 001) in file_lines and lists it.
        :return: List of editions found in file_lines.
        """
        header, output = [], []
        for text in self._chunk_text(file_lines):
            for lines in text:
                if re.match(r'^&P\d.*$', lines):
                    header.append(lines)
                elif re.match(r'^P\d.*$', lines):
                    header.append(lines)
        for string in header:
            if len(string) > 1:
                split_string = string.split('=')
                edition = split_string[1].lstrip()
                output.append(edition)
        return output

    def _find_metadata(self, file_lines):
        """
        Finds metadata in file_lines and lists it.
        :return: List of metadata found in file_lines.
        """
        final, lines = [], []
        for text in self._chunk_text(file_lines):
            if text[0].startswith('Primary publication:'):
                lines.append(text[0:25])
            else:
                lines.append('None found.')
        final.append(lines)
        return lines

    def _find_transliteration(self, file_lines):
        """
        Finds any transliteration in file_lines and lists it.
        :return: List of transliterations found in file_lines.
        """
        final, lines = [], []
        for text in self._chunk_text(file_lines):
            if text[0].startswith('Primary publication:'):
                lines.append(text[26:])
            else:
                lines.append(text)
        final.append(lines)
        return lines

    def _ingest(self, file_lines):
        """
        Captures all listed information above and formats it in a clear, and
        disparate manner.
        :return: Dictionary composed of information gathered in above
        functions.
        """
        cdli_number = self._find_cdli_number(file_lines)
        edition = self._find_edition(file_lines)
        metadata = self._find_metadata(file_lines)
        transliteration = self._find_transliteration(file_lines)
        new_text = {'text edition': edition, 'cdli number': cdli_number,
                    'metadata': metadata[0],
                    'transliteration': transliteration[0]}
        self.text = new_text  # pylint: disable= attribute-defined-outside-init

    def ingest_text_file(self, file_lines):
        """
        Captures all listed information above and formats it in a clear, and
        disparate manner for every text found in a text file.
        :return: List of dictionaries composed of information gathered in above
        functions.
        """
        for text_lines in self._chunk_text(file_lines):
            self._ingest(text_lines)
            texts = self.text
            self.texts.append(dict(texts))

    # Should here on out be in new method called pretty print?

    def table_of_contents(self):
        """
        Prints a table of contents from which one use can identify the edition
        and cdli number for printing purposes, as well as whether or not the
        text has metadata.
        :return: string of edition and number.
        """
        table = []
        for toc in self.texts:
            text = '{} {}{} {} {}'.format('edition:', toc['text edition'], ';',
                                          'cdli number:', toc['cdli number'])
            table.append(text)
        return table

    def call_text(self, cdli_number):
        """
        Prints transliteration with cdli number.
        :return: transliteration
        """
        text = next((item for item in self.texts if
                     item['cdli number'] == [cdli_number]), None)
        return text['transliteration']

    def call_metadata(self, cdli_number):
        """
        Prints metadata with cdli number.
        :return: metadata
        """
        my_item = next((item for item in self.texts if
                        item['cdli number'] == [cdli_number]), None)
        return my_item['metadata']
