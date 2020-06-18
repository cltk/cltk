"""
Stopwords were defined by picking up in
Altnordisches Elementarbuch by Ranke and Hofmann
A new introduction to Old Norse by Barnes
Viking Language 1 by Byock (this book provides a list of most frequent words in the sagas sorted by part of speech)
"""

from string import punctuation
from cltk.stop.stop import BaseCorpusStoplist

__author__ = ["Clément Besnier <clemsciences@aol.com>"]
__license__ = 'GPL License.'


STOPS_LIST = ['í',  # prepositions and adverbs
              'gegnum',
              'svá',
              'eigi',
              'ekki',
              'vel',
              'upp',
              'síðan',
              'þó',
              'heim',
              'út',
              "hér",
              "mjök",
              'ór',
              'áðr',
              'saman',
              'inn',
              'undir',
              'heldr',
              'brott',
              'enn',
              'niðr',
              'ofan',
              'aptr',
              'illa',
              'lengi',
              'hversu',
              'aldri',
              'mikit',
              'um',
              'fram',
              'umhverfis',
              'innan',
              'meðal',
              'á',
              'milli',
              'til',
              'at',
              'frá',
              'gegn',
              'hjá',
              'mót',
              'nær',
              'undan',
              'eptir',
              'fyrir',
              'með',
              'við',
              'yfir',
              'útan',
              'án',
              'meðan'  # adverbs
              'þegar',
              'þangar',
              'hva',
              'hverr',
              'ok',  # conjuctions and relative pronouns
              'eða',
              'en',
              'sem',
              'er',
              'þá',
              'ef',
              'hvárt',
              'bæði',
              'þótt',
              'né',
              'enda',
              'hvági',
              'sá',  # demonstrative
              'þess',
              'þeim',
              'þann',
              'þeir',
              'þeira',
              'sú',
              'þeirar',
              'þeiri',
              'þær',
              'þat',
              'því',
              'þau',
              'því',
              'siá',
              'þessa',
              'þessum',
              'þenna',
              'þessír',
              'þessar',
              'þessi',
              'þetta',
              'þessu'
              ]


class CorpusStoplist(BaseCorpusStoplist):

    def __init__(self,):
        BaseCorpusStoplist.__init__(self)
        self.punctuation = punctuation
        if not self.numpy_installed or not self.sklearn_installed:
            print('\n\nThe Corpus-based Stoplist method requires numpy and scikit-learn for calculations. '
                  'Try installing with `pip install numpy sklearn scipy`.\n\n')
            raise ImportError
        else:
            from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
            self.vectorizer = CountVectorizer(input='content')  # Set df?
            self.tfidf_vectorizer = TfidfVectorizer(input='content')

