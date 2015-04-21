"""This module's main class reads a text corpus and assembles a list of n
most common words."""

from cltk.corpus.utils.formatter import assemble_tlg_author_filepaths
from cltk.corpus.utils.formatter import assemble_phi5_author_filepaths
from cltk.corpus.utils.formatter import tlg_plaintext_cleanup
from cltk.corpus.utils.formatter import phi5_plaintext_cleanup
from cltk.utils.cltk_logger import logger
from collections import Counter
from nltk.tokenize.punkt import PunktLanguageVars
import os


class Stopwords:
    """Methods for making and saving stopword lists."""

    def __init__(self, language):
        """Language taken as argument, necessary used when saving stopwords to
        ``cltk_data/user_data``."""
        self.language = language

    def make_list_from_str(self, string, threshold=100, save=False):
        """Build stopword list from incoming string.
        :param threshold: Ranked number under which stopwords are not included.
        :type int
        :rtype list
        :return A list of most common words ranked from most to least common,
        up to the threshold number.
        """
        punkt = PunktLanguageVars()
        string_list = [chars for chars in string if chars not in [',', '.', ';', ':', '"', "'", '?', '-', '!', '*', '[', ']', '{', '}']]
        string_joined = ''.join(string_list)
        tokens = punkt.word_tokenize(string_joined)
        counter = Counter(tokens)
        counter_common = counter.most_common(threshold)
        stops_list = [x[0] for x in counter_common]
        return stops_list

    def _assemble_corpus_string(self, corpus):
        """Takes a list of filepaths, returns a string containing contents of
        all files."""

        if corpus == 'phi5':
            filepaths = assemble_phi5_author_filepaths()
        elif corpus == 'tlg':
            filepaths = assemble_tlg_author_filepaths()

        all_strings = ''
        for filepath in filepaths:
            with open(filepath) as file_open:
                file_read = file_open.read().lower()
            if corpus == 'phi5':
                file_clean = phi5_plaintext_cleanup(file_read)
            elif corpus == 'tlg':
                file_clean = tlg_plaintext_cleanup(file_read)
            all_strings += file_clean
        return all_strings

    def make_list_from_corpus(self, corpus, threshold=100, save=False):
        """Build stopword list from one of several available corpora.
        Build stopword list from incoming string.
        :param threshold: Ranked number under which stopwords are not included.
        :type threshold: int
        :param corpus: Corpus for which stopwords will be built.
        :type corpus: str
        :rtype list
        :return A list of most common words ranked from most to least common,
        up to the threshold number.
        """
        assert corpus in ['phi5', 'tlg'], \
            "Corpus '{0}' not available. Choose from 'phi5' or 'tlg'".format(corpus)
        all_strings = self._assemble_corpus_string(corpus=corpus)
        stopwords = self.make_list_from_str(all_strings, threshold=threshold)

        if not save:
            return stopwords
        elif save:
            user_data_rel = '~/cltk_data/user_data'
            user_data = os.path.expanduser(user_data_rel)
            stops_path = os.path.join(user_data, self.language + 'stops_' + corpus )
            with open(stops_path, 'w') as file_open:
                file_open = file_open.write(str(stopwords))
                logger.info('File saved here!!!') #!


if __name__ == '__main__':
    s = Stopwords('latin')
    l = s.make_list_from_corpus('phi5', threshold=200)
    print(l)
    print(len(l))
