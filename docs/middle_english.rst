Stopword Filtering
==================

To use the CLTK's built-in stopwords list, We use an example from Chaucer's "The Summoner's Tale":

.. code-block:: python

   In [1]: from nltk.tokenize.punkt import PunktLanguageVars

   In [2]: from cltk.stop.middle_english.stops import STOPS_LIST

   In [3]: sentence = 'This frere bosteth that he knoweth helle'

   In [4]: p = PunktLanguageVars()

   In [5]: tokens = p.word_tokenize(sentence.lower())

   In [6]: [w for w in tokens if not w in STOPS_LIST]
   Out[6]:
   ['frere',
    'bosteth',
    'knoweth',
    'helle',
    '.']
