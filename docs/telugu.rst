Telugu
********

Telugu is a Dravidian language native to India. Inscriptions with Telugu words dating back to 400 BC to 100 BC have been discovered in Bhattiprolu in the Guntur district of Andhra Pradesh. Telugu literature can be traced back to the early 11th century period when Mahabharata was first translated to Telugu from Sanskrit by Nannaya. It flourished under the rule of the Vijayanagar empire, where Telugu was one of the empire's official languages. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Telugu_language>`_)


Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``telugu_``) to discover available Telugu corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('telugu')

   In [3]: c.list_corpora
   Out[3]:
   ['telugu_text_wikisource']


Tokenizer
=========

This tool can help break up a sentence into smaller constituents i.e into words.

.. code-block:: python

   In [1]: from cltk.tokenize.indian_tokenizer import indian_punctuation_tokenize_regex as i_word

   In [2]: sentence = "ఎలా టైపు చెయ్యాలో వివరంగా తెలుసుకోండి"

   In [3]: telugu_text_tokenize = i_word(sentence)

   In [4]: telugu_text_tokenize
   ['ఎలా', 'టైపు', 'చెయ్యాలో', 'వివరంగా', 'తెలుసుకోండి']
