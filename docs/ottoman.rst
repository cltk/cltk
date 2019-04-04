Ottoman
********

Ottoman Turkish, or the Ottoman language, is the variety of the Turkish language that was used in the Ottoman Empire. Ottoman Turkish was highly influenced by Arabic and Persian. Arabic and Persian words in the language accounted for up to 88% of its vocabulary. As in most other Turkic and other foreign languages of Islamic communities, the Arabic borrowings were not originally the result of a direct exposure of Ottoman Turkish to Arabic, a fact that is evidenced by the typically Persian phonological mutation of the words of Arabic origin. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Ottoman_Turkish_language>`_)

Alphabet
=========

The Ottoman digits and alphabet are placed in `cltk/corpus/ottoman/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/ottoman/alphabet.py>`_.

The digits are placed in a dict ``NUMERALS`` with the digit the same as the index (0-9). There is a dictionary named NUMERALS_WRITINGS for their writing also. For example, the persian digit for 5 can be accessed in this manner:

.. code-block:: python

   In [1]: from cltk.corpus.ottoman.alphabet import NUMERALS, NUMERALS_WRITINGS
   In [2]: NUMERALS[5]
   Out[2]: '۵'
   In [3]: NUMERALS_WRITINGS[5]
   Out[3]: 'بش'

One can also have the alphabetic orders of the charachters form ALPHABETIC_ORDER dictionary. The keys are the characters and the values are their order. The corresponding dictionary can be imported:

.. code-block:: python

   In [1]: from cltk.corpus.ottoman.alphabet import ALPHABETIC_ORDER, CIM
   In [2]: ALPHABETIC_ORDER[CIM]
   Out[2]: 6