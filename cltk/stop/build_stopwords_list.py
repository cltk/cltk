"""This module's main class reads a text corpus and assembles a list of n
most common words."""

from cltk.corpus.utils.formatter import assemble_tlg_works_filepaths
from collections import Counter
from nltk.tokenize.punkt import PunktLanguageVars


class Stopwords:

    def __init__(self, language):
        self.language = language

    def make_list_from_str(self, string, threshold=100):
        """Build stopword list from incoming string.
        :param threshold: Ranked number under which stopwords are not included.
        :type int
        :rtype list
        :return A list of most common words ranked from most to least common,
        up to the threshold number.
        """
        punkt = PunktLanguageVars()
        string_list = [chars for chars in string if chars not in [',', '.', ';', ':', '"', "'", '?', '-']]
        string_joined = ''.join(string_list)
        tokens = punkt.word_tokenize(string_joined)
        counter = Counter(tokens)
        counter_common = counter.most_common(threshold)
        stops_list = [x[0] for x in counter_common]
        return stops_list

    def make_list_from_corpus(self, threshold=100, corpus=None):
        """Build stopword list from one of several available corpora.
        Build stopword list from incoming string.
        :param threshold: Ranked number under which stopwords are not included.
        :type int
        :rtype ?
        :return ?
        """
        assert corpus in ['phi5', 'tlg'], \
            "Corpus {0} not available. Choose from 'phi5' or 'tlg'".format(corpus)
        #p = PunktLanguageVars()