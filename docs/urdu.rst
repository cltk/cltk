Urdu
*******

Alphabet
========

The Urdu alphabet and digits are placed in `cltk/corpus/urdu/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/urdu/alphabet.py>`_.

The digits are placed in a list ``DIGITS`` with the digit the same as the list index (0-9). For example, the urdu digit for 4 can be accessed in this manner:

.. code-block:: python

   In [1]: from cltk.corpus.urdu.alphabet import DIGITS
   In [2]: DIGITS[4]
   Out[2]: '٤'

Persian has three ``SHORT_VOWELS`` that are essentially diacritics used in the script. It also has four LONG_VOWELS that are actually part of the alphabet. The corresponding lists can be imported:

.. code-block:: python

   In [1]: from cltk.corpus.urdu.alphabet import SHORT_VOWELS
   In [2]: SHORT_VOWELS
   Out[2]: ['َ', 'ِ', 'ُ']

In [3]: from cltk.corpus.urdu.alphabet import LONG_VOWELS
   In [4]: LONG_VOWELS
   Out[4]: ['ا', 'و', 'ی', 'ے']
	
The rest of the alphabet are ``CONSONANTS`` that can be accessed in a similar way.

There are three ``SPECIAL`` characters that are ligatures or different orthographical shapes of the alphabet.

.. code-block:: python

   In [1]: from cltk.corpus.urdu.alphabet import SPECIAL
   In [2]: SPECIAL
   Out[2]: ['ﺁ', 'ۀ', 'ﻻ']
