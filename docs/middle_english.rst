Middle English
**************

Middle English is collectively the varieties of the English language spoken after the Norman Conquest (1066) until the late 15th century; scholarly opinion varies but the Oxford English Dictionary specifies the period of 1150 to 1500.
(Source: `Wikipedia <https://en.wikipedia.org/wiki/Middle_English>`_)

Text Normalization
==================

CLTK's normalizer attempts to clean the given text, converting it into a canonical form.

Lowercase Conversion
--------------------

The ``to_lower`` parameter converts the string into lowercase.

.. code-block:: python

   In [1]: from cltk.corpus.middle_english.alphabet import normalize_middle_english
   
   In [2]: normalize_middle_english("Whan Phebus in the Crabbe had nere hys cours ronne And toward the leon his journé gan take", to_lower=True)
   Out [2]: 'whan phebus in the crabbe had nere hys cours ronne and toward the leon his journé gan take'

Punctuation Removal
-------------------
``punct`` is responsible for punctuation removal

.. code-block:: python

   In [3]: normalize_middle_english("Thus he hath me dryven agen myn entent, And contrary to my course naturall.", punct=True)
   Out [3]: 'thus he hath me dryven agen myn entent and contrary to my course naturall'

Canonical Form
--------------

The ``alpha_conv`` follows the established spelling conventions developed thorughout the last last century.
`þ` and `ð` are both converted to `th` while `3` is converted to y at the start of the word and to `gh` otherwise.

.. code-block:: python

   In [4]: normalize_middle_english("as 3e lykeþ best", alpha_conv=True)
   Out [4]: 'as ye liketh best'

Stemming
========
CLTK supports a rule-based affix stemmer for ME.

Keep in mind, that while Middle English is considered a weakly inflected language with a grammatical structure resembling that of Modern English, its lack of orthographical conventions presents a difficulty when accounting for various affixes.

.. code-block:: python

   In [1]: from cltk.stem.middle_english import affix_stemmer
   
   In [2]: from cltk.corpus.middle_english.alphabet import normalize_middle_english
   
   In [3]: text = normalize_middle_english('The speke the henmest kyng, in the hillis he beholdis.').split(" ")
   
   In [4]: affix_stemmer(text)
   Out [4]: 'the spek the henm kyng in the hill he behold'
   
The stemmer can also take an additional parameter of a hard-coded exception dictionary. An example follows utilizing the compiled stopwords list.

.. code-block:: python

   In[7]: from cltk.stop.middle_english.stops import STOPS_LIST
   
   In[8]: exceptions = dict(zip(STOPS_LIST, STOPS_LIST))
   
   In[9]: affix_stemer('byfore him'.split(" "), exception_list = exceptions)
   Out[9]: 'byfore him'

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
    
Stresser
========

The historical events of early 11th century Britain were intertwined with its phonological development. The Norman Conquest in 1066 is mainly responsible for the influx of both Francien and Latin words and by extension for the highly variable spelling and phonology of ME.

While the Stresser provided by CLTK is unable to recognize the stressing of a given word, it does accept some of the most common stressing rules as parameters (Latin/Germanic/French)

.. code-block:: python
   
   In [1]: from cltk.phonology.middle_english.transcription import Word
   
   In [2]: ".".join(Word('beren').stresser(stress_rule = "FSR"))
   Out[2]: "ber.'en"
   
   In [3]: ".".join(Word('yisterday').stresser(stress_rule = "GSR"))
   Out [3]: "yi.ster.'day"
   
   In [4]: ".".join(Word('verbum').stresser(stress_rule = "LSR"))
   Out [4]: "ver.'bum"

Syllabify
=========

The ``Word`` class provides a syllabification module for ME words.

.. code-block:: python
   
   In [1]: from cltk.phonology.middle_english.transcription import Word
   
   In [2]: w = Word("hymsylf")
   
   In [3]: w.syllabify()
   Out [3]: ['hym', 'sylf']
   
   In [4]: w.syllabified_str()
   Out[4]: 'hym.sylf'
