Kannada
********
Kannada is a Dravidian language spoken predominantly by Kannada people in India, mainly in the state of Karnataka, and by significant linguistic minorities in the states of Andhra Pradesh, Telangana, Tamil Nadu, Maharashtra, Kerala, Goa and abroad. The language has roughly 38 million native speakers who are called Kannadigas (Kannadigaru), and a total of 51 million speakers according to a 2001 census. It is one of the scheduled languages of India and the official and administrative language of the state of Karnataka. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Kannada>`_)

Alphabet
========

The Kannada alphabet and digits are placed in `cltk/corpus/kannada/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/kannada/alphabet.py>`_.

The digits are placed in a list ``NUMERALS`` with the digit the same as the list index (0-9). For example, the kannada digit for 6 can be accessed in this manner:

.. code-block:: python

   In [1]: from cltk.corpus.kannada.alphabet import NUMERALS
   In [2]: NUMERALS[6]
   Out[2]: '೬'

The vowels are places in a list ``VOWELS`` and can be accessed in this manner :

.. code-block:: python

   In [1]: from cltk.corpus.kannada.alphabet import VOWELS
   In [2]: VOWELS
   Out[2]: ['ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಉ', 'ಊ', 'ಋ','ೠ', 'ಎ', 'ಏ', 'ಐಒ', 'ಒ', 'ಓ', 'ಔ']

The rest of the alphabets are ``VOWEL_SIGNS``, ``YOGAVAAHAKAS`` ,``UNSTRUCTURED_CONSONANTS`` and ``STRUCTURED_CONSONANTS`` that can be accessed in a similar way.
