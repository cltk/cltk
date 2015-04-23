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
from time import strftime


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
        stopwords = [x[0] for x in counter_common]

        if not save:
            return stopwords
        elif save:
            self._save_stopwords(stopwords)

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

    def _save_stopwords(self, stopwords):
        """Take a list of stopwords and save to ``cltk_data/user_data``.
        :param stopwords: A list of stopwords.
        :type stopwords: list
        """
        user_data_rel = '~/cltk_data/user_data'
        user_data = os.path.expanduser(user_data_rel)
        if not os.path.isdir(user_data):
            os.makedirs(user_data)
        stops_path = os.path.join(user_data, 'stops_' + self.language + '_' + strftime("%Y_%m_%d_%H%M") + '.py')
        with open(stops_path, 'w') as file_open:
            file_open.write('STOPS_LIST = {0}'.format(stopwords))
        message = "Custom stopword file saved at '{0}'.".format(stops_path)
        logger.info(message)
        print(message)

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
            self._save_stopwords(stopwords)
