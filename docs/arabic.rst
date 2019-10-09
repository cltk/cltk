Arabic
******
Classical Arabic is the form of the Arabic language used in Umayyad and Abbasid literary texts from the 7th century AD to the 9th century AD. The orthography of the Qurʾān was not developed for the standardized form of Classical Arabic; rather, it shows the attempt on the part of writers to utilize a traditional writing system for recording a non-standardized form of Classical Arabic. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Classical_Arabic>`_)

Corpora
=======

Use ``CorpusImporter()``.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('arabic')

   In [3]: c.list_corpora
   Out[3]:
   ['arabic_text_perseus','arabic_text_quranic_corpus','arabic_morphology_quranic-corpus']

   In [4]: c.import_corpus('arabic_text_perseus')  # ~/cltk_data/arabic/text/arabic_text_perseus/

Alphabet
========

The Arabic alphabet are placed in `cltk/corpus/arabic/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/arabic/alphabet.py>`_.

.. code-block:: python

   In [1]: from cltk.corpus.arabic.alphabet import *
  # all Hamza forms
   In [2]: HAMZAT
   Out[2]: ('ء', 'أ', 'إ', 'آ', 'ؤ', 'ؤ', 'ٔ', 'ٕ')
  # print HAMZA from hamza const and from HAMZAT list

   In [3] HAMZA
   Out[3] 'ء'

   In [4] HAMZAT[0]
   Out[4] 'ء'
  # listing all Arabic letters

   In [5] LETTERS
   out [5] 'ا ب ت ة ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي ء آ أ ؤ إ ؤ'
  # Listing all shaped forms for example  Beh letter

   In [6] SHAPED_FORMS[BEH]
   Out[6] ('ﺏ', 'ﺐ', 'ﺑ', 'ﺒ')
  # Listing all Punctuation marks

   In [7] PUNCTUATION_MARKS
   Out[7] ['،', '؛', '؟']
  # Listing all Diacritics  FatHatanً ,Dammatanٌ ,Kasratanٍ ,FatHaَ ,Dammaُ ,Kasraِ ,Sukunْ ,Shaddaّ

   In [8] TASHKEEL
   Out[8] ('ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ْ', 'ّ')
  # Listing HARAKAT

   In [9] HARAKAT
   Out[9] ('ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ْ')
  # Listing SHORTHARAKAT

   In [10] SHORTHARAKAT
   Out[10] ('َ', 'ُ', 'ِ', 'ْ')
  # Listing Tanween

   In [11] TANWEEN
   Out[11] ('ً', 'ٌ', 'ٍ')
  # Kasheeda, Tatweel

   In [12] NOT_DEF_HARAKA
   Out[12] 'ـ'

  # WESTERN_ARABIC_NUMERALS numerals

   In [13] WESTERN_ARABIC_NUMERALS
   Out[13] ['0','1','2','3','4','5','6','7','8','9']
  # EASTERN ARABIC NUMERALS from 0 to 9

   In [14] EASTERN_ARABIC_NUMERALS
   Out[14] ['۰', '۱', '۲', '۳', '٤', '۵', '٦', '۷', '۸', '۹']
  # Listing The Weak letters  .

   In [15] WEAK
   Out[15]  ('ا', 'و', 'ي', 'ى')
  # Listing all Ligatures Lam-Alef

   In [16] LIGATURES_LAM_ALEF
   Out[16] ('ﻻ', 'ﻷ', 'ﻹ', 'ﻵ')
  # listing small letters

   In [17] SMALL
   Out[17] ('ٰ', 'ۥ', 'ۦ')
  # Import letters names in arabic

   In [18] Names[ALEF]
   Out[18]  'ألف'

CLTK Arabic Support
===================

1. Pyarabic
```````````
Specific Arabic language library for Python, provides basic functions to manipulate Arabic letters and text, like detecting Arabic letters, Arabic letters groups and characteristics, remove diacritics etc.Developed by `Taha Zerrouki: <http://tahadz.com>`_.

1.1. Features
-------------
1. Arabic letters classification
2. Text tokenization
3. Strip Harakat (all, except Shadda, tatweel, last_haraka)
4. Sperate and join Letters and Harakat
5. Reduce tashkeel
6. Measure tashkeel similarity (Harakat, fully or partially vocalized, similarity with a template)
7. Letters normalization (Ligatures and Hamza)
8. Numbers to words
9. Extract numerical phrases
10. Pre-vocalization of numerical phrases
11. Unshiping texts

1.2. Applications
-----------------
- Arabic text processing

1.3. Usage
----------

.. code-block:: python

   In [1] from cltk.corpus.arabic.utils.pyarabic import araby
   
   In [2] char = 'ْ'
   
   In [3] araby.is_sukun(char)  # Checks for Arabic Sukun Mark
   Out[3] True

   In [4] char = 'ّ'
   
   In [5] araby.is_shadda(char)  # Checks for Arabic Shadda Mark
   Out[5] True

   In [6] text = "الْعَرَبِيّةُ"

   In [7] araby.strip_harakat(text)  # Strip Harakat from arabic word except Shadda.
   Out[7] العربيّة
   
   In [8] text = "الْعَرَبِيّةُ"

   In [9] araby.strip_lastharaka(text)# Strip the last Haraka from arabic word except Shadda
   Out[9] الْعَرَبِيّة

   In [10] text = "الْعَرَبِيّةُ"

   In [11] araby.strip_tashkeel(text)  # Strip vowels from a text,  include Shadda
   Out[11] العربية


Stopword Filtering
==================
To use the CLTK's built-in stopwords list:

.. code-block:: python

   In [1]: from cltk.stop.arabic.stopword_filter import stopwords_filter as ar_stop_filter

   In [2]: text = 'سُئِل بعض الكُتَّاب عن الخَط، متى يَسْتحِقُ أن يُوصَف بِالجَودةِ؟'

   In [3]: ar_stop_filter(text)
   Out[3]: ['سئل', 'الكتاب', 'الخط', '،', 'يستحق', 'يوصف', 'بالجودة', '؟']

Word Tokenization
=================
.. code-block:: python

   In [1]: from cltk.tokenize.word import WordTokenizer

   In [2]: word_tokenizer = WordTokenizer('arabic')

   In [3]: text = 'اللُّغَةُ الْعَرَبِيَّةُ جَمِيلَةٌ.'

   In [4]: word_tokenizer.tokenize(text)
   Out[4]: ['اللُّغَةُ', 'الْعَرَبِيَّةُ', 'جَمِيلَةٌ', '.']


Transliteration
===============
The CLTK Provides `Buckwalter <https://en.wikipedia.org/wiki/Buckwalter_transliteration>`_ and `ISO233-2 <https://fr.wikipedia.org/wiki/ISO_233-2>`_ Transliteration Systems for the Arabic language.

Available Transliteration Systems
`````````````````````````````````

.. code-block:: python

   In [1] from cltk.phonology.arabic.romanization import available_transliterate_systems

   In [2] available_transliterate_systems()
   Out[2] ['buckwalter', 'iso233-2', 'asmo449']

Usage
`````

.. code-block:: python

   In [1] from cltk.phonology.arabic.romanization import transliterate

   In [2] mode = 'buckwalter'

   In [3] ar_string = 'بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ' # translate in English: In the name of Allah, the Most Merciful, the Most Compassionate

   In [4] ignore = '' # this is for ignore an arabic char from transliterate operation

   In [5] reverse = True # true means transliteration from arabic native script to roman script such as Buckwalter

   In [6] transliterate(mode, ar_string, ignore, reverse)
   Out[6] 'bisomi Allhi Alra~Hom`ni Alra~Hiyomi'
