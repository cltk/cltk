Punjabi
*******

Corpora
=======

Use ``CorpusImporter`` or browse the `CLTK Github repository <http://github.com/cltk>`_ (anything beginning with ``punjabi_``) to discover available Punjabi corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter
   In [2]: c = CorpusImporter('punjabi')
   In [3]: c.list_corpora
   Out[3]:
   ['punjabi_text_gurban']

Now from the list of available corpora import any one you like.

Alphabet
=========

The Punjabi digits, vowels, consonants, and symbols are placed in `cltk/corpus/punjabi/alphabet.py <https://github.com/cltk/cltk/blob/master/cltk/corpus/punjabi/alphabet.py>`_. It is fully commented, so look there for more information about the language's phonology.

To use Punjabi's independent vowels, for example:

.. code-block:: python

   In [1]: from cltk.corpus.punjabi.alphabet import INDEPENDENT_VOWELS

   In [2]: print(INDEPENDENT_VOWELS)
   Out[2]: ['ਆ', 'ਇ', 'ਈ', 'ਉ', 'ਊ', 'ਏ', 'ਐ', 'ਓ', 'ਔ']

These are the INDEPENDENT_VOWELS, they don't need any other consonant to be printed, they are printed as just they are, they represent the sounds "aa", "i", "iii", "u", "uuu", "a", "oo", "o" and "ou", respectively.

Similarly there are lists for ``DIGITS``, ``DEPENDENT_VOWELS``, ``CONSONANTS``, ``BINDI_CONSONANTS`` (nasal pronunciation) and some ``OTHER_SYMBOLS`` (mostly for pronunciation).


Numerifier
==========
These convert English numbers into Punjabi and vice-verse.

.. code-block:: python

   In[1]: from cltk.corpus.punjabi.numerifier import punToEnglish_number

   In[2]: from cltk.corpus.punjabi.numerifier import englishToPun_number

   In[3]: c = punToEnglish_number('੧੨੩੪੫੬੭੮੯੦')

   In[4]: print(c)
   Out[4]: 1234567890

   In[5]: c = englishToPun_number(1234567890)

   In[6]: print(c)
   Out[6]: ੧੨੩੪੫੬੭੮੯੦

Stopword Filtering
==================
To use the CLTK's built-in stopwords list:

.. code-block:: python

   In[1]: from cltk.tokenize.indian_tokenizer import indian_punctuation_tokenize_regex
   
   In[2]: from cltk.stop.punjabi.stops import STOPS_LIST
   
   In[3]: sample = "ਪੰਜਾਬੀ ਪੰਜਾਬ ਦੀ ਮੁਖੱ ਬੋੋਲਣ ਜਾਣ ਵਾਲੀ ਭਾਸ਼ਾ ਹੈ।"
   
   In[4]: x = indian_punctuation_tokenize_regex(sample)
   
   In[5]: print(x)
   Out[5]: ['ਪੰਜਾਬੀ', 'ਪੰਜਾਬ', 'ਦੀ', 'ਮੁਖੱ', 'ਬੋੋਲਣ', 'ਜਾਣ', 'ਵਾਲੀ', 'ਭਾਸ਼ਾ', 'ਹੈ', '।']
   
   In[6]: lis = [w for w in x if not w in STOPS_LIST]
   
   In[7]: print (lis)
   Out[7]: ['ਪੰਜਾਬੀ', 'ਪੰਜਾਬ', 'ਮੁਖੱ', 'ਬੋੋਲਣ', 'ਜਾਣ', 'ਭਾਸ਼ਾ', '।']
