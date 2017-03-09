About 


Malayalam originated from Middle Tamil (Sen-Tamil) in the 7th century.[12] An alternative theory proposes a split in even more ancient times.[12] Malayalam incorporated many elements from Sanskrit through the ages.[13] Before Malayalam came into being, Old Tamil was used in literature and courts of a region called Tamilakam, including present day Kerala state, a famous example being Silappatikaram. Silappatikaram was written by Chera prince Ilango Adigal from Chunkaparra, and is considered a classic in Sangam literature. Modern Malayalam still preserves many words from the ancient Tamil vocabulary of Sangam literature.

The earliest script used to write Malayalam was the Vatteluttu alphabet, and later the Kolezhuttu, which derived from it.[14] As Malayalam began to freely borrow words as well as the rules of grammar from Sanskrit, the Grantha alphabet was adopted for writing and came to be known as Arya Eluttu.
Source: Wikipedia
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
