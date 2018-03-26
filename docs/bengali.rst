Bengali
********
Bengali also known by its endonym Bangla is an Indo-Aryan language spoken in South Asia. It is the national and official language of the People's Republic of Bangladesh, and the official language of several northeastern states of the Republic of India, including West Bengal, Tripura, Assam (Barak Valley) and Andaman and Nicobar Islands. With over 210 million speakers, Bengali is the seventh most spoken native language in the world. 
Source: `Wikipedia 
<https://en.wikipedia.org/wiki/Bengali_language>`_.

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``bengali_``) to discover available Bengali corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('bengali')

   In [3]: c.list_corpora
   Out[3]:
   ['bengali_text_wikisource']

Tokenizer
=========

This tool can help break up a sentence into smaller constituents. 

.. code-block:: python

   In [1]: from cltk.tokenize.sentence import TokenizeSentence

   In [2]: sentence = "রাজপণ্ডিত হব মনে আশা করে | সপ্তশ্লোক ভেটিলাম রাজা গৌড়েশ্বরে ||"

   In [3]: tokenizer = TokenizeSentence('bengali')

   In [4]: bengali_text_tokenize = tokenizer.tokenize(sentence)

   In [5]: bengali_text_tokenize
   ['রাজপণ্ডিত', 'হব', 'মনে', 'আশা', 'করে', '|', 'সপ্তশ্লোক', 'ভেটিলাম', 'রাজা', 'গৌড়েশ্বরে', '|', '|']



