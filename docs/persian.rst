Persian
********

Persian is one of the Western Iranian languages within the Indo-Iranian branch of the Indo-European language family. The Old Persian language is one of the two directly attested Old Iranian languages (the other being Avestan). Old Persian appears primarily in the inscriptions, clay tablets, and seals of the Achaemenid era (c. 600 BCE to 300 BCE). Examples of Old Persian have been found in what is now Iran, Romania (Gherla), Armenia, Bahrain, Iraq, Turkey and Egypt, the most important attestation by far being the contents of the Behistun Inscription (dated to 525 BCE). Avestan is one of the Eastern Iranian languages within the Indo-European language family known only from its use as the language of Zoroastrian scripture, i.e. the Avesta. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_Persian>`_)

Alphabet
=========

The Persian digits and alphabet are placed in `cltk/corpus/persian/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/persian/alphabet.py>`_.

The digits are placed in a list ``DIGITS`` with the digit the same as the list index (0-9). For example, the persian digit for 5 can be accessed in this manner:

.. code-block:: python

   In [1]: from cltk.corpus.persian.alphabet import DIGITS
   In [2]: DIGITS[5]
   Out[2]: '۵'

Persian has three ``SHORT_VOWELS`` that are essentially diacritics used in the script. It also has three ``LONG_VOWELS`` that are actually part of the alphabet. The corresponding lists can be imported:

.. code-block:: python

   In [1]: from cltk.corpus.persian.alphabet import SHORT_VOWELS
   In [2]: SHORT_VOWELS
   Out[2]: ['َ', 'ِ', 'ُ']
   In [3]: from cltk.corpus.persian.alphabet import LONG_VOWELS
   In [4]: LONG_VOWELS
   Out[4]: ['ا', 'و', 'ی']

The rest of the alphabet are ``CONSONANTS`` that can be accessed in a similar way.

There are three ``SPECIAL`` characters that are ligatures or different orthographical shapes of the alphabet.

.. code-block:: python

   In [1]: from cltk.corpus.persian.alphabet import SPECIAL
   In [2]: SPECIAL
   Out[2]: ['ﺁ', 'ۀ', 'ﻻ']
