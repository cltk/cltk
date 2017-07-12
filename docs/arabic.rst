Arabic
********

Alphabet
========

The Arabic alphabet and digits are placed in `cltk/corpus/arabic/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/arabic/alphabet.py>`_.

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



