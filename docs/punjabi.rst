Punjabi
*******

At this time only the support of the punjabi alphabets and digits is added, and two functions in numerifier are added in the punjabi module

Numerifier
==========

.. code-block:: python

   In[1]: from cltk.corpus.punjabi.numerifier import punToEnglist_number

   In[2]: from cltk.corpus.punjabi.numerifier import englishToPun_number

   In[3]: c = punToEnglish_number('੧੨੩੪੫੬੭੮੯੦')

   In[4]: print c

   Out[4]: 1234567890

   In[5]: c = englishToPun_number(1234567890)

   In[6]: print c

   Out[6]: ੧੨੩੪੫੬੭੮੯੦
