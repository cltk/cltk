Middle High German
******************

Middle High German (abbreviated MHG, German: Mittelhochdeutsch, abbr. Mhd.) is the term for the form of German spoken in the High Middle Ages. It is conventionally dated between 1050 and 1350, developing from Old High German and into Early New High German. High German is defined as those varieties of German which were affected by the Second Sound Shift; the Middle Low German and Middle Dutch languages spoken to the North and North West, which did not participate in this sound change, are not part of MHG. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Middle_High_German>`_)

ASCII Encoding
==============

Using the ``Word`` class, you can easily convert a string to its ASCII encoding, essentialy striping it of its diacritics.

.. code-block:: python
  
  In [1]: from cltk.phonology.middle_high_german.transcription import Word
    
  In [2]: w = Word("vogellîn")
    
  In [3]: w.ASCII_encoding()
  Out[3]: 'vogellin'

Stemming
========
 
.. note::
   The stemming algorithm is still under developement and can sometimes produce inaccurate results.

CLTK's stemming function, attempts to reduce inflected words to their stem by suffix stripping. 

.. code-block:: python
 
   In [1]: from cltk.stem.middle_high_german.stem import stemmer_middle_high_german
   
   In [2]: stemmer_middle_high_german("Man lūte dā zem münster nāch gewoneheit")
   Out[2]: ['Man', 'lut', 'dâ', 'zem', 'munst', 'nâch', 'gewoneheit']

The stemmer strips umlauts by default, to toggle it off, simply set ``rem_umlauts = False``

.. code-block:: python
  
   In [3]: stemmer_middle_high_german("Man lūte dā zem münster nāch gewoneheit", rem_umlauts = False)
   Out[3]: ['Man', 'lût', 'dâ', 'zem', 'münst', 'nâch', 'gewoneheit']

The stemmer can also take an user-defined dictionary as an optional parameter. 

.. code-block:: python
  
   In [4]: stemmer_middle_high_german("swaȥ kriuchet unde fliuget und bein zer erden biuget", rem_umlauts = False)
   Out[4]: ['swaȥ', 'kriuchet', 'unde', 'fliuget', 'und', 'bein', 'zer', 'erden', 'biuget']
   
   In [5]: stemmer_middle_high_german("swaȥ kriuchet unde fliuget und bein zer erden biuget", rem_umlauts = False, exceptions = {"biuget" : "biegen"})
   Out[5]: ['swaȥ', 'kriuchet', 'unde', 'fliuget', 'und', 'bein', 'zer', 'erden', 'biegen']


Syllabification
===============

A syllabifier is contained in the ``Word`` module:

.. code-block:: python

    In [1]: from cltk.phonology.middle_high_gemran import Word
    
    In [2]: Word('entslâfen').syllabify()
    Out[2]: ['ent', 'slâ', 'fen']

Note that the syllabifier is case-insensitive:

.. code-block:: python

    In [3]: Word('Fröude').syllabify()
    Out[3]: ['fröu', 'de']
    
You can also load the sonority of MHG phonemes to the ``phonology`` syllabifier:

.. code-block:: python
  
  In [4]: from cltk.phonology.syllabify import Syllabifier
  
  In [5]: s = Syllabifier(language='middle high german')
  
  In [6]: s.syllabify('lobebæren')
  Out[6]: ['lo', 'be', 'bæ', 'ren']

Stopword Filtering
==================

CLTK offers a built-in stop word list for Middle High German.

.. code-block:: python

   In [1]: from cltk.stop.middle_high_german.stops import STOPS_LIST
   
   In [2]: from cltk.tokenize.word import WordTokenizer
   
   In [3]: word_tokenizer = WordTokenizer('middle_high_german')
   
   In [4]: sentence = "Wol mich lieber mære diu ich hān vernomen daȥ der winter swære welle ze ende komen"
   
   In [5]: tokens = word_tokenizer.tokenize(sentence.lower())
   
   In [6]: [word for word in tokens if word not in STOPS_LIST]
   Out[6]: ['lieber', 'mære', 'hān', 'vernomen', 'winter', 'swære', 'welle', 'komen']


Text Normalization
==================

Text normalization attempts to narrow the disrepancies between various corpora. 

Lowercase Conversion
--------------------
By default, the function converts the whole string to lowercase. However, since in MHG uppercase is only used at the start of a sentence or to denote eponyms, you may also set ``to_lower_beginning = True`` to only convert the words at the beginning of a sentence.

.. code-block:: python

   In [1]: from cltk.corpus.middle_high_german.alphabet import normalize_middle_high_german
   
   In [2]: normalize_middle_high_german("Dô erbiten si der nahte und fuoren über Rîn")
   Out[2]: 'dô erbiten si der nahte und fuoren über rîn'
   
   In [3]: normalize_middle_high_german("Dô erbiten si der nahte und fuoren über Rîn",to_lower_all = False, to_lower_beginning = True)
   Out[3]: 'dô erbiten si der nahte und fuoren über Rîn'


Alphabet Conversion
-------------------
Various online corpora use the characters *ā*, *ō*, *ū*, *ē*, *ī* to represent *â*, *ô*, *û*, *ê* and *î* respectively.
Sometimes, *ae* and *oe* are also  used instead of *æ* and *œ*. By default, the normalizer converts the text to the canonical form.

.. code-block:: python
  
   In [4]: normalize_middle_high_german("Mit ūf erbürten schilden in was ze strīte nōt", alpha_conv = True)
   Out[4]: 'mit ûf erbürten schilden in was ze strîte nôt'


Punctuation
-----------
Punctuation is also handled by the normalizer.

.. code-block:: python
  
   In [5]: normalize_middle_high_german("Si sprach: ‘herre Sigemunt, ir sult iȥ lāȥen stān", punct = True)
   Out[5]: 'si sprach herre sigemunt ir sult iȥ lâȥen stân'

Phonetic Indexing
=================

Phonetic Indexing helps identifying and processing homophones.

Soundex
-------
The ``Word`` class provides a modified Soundex algorithm modified for MHG.

.. code-block:: python

   In [1]: from cltk.phonology.middle_high_german.transcription import Word
 
   In [2]: w1 = Word("krippe")
 
   In [3]: w1.phonetic_index(p = "SE")
   Out[3]: 'K510'
 
   In [4]: w2 = Word("krîbbe")
 
   In [5]: w2.phonetic_indexing(p = "SE")
   Out[5]: 'K510'

Transliteration
===============

CLTK's transcriber rewrites a word into the International Phonetical Alphabet (IPA). As of this version, the Transcribe class doesn't support any specific dialects and serves as a superset encompassing various regional accents.


.. code-block:: python

   In [1]: from cltk.phonology.middle_high_german.transcription import Transcriber
  
   In [2]: tr = Transcriber()
  
   In [3]: tr.transcribe("Slâfest du, friedel ziere?", punctuation = True)
   Out[3]: '[Slɑːfest d̥ʊ, frɪ͡əd̥el t͡sɪ͡əre?]'
  
   In [4]: tr.transcribe("Slâfest du, friedel ziere?", punctuation = False)
   Out[4]: '[Slɑːfest d̥ʊ frɪ͡əd̥el t͡sɪ͡əre]'

  
Word Tokenization
=================

The ``WordTokenizer`` class takes a string as input and returns a list of tokens.

.. code-block:: python

   In [1]: from cltk.tokenize.word import WordTokenizer
   
   In [2]: word_tokenizer = WordTokenizer('middle_high_german')
   
   In [3]: text = "Mīn ougen   wurden liebes alsō vol, \n\n\ndō ich die minneclīchen ērst gesach,\ndaȥ eȥ mir hiute und   iemer mē tuot wol."
   
   In [4]: word_tokenizer.tokenize(text)
   Out[4]: ['Mīn', 'ougen', 'wurden', 'liebes', 'alsō', 'vol', ',', 'dō', 'ich', 'die', 'minneclīchen', 'ērst', 'gesach', ',', 'daȥ', 'eȥ', 'mir', 'hiute', 'und', 'iemer', 'mē', 'tuot', 'wol', '.']





Lemmatization
=============

The CLTK offers a series of lemmatizers that can be combined in a backoff chain, i.e. if one lemmatizer is unable to return a headword for a token, this token can be passed onto another lemmatizer until either a headword is returned or the sequence ends.
There is a generic version of the backoff Middle High German lemmatizer which requires data from `the CLTK Middle High German models data found here <https://github.com/cltk/middle_high_german_models_cltk/tree/master/lemmata/backoff>`_. The lemmatizer expects this model to be stored in a folder called cltk_data in the user's home directory.

