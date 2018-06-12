Akkadian
********

Akkadian is an extinct East Semitic language (part of the greater Afroasiatic language family) that was spoken in ancient Mesopotamia. \
The earliest attested Semitic language, it used the cuneiform writing system, which was originally used to write the unrelated Ancient \
Sumerian, a language isolate. From the second half of the third millennium BC (ca. 2500 BC), texts fully written in Akkadian begin to \
appear. Hundreds of thousands of texts and text fragments have been excavated to date, covering a vast textual tradition of \
mythological narrative, legal texts, scientific works, correspondence, political and military events, and many other examples. \
By the second millennium BC, two variant forms of the language were in use in Assyria and Babylonia, known as Assyrian and \
Babylonian respectively. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Akkadian>`_)


Syllabifier
=========

Syllabify Akkadian words.

.. code-block:: python

   In [1]: from cltk.stem.akkadian.syllabifier import Syllabifier

   In [2]: word = "epištašu"

   In [3]: syll = Syllabifier()

   In [4]: syll.syllabify(word)
   ['e', 'piš', 'ta', 'šu']

Stress
=====

This function identifies the stress on an Akkadian word.

.. code-block:: python

   In[2]: from cltk.phonology.akkadian.stress import StressFinder

   In[3]: stresser = StressFinder()

   In[4]: word = "šarrātim"

   In[5]: stresser.find_stress(word)

   Out[5]: ['šar', '[rā]', 'tim']

Decliner
=========

This method outputs a list of tuples the first element being a declined noun, the second a dictionary containing its attributes.

.. code-block:: python

   In[2]: from cltk.stem.akkadian.declension import NaiveDecliner

   In[3]: word = 'ilum'

   In[4]: decliner = NaiveDecliner()

   In[5]: decliner.decline_noun(word, 'm')

   Out[5]:
   [('ilam', {'case': 'accusative', 'number': 'singular'}),
    ('ilim', {'case': 'genitive', 'number': 'singular'}),
    ('ilum', {'case': 'nominative', 'number': 'singular'}),
    ('ilīn', {'case': 'oblique', 'number': 'dual'}),
    ('ilān', {'case': 'nominative', 'number': 'dual'}),
    ('ilī', {'case': 'oblique', 'number': 'plural'}),
    ('ilū', {'case': 'nominative', 'number': 'plural'})]

Stems and Bound Forms
=========

These two methods reduce a noun to its stem or bound form.

.. code-block:: python

   In[2]: from cltk.stem.akkadian.stem import Stemmer

   In[3]: stemmer = Stemmer()

   In[4]: word = "ilātim"

   In[5]: stemmer.get_stem(word, 'f')

   Out[5]: 'ilt'

.. code-block:: python

   In[2]: from cltk.stem.akkadian.bound_form import BoundForm

   In[3]: bound_former = BoundForm()

   In[4]: word = "kalbim"

   In[5]: bound_former.get_bound_form(word, 'm')

   Out[5]: 'kalab'

Consonant and Vowel patterns
======

It's useful to be able to parse Akkadian words as sequences of consonants and vowels.

.. code-block:: python

   In[2]: from cltk.stem.akkadian.cv_pattern import CVPattern

   In[3]: cv_patterner = CVPattern()

   In[4]: word = "iparras"

   In[5]: cv_patterner.get_cv_pattern(word)

   Out[5]:
   [('V', 1, 'i'),
    ('C', 1, 'p'),
    ('V', 2, 'a'),
    ('C', 2, 'r'),
    ('C', 2, 'r'),
    ('V', 2, 'a'),
    ('C', 3, 's')]

   In[6]: cv_patterner.get_cv_pattern(word, pprint=True)

   Out[6]: 'V₁C₁V₂C₂C₂V₂C₃'

Stopword Filtering
==================

To use the CLTK's built-in stopwords list for Akkadian:

.. code-block:: python

    In[2]: from nltk.tokenize.punkt import PunktLanguageVars

    In[3]: from cltk.stop.akkadian.stops import STOP_LIST

    In[4]: sentence = "šumma awīlum ina dīnim ana šībūt sarrātim ūṣiamma awat iqbû la uktīn šumma dīnum šû dīn napištim awīlum šû iddâk"

    In[5]: p = PunktLanguageVars()

    In[6]: tokens = p.word_tokenize(sentence.lower())

    In[7]: [w for w in tokens if not w in STOP_LIST]
    Out[7]:
    ['awīlum',
     'dīnim',
     'šībūt',
     'sarrātim',
     'ūṣiamma',
     'awat',
     'iqbû',
     'uktīn',
     'dīnum',
     'dīn',
     'napištim',
     'awīlum',
     'iddâk']