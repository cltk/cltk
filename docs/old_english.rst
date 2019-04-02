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

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: corpus_importer = CorpusImporter("old_english")

   In [3]: corpus_importer.list_corpora
   ['old_english_text_sacred_texts', 'old_english_models_cltk']

To download a corpus, use the `import_corpus` method.  The following will download pre-trained POS models for Old English:

.. code-block:: python

  In [4]: corpus_importer.import_corpus('old_english_models_cltk')


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

Syllabification
===============

There is a facility for using the pre-specified sonoroty hierarchy for Old English to syllabify words.

.. code-block:: python

  In [1]: from cltk.phonology.syllabify import Syllabifier

  In [2]: s = Syllabifier(language='old_english')

  In [3]: s.syllabify('geardagum')
  Out [3]:['gear', 'da', 'gum']


Lemmatization
=============

A basic lemmatizer is provided, based on a hand-built dictionary of word forms.

.. code-block:: python

   In [1]: import cltk.lemmatize.old_english.lemma as oe_l
   In [2]: lemmatizer = oe_l.OldEnglishDictioraryLemmatizer()
   In [3]: lemmatizer.lemmatize('Næs him fruma æfre, or geworden, ne nu ende cymþ ecean')
   Out [3]: [('Næs', 'næs'), ('him', 'he'), ('fruma', 'fruma'), ('æfre', 'æfre'), (',', ','), ('or', 'or'), ('geworden', 'weorþan'), (',', ','), ('ne', 'ne'), ('nu', 'nu'), ('ende', 'ende'), ('cymþ', 'cuman'), ('ecean', 'ecean')]

If an input word form has multiple possible lemmatizations, the system will select the lemma that occurs most 
frequently in a large corpus of Old English texts. If an input word form is not found in the dictionary, then 
it is simply returned.

Note, hovewer, that by passing in an extra parameter ``best_guess=False`` to the lemmatize function, 
one gains access to the underlying dictionary. In this case, a *list* is returned for each token. The list will contain:

* Nothing, if the word form is not found;
* A single string if the form maps to a unique lemma (the usual case);
* Multiple strings if the form maps to several lemmatas.

.. code-block:: python

   In [1]: lemmatizer.lemmatize('Næs him fruma æfre, or geworden, ne nu ende cymþ ecean', best_guess=False)
   Out [1]: [('Næs', ['nesan', 'næs']), ('him', ['him', 'he', 'hi']), ('fruma', ['fruma']), ('æfre', ['æfre']), (',', []), ('or', []), ('geworden', ['weorþan', 'geweorþan']), (',', []), ('ne', ['ne']), ('nu', ['nu']), ('ende', ['ende']), ('cymþ', ['cuman']), ('ecean', [])]

By specifying ``return_frequencies=True`` the log of the relative frequencies of the *lemmata* is also returned:

..code-block:: python

   In [1]: lemmatizer.lemmatize('Næs him fruma æfre, or geworden, ne nu ende cymþ ecean', best_guess=False, return_frequencies=True)
   
   Out [1]: [('Næs', [('nesan', -11.498420778767347), ('næs', -5.340383031833549)]), ('him', [('him', -2.1288142618657147), ('he', -1.4098446677862744), ('hi', -2.3713533259849857)]), ('fruma', [('fruma', -7.3395376954076745)]), ('æfre', [('æfre', -4.570372796517447)]), (',', []), ('or', []), ('geworden', [('weorþan', -8.608049020871182), ('geweorþan', -9.100525505968976)]), (',', []), ('ne', [('ne', -1.9050995182359884)]), ('nu', [('nu', -3.393566264402446)]), ('ende', [('ende', -5.038516324389812)]), ('cymþ', [('cuman', -5.943525084818863)]), ('ecean', [])]


POS tagging
===========

You can get the POS tags of Old English texts using the CLTK's wrapper around the NLTK tokenizer. First, download the model by importing the ``old_english_models_cltk`` corpus. 

There are a number of different pre-trained models available for POS tagging of Old English.  Each represents a trade-off between accuracy of tagging and speed of tagging.  Listed in order of increasing accuracy (= decreasing speed), the models are:

* Unigram
* Trigram -> Bigram -> Unigram n-gram backoff model
* Conditional Random Field (CRF) model
* Perceptron model

(Bigram and trigram models are also available, but unsuitable due to low recall.)

The taggers were trained from annotated data from the `The ISWOC Treebank <http://iswoc.github.io/>`_ (license: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 License). 

The POS tag scheme is explained here: https://proiel.github.io/handbook/developer/

``Bech, Kristin and Kristine Eide. 2014. The ISWOC corpus. 
Department of Literature, Area Studies and European Languages, 
University of Oslo. http://iswoc.github.com.``

Example: Tagging with the CRF tagger
------------------------------------

The following sentence is from the beginning of Beowulf:

.. code-block:: python

    In [1]: from cltk.tag.pos import POSTag

    In [2]: tagger = POSTag('old_english')

    In [3]: sent = 'Hwæt! We Gardena in geardagum, þeodcyninga, þrym gefrunon, hu ða æþelingas ellen fremedon.'

    In [4]: tagger.tag_crf(sent)

    Out[4]:[('Hwæt', 'I-'), ('!', 'C-'), 
    ('We', 'NE'), ('Gardena', 'NE'), ('in', 'R-'), ('geardagum', 'NB'), (',', 'C-'), 
    ('þeodcyninga', 'NB'), (',', 'C-'), ('þrym', 'PY'), ('gefrunon', 'NB'), 
    (',', 'C-'), ('hu', 'DU'), ('ða', 'PD'), ('æþelingas', 'NB'), ('ellen', 'V-'), 
    ('fremedon', 'V-'), ('.', 'C-')]

Swadesh
=======
The corpus module has a class for generating a Swadesh list for Old English.

.. code-block:: python

   In [1]: from cltk.corpus.swadesh import Swadesh

   In [2]: swadesh = Swadesh('eng_old')

   In [3]: swadesh.words()[:10]
   Out[3]: ['ic, iċċ, ih', 'þū', 'hē', 'wē', 'ġē', 'hīe', 'þēs, þēos, þis', 'sē, sēo, þæt', 'hēr', 'þār, þāra, þǣr, þēr']
