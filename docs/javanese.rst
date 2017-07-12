Javanese
********

Javanese is the language of the Javanese people from the central and eastern parts of the island of Java, in Indonesia. Javanese is one of the Austronesian languages, but it is not particularly close to other languages and is difficult to classify. The 8th and 9th centuries are marked by the emergence of the Javanese literary tradition – with Sang Hyang Kamahayanikan, a Buddhist treatise; and the Kakawin Rāmâyaṇa, a Javanese rendering in Indian metres of the Vaishnavist Sanskrit epic Rāmāyaṇa. (Source: `Wikipedia <https://en.wikipedia.org/wiki/Javanese_language>`_)


Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``javanese_``) to discover available javanese corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('javanese')

   In [3]: c.list_corpora
   Out[3]:
   ['javanese_text_gretil']