To use the generic version of the backoff Middle High German Lemmatizer:

.. code-block:: python

   In [1]: from cltk.lemmatize.middle_high_german.backoff import BackoffMHGLemmatizer

   In [2]: lemmatizer = BackoffMHGLemmatizer()

   In [3]: tokens = "uns ist in alten mæren".split(" ")

   In [4]: lemmatizer.lemmatize(tokens)
   Out[4]: [('uns', {'uns', 'unser', 'unz', 'wir'}), ('ist', {'sîn/wider(e)+', 'ist', 'sîn/inne+', 'sîn/mit(e)<+', 'sîn/vür(e)+', 'sîn/abe+', 'sîn/obe+', 'sîn/vor(e)+', 'sîn/vür(e)>+', 'sîn/ûze+', 'sîn/ûz+', 'sîn/bî<.+', 'sîn/vür(e)<+', 'sîn/innen+', 'sîn/âne+', 'sîn/bî+', 'sîn/ûz<+', 'sîn', 'sîn/ûf<.+'}), ('in', {'ër', 'in/hin(e)+', 'in/>+gân', 'in/+gân', 'în/+gân', 'in/+lâzen', 'în', 'in/<.+wintel(e)n', 'in/>+rinnen', 'in/dar(e)+', 'in/.>+slîzen', 'în/hin(e)+', 'în/+lèiten', 'în/+var(e)n', 'in', 'in/>+tragen', 'in/+tropfen', 'în/+lègen', 'in/>+winten', 'în/+brèngen', 'in/>+büègen', 'ërr', 'în/+zièhen', 'in/<.+gân', 'in/+zièhen', 'in/>+tûchen', 'dër', 'în/dâr+', 'in/war(e).+', 'in/<.+lâzen', 'in/>+rîten', 'în/+lâzen', 'in/>+lâzen', 'in/+stapfen', 'în/+sènten', 'in/>.+lâzen', 'in/>+stân', 'in/+drücken', 'in/>+ligen', 'in/dâr+ ', 'in/+var(e)n', 'in/+vüèren', 'in/<.+vallen', 'in/>+vlièzen', 'in/<.+rîten', 'in/hër(e).+', 'ne', 'in/>+wonen', 'in/<.+sigel(e)n', 'in/+lègen', 'în/+dringen', 'in/>+ge-trîben', 'in/+diènen', 'in/>+ge-stëchen', 'in/>+stècken', 'in/hër(e)+', 'in/>+stëchen', 'in/dâr+', 'in/+blâsen', 'în/dâr.+', 'in/>+wîsen', 'în/+îlen', 'in/>+laden', 'în/+komen', 'în/+ge-lèiten', 'in/<.+vloèzen', 'ër ', 'in/>+sètzen', 'in/hièr+', 'in/>+bûwen', 'in/>+lèiten', 'în/+ge-binten', '[!]', 'în/+trîben', 'in/<.+blâsen', 'in/+komen', 'în/+krièchen', 'in/+trîben', 'in/<.+ligen', 'in/+stëchen', 'in/<+gân', 'in/dâr.+', 'în/hër(e)+', 'in/+kêren', 'in/<.+var(e)n', 'in/+rîten', 'in/>+vallen', 'in/<.+vüèren'}), ('alten', {'alt', 'alter', 'alten'}), ('mæren', {'mæren', 'mære'})]



POS tagging
===========

.. code-block:: python
    In [1]: from cltk.tag.pos import POSTag

    In [2]: mhg_pos_tagger = POSTag("middle_high_german")

    In [3]: mhg_pos_tagger.tag_tnt("uns ist in alten mæren wunders vil geseit")
    Out[3]: [('uns', 'PPER'), ('ist', 'VAFIN'), ('in', 'APPR'), ('alten', 'ADJA'), ('mæren', 'ADJA'),
             ('wunders', 'NA'), ('vil', 'AVD'), ('geseit', 'VVPP')]

