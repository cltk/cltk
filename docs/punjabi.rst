Punjabi
*******

Alphabets
=========

The punjabi alphabets and numbers are placed in alphabet.py file, so we can use them, the alphabet.py file in cltk/corpus/punjabi/ is fully commented, for more info you can see the comments there.

This module is necessary for the working all other modules, so directly or indirectly, they are importing this module.

Here, the basics about the file are explained.

It contains, list, which store the digits, vowels, consonants and symbols of punjabi language in lexiological order.
You can check it

.. code-block:: python

   In[1]: from cltk.corpus.punjabi.alphabet import INDEPENDENT_VOWELS

   In[2]: print (INDEPENDENT_VOWELS)
   Out[2]: ['ਆ', 'ਇ', 'ਈ', 'ਉ', 'ਊ', 'ਏ', 'ਐ', 'ਓ', 'ਔ']

These are the INDEPENDENT_VOWELS, they don't need any other consonant to be printed, they are printed as just they are, they represent the sound aa, i, iii, u, uuu, a, oo, o and ou respectively.

Similarly there is the list of DIGITS, DEPENDENT_VOWELS, CONSONANTS, BINDI_CONSONANTS(just like consonants but just change in some sound) and some OTHER_SYMBOLS, which can be used and imported in the same way as is done with the INDEPENDENT_VOWELS.

Numerifier
==========

.. code-block:: python

   In[1]: from cltk.corpus.punjabi.numerifier import punToEnglist_number

   In[2]: from cltk.corpus.punjabi.numerifier import englishToPun_number

   In[3]: c = punToEnglish_number('੧੨੩੪੫੬੭੮੯੦')

   In[4]: print(c)
   Out[4]: 1234567890

   In[5]: c = englishToPun_number(1234567890)

   In[6]: print(c)
   Out[6]: ੧੨੩੪੫੬੭੮੯੦
