Malayalam is a language spoken in India, predominantly in the state of Kerala. It is one of the 22 scheduled languages of India and was designated as a Classical Language in India in 2013.
Source: https://en.m.wikipedia.org/wiki/Malayalam

Malayalam
********

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``malayalam_``) to discover available Malayalam corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('malayalam')

   In [3]: c.list_corpora
   Out[3]:
   ['malayalam_text_gretil']
