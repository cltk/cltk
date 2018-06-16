Old English
***********

Old English is the earliest historical form of the English language, spoken in England and southern and eastern Scotland in the early Middle Ages. It was brought to Great Britain by Anglo-Saxon settlers probably in the mid 5th century, and the first Old English literary works date from the mid-7th century.
(Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_English>`_)


IPA Transcription
=================

CLTK's IPA transcriber can be found under the ``Transcriber`` module.

.. code-block:: python
   
   In [1]: fron cltk.phonology.old_english.phonology import Transcriber
   
   In [2]: t = Transcriber()
   
   In [3]: t.transcribe('Fæder ūre þū þe eeart on heofonum,', punctuation = True) 
   Out[3]: '[fæder uːre θuː θe eːɑrˠt on heovonum,]'
   
   In [4]: t.transcribe('Hwæt! wē Gār-Dena in ġēar-dagum', punctuation = False)
   Out[4]: '[ʍæt weː gɑːrdenɑ in jæːɑ̯rdɑgum]'

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


Text Normalization
==================

Diacritic Stripping
-------------------

The ``Word`` module provides a method useful for stripping various diacritical marks

.. code-block:: python

   In [1]: from cltk.phonology.old_english.phonology import Word
   
   In [2]: Word('ġelǣd').remove_diacritics()
   Out[2]: 'gelæd'

ASCII Encoding
--------------

For converting to ASCII, you can call ``ascii_encoding``

.. code-block:: python
   
   In [3]: Word('oðþæt').ascii_encoding()
   Out[3]: 'odthaet'
   
   In [4]: Word('ƿeorðunga').ascii_encoding()
   Out[4]: 'weordunga'

Swadesh
=======
The corpus module has a class for generating a Swadesh list for Old English.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import Swadesh

   In [2]: swadesh = Swadesh('eng_old')

   In [3]: swadesh.words()[:10]
   Out[3]: ['ic, iċċ, ih', 'þū', 'hē', 'wē', 'ġē', 'hīe', 'þēs, þēos, þis', 'sē, sēo, þæt', 'hēr', 'þār, þāra, þǣr, þēr']
