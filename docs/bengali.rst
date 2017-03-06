Bengali
********

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

   In [1]: from cltk.tokenize.indian_tokenizer import indian_punctuation_tokenize_regex as i_word

   In [2]: sentence = "গল্প-উপন্যাস লিখতেন; কিন্তু ঐ অস্থিরচিত্ততার জন্যই কোন লেখা সম্পূর্ণ করতেন না।"

   In [3]: bengali_text_tokenize = i_word(sentence)

   In [4]: bengali_text_tokenize
   ['গল্প', '-', 'উপন্যাস', 'লিখতেন', ';', 'কিন্তু', 'ঐ', 'অস্থিরচিত্ততার', 'জন্যই', 'কোন', 'লেখা', 'সম্পূর্ণ', 'করতেন', 'না', '।']




