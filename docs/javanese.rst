Javanese
********

Javanese is the language of the Javanese people from the central and eastern parts of the island of Java, in Indonesia. There are also pockets of Javanese speakers in the northern coast of western Java. It is the native language of more than 98 million people (more than 42% of the total population of Indonesia). (Source: `Wikipedia <https://en.wikipedia.org/wiki/Javanese_language>`_)

Corpora
=======

Use ``CorpusImporter()`` or browse the `CLTK GitHub organization <https://github.com/cltk>`_ (anything beginning with ``javanese_``) to discover available javanese corpora.

.. code-block:: python

   In [1]: from cltk.corpus.utils.importer import CorpusImporter

   In [2]: c = CorpusImporter('javanese')

   In [3]: c.list_corpora
   Out[3]:
   ['javanese_text_gretil']
