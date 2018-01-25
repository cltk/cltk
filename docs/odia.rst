Odia
********

Odia is an Indian language, belonging to the Indo-Aryan branch of the Indo-European language family. It is mainly spoken in the Indian states of Odisha and in parts of West Bengal, Jharkhand, Chhattisgarh and Andhra Pradesh. Odia is one of the many official languages in India; it is the official language of Odisha and the second official language of Jharkhand. Odia is the predominant language of Odisha, where Odia speakers comprise around 83.33% of the population according to census surveys.
(Source: `Wikipedia <https://en.wikipedia.org/wiki/Odia_language>`_)

Alphabet
========

The Odia alphabet and digits are placed in `cltk/corpus/odia/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/odia/alphabet.py>`_.

The digits are placed in a list ``NUMERALS`` with the digit the same as the list index (0-9). For example, the odia digit for 4 can be accessed in this manner:

.. code-block:: python

   In [1]: from cltk.corpus.odia.alphabet import NUMERALS
   In [2]: NUMERALS[4]
   Out[2]: '୪'

The vowels are places in a list ``VOWELS`` and can be accessed in this manner :

.. code-block:: python

   In [1]: from cltk.corpus.odia.alphabet import VOWELS
   In [2]: VOWELS
   Out[2]: ['ଅ', 'ଆ', 'ଇ', 'ଈ', 'ଉ', 'ଊ', 'ଋ', 'ୠ', 'ଌ', 'ୡ', 'ଏ', 'ଐ', 'ଓ', 'ଔ']

The rest of the alphabet are ``UNSTRUCTURED_CONSONANTS`` and ``STRUCTURED_CONSONANTS`` that can be accessed in a similar way.
