Arabic
******
Arabic is the form of the Arabic language used in Umayyad and Abbasid literary texts from the 7th century AD to the 9th century AD.
The orthography of the Qurʾān was not developed for the standardized form of Classical Arabic; rather, it shows the attempt on the part of writers to utilize a traditional writing system for recording a non-standardized form of Classical Arabic. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Classical_Arabic>`_)

Corpora
=======

Use ``CorpusImporter()``.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('arabic')

   In [3]: c.list_corpora
   Out[3]:
   ['arabic_text_perseus','quranic-corpus','quranic-corpus-morphology']


Alphabet
========

The Arabic alphabet and digits are placed in `cltk/corpus/arabic/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/arabic/alphabet.py>`_.

.. code-block:: python

    In [1]: from cltk.corpus.arabic.alphabet import *

    # all Hamza forms
    In [2]: HAMZAT
    Out[2]: ('ء', 'أ', 'إ', 'آ', 'ؤ', 'ؤ', 'ٔ', 'ٕ')

    # print HAMZA from hamza const and from HAMZAT list

    In [3] HAMZA
    Out [3] 'ء'

    In [4] HAMZAT[0]
    Out [4] 'ء'

    # listing all Arabic letters

    In [5] LETTERS
    out [5] 'ا ب ت ة ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي ء آ أ ؤ إ ؤ'

    # Listing all shaped forms for example  Beh letter

    In [6] SHAPED_FORMS[BEH]
    Out [6] ('ﺏ', 'ﺐ', 'ﺑ', 'ﺒ')

    # Listing all Punctuation marks

    In [7] PUNCTUATION_MARKS
    Out [7] ['،', '؛', '؟']

    # Listing all Diacritics  FatHatanً ,Dammatanٌ ,Kasratanٍ ,FatHaَ ,Dammaُ ,Kasraِ ,Sukunْ ,Shaddaّ

    In [8] TASHKEEL
    Out [8] ('ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ْ', 'ّ')

    # Listing HARAKAT

    In [9] HARAKAT
    Out [9] ('ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ْ')

    # Listing SHORTHARAKAT

    In [10] SHORTHARAKAT
    Out [10] ('َ', 'ُ', 'ِ', 'ْ')

    # Listing Tanween

    In [11] TANWEEN
    Out [11] ('ً', 'ٌ', 'ٍ')

    # Kasheeda, Tatweel

    In [12] NOT_DEF_HARAKA
    Out [12] 'ـ'


    # WESTERN_ARABIC_NUMERALS numerals

    In [13] WESTERN_ARABIC_NUMERALS
    Out [13] ['0','1','2','3','4','5','6','7','8','9']

    # EASTERN ARABIC NUMERALS from 0 to 9

    In [14] EASTERN_ARABIC_NUMERALS
    Out [14] ['۰', '۱', '۲', '۳', '٤', '۵', '٦', '۷', '۸', '۹']

    # Listing The Weak letters  .

    In [15] WEAK
    Out [15]  ('ا', 'و', 'ي', 'ى')

    # Listing all Ligatures Lam-Alef

    In [16] LIGATURES_LAM_ALEF
    Out [16] ('ﻻ', 'ﻷ', 'ﻹ', 'ﻵ')

    # listing small letters

    In [17] SMALL
    Out [17] ('ٰ', 'ۥ', 'ۦ')

    # Import letters names in arabic

    In [18] Names[ALEF]
    Out [18]  'ألف'

The digits are placed in a list ``DIGITS`` with the digit the same as the list index (0-9). For example, the arabic digit for 4 can be accessed in this manner:

.. code-block:: python
   In [1]: from cltk.corpus.arabic.alphabet import DIGITS
   In [2]: DIGITS[4]
   Out[2]: '٤'

Arabic has three ``SHORT_VOWELS`` that are essentially diacritics used in the script. It also has three LONG_VOWELS that are actually part of the alphabet. The corresponding lists can be imported:

.. code-block:: python
   In [1]: from cltk.corpus.arabic.alphabet import SHORT_VOWELS
   In [2]: SHORT_VOWELS
   Out[2]: ['َ', 'ِ', 'ُ']
   In [3]: from cltk.corpus.arabic.alphabet import LONG_VOWELS
   In [4]: LONG_VOWELS
   Out[4]: ['ا', 'و', 'ي']

The rest of the alphabet are ``CONSONANTS`` that can be accessed in a similar way.

There are two ``SPECIAL`` characters. The first one is called "shaddah", and it signifies that a consonant is pronounced twice. The second is a ligature.

.. code-block:: python
   In [1]: from cltk.corpus.arabic.alphabet import SPECIAL
   In [2]: SPECIAL
   Out[2]: ['‎ّ', 'ﻻ']

