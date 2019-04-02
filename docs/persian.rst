Persian
********

Persian is one of the Western Iranian languages within the Indo-Iranian branch of the Indo-European language family. The Old Persian language is one of the two directly attested Old Iranian languages (the other being Avestan). Old Persian appears primarily in the inscriptions, clay tablets, and seals of the Achaemenid era (c. 600 BCE to 300 BCE). Examples of Old Persian have been found in what is now Iran, Romania (Gherla), Armenia, Bahrain, Iraq, Turkey and Egypt, the most important attestation by far being the contents of the Behistun Inscription (dated to 525 BCE). Avestan is one of the Eastern Iranian languages within the Indo-European language family known only from its use as the language of Zoroastrian scripture, i.e. the Avesta. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Old_Persian>`_)

Alphabet
=========

The Persian digits and alphabet are placed in `cltk/corpus/persian/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/persian/alphabet.py>`_.

The digits are placed in a dict ``NUMERALS`` with the digit the same as the index (0-9). There is a dictionary named NUMERALS_WRITINGS for their writing also. For example, the persian digit for 5 can be accessed in this manner:

.. code-block:: python

   In [1]: from cltk.corpus.persian.alphabet import NUMERALS, NUMERALS_WRITINGS
   In [2]: NUMERALS[5]
   Out[2]: '۵'
   In [3]: NUMERALS_WRITINGS[5]
   Out[3]: 'پنج'

One can also have the alphabetic orders of the charachters form ALPHABETIC_ORDER dictionary. The keys are the characters and the values are their order. The corresponding dictionary can be imported:

.. code-block:: python

   In [1]: from cltk.corpus.persian.alphabet import ALPHABETIC_ORDER, JIM
   In [2]: ALPHABETIC_ORDER[JIM]
   Out[2]: 6
