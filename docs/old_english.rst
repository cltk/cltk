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

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``old_english_``) to discover available Old English corpora.

.. code-block:: python

   >>> from cltk.corpus.utils.importer import CorpusImporter

   >>> corpus_importer = CorpusImporter("old_english")

   >>> corpus_importer.list_corpora
   ['old_english_text_sacred_texts', 'old_english_models_cltk']

To download a corpus, use the `import_corpus` method.  The following will download pre-trained POS models for Old English:

.. code-block:: python
  >>> corpus_importer.import_corpus('old_english_models_cltk')


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

Transliteration
===============

Anglo-Saxon runic transliteration
---------------------------------

You can call the runic transliteration module for converting runic script into latin characters:

.. code-block:: python
   
   In [1]: from cltk.phonology.old_english.phonology import Transliterate as t
   
   In [2]: t.transliterate('ᚩᚠᛏ ᛋᚳᚣᛚᛞ ᛋᚳᛖᚠᛁᛝ ᛋᚳᛠᚦᛖᚾᚪ ᚦᚱᛠᛏᚢᛗ', 'Latin')
   Out[2]: 'oft scyld scefin sceathena threatum'

The reverse process is also possible:

.. code-block:: python
   
   In [3]: t.transliterate('Hƿæt Ƿe Gardena in geardagum', 'Anglo-Saxon')
   Out[3]: 'ᚻᚹᚫᛏ ᚹᛖ ᚷᚪᚱᛞᛖᚾᚪ ᛁᚾ ᚷᛠᚱᛞᚪᚷᚢᛗ'

POS tagging
===========

You can get the POS tags of Old English texts using the CLTK's wrapper around the NLTK tokenizer. First, download the model by importing the ``old_english_models_cltk`` corpus. 

There are a number of different pre-trained models available for POS tagging of Old English.  Each represents a trade-off between accuracy of tagging and speed of tagging.  Listed in order of increasing accuracy (= decreasing speed), the models are:

* Unigram
* Trigram -> Bigram -> Unigram n-gram backoff model
* Conditional Random Field (CRF) model
* Perceptron model

(Bigram and trigram models are also available, but unsuitable due to low accuracy.)

The taggers were trained from annotated data from the `The ISWOC Treebank <http://iswoc.github.io/>`_ (version 0.9, license: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License). 

The POS tag scheme is explained here: https://proiel.github.io/handbook/developer/

```Bech, Kristin and Kristine Eide. 2014. The ISWOC corpus. Department of Literature, Area Studies and European Languages, University of Oslo. http://iswoc.github.com.```

### Example: Tagging with the CRF tagger
``````````

The following sentence is from the beginning of Beowulf:

.. code-block:: python

    In [1]: from cltk.tag.pos import POSTag

    In [2]: tagger = POSTag('old_english')

    In [3]: sent = 'Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon.'

    In [4]: tagger.tag_crf(sent)

    Out[4]:[('Hwæt', 'I-'), ('!', 'C-'), ('We', 'NE'), ('Gardena', 'NE'), ('in', 'R-'), ('geardagum', 'NB'), (',', 'C-'), ('þeodcyninga', 'NB'), (',', 'C-'), ('þrym', 'PY'), ('gefrunon', 'NB'), (',', 'C-'), ('hu', 'DU'), ('ða', 'PD'), ('æþelingas', 'NB'), ('ellen', 'V-'), ('fremedon', 'V-'), ('.', 'C-')]

Swadesh
=======
The corpus module has a class for generating a Swadesh list for Old English.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import Swadesh

   In [2]: swadesh = Swadesh('eng_old')

   In [3]: swadesh.words()[:10]
   Out[3]: ['ic, iċċ, ih', 'þū', 'hē', 'wē', 'ġē', 'hīe', 'þēs, þēos, þis', 'sē, sēo, þæt', 'hēr', 'þār, þāra, þǣr, þēr']
