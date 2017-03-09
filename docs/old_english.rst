Old English
***********
Chinese is a group of related, but in many cases mutually unintelligible, language varieties, forming a branch of the Sino-Tibetan language family. Chinese is spoken by the Han majority and many other ethnic groups in China. Nearly 1.2 billion people (around 16% of the world's population) speak some form of Chinese as their first language. Standard Chinese is a standardized form of spoken Chinese based on the Beijing dialect of Mandarin. It is the official language of China and Taiwan, as well as one of four official languages of Singapore. It is one of the six official languages of the United Nations. The written form of the standard language, based on the logograms known as Chinese characters , is shared by literate speakers of otherwise unintelligible dialects. (Source:`Wikipedia <https://en.wikipedia.org/wiki/Chinese_language>`_)

Stopword Filtering
==================

To use the CLTK's built-in stopwords list, We use an example from Beowulf:

.. code-block:: python

   In [1]: from nltk.tokenize.punkt import PunktLanguageVars

   In [2]: from cltk.stop.old_english.stops import STOPS_LIST

   In [3]: sentence = 'þe hie ær drugon aldorlease lange hwile.'

   In [4]: p = PunktLanguageVars()

   In [5]: tokens = p.word_tokenize(sentence.lower())

   In [6]: [w for w in tokens if not w in STOPS_LIST]
   Out[6]:
   ['hie',
    'drugon',
    'aldorlease',
    'catilina',
    'lange',
    'hwile',
    '.']


