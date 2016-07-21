Punjabi
*******

Alphabets
=========

The punjabi alphabets and numbers are placed in alphabet.py file, so we can use them, the alphabet.py file in cltk/corpus/punjabi/ is fully commented, for more info you can see the comments there.

This module is necessary for the working all other modules, so directly or indirectly, they are importing this module.

Here, the basics about the file are explained.

It contains, DIGITS list, which store the digits in punjabi language in increasing order.
You can check it

.. code-block:: python

   In[1]: from cltk.corpus.punjabi.alphabet import DIGITS

   In[2]: print (DIGITS)
   Out[2]: ['੦', '੧', '੨', '੩', '੪', '੫', '੬', '੭', '੮', '੯']

Similarly there is the list of INDEPENDENT_VOWELS, DEPENDENT_VOWELS, CONSONANTS, BINDI_CONSONANTS(just like consonants but just change in some sound) and some OTHER_SYMBOLS, which can be used and imported in the same way as is done with the DIGITS.

One important thing, some editors like vim, was not able to render the punjabi symbols like in DEPENDENT_VOWELS and OTHER_SYMBOLS correctly, so on adding the space in the list(during writing them) corrected this bug, but actually the space is not neccessary, so a trimmer function is also added which removes the left and right spaces.


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
