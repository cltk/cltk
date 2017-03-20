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

The Arabic alphabet are placed in `cltk/corpus/arabic/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/arabic/alphabet.py>`_.

.. code-block:: python

	In [1]: from cltk.corpus.arabic.alphabet import *

	# all Hamza forms
	In [2]: HAMZAT
	Out[2]: ['ء', 'أ', 'إ', 'آ', 'ؤ', 'ئ']

	# print HAMZA from hamza const and from HAMZAT list

	In [3] HAMZA
	Out [3] 'ء'

	In [4] HAMZAT[0]
	Out [4] 'ء'

  # listing all Arabic letters

	In [5] ARABIC_LETTERS
	out [5] ['ا', 'ى', 'ب', 'ة', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ع', 'ص', 'ض', 'ط', 'ظ', 'ع',
          'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']

	# Listing all shaped forms for example  Beh letter

	In [6] SHAPED_FORMS[6]
	Out [6] {'ﺒ', 'ﺐ', 'ﺏ', 'ﺑ'}

	# Listing all Punctuation marks

	In [7] PONCTUATION_MARKS
	Out [7] ['،', '؛', '؟']

	# Listing all Diacritics  FatHatanً ,Dammatanٌ ,Kasratanٍ ,FatHaَ ,Dammaُ ,Kasraِ ,Sukunْ ,Shaddaّ

	In [8] HARAKAT
	Out [8] ['ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ْ', 'ّ']

	# WESTERN_ARABIC_NUMERALS numerals

	In [9] WESTERN_ARABIC_NUMERALS
	Out [9] ['0','1','2','3','4','5','6','7','8','9']

	# EASTERN ARABIC NUMERALS from 0 to 9

	In [10] EASTERN_ARABIC_NUMERALS
	Out [10] ['۰', '۱', '۲', '۳', '٤', '۵', '٦', '۷', '۸', '۹']

	# Listing The Weak letters  .

	In [11] WEAK_LETTERS
  Out [11]  ['ا', 'و', 'ي']

	# Listing all Ligatures Lam-Alef

	In [12] LIGATURES_LAM_ALEF
	Out [12] ['لا', 'ﻼ', 'لأ', 'ﻸ', 'لإ', 'ﻺ', 'لآ', 'ﻶ']

	# Kasheeda, Tatweel

	In [13] KASHEEDA
	Out [13] 'ـ'
